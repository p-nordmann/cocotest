from cocotb.handle import HierarchyObject
from cocotb.triggers import Timer

import cocotest
from cocotest import DUTSpec

# Regular heartbeat, no RTL error here.
dut_heartbeat = DUTSpec(
    "ghdl",
    ["testbench/heartbeat/heartbeat.vhd"],
    "heartbeat",
    "vhdl",
    ["--std=08"],
    ["--std=08"],
)


async def test_python_error(dut_heartbeat: HierarchyObject):
    await Timer(1, unit="us")
    assert False, "this is a python error"


@cocotest.mark.skip
async def test_python_error_skipped(dut_heartbeat: HierarchyObject):
    await Timer(1, unit="us")
    assert False, "this is a python error"


# RTL file with a syntax error.
dut_syntax_error = DUTSpec(
    "ghdl",
    ["testbench/failures/heartbeat_syntax_error.vhd"],
    "heartbeat",
    "vhdl",
    ["--std=08"],
    ["--std=08"],
)


async def test_build_error(dut_syntax_error: HierarchyObject):
    await Timer(1, unit="us")


# RTL file with a runtime error.
dut_runtime_error = DUTSpec(
    "ghdl",
    ["testbench/failures/heartbeat_runtime_error.vhd"],
    "heartbeat",
    "vhdl",
    ["--std=08"],
    ["--std=08"],
)


async def test_runtime_error(dut_runtime_error: HierarchyObject):
    await Timer(1, unit="us")
