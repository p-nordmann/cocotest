import os
from dataclasses import dataclass
from types import ModuleType
from typing import Any, Callable, NamedTuple


class TestModule(NamedTuple):
    module: ModuleType
    path: str


@dataclass
class DUTSpec:
    simulator: str
    sources: list[os.PathLike[str]]
    hdl_toplevel: str
    lang: str
    build_args: list[str]
    elab_args: list[str]
    extra_args: list[str]


@dataclass(frozen=True)
class TestCase:
    module: ModuleType
    path: str
    function: Callable[..., Any]
    dut: DUTSpec

    @property
    def node_id(self) -> str:
        return f"{self.path}::{self.function.__name__}"
