# agent-tools

Worktree-based agent workflow management toolkit.

## Overview

`agent-tools` provides a Python-based CLI for managing isolated Git worktrees for agent workflows. It enables agents to work in isolated environments, commit changes, push branches, and optionally merge locally—all without requiring PR automation bots or GitHub Actions.

## Features

- **Isolated Worktrees**: Each agent gets its own isolated Git worktree
- **Simple CLI**: `start`, `run`, `commit`, `push`, `merge`, `clean` commands
- **Manual PR Creation**: Push branch and create PR manually in GitHub UI
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Installable**: Can be installed via pip or used as submodule
- **Well-tested**: 80%+ test coverage with unit, integration, and negative tests

## Quick Start

### Installation

```bash
# From source
git clone https://github.com/tnedr/agent-ops
cd agent-ops/agt
uv pip install -e .  # or: pip install -e .

# Or as submodule
git submodule add -b main https://github.com/tnedr/agent-ops .tools
cd .tools/agt
uv pip install -e .  # or: pip install -e .
```

**Note**: This project follows UV Cache Workflow Guidelines. If using `uv`, ensure `UV_CACHE_DIR` is set (e.g., `E:\uv-cache` on Windows).

### Usage

```bash
# Start isolated worktree
agt start

# Generate code or make changes
agt run "python my_task.py"

# Commit changes
agt commit "feat: add generated code"

# Push to remote (then open PR manually)
agt push

# Optional: merge locally (if permitted)
agt merge         # Fast-forward merge to main

# Optional: cleanup after merge
agt clean         # Remove worktree
```

## Project Structure

```
agent-tools/
├── agt/                 # Python package (CLI + worktree helpers)
│   ├── __init__.py
│   ├── cli.py           # CLI commands (start, run, commit, push, merge, clean)
│   ├── worktree.py      # Git worktree management
│   └── pyproject.toml
├── bin/
│   └── agt              # Standalone entrypoint script
├── docs/                 # Documentation
│   ├── quick_start.md
│   ├── cli_reference.md
│   ├── architecture.md
│   └── legacy/          # Deprecated PR-bot documentation
├── tests/               # Test suite (80%+ coverage)
│   ├── test_worktree.py
│   ├── test_cli.py
│   ├── test_integration.py
│   └── test_negative.py
├── examples/            # Usage examples
├── .github/
│   └── workflows/       # CI/CD workflows
```

## Development

This project follows UV Cache Workflow Guidelines:

- Uses `uv` for package management
- Minimal `.venv`, maximum cache usage
- Global cache at `E:\uv-cache` (or `UV_CACHE_DIR`)

### Prerequisites

```bash
# Set UV cache directory (one-time setup)
# Windows PowerShell:
setx UV_CACHE_DIR "E:\uv-cache"

# Linux/Mac:
export UV_CACHE_DIR="$HOME/.uv-cache"
# Add to ~/.bashrc or ~/.zshrc for persistence
```

### Setup

```bash
cd agt

# Create minimal venv (if not exists)
python -m venv .venv --symlinks  # Windows
# or: python3 -m venv .venv --symlinks  # Linux/Mac

# Install with uv (uses global cache)
uv pip install -e ".[dev]"  # or: pip install -e ".[dev]"
```

**Note**: If using `uv`, ensure `UV_CACHE_DIR` is set (e.g., `E:\uv-cache` on Windows). This uses global cache for faster installs and minimal `.venv` size. The `.venv` should be minimal (< 50MB), while the global cache can be 5-15GB (shared across all projects).

### Run Tests

```bash
# All tests with coverage
pytest tests/ -v --cov=agt --cov-report=term-missing

# Only unit tests
pytest tests/test_worktree.py tests/test_cli.py -v

# Only integration tests
pytest tests/test_integration.py -v
```

### Run Linter

```bash
ruff check .
ruff check --select I .  # Check import sorting
```

## Documentation

See the [docs/](docs/) directory for detailed documentation:

- [Quick Start Guide](docs/quick_start.md) - Get started with agent-tools
- [CLI Reference](docs/cli_reference.md) - Complete command reference
- [Architecture](docs/architecture.md) - Architecture overview
- [Worktree Agent User Manual](docs/worktree_agent_user_manual.md) - Complete guide for using agent-tools with multiple concurrent agents
- [Changelog](docs/CHANGELOG.md) - Version history

**Note:** Legacy documentation files containing PR-bot and GitHub Actions references have been archived in [docs/legacy/](docs/legacy/). These are deprecated and not applicable to the current local CLI-only version.

## Installation Methods

### As Git Submodule (Recommended)

```bash
git submodule add -b main https://github.com/tnedr/agent-ops .tools
cd .tools/agt
uv pip install -e .  # or: pip install -e .
```

**Note**: Uses UV Cache Workflow - minimal `.venv`, global cache (`E:\uv-cache` or `UV_CACHE_DIR`).

### From PyPI (when published)

```bash
uv pip install agent-tools  # or: pip install agent-tools
# or
pipx install agent-tools
```

### From Source

```bash
git clone https://github.com/tnedr/agent-ops
cd agent-ops/agt
uv pip install -e .  # or: pip install -e .
```

## Versioning

This project uses semantic versioning. To use a specific version:

```bash
# Git submodule
git submodule add -b v0.1.0 https://github.com/tnedr/agent-ops .tools

# PyPI (when published)
uv pip install agent-tools==0.1.0  # or: pip install agent-tools==0.1.0
```

## Testing in Another Project

Want to try it out? See [Worktree Agent User Manual](docs/worktree_agent_user_manual.md) for a complete guide including multiple concurrent agents.

```bash
# Quick test
git submodule add -b main https://github.com/tnedr/agent-ops .tools
cd .tools/agt && uv pip install -e . && cd ../..
# or: cd .tools/agt && pip install -e . && cd ../..
agt start
agt run "echo 'test' > test.txt"
agt commit "test: verify agent-tools"
agt push
```

See [Worktree Agent User Manual](docs/worktree_agent_user_manual.md) for detailed troubleshooting and Windows PowerShell instructions.

## Contributing

Contributions are welcome! Please ensure:

- All tests pass: `pytest tests/ -v`
- Code coverage stays above 80%
- Code follows style guidelines: `ruff check .`

## License

MIT
