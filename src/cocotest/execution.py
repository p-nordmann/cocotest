import os

from cocotb_tools.runner import get_runner

from .core_types import TestCase


def run_test(test_case: TestCase):
    dut = test_case.dut
    import_root = os.getcwd()
    module_path = os.path.abspath(test_case.path)
    function_name = test_case.function.__name__
    module_name = test_case.module.__name__

    build_dir = os.path.join(
        "sim_build", module_name, function_name
    )  # TODO: one build dir per dut?

    runner = get_runner(dut.simulator)
    runner.build(
        hdl_library="work",
        sources=dut.sources,
        build_args=dut.build_args,
        hdl_toplevel=dut.hdl_toplevel,
        build_dir=build_dir,
        log_file=os.path.join(build_dir, "build_logs.log"),
    )
    runner.test(
        test_module="cocotest._cocotb_bootstrap",
        hdl_toplevel=dut.hdl_toplevel,
        hdl_toplevel_library="work",
        hdl_toplevel_lang=dut.lang,
        elab_args=dut.elab_args,
        test_args=dut.extra_args,
        extra_env={
            "COCOTEST_IMPORT_ROOT": import_root,
            "COCOTEST_TEST_MODULE": module_path,
            "COCOTEST_TEST_FUNCTION": function_name,
            "COCOTEST_CWD": os.getcwd(),
        },
        build_dir=build_dir,
        test_dir=build_dir,  # WARNING: must be the same as build_dir
        test_filter=f"\.{function_name}$",
    )
