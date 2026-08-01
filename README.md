# cocotest

Cocotest is a simple test orchestration framework for cocotb.

## Status

More README coming soon...

## Quickstart

Cocotest is intended to work in similar fashion to pytest.
We do not intend to provide as many features as pytest, far from it, but we take a lot of inspiration from it.
Cocotest should feel familiar for developers with experience in the Python ecosystem.

### Installation

Currently, we do not provide a distribution on PyPI, but we intend to change that in the near future!

For now, you may install from the Github repository instead. Example with uv or pip:

```
# You may target master:
uv add "cocotest @ git+https://github.com/p-nordmann/cocotest"

# Or you may target a specific revision:
uv add "cocotest @ git+https://github.com/p-nordmann/cocotest@some_revision"

# Similarly, with pip:
pip install git+https://github.com/p-nordmann/cocotest@some_revision
```

### Getting started

Once cocotest is installed, you can run your tests with the following command:

```
cocotest /path/to/tests

# Or with uv:
uv run cocotest /path/to/tests
```

Of course, you need to write your tests in such a way that cocotest knows what to do with them:

```
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
```

Here there are two important things:

- `dut = DUTSpec(...)`: this is where we tell cocotest about the DUT that we will use, so it knows how to launch cocotb;
- `async def test_heartbeat_pass(dut: HierarchyObject)`: here we declare a test.

There are 3 conditions for our test to be detected by cocotest:

- `async def`: the test function must be asynchronous, as it will be run inside cocotb and manipulate the DUT;
- `test_...`: its name must start with "test\_" so cocotest knows how to find it;
- `dut`: its DUT argument for the cocotb test must have the same name as some `DUTSpec` instance present in the scope. This way, cocotest will know what cocotb test to launch with which DUT.

And... that's it! Just use the `cocotest` command and your test will run.
No need for fancy makefiles, no need for `@cocotb.test`; you can now define various DUTs to use in various test cases which will be automatically run by cocotest. :)

## Contributing

Before contributing, read [CONTRIBUTING.md](./CONTRIBUTING.md).

Note: contributions are closed for the moment.

## Testing cocotest

Cocotest is made for running cocotb tests, but it must itself be tested so we know it works.
For this, we rely on good old pytest.

### A word about test dependencies

Most of the tests can be run with the dev dependencies from the uv project.
However, some tests will try to spawn a cocotest subprocess.
With this cocotest call, they will try to run ghdl.
For that reason, you need to install ghdl if you want to be able to run all of the tests.

### Running the tests

Once you have all the dependencies installed, you can run the tests using pytest:

```
# with uv:
uv run pytest tests

# or, if you have a virtual env active:
pytest tests
```

## License

This work is distributed under the MIT license, see the LICENSE file for more information.
