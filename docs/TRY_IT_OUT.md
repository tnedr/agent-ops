# Try It Out in Another Project

Quick guide to test `agent-tools` in a different repository.

## Prerequisites

- ✅ Git repository with `main` branch
- ✅ Python 3.11+ installed
- ✅ Git worktree support
- ✅ (Optional) PowerShell 7+ for Windows users

### Verify Prerequisites

```bash
# Check Python version
python --version  # Should be 3.11+

# Check Git version
git --version  # Should support worktree

# Check Git worktree support
git worktree list
```

## Quick Test (5 minutes)

### Option 1: Manual Setup

```bash
# 1. Add as submodule
git submodule add -b main https://github.com/tnedr/agent-ops .tools
git submodule update --init --recursive

# 2. Install
cd .tools/agt
pip install -e .  # or: uv pip install -e .
cd ../..

# 3. Test basic workflow
agt start
agt run "echo '# Test from agent-tools' > test_agent.txt"
agt commit "test: verify agent-tools workflow"
agt push
agt clean
```

### Option 2: Automated Setup (Windows PowerShell)

If you have a setup script available:

```powershell
# Using setup script (if available)
.\scripts\setup-agent-tools.ps1 `
  -RepoUrl "https://github.com/tnedr/agent-ops" `
  -Install `
  -Test
```

## Full Workflow Test

### Step-by-Step

```bash
# 1. Start worktree
agt start
# Output: ✅ Worktree ready: .work/agent-xxxx (branch feat/agent-xxxx)
#         AGENT_ID=agent-xxxx

# 2. Create/modify files
agt run "echo 'Hello from agent' > output.txt"
agt run "ls -la"

# 3. Commit changes
agt commit "feat: add test output"

# 4. Push to remote
agt push
# Output: 🚀 Pushed to remote; open a PR in the UI if needed

# 5. Verify branch was created
git branch -a | grep feat/agent

# 6. Optional: Open PR manually in GitHub UI
# (or use: gh pr create --title "Test PR" --body "Testing agent-tools")

# 7. Optional: Merge locally (if permitted and no branch protection)
agt merge

# 8. Clean up
agt clean
```

### Alternative: Using Python Module

If `agt` command is not in PATH:

```bash
# Use Python module directly
python -m agt start
python -m agt run "echo 'test' > test.txt"
python -m agt commit "test: verify agent-tools"
python -m agt push
python -m agt clean
```

## Windows PowerShell Specific

### Setup in PowerShell

```powershell
# Set repository URL
$REPO_URL = "https://github.com/tnedr/agent-ops"

# Add submodule
git submodule add -b main $REPO_URL .tools
git submodule update --init --recursive

# Install (check for uv first)
if (Get-Command uv -ErrorAction SilentlyContinue) {
    cd .tools/agt
    uv pip install -e .
} else {
    cd .tools/agt
    pip install -e .
}
cd ../..

# Test (use python -m agt on Windows for best compatibility)
python -m agt start
python -m agt run "Set-Content -Path test.txt -Value 'test'"
python -m agt commit "test: PowerShell test"
python -m agt push
```

### Windows Command Compatibility

**Important**: When using `agt run`, use PowerShell-compatible commands:

❌ **Don't use** (Unix commands):
```powershell
python -m agt run "ls -la"
python -m agt run "echo 'test' > file.txt"
```

✅ **Use instead** (PowerShell commands):
```powershell
python -m agt run "Get-ChildItem"
python -m agt run "Set-Content -Path file.txt -Value 'test'"
python -m agt run "New-Item -ItemType File -Path newfile.txt"
```

### Unicode Output

**Fixed in v0.1.0**: The CLI automatically handles Windows terminal encoding issues. If Unicode characters can't be displayed, ASCII fallbacks are used automatically.

### Environment Variables

PowerShell automatically preserves `AGENT_ID` between commands in the same session:

```powershell
agt start
# AGENT_ID is set automatically
$env:AGENT_ID  # Shows the agent ID

# Use in subsequent commands
agt run "command"
agt commit "message"
```

## Verify Installation

```bash
# Check if agt command is available
agt --help

# Check version
python -m agt --help

# Verify worktree creation
agt start
ls -la .work/  # or: dir .work\ on Windows
agt clean
```

## Troubleshooting

### Issue: Command not found

**Symptoms**: `agt: command not found` or `'agt' is not recognized`

**Solutions**:

```bash
# Option 1: Use Python module (recommended on Windows)
python -m agt start

# Option 2: Check installation
cd .tools/agt
pip install -e . --force-reinstall
cd ../..

