import os
import subprocess


def _invoke(*arguments: str) -> tuple[int, str]:
    result = subprocess.run(
        ["cocotest", *arguments],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return result.returncode, result.stdout


def test_heartbeat_should_pass():
    code, output = _invoke("testbench/heartbeat/test_heartbeat_1.py")

    # Make sure the test is in output
    assert (
        "testbench/heartbeat/test_heartbeat_1.py::test_heartbeat_pass: PASS" in output
    )

    # Make sure we returned a correct exit code.
    assert code == 0


def test_heartbeat_should_not_run():
    code, output = _invoke("testbench/heartbeat/test_heartbeat_2.py")

    # Here we make sure that the first test runs and not the others.
    assert (
        "testbench/heartbeat/test_heartbeat_2.py::test_heartbeat_should_run: PASS"
        in output
    )

    assert "test_heartbeat_should_not_run_1" not in output
    assert "test_heartbeat_should_not_run_2" not in output
    assert "not_a_test" not in output

    # Make sure we returned a correct exit code.
    assert code == 0


def test_cwd_should_be_the_same():
    os.environ["TEST_EXPECTED_CWD"] = os.getcwd()
    code, output = _invoke("testbench/heartbeat/test_heartbeat_3.py")

    # We make sure that the test runs and passes
    assert (
        "testbench/heartbeat/test_heartbeat_3.py::test_heartbeat_getcwd: PASS" in output
    )
    assert code == 0


def test_error_code_failures():
    code, output = _invoke("testbench/failures/test_failures.py")

    assert "testbench/failures/test_failures.py::test_python_error: FAIL" in output
    assert (
        "testbench/failures/test_failures.py::test_build_error: BUILD_ERROR" in output
    )
    assert (
        "testbench/failures/test_failures.py::test_runtime_error: RUNTIME_ERROR"
        in output
    )
    assert code == 1


def test_error_code_skip():
    code, output = _invoke("testbench/failures/test_skip.py")

    assert "testbench/failures/test_skip.py::test_python_error_skipped: SKIP" in output
    assert code == 0


def test_error_code_xfail():
    code, output = _invoke("testbench/failures/test_xfail_xpass.py")

    assert (
        "testbench/failures/test_xfail_xpass.py::test_python_error_xfail: XFAIL"
        in output
    )
    assert (
        "testbench/failures/test_xfail_xpass.py::test_heartbeat_xpass: XPASS" in output
    )
    assert (
        "testbench/failures/test_xfail_xpass.py::test_build_error_xfail: XFAIL"
        in output
    )
    assert (
        "testbench/failures/test_xfail_xpass.py::test_runtime_error_xfail: XFAIL"
        in output
    )
    assert code == 0
