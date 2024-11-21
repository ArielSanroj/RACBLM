import logging
import os
from datetime import datetime

def setup_logger(name: str, log_level: int = logging.INFO) -> logging.Logger:
    """
    Set up and configure a logger instance.

    Args:
        name (str): The name of the logger (typically __name__)
        log_level (int): The logging level (default: logging.INFO)

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Create file handler
    log_file = os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # Add handlers to logger if they haven't been added already
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# Create a default logger instance
default_logger = setup_logger('default')

def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance. If name is None, returns the default logger.

    Args:
        name (str, optional): The name of the logger

    Returns:
        logging.Logger: Logger instance
    """
    if name is None:
        return default_logger
    return setup_logger(name)