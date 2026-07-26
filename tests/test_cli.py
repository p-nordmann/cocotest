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
    code, output = _invoke("testbench/test_heartbeat_1.py")

    # For now this test is a bit specific: we make sure to find a few strings
    # in stdout so we know the test has run.
    assert "Running on GHDL" in output
    assert "running test_heartbeat_1.test_heartbeat_pass" in output
    assert "TESTS=1 PASS=1 FAIL=0 SKIP=0" in output

    # Additionally, we look for a custom string.
    assert "Inside test: test_heartbeat_pass\n" in output

    # Make sure we returned a correct exit code.
    assert code == 0


def test_heartbeat_should_not_run():
    code, output = _invoke("testbench/test_heartbeat_2.py")

    # Here we make sure that the first test runs and not the others.
    assert "Inside test: test_heartbeat_should_run\n" in output

    assert "Inside test: test_heartbeat_should_not_run_1\n" not in output
    assert "Inside test: test_heartbeat_should_not_run_2\n" not in output
    assert "Inside test: not_a_test\n" not in output

    # Make sure we returned a correct exit code.
    assert code == 0
