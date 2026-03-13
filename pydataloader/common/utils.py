from functools import wraps
import time
from typing import Callable
from typing_extensions import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def timer(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.time()
        result = func(*args, **kwargs)
        print(
            f"Function '{func.__name__}' took {time.time() - start_time:.2f}s to complete."
        )
        return result

    return wrapper


@timer
class CounterStats:
    def __enter__(self):
        self.lines = 0
        self.num_samples = 0
        return self

    def __exit__(self, exc_type, exc, tb):
        print(f"Total lines: {self.lines}")
        print(f"Total samples: {self.num_samples}")

