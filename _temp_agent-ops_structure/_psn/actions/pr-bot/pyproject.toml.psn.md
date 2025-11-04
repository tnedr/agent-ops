# === FILE: actions\pr-bot\pyproject.toml ===
# Path: actions\pr-bot\pyproject.toml
# Type: toml
# Size: 294.0B
# Modified: 2025-11-04T13:40:24.511520

[project]
name = "pr-bot"
version = "2.3.0"
description = "One-shot GitHub PR automator with CI polling"
requires-python = ">=3.11"

# No external dependencies - uses only Python standard library
dependencies = []

[tool.uv]
# This is a standalone action, no workspace needed here
