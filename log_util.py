import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class ColorFormatter(logging.Formatter):
    """Custom formatter for colorizing log levels."""

    COLOR_MAP = {
        logging.DEBUG: Fore.BLUE + Style.BRIGHT,  # Blue for debug
        logging.INFO: Fore.GREEN,  # Green for info
        logging.WARNING: Fore.YELLOW,  # Yellow for warnings
        logging.ERROR: Fore.RED,  # Red for errors
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT  # Magenta for critical
    }

    def format(self, record):
        color = self.COLOR_MAP.get(record.levelno, "")
        log_msg = super().format(record)
        return f"{color}{log_msg}{Style.RESET_ALL}"


def get_logger(name, level=logging.DEBUG):
    """Creates a logger with colorized output."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Define format
    formatter = ColorFormatter("[%(asctime)s] [%(name)s] [%(lineno)d] [%(levelname)s]: %(message)s",
                               datefmt="%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(formatter)

    # Add handler to logger
    if not logger.handlers:  # Avoid adding multiple handlers
        logger.addHandler(console_handler)

    return logger


# Example usage
if __name__ == "__main__":
    logger = get_logger("MyLogger", level=logging.DEBUG)

    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
