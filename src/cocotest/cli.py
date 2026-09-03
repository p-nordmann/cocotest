import argparse
import os
import signal
import sys
from contextlib import contextmanager
from types import FrameType
from uuid import uuid4

from .discovery import discover_duts, discover_test_cases, discover_test_modules
from .execution import run_test
from .utils import terminate_session


def main():
    parser = argparse.ArgumentParser(
        prog="cocotest",
        description="collects and runs cocotb tests",
    )
    parser.add_argument(
        "path",
        default=".",
        help="test file or directory",
    )
    args = parser.parse_args()

    # Make sure to prepend the current working directory to sys.path
    sys.path.insert(0, os.getcwd())

    # Discover modules, duts and test cases
    test_modules = discover_test_modules(args.path)
    dut_index = discover_duts(test_modules)
    cases = discover_test_cases(test_modules, dut_index)

    # Note: in the case of some simulators, it seems that SIGINT is ignored by the
    # subprocesses when cocotb is terminated. This can be painful when developing
    # testbenches, so we make sure to kill the subprocesses when we receive SIGINT or SIGTERM.
    with _with_termination_cleanup():
        # Run test cases and exit with an error code.
        results = []
        for case in cases:
            result = run_test(case)
            print(f"{case.node_id}: {result.status.name}")
            results.append(result)

        for result in results:
            if result.is_failure():
                raise SystemExit(1)
        raise SystemExit(0)


@contextmanager
def _with_termination_cleanup():
    """Prepares the environment for running tests and makes sure to terminate
    subprocesses upon interruption.

    In order to find all the subprocesses that we should kill, we use a trick: we add
    a COCOTEST_SESSION environment variable before spawning them, so they inherit
    it automatically. Then, when being terminated, we look for all the processes
    with the correct COCOTEST_SESSION and kill them.

    Returns an exit code.
    """

    # We raise a custom exception on SIGINT and SIGTERM
    class Terminate(Exception):
        """Used when cocotest is interrupted with SIGTERM or SIGINT."""

    def on_terminate(signum: int, frame: FrameType | None):
        raise Terminate

    signal.signal(signal.SIGTERM, on_terminate)
    signal.signal(signal.SIGINT, on_terminate)

    # Here we prepare the environment variable
    os.environ["COCOTEST_SESSION"] = uuid4().hex

    # Then we wrap the actual logic, except, finally
    try:
        yield
    except Terminate:
        terminate_session()
        raise SystemExit(2)
    finally:
        os.environ.pop("COCOTEST_SESSION", None)
