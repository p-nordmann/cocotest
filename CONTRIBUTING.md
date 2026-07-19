# Contributing

This file explains what you need to know in order to contribute to the project.

TODO

## Contributions status

Contributions are closed for now.

## Roadmap

### Imports from within test files during cocotb discovery

#### Current state

We deliberately decided to very few changes to the importing environment of test files.
We only add the current working directory to `sys.path`, to make sure the directory from which cocotest is called is accessible.
This way, test files can only import modules already available through the normal environment.

For instance, in the following case:

```
tests/
├── helpers.py
└── unit/
    ├── helpers.py
    └── test_example.py
```

If `test_example.py` has an `import helpers` statement, which module will be imported?

- if you run `cocotest` from `tests`, it will import `tests/helpers.py`;
- if you run it from `tests/unit` instead, it will import `tests/units/helpers.py`.

This solution makes things simple: we do not have to manage ambiguities.

Alternatively, if there is an `from . import helpers`, or `from .helpers import ...`, the import will fail, because we are not in a Python package.

#### Future improvements

A better UX would be to specify the import root from a configuration file.

We could support `cocotest.toml` or a `[tool.cocotest]` section in `pyproject.toml`.

Finding the configuration would start from the test file and recursively go up until finding one or hitting a boundary.

Boundaries would be:

- a cocotest.toml file,
- a pyproject.toml file,
- a VCS root (parent to a .git folder),
- the starting directory.

## Fixtures

TODO

## Multiprocessing: `-j` parameter

TODO

## Filtering: `-k` parameter

TODO

## Test skipping

TODO

## Logging

TODO

## Debugger frontend

TODO

## Documentation

TODO
