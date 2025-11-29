"""
logger.py
----------
Implements a simple but robust logging utility for the UDON IDS backend.
Logs key operational events to both console and file with timestamps.
"""

import logging
from datetime import datetime
import os


class SystemLogger:
    """
    Provides structured logging for backend modules with timestamps.
    """

    def __init__(self, name: str):
        self.name = name
        logDirectory = "logs"
        os.makedirs(logDirectory, exist_ok=True)

        # Define log file path
        logFile = os.path.join(logDirectory, f"{name}.log")

        # Configure logging format and handlers
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(logFile),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(name)

    def logInfo(self, message: str) -> None:
        """Logs informational messages."""
        self.logger.info(message)

    def logWarning(self, message: str) -> None:
        """Logs warnings or recoverable issues."""
        self.logger.warning(message)

    def logError(self, message: str) -> None:
        """Logs errors or exceptions."""
        self.logger.error(message)
