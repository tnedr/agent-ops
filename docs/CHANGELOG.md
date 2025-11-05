# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-01-XX

### Added

- **Domain-based CLI structure**: New `ws`, `cfg`, `env`, and `task` domains for better command organization
- **New workspace commands**: `agt ws new`, `agt ws run`, `agt ws save`, `agt ws push`, `agt ws merge`, `agt ws clean`
- **New config commands**: `agt cfg vscode` (replaces `agt vscode init`)
- **New environment commands**: `agt env check`, `agt env python`
- **Task module preview**: `agt task list/add/pick/done` commands reserved for future development (not yet implemented)
- **Alias system**: Legacy single-word commands still work with deprecation warnings
- **Complete command reference**: New [COMMANDS.md](docs/COMMANDS.md) documentation

### Changed

- **CLI refactoring**: Commands now use domain-based structure (`ws`, `cfg`, `env`) instead of single words
- **Command renaming**: `agt commit` → `agt ws save`, `agt start` → `agt ws new`, `agt vscode init` → `agt cfg vscode`
- **Error messages**: Updated to use new domain-based command names

### Deprecated

- **Legacy aliases**: The following commands are deprecated and will be removed in v0.4:
  - `agt start` → Use `agt ws new`
  - `agt commit` → Use `agt ws save`
  - `agt run` → Use `agt ws run`
  - `agt push` → Use `agt ws push`
  - `agt merge` → Use `agt ws merge`
  - `agt clean` → Use `agt ws clean`
  - `agt vscode init` → Use `agt cfg vscode`
- Deprecation warnings are shown when using legacy commands

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

