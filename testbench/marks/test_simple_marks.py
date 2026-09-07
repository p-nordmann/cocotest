from cocotb.handle import HierarchyObject
from cocotb.triggers import Timer

import cocotest
from cocotest import DUTSpec

# Regular heartbeat, no RTL error here.
dut = DUTSpec(
    "ghdl",
    ["testbench/heartbeat/heartbeat.vhd"],
    "heartbeat",
    "vhdl",
    ["--std=08"],
    ["--std=08"],
)


@cocotest.mark.abc
async def test_mark_abc(dut: HierarchyObject):
    await Timer(1, unit="us")


@cocotest.mark.efg
async def test_mark_efg(dut: HierarchyObject):
    await Timer(1, unit="us")


@cocotest.mark.hij
@cocotest.mark.klm
async def test_mark_hij_klm(dut: HierarchyObject):
    # Here we make sure that we can safely add 2 marks
    await Timer(1, unit="us")
