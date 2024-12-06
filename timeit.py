import time

from log_util import get_logger

logger = get_logger(__name__)


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Call the wrapped function
        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate elapsed time
        logger.info(f"Function '{func.__name__}' executed in {elapsed_time:.6f} seconds")
        return result  # Return the function's result

    return wrapper
