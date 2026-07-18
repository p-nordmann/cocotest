import inspect
import os

from .core_types import DUTSpec, TestCase, TestModule
from .errors import DiscoveryError
from .utils import get_module_name, get_test_dut, import_from_path, is_test_case


def is_test_file_name(name: str) -> bool:
    return name.startswith("test_") and name.endswith(".py")


def discover_test_files(test_path: str) -> list[str]:
    """Finds all test files under `test_path`."""

    if not os.path.exists(test_path):
        raise DiscoveryError(f"test path does not exist: {test_path}")

    if os.path.isfile(test_path) and test_path.endswith(".py"):
        # In case the user specifies a python file directly,
        # we consider it a test file in any case.
        return [test_path]

    if os.path.isfile(test_path):
        raise DiscoveryError(f"test path is not a python file: {test_path}")

    test_files = []
    for root, dirs, files in os.walk(test_path):
        for name in files:
            if is_test_file_name(name):
                test_files.append(os.path.join(root, name))

    return test_files


def discover_test_modules(test_path: str) -> list[TestModule]:
    test_modules: list[TestModule] = []
    for path in discover_test_files(test_path):
        module_name = get_module_name(path)
        module = import_from_path(path, module_name)
        test_modules.append(TestModule(module, path))
    return test_modules


ModuleDUTSpecs = dict[str, DUTSpec]
"""Mapping dut_name->DUTSpec for a single module."""

DUTSpecIndex = dict[str, ModuleDUTSpecs]
"""Mapping module_name->dut_name->DUTSpec for all modules."""


def discover_duts(test_modules: list[TestModule]) -> DUTSpecIndex:
    index: DUTSpecIndex = {}
    for module, path in test_modules:
        index[module.__name__] = {}
        for name, value in vars(module).items():
            if isinstance(value, DUTSpec):
                index[module.__name__][name] = value
    return index


def discover_test_cases(
    test_modules: list[TestModule], dut_index: DUTSpecIndex
) -> list[TestCase]:
    cases = []
    for module, path in test_modules:
        duts: ModuleDUTSpecs = {}
        if module.__name__ in dut_index:
            duts = dut_index[module.__name__]
        for name, candidate in inspect.getmembers(module):
            if is_test_case(candidate, module=module, duts=duts):
                cases.append(
                    TestCase(
                        module,
                        path,
                        candidate,
                        get_test_dut(candidate, duts=duts),
                    )
                )
    return cases
