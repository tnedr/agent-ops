# agent-ops

Modular PR-bot and Agent/Doc-Ops GitHub Actions repository.

## Overview


This repository contains reusable GitHub Actions for automating PR workflows and agent operations.

## Actions

### PR Bot (`actions/pr-bot`)

One-shot GitHub PR automator with optional CI polling.

**Features:**
- Auto-merge PRs with squash merge
- Optional CI check polling (wait for green checks)
- Admin override flag (`--force`) to merge even with failed checks
- Automatic branch deletion after merge
- Works in both standalone mode and GitHub Actions context

**Usage:**

**From another repository:**

```yaml
name: Auto-merge PR

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

jobs:
  merge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Auto-merge with PR-bot
        uses: tnedr/agent-ops/actions/pr-bot@main
        with:
          ci: "false"    # Wait for green CI checks (true/false)
          force: "false" # Admin override - merge even with red checks
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**From the same repository (local path):**

```yaml
name: Auto-merge PR

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review, labeled]

jobs:
  merge:
    # Only run if PR has 'automerge' label - prevents infinite loops
    if: contains(github.event.pull_request.labels.*.name, 'automerge')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Auto-merge with PR-bot
        uses: ./actions/pr-bot
        with:
          ci: "false"
          force: "false"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Note:** The workflow requires an `automerge` label on the PR to prevent infinite loops when the bot merges PRs.

**Configuration:**

- `ci`: Set to `"true"` to wait for CI checks to pass before merging (default: `"false"`)
- `force`: Set to `"true"` to merge even if checks fail (requires admin permissions, default: `"false"`)

**Versioning:**

You can use specific versions:
- `@main` - Latest from main branch (may be unstable)
- `@v1` - Specific version tag (recommended for production)
- `@v1.0.0` - Exact version tag

To create a version tag:
```bash
git tag v1
git push origin v1
```

## Development

This project follows UV Cache Workflow Guidelines:

- Uses `uv` for package management
- Minimal `.venv`, maximum cache usage
- Global cache location: `E:\uv-cache` (Windows)

### Setup

```bash
# Install dependencies
uv pip install -e .
```

### Structure

```
agent-ops/
├── actions/
│   └── pr-bot/          # PR automation action
├── agt/                 # Agent tools Python package
│   ├── __init__.py
│   ├── cli.py           # CLI commands (start, run, finish)
│   ├── worktree.py      # Git worktree management
│   └── pyproject.toml
├── bin/
│   └── agt              # Standalone entrypoint script
├── docs/                 # Documentation
│   ├── quick_start.md
│   ├── cli_reference.md
│   ├── AGENT-INTEGRATION.md
│   ├── WORKFLOW-SYNTAX.md
│   └── ...
├── tests/               # Test suite
├── examples/            # Usage examples
├── .github/
│   ├── workflows/       # GitHub workflows
│   └── actions/         # Reusable actions
└── pyproject.toml       # Root workspace configuration
```

## Agent Tools

This repository also includes `agent-tools`, a Python CLI for managing isolated Git worktrees for agent workflows.

### Local agent workflow (no CI, no bot)

```bash
# Install agent-tools
cd agt
pip install -e .

# Use it
agt start                    # Create isolated worktree + branch
agt run "python my_task.py"  # Generate code
agt commit "feat: add generated code"
agt push                    # Push branch (open PR manually)

# Optional cleanup after PR is merged
agt clean                   # Remove worktree
```

See [agt/README.md](agt/README.md) for more details.

## Documentation

See the [docs/](docs/) directory for detailed documentation:

- [Quick Start](docs/quick_start.md) - Get started with agent-tools
- [CLI Reference](docs/cli_reference.md) - Complete command reference
- [Architecture](docs/architecture.md) - Architecture overview
- [Changelog](docs/CHANGELOG.md) - Version history

**Note:** Some documentation files (AGENT-INTEGRATION.md, WORKFLOW-SYNTAX.md, etc.) may contain references to PR-bot functionality that is no longer part of this repository.

## License

MIT

