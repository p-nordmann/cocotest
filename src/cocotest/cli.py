import argparse
import os
import sys

from .discovery import discover_duts, discover_test_cases, discover_test_modules
from .execution import run_test


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

    # Process test cases
    for case in cases:
        run_test(case)
