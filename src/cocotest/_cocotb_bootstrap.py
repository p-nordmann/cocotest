"""
This module serves as an entrypoint for cocotb runner.

It makes sure to wrap the target test function into cocotb.test
"""

import os
import sys

import cocotb

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

# Mark the test function as a test for cocotb
selected_test = cocotb.test(
    name=f"cocotest_{function_name}",
)(function)
