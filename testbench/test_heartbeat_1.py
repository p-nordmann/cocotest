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
    await Timer(1, unit="us")
