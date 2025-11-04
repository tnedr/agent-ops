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

```yaml
- name: Auto-merge with PR-bot
  uses: ./actions/pr-bot
  with:
    ci: "false"    # Wait for green CI checks (true/false)
    force: "false" # Admin override - merge even with red checks
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Configuration:**

- `ci`: Set to `"true"` to wait for CI checks to pass before merging
- `force`: Set to `"true"` to merge even if checks fail (requires admin permissions)

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
├── .github/
│   └── workflows/       # GitHub workflows
└── pyproject.toml       # Root workspace configuration
```

## License

MIT

