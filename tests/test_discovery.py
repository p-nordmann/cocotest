import os
import sys
import warnings

import pytest

from cocotest.decorators import _get_marks
from cocotest.discovery import discover_duts, discover_test_cases, discover_test_modules
from cocotest.utils import get_module_name


@pytest.fixture(autouse=True)
def insert_cwd_in_path():
    """Makes sure that the CWD is inserted to the front of sys.path.

    For the following tests, we do not call the CLI, so we skip the part
    where the CWD is added to sys.path. This fixture does it instead.
    """
    sys.path.insert(0, os.getcwd())


path_duts = "testbench/discovery/duts"


def test_discover_test_modules():
    modules = discover_test_modules(path_duts)
    module_paths = {m.path for m in modules}

    assert len(modules) == 2
    assert module_paths == {
        f"{path_duts}/test_dut_discovery_1.py",
        f"{path_duts}/nested_tests/test_dut_discovery_2.py",
    }


def test_discover_duts():
    modules = discover_test_modules(path_duts)
    dut_index = discover_duts(modules)
    dut_names = {
        module_name: set(duts.keys()) for module_name, duts in dut_index.items()
    }

    module_name_1 = get_module_name(f"{path_duts}/test_dut_discovery_1.py")
    module_name_2 = get_module_name(f"{path_duts}/nested_tests/test_dut_discovery_2.py")
    assert dut_names == {
        module_name_1: {"dut_1", "dut_2"},
        module_name_2: {"dut_3", "dut_4", "dut_5"},
    }


def test_discover_test_cases():
    modules = discover_test_modules(path_duts)
    dut_index = discover_duts(modules)
    cases = discover_test_cases(modules, dut_index)
    case_names = {case.function.__name__ for case in cases}

    assert case_names == {
        "test_should_be_discovered_1",
        "test_should_be_discovered_2",
        "test_should_be_discovered_3",
        "test_should_be_discovered_4",
        "test_should_be_discovered_5",
    }

    # NOTE: in particular, "test_should_not_be_discovered" should not be in case_names.
    assert "test_should_not_be_discovered_3" not in case_names


def test_simple_marks():
    modules = discover_test_modules("testbench/marks/test_simple_marks.py")
    dut_index = discover_duts(modules)
    cases = discover_test_cases(modules, dut_index)

    def find_marks(*marks: str):
        return {
            case.function.__name__
            for case in cases
            if all(mark in _get_marks(case.function) for mark in marks)
        }

    assert find_marks("abc") == {"test_mark_abc"}
    assert find_marks("efg") == {"test_mark_efg"}
    assert find_marks("hij", "klm") == {"test_mark_hij_klm"}


def test_multiple_params():
    modules = discover_test_modules("testbench/discovery/test_multiple_params.py")
    dut_index = discover_duts(modules)

    with warnings.catch_warnings(record=True) as recorded_warnings:
        cases = discover_test_cases(modules, dut_index)

        assert len(recorded_warnings) == 2
        assert len(cases) == 0
