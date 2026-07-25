# cocotest

Cocotest is a simple test orchestration framework for cocotb.

## Status

README coming soon...

## Contributing

Before contributing, read [CONTRIBUTING.md](./CONTRIBUTING.md).

Note: contributions are closed at the moment.

## Running the tests

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
