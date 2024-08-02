## Setting Up Local Development Environment
### Poetry
Poetry is used to manage dependencies and virtual environments. To install poetry, run the following command:
```bash
brew install pipx
pipx install poetry
```

To install the dependencies, run the following command:
```bash
poetry install
```

To activate the virtual environment, run the following command:
```bash
poetry shell
```

### Pre-Commit
Additionally, pre-commit is used to manage pre-commit hooks. The following hooks are used:
- ruff -- for python linting and formatting
- mypy -- for static type checking

To install pre-commit, run the following command:
```bash
brew install pre-commit
```

To install the pre-commit hooks, run the following command:
```bash
pre-commit install
```

## Running tests
Pytest is used to run tests. To run tests, run the following command:
```bash
poetry run pytest
```
