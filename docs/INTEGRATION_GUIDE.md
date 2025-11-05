# Integration Guide: Using agent-ops as Submodule

Complete step-by-step guide for integrating `agent-ops` into your project as a Git submodule.

## Overview

This guide shows you how to:
1. Add `agent-ops` as a submodule to your repository
2. Set up the environment automatically
3. Use the CLI tools and VS Code Command Runner integration
4. Update the submodule when needed
5. Test that everything works

## Prerequisites

Before starting, ensure you have:

- ✅ Git repository (your project)
- ✅ Python 3.11+ installed
- ✅ Git with worktree support
- ✅ (Optional) UV package manager for faster installs
- ✅ (Optional) VS Code or Cursor with Command Runner extension

### Verify Prerequisites

```bash
# Check Python version
python --version  # Should be 3.11+

# Check Git version
git --version  # Should support worktree

# Check Git worktree support
git worktree list

# Check UV (optional, recommended)
uv --version  # If available, uses global cache
```

## Step 1: Add Submodule

Add `agent-ops` as a submodule to your repository:

```bash
# Navigate to your project root
cd /path/to/your/project

# Add the submodule
git submodule add -b main https://github.com/tnedr/agent-ops .tools

# Initialize and update submodules
git submodule update --init --recursive
```

This creates:
- `.tools/` directory containing the agent-ops repository
- `.gitmodules` file in your project root (tracked by Git)

## Step 2: Setup Environment

### Option A: Automated Setup (Recommended)

Use the wrapper script for automatic setup:

```bash
# 1. Copy the wrapper script template
cp .tools/scripts/agt.sh.example scripts/agt.sh
chmod +x scripts/agt.sh

# 2. First run (auto-creates venv and tests it)
./scripts/agt.sh run env.check
```

**What happens:**
- Creates `.tools/.venv` automatically (if missing)
- Installs agent-tools with all dependencies
- Generates VS Code Command Runner settings
- Tests the installation with `env.check` command

**Expected output:**
```
⚙️  Creating minimal .venv (uv venv)…
✅  agent-tools ready in .tools/.venv (cache: E:\uv-cache)
Venv OK – Colorama loaded
```

### Option B: Manual Setup

If you prefer manual control:

```bash
# Navigate to submodule
cd .tools

# Run bootstrap script
./bootstrap.sh

# Go back to project root
cd ..
```

**What the bootstrap script does:**
- Creates minimal `.venv` using `uv venv` (UV Cache Workflow compliant)
- Installs agent-tools with CLI extras (colorama)
- Uses global cache (`UV_CACHE_DIR`) for fast installs

## Step 3: Verify Installation

Test that everything is set up correctly:

```bash
# Test the CLI
.tools/.venv/bin/agt --help
# or with wrapper:
./scripts/agt.sh --help

# Test venv and dependencies
./scripts/agt.sh run env.check
# Should output: Venv OK – Colorama loaded (in green)

# Test math command
./scripts/agt.sh run "python ${workspaceFolder}/.tools/scripts/multiply.py 3 7"
# Should output: 21.0

# Test time command
./scripts/agt.sh run "python ${workspaceFolder}/.tools/scripts/current_time.py"
# Should output: 2025-11-05T... (UTC timestamp)
```

## Step 4: VS Code Command Runner Integration

The wrapper script automatically generates VS Code Command Runner settings on first run.

### Available Commands

After setup, you can use these commands in VS Code/Cursor:

1. **Press `F1` → `Command Runner: Run...`**
2. **Select from available commands:**
   - `math.multiply` - Multiply two numbers (a×b)
   - `time.now` - Get current UTC timestamp
   - `env.check` - Verify venv and colorama dependency

3. **Or use in chat:**
   ```
   > run command: math.multiply 7 6
   > run command: time.now
   > run command: env.check
   ```

### Manual Regeneration

If you need to regenerate the settings:

```bash
python .tools/scripts/update_command_runner.py
```

This updates `.vscode/settings.json` with all commands from `.tools/config/tools.yml`.

## Step 5: Basic Usage

### Start a Worktree

```bash
# Using wrapper script (recommended)
./scripts/agt.sh start

# Or directly
.tools/.venv/bin/agt start
```

**Output:**
```
✅ Worktree ready: .work/agent-xxxx (branch feat/agent-xxxx)
AGENT_ID=agent-xxxx
```

### Run Commands in Worktree

```bash
# Using wrapper
./scripts/agt.sh run "python my_script.py"
./scripts/agt.sh run "echo 'test' > test.txt"

# Or directly
.tools/.venv/bin/agt run "python my_script.py"
```

### Commit Changes

```bash
./scripts/agt.sh commit "feat: add new feature"
```

