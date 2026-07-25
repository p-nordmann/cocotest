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
    code, output = _invoke("testbench/test_heartbeat.py")

    # For now this test is a bit specific: we make sure to find a few strings
    # in stdout so we know the test has run.
    assert "Running on GHDL" in output
    assert "running test_heartbeat.test_heartbeat_pass" in output
    assert "TESTS=1 PASS=1 FAIL=0 SKIP=0" in output

    # Make sure we returned a correct exit code.
    assert code == 0
