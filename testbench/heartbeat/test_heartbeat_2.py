from cocotb.handle import HierarchyObject
from cocotb.triggers import Timer

from cocotest import DUTSpec

dut = DUTSpec(
    "ghdl",
    ["testbench/heartbeat/heartbeat.vhd"],
    "heartbeat",
    "vhdl",
    ["--std=08"],
    ["--std=08"],
)


async def test_heartbeat_should_run(dut: HierarchyObject):
    await Timer(1, unit="us")


async def test_heartbeat_should_not_run_1():
    await Timer(1, unit="us")


def test_heartbeat_should_not_run_2(dut: HierarchyObject):
    pass


async def not_a_test(dut: HierarchyObject):
    await Timer(1, unit="us")
