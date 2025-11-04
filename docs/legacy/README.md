# Legacy Documentation

## ⚠️ Deprecated - Do Not Use

These documentation files contain references to **PR-bot** and **GitHub Actions** functionality that has been **completely removed** from the current version of `agent-tools`.

**These files are archived for historical reference only. They are NOT applicable to the current version.**

The current version of `agent-tools` focuses on **local CLI workflow** only:
- `agt start` - Create isolated worktree
- `agt run` - Execute commands
- `agt commit` - Commit changes
- `agt push` - Push to remote
- `agt merge` - Merge locally (optional)
- `agt clean` - Remove worktree

## Files in this directory

- **AGENT-INTEGRATION.md** - Old integration guide for PR-bot and GitHub Actions
- **GITHUB-ACTION-GUIDE.md** - GitHub Actions workflow guide (deprecated)
- **COMPLETE-WORKFLOW.md** - Complete workflow with PR-bot (deprecated)
- **WORKFLOW-SYNTAX.md** - Workflow syntax reference for GitHub Actions (deprecated)

## Why deprecated?

The PR-bot and GitHub Actions functionality was removed to simplify the toolkit and focus on local development workflows. If you need automated PR merging, consider:

1. Using GitHub's built-in merge capabilities manually
2. Implementing a separate PR automation tool
3. Using GitHub Actions directly with your own workflow

## Current documentation

For up-to-date documentation, see:
- [Quick Start Guide](../quick_start.md)
- [CLI Reference](../cli_reference.md)
- [Architecture](../architecture.md)

