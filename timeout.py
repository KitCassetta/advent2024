import signal
from functools import wraps


class TimeoutException(Exception):
    """Custom exception to raise when a function times out."""
    pass


def timeout(seconds: int):
    """
    A decorator that forces a timeout on a function.

    Args:
        seconds (int): Maximum time (in seconds) a function can execute.

    Raises:
        TimeoutException: If the function takes longer than the specified time.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def handler(signum, frame):
                raise TimeoutException(f"Function '{func.__name__}' timed out after {seconds} seconds.")

            # Set up the timeout handler
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)  # Start the timer

            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)  # Cancel the alarm

            return result

        return wrapper

    return decorator
