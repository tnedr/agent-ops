# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-XX

### Added

- Initial release of agent-tools
- `agt start` command to create isolated worktrees
- `agt run` command to execute commands in worktree
- `agt commit` command to commit changes
- `agt push` command to push branch to remote
- `agt merge` command for fast-forward merge (optional)
- `agt clean` command to remove worktree
- Python package structure with CLI entrypoint
- Comprehensive test suite (unit, integration, negative tests)
- 80%+ code coverage requirement in CI
- GitHub Actions workflows for CI/CD and releases
- Documentation (quick start, CLI reference, architecture)

### Features

- Git worktree management
- Unique agent ID generation
- Environment variable management
- Cross-platform support (Windows, Linux, macOS)
- Local CLI-only workflow (no PR-bot dependencies)
- Manual PR creation workflow
- Windows compatibility fixes (Unicode fallback, commit command)

### Fixed

- **Windows compatibility**: Commit command now uses argument list instead of shell command (fixes quote parsing issues)
- **Unicode encoding**: Automatic fallback to ASCII-safe characters on Windows terminals
- **Package structure**: Fixed hatchling build configuration for flat package structure

### Testing

- Unit tests for worktree operations and CLI commands
- Integration tests with temporary Git repositories
- Negative test cases for error handling
- Coverage reporting with 80% minimum threshold
- CI workflow with linting and test automation

