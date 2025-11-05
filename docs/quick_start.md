# Quick Start Guide

## Installation

### Option 1: From source (development)

```bash
git clone https://github.com/tnedr/agent-ops
cd agent-ops/agt
uv pip install -e .  # or: pip install -e .
```

**Note**: This project follows UV Cache Workflow Guidelines. If using `uv`, packages are cached globally (e.g., `E:\uv-cache`), keeping `.venv` minimal.

### Option 2: As submodule (Recommended)

```bash
# Add submodule
git submodule add -b main https://github.com/tnedr/agent-ops .tools
git submodule update --init --recursive

# Automated setup (creates venv with UV cache)
cd .tools
./bootstrap.sh
cd ../..
```

**Note**: The `bootstrap.sh` script uses UV for cache-aware installation. It automatically creates a minimal `.venv` and installs dependencies using the global cache (`UV_CACHE_DIR`). This ensures fast installs and minimal disk usage per project.

### Option 3: Via pipx (when published to PyPI)

```bash
pipx install agent-tools
```

### Submodule Workflow

When using `agent-tools` as a Git submodule (recommended for production):

| Aspect | Manual Clone | Submodule |
|--------|--------------|-----------|
| **Version Pinning** | Manual tracking | Git commit points to exact state |
| **One-line Clone** | `git clone ... && cd .tools/agt` | `git clone ... && git submodule update --init --recursive` |
| **VS Code Paths** | Machine-specific absolute paths | Stable `${workspaceFolder}/.tools/agt` |
| **Dependency Updates** | Manual pull | Explicit `git submodule update --remote` + commit |
| **Reproducibility** | Depends on manual sync | Deterministic (commit hash) |

**Benefits of submodule approach:**
- ✅ Version pinning ensures reproducible builds
- ✅ Stable paths work across different machines
- ✅ Explicit updates prevent unexpected changes
- ✅ CI/CD can use specific commit hashes

**Updating submodule:**
```bash
# Update to latest main branch
git submodule update --remote .tools
git commit -m "chore: update agent-tools submodule"
```

## Basic Usage

### First-time Setup

If using the submodule approach, run the bootstrap script once:

```bash
git submodule update --init --recursive
cd .tools
./bootstrap.sh
cd ../..

# Test the setup
./scripts/agt.sh run env.check  # or: cd .tools/.venv/bin && ./agt run env.check
```

This will:
- Create a minimal `.venv` using `uv venv` (UV Cache Workflow compliant)
- Install agent-tools with CLI extras (colorama)
- Test the venv with `env.check` command

### 1. Start an agent worktree

```bash
agt start
# or with wrapper: ./scripts/agt.sh start
```

This creates:
- A unique agent ID (e.g., `agent-a1b2c3d4`)
- A new Git worktree in `.work/agent-a1b2c3d4`
- A new branch `feat/agent-a1b2c3d4`
- Sets `AGENT_ID` environment variable

### 2. Run commands in the worktree

```bash
agt run python my_script.py
agt run "git add . && git status"
agt run npm install
```

Commands run in the isolated worktree directory.

### 3. Commit changes

```bash
agt commit "feat: add new feature"
```

This stages all changes and creates a commit in the worktree.

### 4. Push to remote

```bash
agt push
```

This pushes the branch to the remote repository. You can then open a PR manually in the GitHub UI.

### 5. Merge locally (optional)

```bash
agt merge
```

This merges the branch into `main` using fast-forward merge. **Warning:** Only works if you have write access to `main` and no branch protection rules. Otherwise, use manual PR review.

### 6. Clean up (optional)

```bash
agt clean
```

This removes the worktree after you're done. The branch remains on the remote.

## Complete Workflow Example

```bash
# Start isolated worktree
agt start

# Generate code or make changes
agt run "python my_script.py"

# Commit changes
agt commit "feat: add generated code"

# Push to remote
agt push          # open PR manually in GitHub UI

# Optional: merge locally (if permitted)
agt merge         # only if no branch protection

# Optional: cleanup after merge
agt clean
```

## Environment Variables

- `AGENT_ID`: Set automatically by `agt start`, used by `run`, `commit`, `push`, and `clean`

## Requirements

- Python 3.11+
- Git with worktree support

