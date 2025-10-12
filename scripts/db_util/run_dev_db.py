#!/usr/bin/env python3
"""
Development Database Runner
Runs a PostgreSQL container using configuration from app/config.py
"""

import subprocess
import sys
from pathlib import Path

# Add project root to path so we can import app config
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.config import settings
from app.core.constants import DATA_DIR

CONTAINER_NAME = "licensing-postgres-dev"
DB_DATA_DIR = DATA_DIR / "postgres"


def run_postgres_container():
    """Run PostgreSQL container with configuration from config.py"""

    DB_DATA_DIR.mkdir(parents=True, exist_ok=True)
    db_path = DB_DATA_DIR.as_posix()

    print(f"Starting PostgreSQL container...")
    print(f"  Database: {settings.postgres_db_name}")
    print(f"  User:     {settings.postgres_username}")
    print(f"  Host:     {settings.postgres_host}:{settings.postgres_port}")
    print(f"  Data dir: {db_path}")
    print()

    docker_cmd = [
        "docker", "run", "-it", "--rm",
        "--name", CONTAINER_NAME,
        "-p", f"{settings.postgres_port}:5432",
        "-v", f"{db_path}:/var/lib/postgresql/data",
        "-e", f"POSTGRES_USER={settings.postgres_username}",
        "-e", f"POSTGRES_PASSWORD={settings.postgres_password}",
        "-e", f"POSTGRES_DB={settings.postgres_db_name}",
        "postgres:15",
    ]

    try:
        print(f"Connection string: postgresql://{settings.postgres_username}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db_name}")
        print("Press Ctrl+C to stop the container")
        print()
        subprocess.run(docker_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start PostgreSQL container: {e}")
        return False
    except KeyboardInterrupt:
        print("\nStopping PostgreSQL container...")
        return True
    except FileNotFoundError:
        print("Docker not found. Please install Docker and try again.")
        return False

    return True


if __name__ == "__main__":
    run_postgres_container()
