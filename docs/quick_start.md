# Quick Start Guide

## Installation

### Option 1: From source (development)

```bash
git clone https://github.com/<ORG>/agent-tools
cd agent-tools/agt
pip install -e .
```

### Option 2: As submodule

```bash
git submodule add -b main https://github.com/<ORG>/agent-tools .tools
cd .tools/agt
pip install -e .
```

### Option 3: Via pipx (when published to PyPI)

```bash
pipx install agent-tools
```

## Basic Usage

### 1. Start an agent worktree

```bash
agt start
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

### 5. Clean up (optional)

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

# Optional: cleanup after PR is merged
agt clean
```

## Environment Variables

- `AGENT_ID`: Set automatically by `agt start`, used by `run`, `commit`, `push`, and `clean`

## Requirements

- Python 3.11+
- Git with worktree support

