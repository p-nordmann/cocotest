# Contributing

This file will explain what you need to know in order to contribute to the project.

TODO

## Contributions status

Contributions are closed for now.

## Roadmap

### Documentation

<u>**Difficulty:**</u> ⭐ (easy)

We need to setup a documentation system so we can generate docs from the current state of the repository.

In particular, we want to document all current features. This should not be too long as there are very few.

### Test skipping

<u>**Difficulty:**</u> ⭐ (easy)

This feature will be simple: decorate a test with `cocotest.skip` in order to skip it.

```
@cocotest.skip
async def test_my_super_test(dut):
    ...
```

Currently this is not implemented.

### Fixtures

<u>**Difficulty:**</u> ⭐/⭐⭐ (easy to medium)

TODO

### Filtering: `-k` option in the command line

<u>**Difficulty:**</u> ⭐/⭐⭐ (easy to medium)

Currently, we can only specify a directory or a file path when running cocotest.

We want to provide a finer way to filter tests with the `-k` option in the command line, similar to pytest.

We want to support exact substring match across file names, test names, dut names.
On top of that we want to support simple combination of patterns with `and`, `or` and `not` keywords.

Example:

```
cocotest -k 'my_dut and not some_test'
```

Note: it is left to be specified whether the `-k` option should take priority over test skipping.

### Avoiding virtual environment directories

<u>**Difficulty:**</u> ⭐/⭐⭐ (easy to medium)

TODO

### Imports from within test files during cocotb discovery

<u>**Difficulty:**</u> ⭐⭐ (medium)

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

### Logging

<u>**Difficulty:**</u> ⭐⭐⭐ (hard)

TODO

### Multiprocessing: `-j` parameter

<u>**Difficulty:**</u> ⭐⭐⭐ (hard)

TODO

### Debugger frontend

<u>**Difficulty:**</u> ⭐⭐⭐ (hard)

TODO
