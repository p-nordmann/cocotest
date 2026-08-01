import os

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


async def test_heartbeat_getcwd(dut: DUTSpec):
    print("Inside test: test_heartbeat_getcwd")
    print(f"os.getcwd: {os.getcwd()}")
    pass
