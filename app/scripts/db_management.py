import subprocess
import logging
from pathlib import Path
from app.config import settings
from app.core.constants import DATA_DIR, PROJECT_ROOT

# Set up logger
logger = logging.getLogger(__name__)

# === Postgres Config ===
APP_PG_CONTAINER_NAME = "licensing-postgres-app"
DB_DATA_DIR = DATA_DIR / "postgres"
DB_DATA_DIR.mkdir(parents=True, exist_ok=True)

# === Docker Compose Configuration ===
DOCKER_COMPOSE_DIR = PROJECT_ROOT / "docker"
DOCKER_COMPOSE_FILE = DOCKER_COMPOSE_DIR / "docker-compose.yml"

# ========== POSTGRES (Original Functions) ==========
def start_app_managed_postgres():
    """Start PostgreSQL container managed by the app"""
    logger.info("Starting app-managed PostgreSQL container...")

    # First, try to remove any existing container with the same name
    # subprocess.run(["docker", "rm", "-f", APP_PG_CONTAINER_NAME], check=False)

    # Check if port is already in use
    result = subprocess.run(
        ["docker", "ps", "-q", "-f", f"publish={settings.postgres_port}"],
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        logger.warning(f"Port {settings.postgres_port} is already in use by another container")
        logger.info("Using existing container...")
        return

    # For Docker Desktop on Windows, use the absolute path but with proper formatting
    # This avoids the complex path translation issues
    db_path = DB_DATA_DIR.as_posix()

    env_args = []
    if hasattr(settings, 'postgres_username') and settings.postgres_username:
        env_args += ["-e", f"POSTGRES_USER={settings.postgres_username}"]
    else:
        env_args += ["-e", "POSTGRES_USER=postgres"]
        
    if hasattr(settings, 'postgres_password') and settings.postgres_password:
        env_args += ["-e", f"POSTGRES_PASSWORD={settings.postgres_password}"]
    else:
        env_args += ["-e", "POSTGRES_PASSWORD=password"]
        
    if hasattr(settings, 'postgres_db_name') and settings.postgres_db_name:
        env_args += ["-e", f"POSTGRES_DB={settings.postgres_db_name}"]
    else:
        env_args += ["-e", "POSTGRES_DB=license_db"]

    try:
        logger.info(f"Attempting to mount database at: {db_path}")
        subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "-d",
                "--name",
                APP_PG_CONTAINER_NAME,
                "-p",
                f"{settings.postgres_port}:5432",
                "-v",
                f"{db_path}:/var/lib/postgresql/data",
                *env_args,
                "postgres:15",
            ],
            check=True,
        )
        logger.info("Successfully mounted database with persistent storage")
    except subprocess.CalledProcessError as e:
        logger.error(f"Volume mounting failed: {e}")
        logger.warning("Using container without persistent storage")
        subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "-d",
                "--name",
                APP_PG_CONTAINER_NAME,
                "-p",
                f"{settings.postgres_port}:5432",
                *env_args,
                "postgres:15",
            ],
            check=True,
        )

    logger.info(f"PostgreSQL started on port {settings.postgres_port}")
    logger.info(f"Database data stored in: {DB_DATA_DIR}")
    logger.info(f"Database: {settings.postgres_db_name}")
    logger.info(f"Username: {settings.postgres_username}")
    logger.info(f"Password: {'*' * len(settings.postgres_password)}")


def stop_app_managed_postgres():
    """Stop app-managed PostgreSQL container"""
    logger.info("Stopping app-managed PostgreSQL container...")
    subprocess.run(["docker", "rm", "-f", APP_PG_CONTAINER_NAME], check=False)
    logger.info("PostgreSQL container removed.")


def is_app_managed_postgres_running():
    """Check if app-managed PostgreSQL container is running"""
    result = subprocess.run(
        ["docker", "ps", "-q", "-f", f"name={APP_PG_CONTAINER_NAME}"],
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def get_app_managed_postgres_url():
    """Get PostgreSQL URL for app-managed database"""
    if not is_app_managed_postgres_running():
        logger.warning("App-managed PostgreSQL container is not running. Using environment PostgreSQL.")
        return None
    
    return settings.database_url
    

# ========== DOCKER COMPOSE MANAGEMENT (New Functions) ==========
def start_docker_compose_services():
    """Start all services using Docker Compose"""
    logger.info("Starting services with Docker Compose...")
    
    try:
        # Change to docker directory and start services
        subprocess.run(
            ["docker-compose", "up", "-d"],
            cwd=DOCKER_COMPOSE_DIR,
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("Docker Compose services started successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to start Docker Compose services: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False

def stop_docker_compose_services():
    """Stop all services using Docker Compose"""
    logger.info("Stopping Docker Compose services...")
    
    try:
        subprocess.run(
            ["docker-compose", "down"],
            cwd=DOCKER_COMPOSE_DIR,
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("Docker Compose services stopped successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to stop Docker Compose services: {e}")
        return False

def restart_docker_compose_services():
    """Restart all services using Docker Compose"""
    logger.info("Restarting Docker Compose services...")
    
    try:
        subprocess.run(
            ["docker-compose", "restart"],
            cwd=DOCKER_COMPOSE_DIR,
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("Docker Compose services restarted successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to restart Docker Compose services: {e}")
        return False

def is_docker_compose_running():
    """Check if Docker Compose services are running"""
    try:
        result = subprocess.run(
            ["docker-compose", "ps", "-q"],
            cwd=DOCKER_COMPOSE_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError:
        return False

def get_docker_compose_postgres_url():
    """Get PostgreSQL URL for Docker Compose managed database"""
    # Use the service name 'postgres' as defined in docker-compose.yml
    return f"postgresql://{settings.postgres_username}:{settings.postgres_password}@postgres:5432/{settings.postgres_db_name}"

def get_docker_compose_redis_url():
    """Get Redis URL for Docker Compose managed Redis"""
    return "redis://redis:6379" 