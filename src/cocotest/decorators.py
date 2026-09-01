from types import SimpleNamespace
from typing import Awaitable, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


class Mark(SimpleNamespace):
    """Collection of marks."""

    @staticmethod
    def skip(fn: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        """Notifies cocotest that a test must be skipped."""
        setattr(fn, "_cocotest_skip", True)
        return fn

    @staticmethod
    def xfail(fn: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        """Marks a test function as expected to fail."""
        setattr(fn, "_cocotest_xfail", True)
        return fn


mark = Mark()
