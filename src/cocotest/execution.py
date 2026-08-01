import os

from cocotb_tools.runner import get_runner

from .core_types import TestCase


def run_test(case: TestCase):
    build_dir = os.path.join(
        "sim_build", case.module.__name__, case.function.__name__
    )  # TODO: one build dir per dut?

    runner = get_runner(case.dut.simulator)
    runner.build(
        hdl_library="work",
        sources=case.dut.sources,
        build_args=case.dut.build_args,
        hdl_toplevel=case.dut.hdl_toplevel,
        build_dir=build_dir,
        log_file=os.path.join(build_dir, "build_logs.log"),
    )
    runner.test(
        test_module="cocotest._cocotb_bootstrap",
        hdl_toplevel=case.dut.hdl_toplevel,
        hdl_toplevel_library="work",
        hdl_toplevel_lang=case.dut.lang,
        elab_args=case.dut.elab_args,
        test_args=case.dut.extra_args,
        extra_env={
            "COCOTEST_IMPORT_ROOT": os.getcwd(),
            "COCOTEST_TEST_MODULE": os.path.abspath(case.path),
            "COCOTEST_TEST_FUNCTION": case.function.__name__,
            "COCOTEST_CWD": os.getcwd(),
        },
        build_dir=build_dir,
        test_dir=build_dir,  # WARNING: must be the same as build_dir
        test_filter=f"\.{case.function.__name__}$",
    )
