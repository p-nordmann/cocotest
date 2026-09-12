from cocotb.handle import HierarchyObject
from cocotb.triggers import Timer
from cocotb.types import Logic

from cocotest import DUTSpec

dut = DUTSpec(
    "ghdl",
    ["testbench/heartbeat/heartbeat.vhd"],
    "heartbeat",
    "vhdl",
    ["--std=08"],
    ["--std=08"],
)


async def test_heartbeat_pass(dut: HierarchyObject):
    await Timer(1, unit="us")
    # Here we ensure the DUT is correctly passed to the test
    assert dut.clk.value == Logic(1)
