from cocotb.handle import HierarchyObject

from cocotest import DUTSpec
from testbench.discovery.nested_tests.some_helper import dut_3

dut_4 = DUTSpec(
    "ghdl",
    ["testbench/heartbeat.vhd"],
    "heartbeat",
    "vhdl",
    [],
    [],
    [],
)

dut_5 = DUTSpec(
    "ghdl",
    ["testbench/heartbeat.vhd"],
    "heartbeat",
    "vhdl",
    [],
    [],
    [],
)


async def test_should_be_discovered_3(dut_3: HierarchyObject): ...


async def test_should_be_discovered_4(dut_4: HierarchyObject): ...


async def test_should_be_discovered_5(dut_5: HierarchyObject): ...
