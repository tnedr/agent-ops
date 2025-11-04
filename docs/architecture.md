# Architecture

## Overview

`agent-tools` provides a Python-based toolkit for managing isolated Git worktrees for agent workflows. It replaces shell scripts with a maintainable, testable Python package.

## Package Structure

```
agt/
├── __init__.py          # Package metadata
├── __main__.py          # Allows `python -m agt`
├── worktree.py          # Low-level Git worktree operations
└── cli.py               # CLI entrypoint and command handlers
```

## Core Components

### `agt.worktree`

Low-level Git worktree operations:

- `get_repo_root()`: Find Git repository root
- `generate_agent_id()`: Generate unique agent IDs
- `add_worktree()`: Create new worktree and branch
- `remove_worktree()`: Clean up worktree
- `find_pr_bot()`: Locate `pr_bot.py` script

### `agt.cli`

Command-line interface:

- `cmd_start()`: Initialize agent worktree
- `cmd_run()`: Execute commands in worktree
- `cmd_finish()`: Complete workflow with PR creation and merge

## Workflow

1. **Start**: User runs `agt start`
   - Generates unique agent ID
   - Creates worktree in `.work/agent-<id>`
   - Creates branch `feat/agent-<id>`
   - Sets `AGENT_ID` environment variable

2. **Run**: User runs `agt run <command>`
   - Validates `AGENT_ID` is set
   - Executes command in worktree directory
   - Output returned to user

3. **Commit**: User runs `agt commit "<message>"`
   - Stages all changes (`git add -A`)
   - Creates commit with provided message
   - Prints confirmation

4. **Push**: User runs `agt push`
   - Pushes branch to remote repository
   - Sets upstream tracking
   - User opens PR manually in GitHub UI

5. **Clean** (optional): User runs `agt clean`
   - Removes worktree directory
   - Cleans up Git worktree references
   - Branch remains on remote

### Git Worktree

Uses Git's native worktree feature:

- Each agent gets isolated filesystem directory
- Shares Git objects with main repository
- Independent branch state

## Distribution

### Installation Methods

1. **Submodule**: Clone as Git submodule
2. **PyPI**: Install via `pip install agent-tools` (when published)
3. **GitHub Action**: Use composite action in CI/CD

### Entry Points

- `python -m agt`: Run as module
- `agt` command: Via `console_scripts` in `pyproject.toml`
- `bin/agt`: Standalone script for submodule installations

## Testing

- Unit tests in `tests/` directory
- Uses `pytest` framework
- Tests worktree operations with mock repositories

## Future Enhancements

- Support for multiple concurrent worktrees
- Worktree state persistence
- Configurable worktree locations
- Integration with more PR automation tools

