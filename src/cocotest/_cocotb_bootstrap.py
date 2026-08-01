"""
This module serves as an entrypoint for cocotb runner.

It makes sure to wrap the target test function into cocotb.test
"""

import os
import sys

import cocotb
from cocotb.handle import HierarchyObject

from .utils import get_module_name, import_from_path

# Retrieve environment variables provided by the runner
import_root = os.environ["COCOTEST_IMPORT_ROOT"]
module_path = os.environ["COCOTEST_TEST_MODULE"]
function_name = os.environ["COCOTEST_TEST_FUNCTION"]

# Reproduce the same import as cocotest
sys.path.insert(0, import_root)
module_name = get_module_name(module_path)
module = import_from_path(module_path, module_name)
function = getattr(module, function_name)


# Wrap the test case into a function marked for cocotb
# TODO preprocess fixtures here
@cocotb.test(name=function_name)
async def testcase(dut: HierarchyObject):

    # Make sure to retrieve the expected working directory from the
    # environment variables and change current working directory.
    # Otherwise, we get the current working directory from the simulator,
    # which will most likely not match the expected working directory in
    # the test case.
    os.chdir(os.environ["COCOTEST_CWD"])

    return await function(dut)


# Hack the module name for display
module_name_short = os.path.basename(module_path)[:-3]
testcase.module = module_name_short
testcase.fullname = f"{module_name_short}.{function_name}"
