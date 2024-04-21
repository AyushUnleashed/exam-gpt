# Configure logging
import logging
from rich.logging import RichHandler


# Setup logging to use the RichHandler
# def setup_logging():
#     logging.basicConfig(
#         level="INFO",
#         format="%(message)s",
#         datefmt="[%X]",
#         handlers=[RichHandler()]
#     )

#     logger = logging.getLogger("rich")
#     return logger

def setup_logging():
    # Configure logger
    logger = logging.getLogger("rich")
    if not logger.handlers:  # Check if handlers are already added
        logger.setLevel(logging.INFO)  # Set the logging level

        # Define formatter
        formatter = logging.Formatter("%(message)s", datefmt="[%X]")

        # Console handler with rich logging
        console_handler = RichHandler()
        console_handler.setFormatter(formatter)

        # File handler to save logs to a file
        file_handler = logging.FileHandler("gpt_call.log")
        file_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger