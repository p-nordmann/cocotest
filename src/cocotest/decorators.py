from typing import Awaitable, Callable, ParamSpec, Protocol, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


class MarkDecorator(Protocol):
    def __call__(self, fn: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]: ...


def get_marks(fn: Callable[P, Awaitable[T]]) -> frozenset[str]:
    marks = getattr(fn, "_cocotest_marks", frozenset())
    if not isinstance(marks, frozenset):
        raise ValueError(f"wrong attribute '_cocotest_marks' in '{fn.__name__}'")
    return marks


def _add_mark(fn: Callable[P, Awaitable[T]], mark_name: str):
    marks = get_marks(fn)
    setattr(fn, "_cocotest_marks", marks | {mark_name})


class Mark:
    """Collection of markers."""

    @staticmethod
    def skip(fn: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        """Notifies cocotest that a test must be skipped."""
        _add_mark(fn, "skip")
        return fn

    @staticmethod
    def xfail(fn: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        """Marks a test function as expected to fail."""
        _add_mark(fn, "xfail")
        return fn

    def __getattr__(self, name: str) -> MarkDecorator:
        """Used for custom marks."""

        def marker(fn: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
            _add_mark(fn, name)
            return fn

        return marker


mark = Mark()
