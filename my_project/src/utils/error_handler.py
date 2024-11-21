import logging
from functools import wraps
import streamlit as st
from typing import Callable, Any

logger = logging.getLogger(__name__)

def handle_error(error: Exception, context: str = None) -> None:
    """
    Handle errors gracefully and provide user feedback.

    Args:
        error (Exception): The exception that was raised
        context (str, optional): Additional context about where the error occurred
    """
    error_message = str(error)
    error_type = type(error).__name__

    # Log the error
    if context:
        logger.error(f"Error in {context}: {error_type} - {error_message}")
    else:
        logger.error(f"{error_type}: {error_message}")

    # Display user-friendly error message
    st.error(f"An error occurred: {error_message}")

def error_handler(func: Callable) -> Callable:
    """
    Decorator to handle errors in functions.

    Args:
        func (Callable): The function to wrap with error handling

    Returns:
        Callable: The wrapped function
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            handle_error(e, context=func.__name__)
            return None
    return wrapper