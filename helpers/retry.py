import functools
import time


def retry(timeout=5, tries=3):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for i in range(tries):
                time.sleep(timeout)
                try:
                    return f(*args, **kwargs)
                except Exception:
                    if i < tries - 1:
                        continue
                    else:
                        raise
        return wrapper
    return decorator
