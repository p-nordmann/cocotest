from cocotb.handle import HierarchyObject

from cocotest import DUTSpec

dut = DUTSpec(
    "ghdl",
    ["testbench/heartbeat.vhd"],
    "heartbeat",
    "vhdl",
    ["--std=08"],
    ["--std=08"],
    [],
)


async def test_heartbeat_pass(dut: HierarchyObject):
    print("Inside test: test_heartbeat_pass")
    pass
