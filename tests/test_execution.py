import os
import sys

import pytest

from cocotest.core_types import TestCase
from cocotest.discovery import discover_duts, discover_test_cases, discover_test_modules
from cocotest.execution import TestStatus, run_test


@pytest.fixture(autouse=True)
def insert_cwd_in_path():
    """Makes sure that the CWD is inserted to the front of sys.path.

    For the following tests, we do not call the CLI, so we skip the part
    where the CWD is added to sys.path. This fixture does it instead.
    """
    sys.path.insert(0, os.getcwd())


@pytest.fixture
def cases():
    modules = discover_test_modules("testbench/failures")
    dut_index = discover_duts(modules)
    cases = discover_test_cases(modules, dut_index)
    return {case.function.__name__: case for case in cases}


def test_test_python_error(cases: dict[str, TestCase]):
    case_python_error = cases["test_python_error"]
    result = run_test(case_python_error)
    assert result.status == TestStatus.FAIL


def test_test_build_error(cases: dict[str, TestCase]):
    case_build_error = cases["test_build_error"]
    assert run_test(case_build_error).status == TestStatus.BUILD_ERROR


def test_test_runtime_error(cases: dict[str, TestCase]):
    case_runtime_error = cases["test_runtime_error"]
    assert run_test(case_runtime_error).status == TestStatus.RUNTIME_ERROR


def test_python_error_skipped(cases: dict[str, TestCase]):
    case_python_error_skipped = cases["test_python_error_skipped"]
    result = run_test(case_python_error_skipped)
    assert result.status == TestStatus.SKIP


def test_python_error_xfail(cases: dict[str, TestCase]):
    case_python_error_xfail = cases["test_python_error_xfail"]
    assert run_test(case_python_error_xfail).status == TestStatus.XFAIL


def test_test_build_error_xfail(cases: dict[str, TestCase]):
    case_build_error_xfail = cases["test_build_error_xfail"]
    assert run_test(case_build_error_xfail).status == TestStatus.XFAIL


def test_test_runtime_error_xfail(cases: dict[str, TestCase]):
    case_runtime_error_xfail = cases["test_runtime_error_xfail"]
    assert run_test(case_runtime_error_xfail).status == TestStatus.XFAIL


def test_test_heartbeat_xpass(cases: dict[str, TestCase]):
    case_heartbeat_xpass = cases["test_heartbeat_xpass"]
    assert run_test(case_heartbeat_xpass).status == TestStatus.XPASS
