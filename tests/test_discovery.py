import os
import sys

import pytest

from cocotest.discovery import discover_duts, discover_test_cases, discover_test_modules
from cocotest.utils import get_module_name


@pytest.fixture(autouse=True)
def insert_cwd_in_path():
    """Makes sure that the CWD is inserted to the front of sys.path.

    For the following tests, we do not call the CLI, so we skip the part
    where the CWD is added to sys.path. This fixture does it instead.
    """
    sys.path.insert(0, os.getcwd())


def test_discover_test_modules():
    modules = discover_test_modules("testbench/discovery")
    module_paths = {m.path for m in modules}

    assert len(modules) == 2
    assert module_paths == {
        "testbench/discovery/test_dut_discovery_1.py",
        "testbench/discovery/nested_tests/test_dut_discovery_2.py",
    }


def test_discover_duts():
    modules = discover_test_modules("testbench/discovery")
    dut_index = discover_duts(modules)
    dut_names = {
        module_name: set(duts.keys()) for module_name, duts in dut_index.items()
    }

    module_name_1 = get_module_name("testbench/discovery/test_dut_discovery_1.py")
    module_name_2 = get_module_name(
        "testbench/discovery/nested_tests/test_dut_discovery_2.py"
    )
    assert dut_names == {
        module_name_1: {"dut_1", "dut_2"},
        module_name_2: {"dut_3", "dut_4", "dut_5"},
    }


def test_discover_test_cases():
    modules = discover_test_modules("testbench/discovery")
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
