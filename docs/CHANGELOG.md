# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-XX

### Added

- Initial release of agent-tools
- `agt start` command to create isolated worktrees
- `agt run` command to execute commands in worktree
- `agt finish` command to create PR and merge
- Integration with `pr_bot.py` for PR automation
- Python package structure with CLI entrypoint
- Basic documentation (quick start, CLI reference, architecture)
- Test suite with pytest
- GitHub Actions workflows for CI/CD

### Features

- Git worktree management
- Unique agent ID generation
- Environment variable management
- PR bot script discovery
- Cross-platform support (Windows, Linux, macOS)