# Option 3: Check PATH
# On Windows: Add Python Scripts to PATH
# On Linux/Mac: Ensure ~/.local/bin is in PATH
```

### Issue: Package structure (hatchling build)

**Symptoms**: Installation fails with "No package files found" or similar

**Fix**: The package structure has been fixed. If you encounter this issue:

```bash
cd .tools/agt
# Verify pyproject.toml contains [tool.hatch.build.targets.wheel] section
pip install -e . --force-reinstall
```

### Issue: Repository URL not found

**Symptoms**: `fatal: repository 'https://github.com/tnedr/agent-ops' not found`

**Solutions**:

1. **Verify repository URL**:
   ```bash
   git submodule add -b main https://github.com/tnedr/agent-ops .tools
   ```

2. **Check repository exists and is accessible**:
   ```bash
   git ls-remote https://github.com/tnedr/agent-ops
   ```

3. **Use SSH instead of HTTPS** (if you have SSH keys set up):
   ```bash
   git submodule add -b main git@github.com:tnedr/agent-ops.git .tools
   ```

### Issue: Commit command fails on Windows

**Symptoms**: `error: pathspec 'message' did not match any file(s) known to git`

**Root Cause**: Fixed in v0.1.0 - commit command now uses argument list instead of shell command.

**Solutions**:

1. **Update to latest version**:
   ```bash
   cd .tools
   git pull origin main
   cd agt
   pip install -e . --force-reinstall
   ```

2. **If still failing**, use Python module directly:
   ```powershell
   python -m agt commit "your message"
   ```

### Issue: Unicode encoding errors (Windows)

**Symptoms**: `UnicodeEncodeError: 'charmap' codec can't encode character`

**Status**: ✅ **Fixed in v0.1.0** - Automatic fallback to ASCII-safe characters

**What changed**: The CLI now automatically detects Unicode encoding issues and falls back to ASCII-safe output:
- `✅` → `[OK]`
- `🚀` → `[PUSHED]`
- `❌` → `[ERROR]`

**No action needed** - the fix is automatic.

### Issue: Worktree errors

**Symptoms**: `fatal: 'path/to/worktree' is already a linked worktree`

**Solutions**:

```bash
# List all worktrees
git worktree list

# Remove stuck worktree manually
git worktree remove .work/agent-xxxx --force

# Or remove directory if worktree is broken
rm -rf .work/agent-xxxx  # Linux/Mac
Remove-Item -Recurse -Force .work\agent-xxxx  # Windows PowerShell
```

### Issue: Permission errors

**Symptoms**: `Permission denied` or `fatal: could not read Username`

**Solutions**:

```bash
# Check Git configuration
git config --list | grep user

# Set user if missing
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Check remote permissions
git remote -v
git ls-remote origin

# Ensure you have write access to the repository
```

### Issue: Python version mismatch

**Symptoms**: `requires-python = ">=3.11"` error

**Solutions**:

```bash
# Check Python version
python --version

# Use specific Python version
python3.11 -m pip install -e .  # or python3.12

# Or use py launcher on Windows
py -3.11 -m pip install -e .
```

### Issue: AGENT_ID not preserved (PowerShell)

**Symptoms**: `Run 'agt start' first!` after starting

**Solutions**:

```powershell
# PowerShell preserves env vars in same session
# If switching shells, re-export:
$env:AGENT_ID = "agent-xxxx"  # Use the ID from agt start

# Or use single command chain:
python -m agt start; python -m agt run "command"; python -m agt commit "message"
```

## Integration with Existing Workflows

### If you already use manual worktrees

**Before (manual)**:
```bash
git worktree add .work/manual-branch -b feat/manual
cd .work/manual-branch
# ... work ...
git add . && git commit -m "feat: changes"
git push origin HEAD
```

**After (agent-tools)**:
```bash
agt start
agt run "your-commands"
agt commit "feat: changes"
agt push
```

**Benefits**:
- ✅ Consistent branch naming (`feat/agent-xxxx`)
- ✅ Automated workflow
- ✅ Less manual Git commands
- ✅ Isolated environment per agent

## Clean Up After Testing

### Remove submodule

```bash
# Remove submodule completely
git submodule deinit .tools
git rm .tools
rm -rf .git/modules/.tools

# Or keep it for future use
git submodule update --remote
```

### Remove all agent worktrees

```bash
# List worktrees
git worktree list

# Remove each one
git worktree remove .work/agent-xxxx --force

# Or remove all at once (PowerShell)
Get-ChildItem .work\ | ForEach-Object { git worktree remove $_.FullName --force }
```

## Next Steps

After successful testing:

1. **Set up VS Code tasks** (see `docs/quick_start.md`)
2. **Integrate into your agent workflow**
3. **Use version tags for stability**:
   ```bash
   git submodule add -b v0.1.0 https://github.com/tnedr/agent-ops .tools
   ```
4. **Set up CI/CD** if needed (manual PR creation)

## Test Checklist

- [ ] Prerequisites verified (Python 3.11+, Git with worktree)
- [ ] Submodule added successfully
- [ ] Installation completed (`pip install -e .`)
- [ ] `agt --help` works
- [ ] `agt start` creates worktree
- [ ] `agt run` executes commands
- [ ] `agt commit` creates commits
- [ ] `agt push` pushes to remote
- [ ] Branch appears in remote repository
- [ ] `agt clean` removes worktree
- [ ] (Optional) `agt merge` works if permitted

## Getting Help

If you encounter issues:

1. Check the [CLI Reference](cli_reference.md) for command details
2. Review [Architecture](architecture.md) for understanding the system
3. Check test results in your repository
4. Ensure all prerequisites are met
5. Verify repository URL is correct and accessible

## Example: Complete Test Session

```bash
# Full test session (copy-paste ready)
REPO_URL="https://github.com/tnedr/agent-ops"
git submodule add -b main $REPO_URL .tools
cd .tools/agt && pip install -e . && cd ../..
agt start
agt run "echo 'Agent tools test' > test.txt"
agt run "cat test.txt"
agt commit "test: complete workflow test"
agt push
echo "✅ Test complete! Check GitHub for the new branch."
agt clean
```
