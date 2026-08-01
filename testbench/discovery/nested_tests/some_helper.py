from cocotb.handle import HierarchyObject

from cocotest import DUTSpec

dut_3 = DUTSpec(
    "ghdl",
    ["testbench/heartbeat.vhd"],
    "heartbeat",
    "vhdl",
    [],
    [],
    [],
)


async def test_should_not_be_discovered_3(dut_3: HierarchyObject): ...
