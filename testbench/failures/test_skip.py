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


@cocotest.mark.skip
async def test_python_error_skipped(dut_heartbeat: HierarchyObject):
    await Timer(1, unit="us")
    assert False, "this is a python error"
