import os

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


async def test_heartbeat_getcwd(dut: HierarchyObject):
    assert os.getcwd() == os.environ["TEST_EXPECTED_CWD"]
    await Timer(1, unit="us")
