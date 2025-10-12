"""Simple script to run the license server"""

import uvicorn
import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

RELOAD_EXCLUDES = ["venv", ".git", "__pycache__", "scripts", "client_sdk", "frontend"]

if __name__ == "__main__":
    logger.info("Starting License Management Server")
    logger.info("=" * 40)
    logger.info("Server will be available at: http://localhost:8000")
    logger.info("API Documentation: http://localhost:8000/docs")
    logger.info("Health Check: http://localhost:8000/health")
    logger.info("Press Ctrl+C to stop the server")
    logger.info("=" * 40)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8999,
        reload=True,
        reload_excludes=RELOAD_EXCLUDES,
        log_level="info"
    )