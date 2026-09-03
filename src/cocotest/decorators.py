from types import SimpleNamespace
from typing import Awaitable, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


class Markers(SimpleNamespace):
    """Collection of markers."""

    def __init__(self):
        self._markers = {}

    @staticmethod
    def mark(fn: Callable[P, Awaitable[T]], mark_name: str):
        fn_marks = getattr(fn, "_cocotest_marks", set())
        fn_marks.add(mark_name)
        setattr(fn, "_cocotest_marks", fn_marks)

    @staticmethod
    def has_mark(fn: Callable[P, Awaitable[T]], mark_name: str):
        fn_markers = getattr(fn, "_cocotest_marks", set())
        return mark_name in fn_markers

    @staticmethod
    def skip(fn: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        """Notifies cocotest that a test must be skipped."""
        Markers.mark(fn, "skip")
        return fn

    @staticmethod
    def xfail(fn: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        """Marks a test function as expected to fail."""
        Markers.mark(fn, "xfail")
        return fn


mark = Markers()
