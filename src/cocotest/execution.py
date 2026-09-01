import os
from contextlib import contextmanager
from dataclasses import dataclass
from enum import StrEnum
from subprocess import CalledProcessError

from cocotb_tools.runner import get_results, get_runner

from .core_types import TestCase


class TestStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    BUILD_ERROR = "build_error"
    RUNTIME_ERROR = "runtime_error"
    SKIP = "skip"
    XFAIL = "xfail"
    XPASS = "xpass"


@dataclass(frozen=True)
class TestResult:
    status: TestStatus
    build_log: str | None = None
    test_log: str | None = None


def run_test(case: TestCase) -> TestResult:
    xskip = getattr(case.function, "_cocotest_skip", False)
    xfail = getattr(case.function, "_cocotest_xfail", False)

    if xskip:
        return TestResult(TestStatus.SKIP)

    result = _run_test(case)
    if not xfail:
        return result

    if result.status == TestStatus.PASS:
        return TestResult(TestStatus.XPASS, result.build_log, result.test_log)
    if result.status == TestStatus.FAIL:
        return TestResult(TestStatus.XFAIL, result.build_log, result.test_log)
    if result.status == TestStatus.BUILD_ERROR:
        return TestResult(TestStatus.XFAIL, result.build_log, result.test_log)
    if result.status == TestStatus.RUNTIME_ERROR:
        return TestResult(TestStatus.XFAIL, result.build_log, result.test_log)

    raise RuntimeError(f"unexpected status '{result.status.name}'")


def _run_test(case: TestCase) -> TestResult:
    build_dir = os.path.join(
        "sim_build", case.module.__name__, case.function.__name__
    )  # TODO: one build dir per dut?

    # cocotb Runner changes its failure semantics when PYTEST_CURRENT_TEST
    # is present: failed cocotb tests cause SystemExit instead of returning
    # the results XML. Cocotest needs consistent runner semantics regardless
    # of whether its caller happens to be pytest.
    with _without_pytest_context():
        runner = get_runner(case.dut.simulator)

        try:
            runner.build(
                hdl_library="work",
                sources=case.dut.sources,
                build_args=case.dut.build_args,
                hdl_toplevel=case.dut.hdl_toplevel,
                build_dir=build_dir,
                log_file=os.path.join(build_dir, "build_logs.log"),
            )
        except CalledProcessError:
            return TestResult(
                TestStatus.BUILD_ERROR, os.path.join(build_dir, "build_logs.log")
            )

        try:
            results_path = runner.test(
                test_module="cocotest._cocotb_bootstrap",
                hdl_toplevel=case.dut.hdl_toplevel,
                hdl_toplevel_library="work",
                hdl_toplevel_lang=case.dut.lang,
                test_args=case.dut.test_args,
                extra_env={
                    "COCOTEST_IMPORT_ROOT": os.getcwd(),
                    "COCOTEST_TEST_MODULE": os.path.abspath(case.path),
                    "COCOTEST_TEST_FUNCTION": case.function.__name__,
                    "COCOTEST_CWD": os.getcwd(),
                },
                build_dir=build_dir,
                test_dir=build_dir,  # WARNING: must be the same as build_dir
                test_filter=f"\.{case.function.__name__}$",
                log_file=os.path.join(build_dir, "test_logs.log"),
            )
        except SystemExit:
            return TestResult(
                TestStatus.RUNTIME_ERROR,
                os.path.join(build_dir, "build_logs.log"),
                os.path.join(build_dir, "test_logs.log"),
            )

        total, failures = get_results(results_path)

    return TestResult(
        TestStatus.PASS if failures == 0 else TestStatus.FAIL,
        os.path.join(build_dir, "build_logs.log"),
        os.path.join(build_dir, "test_logs.log"),
    )


@contextmanager
def _without_pytest_context():
    """Temporarily suppresses pytest's PYTEST_CURRENT_TEST env variable."""
    value = os.environ.pop("PYTEST_CURRENT_TEST", None)
    try:
        yield
    finally:
        if value is not None:
            os.environ["PYTEST_CURRENT_TEST"] = value
