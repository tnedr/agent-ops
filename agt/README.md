# agent-tools

Worktree-based agent workflow management toolkit.

## Overview

`agent-tools` provides a Python-based CLI for managing isolated Git worktrees for agent workflows. It replaces shell scripts with a maintainable, testable Python package that can be used locally, as a submodule, or in CI/CD pipelines.

## Features

- **Isolated Worktrees**: Each agent gets its own isolated Git worktree
- **Simple CLI**: `start`, `run`, `commit`, `push`, `clean` commands
- **Manual PR Creation**: Push branch and create PR manually in GitHub UI
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Installable**: Can be installed via pip or used as submodule

## Quick Start

### Installation

```bash
# From source
cd agt
pip install -e .

# Or as submodule
git submodule add -b main https://github.com/<ORG>/agent-tools .tools
cd .tools/agt
pip install -e .
```

### Usage

```bash
# Start a new agent worktree
agt start

# Run commands in the worktree
agt run python my_script.py

# Commit changes
agt commit "feat: new feature"

# Push to remote (then open PR manually)
agt push

# Optional: cleanup after PR is merged
agt clean
```

## Documentation

- [Quick Start Guide](docs/quick_start.md)
- [CLI Reference](docs/cli_reference.md)
- [Architecture](docs/architecture.md)
- [Changelog](docs/CHANGELOG.md)

## Examples

See the [examples/](examples/) directory for:
- `demo_local.sh`: Local workflow example
- `demo_action.yml`: GitHub Actions workflow example

## Development

### Setup

```bash
cd agt
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/ -v
```

### Run Linter

```bash
ruff check .
```

## Project Structure

```
agt/
├── __init__.py          # Package metadata
├── __main__.py          # Allows `python -m agt`
├── worktree.py          # Low-level Git worktree operations
├── cli.py               # CLI entrypoint and command handlers
└── pyproject.toml        # Package configuration

bin/
└── agt                  # Standalone entrypoint script

docs/                    # Documentation
tests/                   # Test suite
examples/                # Usage examples
.github/                 # CI/CD workflows and actions
```

## License

MIT

