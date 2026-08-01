from cocotb.handle import HierarchyObject

from cocotest import DUTSpec

dut_1 = DUTSpec(
    "ghdl",
    ["testbench/heartbeat.vhd"],
    "heartbeat",
    "vhdl",
    ["--std=08"],
    ["--std=08"],
    [],
)

dut_2 = DUTSpec(
    "ghdl",
    ["testbench/heartbeat.vhd"],
    "heartbeat",
    "vhdl",
    [],
    [],
    [],
)


async def test_should_be_discovered_1(dut_1: HierarchyObject): ...


async def test_should_be_discovered_2(dut_2: HierarchyObject): ...
