import hashlib
import inspect
import os
import sys
from importlib.util import module_from_spec, spec_from_file_location
from types import FunctionType, ModuleType
from typing import Any

import psutil

from .core_types import DUTSpec
from .errors import DefinitionError, DiscoveryError


def import_from_path(path: str, module_name: str) -> ModuleType:
    spec = spec_from_file_location(module_name, path)
    if spec is None:
        raise DiscoveryError(f"failed to import {module_name}")
    module = module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def get_module_name(path: str) -> str:
    absolute_path = os.path.abspath(path)
    digest = hashlib.sha1(absolute_path.encode()).hexdigest()[:12]

    file_name = os.path.basename(path)
    base_name = file_name[:-3]  # .py

    return f"cocotest_{base_name}_{digest}"


def is_test_case(
    candidate: Any, *, module: ModuleType, duts: dict[str, DUTSpec]
) -> bool:
    if not inspect.iscoroutinefunction(candidate):
        return False
    if candidate.__module__ != module.__name__:
        return False
    if not candidate.__name__.startswith("test_"):
        return False

    args = inspect.signature(candidate).parameters
    dut_args_count = 0
    for name in args:
        if name in duts:
            dut_args_count += 1

    if dut_args_count == 0:
        return False

    if dut_args_count > 1:
        raise DefinitionError(
            f"test case {candidate.__name__} requires {dut_args_count} duts"
        )

    return True


def get_test_dut(fx: FunctionType, *, duts: dict[str, DUTSpec]) -> DUTSpec:
    args = inspect.signature(fx).parameters
    for name in args:
        if name in duts:
            return duts[name]
    raise RuntimeError("dut not found")


def terminate_session():
    """Kills all the processes of the current cocotest session.

    Heavily inspired by the "Kill process tree" example from psutil's documentation.
    """
    if "COCOTEST_SESSION" not in os.environ or os.environ["COCOTEST_SESSION"] is None:
        return

    session_procs = []
    for p in psutil.process_iter():
        try:
            if p.environ().get("COCOTEST_SESSION") == os.environ["COCOTEST_SESSION"]:
                session_procs.append(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    for p in session_procs:
        if p.pid == os.getpid():
            continue
        try:
            p.kill()
        except psutil.NoSuchProcess:
            pass