### Push to Remote

```bash
./scripts/agt.sh push
```

Then open a PR manually in GitHub UI.

### Clean Up (Optional)

```bash
./scripts/agt.sh clean
```

## Step 6: Update Submodule

When you want to get the latest version of agent-ops:

```bash
# Update to latest main branch
git submodule update --remote .tools

# Or merge specific changes
git submodule update --remote --merge .tools

# Commit the update
git add .tools
git commit -m "chore: update agent-tools submodule"
git push
```

**Note:** After updating, the wrapper script will automatically regenerate VS Code settings if needed.

## Project Structure After Setup

Your project will have this structure:

```
your-project/
├── .tools/                    # agent-ops submodule
│   ├── .venv/                # Minimal virtual environment (auto-created)
│   ├── agt/                  # Python package
│   ├── scripts/              # Helper scripts
│   │   ├── multiply.py
│   │   ├── current_time.py
│   │   ├── venv_check.py
│   │   └── update_command_runner.py
│   ├── config/
│   │   └── tools.yml         # Command definitions
│   ├── bootstrap.sh           # Setup script
│   └── ...
├── scripts/
│   └── agt.sh                 # Wrapper script (you copied this)
├── .vscode/
│   └── settings.json          # Command Runner config (auto-generated)
├── .work/                     # Agent worktrees (created by agt start)
│   └── agent-xxxx/
└── .gitmodules                # Submodule configuration
```

## Troubleshooting

### Problem: "Command not found: agt"

**Solution:** Use the full path or wrapper script:
```bash
# Use wrapper
./scripts/agt.sh start

# Or full path
.tools/.venv/bin/agt start

# Or activate venv
source .tools/.venv/bin/activate  # Linux/Mac
.\.tools\.venv\Scripts\Activate.ps1  # Windows PowerShell
agt start
```

### Problem: "No such file or directory: .tools/scripts/..."

**Solution:** Ensure the submodule is initialized:
```bash
git submodule update --init --recursive
cd .tools
./bootstrap.sh
```

### Problem: "env.check fails with colorama import error"

**Solution:** Reinstall dependencies:
```bash
cd .tools
./bootstrap.sh
```

### Problem: VS Code Command Runner commands not showing

**Solution:** Regenerate settings:
```bash
python .tools/scripts/update_command_runner.py
# Then reload VS Code window (Ctrl+Shift+P → Developer: Reload Window)
```

### Problem: UV cache not working

**Solution:** Set UV_CACHE_DIR environment variable:
```bash
# Windows PowerShell
setx UV_CACHE_DIR "E:\uv-cache"

# Linux/Mac
export UV_CACHE_DIR="$HOME/.uv-cache"
# Add to ~/.bashrc or ~/.zshrc for persistence
```

## Windows-Specific Notes

### PowerShell

Use the wrapper script for best compatibility:
```powershell
# Use wrapper (recommended)
.\scripts\agt.sh start

# Or use Python module
python -m agt start
```

### Command Prompt

```cmd
# Use wrapper
scripts\agt.sh start

# Or activate venv first
.tools\.venv\Scripts\activate.bat
agt start
```

## CI/CD Integration

If you use CI/CD, ensure submodules are checked out:

```yaml
# GitHub Actions example
- uses: actions/checkout@v4
  with:
    submodules: recursive

# Then in your workflow
- name: Setup agent-tools
  run: |
    cd .tools
    ./bootstrap.sh
    cd ..
    
- name: Use agent-tools
  run: .tools/.venv/bin/agt --help
```

## Best Practices

1. **Use the wrapper script** (`scripts/agt.sh`) for consistency
2. **Commit `.gitmodules`** to track submodule version
3. **Update submodule explicitly** with `git submodule update --remote`
4. **Test after updates** with `./scripts/agt.sh run env.check`
5. **Use UV Cache Workflow** for faster installs (set `UV_CACHE_DIR`)

## Next Steps

- Read [Quick Start Guide](quick_start.md) for basic usage
- Read [CLI Reference](cli_reference.md) for all commands
- Read [Worktree Agent User Manual](worktree_agent_user_manual.md) for advanced workflows
- Check [Architecture](architecture.md) for technical details

## Summary

✅ **Added submodule:** `git submodule add -b main https://github.com/tnedr/agent-ops .tools`
✅ **Setup:** `cp .tools/scripts/agt.sh.example scripts/agt.sh && ./scripts/agt.sh run env.check`
✅ **Usage:** `./scripts/agt.sh start`, `./scripts/agt.sh run ...`, etc.
✅ **Update:** `git submodule update --remote .tools`

That's it! You're ready to use agent-ops in your project.

