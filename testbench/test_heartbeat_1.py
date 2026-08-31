from cocotb.handle import HierarchyObject
from cocotb.triggers import Timer

from cocotest import DUTSpec

dut = DUTSpec(
    "ghdl",
    ["testbench/heartbeat.vhd"],
    "heartbeat",
    "vhdl",
    ["--std=08"],
    ["--std=08"],
)


async def test_heartbeat_pass(dut: HierarchyObject):
    print("Inside test: test_heartbeat_pass")
    await Timer(1, unit="us")
