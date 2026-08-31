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


async def test_heartbeat_should_run(dut: HierarchyObject):
    print("Inside test: test_heartbeat_should_run")
    await Timer(1, unit="us")


async def test_heartbeat_should_not_run_1():
    print("Inside test: test_heartbeat_should_not_run_1")
    await Timer(1, unit="us")


def test_heartbeat_should_not_run_2(dut: HierarchyObject):
    print("Inside test: test_heartbeat_should_not_run_2")
    pass


async def not_a_test(dut: HierarchyObject):
    print("Inside test: not_a_test")
    await Timer(1, unit="us")
