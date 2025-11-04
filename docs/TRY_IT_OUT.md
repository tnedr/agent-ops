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

# Check UV (optional, for UV Cache Workflow)
uv --version  # If available, uses global cache
```

## Quick Test (5 minutes)

### Option 1: Manual Setup

```bash
# 1. Add as submodule
git submodule add -b main https://github.com/tnedr/agent-ops .tools
git submodule update --init --recursive

# 2. Install (requires activated virtual environment)
cd .tools/agt

# Activate your virtual environment first, or create one:
# python -m venv .venv --symlinks  # Minimal venv (UV Cache Workflow)
# .\.venv\Scripts\Activate.ps1  # Windows PowerShell
# source .venv/bin/activate      # Linux/Mac

# Use uv for installation (uses global cache, minimal .venv)
uv pip install -e .  # or: pip install -e .
cd ../..

# 3. Test basic workflow
# On Windows, use: python -m agt instead of agt
python -m agt start
python -m agt run "echo '# Test from agent-tools' > test_agent.txt"
python -m agt commit "test: verify agent-tools workflow"
python -m agt push
python -m agt clean
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
python -m agt start
# Output: ✅ Worktree ready: .work/agent-xxxx (branch feat/agent-xxxx)
#         AGENT_ID=agent-xxxx
# 
# IMPORTANT: Extract AGENT_ID from output and set it manually:
# On Windows PowerShell: $env:AGENT_ID = "agent-xxxx"
# On Linux/Mac: export AGENT_ID=agent-xxxx

# 2. Create/modify files
# On Windows, use cmd.exe-compatible commands (not PowerShell cmdlets)
python -m agt run "echo Hello from agent > output.txt"
python -m agt run "dir"  # Use dir instead of ls on Windows

# 3. Commit changes
python -m agt commit "feat: add test output"

# 4. Push to remote
python -m agt push
# Output: 🚀 Pushed to remote; open a PR in the UI if needed

# 5. Verify branch was created
git branch -a | grep feat/agent
# On Windows PowerShell: git branch -a | Select-String "feat/agent"

# 6. Optional: Open PR manually in GitHub UI
# (or use: gh pr create --title "Test PR" --body "Testing agent-tools")

# 7. Optional: Merge locally (if permitted and no branch protection)
python -m agt merge

# 8. Clean up
python -m agt clean
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

# Install (prefer uv for UV Cache Workflow)
if (Get-Command uv -ErrorAction SilentlyContinue) {
    cd .tools/agt
    uv pip install -e .  # Uses global cache (UV_CACHE_DIR), minimal .venv
} else {
    cd .tools/agt
    pip install -e .
}
cd ../..

# Test (use python -m agt on Windows for best compatibility)
python -m agt start
# Extract AGENT_ID from output and set it:
# $env:AGENT_ID = "agent-xxxx"  # Replace xxxx with actual ID

# Use cmd.exe-compatible commands (not PowerShell cmdlets)
python -m agt run "echo test > test.txt"
python -m agt commit "test: PowerShell test"
python -m agt push
```

### Windows Command Compatibility

**Important**: When using `agt run` on Windows, note that `subprocess.run(..., shell=True)` uses **cmd.exe**, not PowerShell.

**Limitations**:
- PowerShell-specific cmdlets (e.g., `Get-ChildItem`, `Set-Content`) may not work as expected
- Use cmd.exe-compatible commands or Python scripts instead

**Recommended approaches**:

1. **Use Python commands** (works cross-platform):
```powershell
python -m agt run "python -c \"print('test')\""
python -m agt run "python -c \"with open('test.txt', 'w') as f: f.write('test')\""
```

2. **Use simple cmd.exe commands**:
```powershell
python -m agt run "dir"
python -m agt run "echo test > file.txt"
python -m agt run "type file.txt"
```

3. **Use Python scripts** (best for complex operations):
```powershell
# Create a script
python -m agt run "python -c \"import os; os.makedirs('subdir', exist_ok=True)\""
```

❌ **Don't use** (PowerShell cmdlets - may not work):
```powershell
python -m agt run "Get-ChildItem"  # PowerShell cmdlet
python -m agt run "Set-Content -Path file.txt -Value 'test'"  # PowerShell cmdlet
```

**Note**: If you need PowerShell-specific functionality, consider running PowerShell commands directly or using Python scripts for cross-platform compatibility.

### Unicode Output

**Fixed in v0.1.0**: The CLI automatically handles Windows terminal encoding issues. If Unicode characters can't be displayed, ASCII fallbacks are used automatically:
- `✅` → `[OK]`
- `🚀` → `[PUSHED]`
- `❌` → `[ERROR]`

### Environment Variables

**Important**: `AGENT_ID` is printed in the output but NOT automatically set as an environment variable. You must extract it from the output and set it manually:

```powershell
# Step 1: Start worktree
python -m agt start
# Output shows: AGENT_ID=agent-xxxx

# Step 2: Extract and set AGENT_ID manually
$env:AGENT_ID = "agent-xxxx"  # Replace xxxx with actual ID from output

# Step 3: Verify it's set
$env:AGENT_ID  # Should show: agent-xxxx

# Step 4: Use in subsequent commands
python -m agt run "command"
python -m agt commit "message"
```

**Note**: On Windows, you may need to use `python -m agt` instead of just `agt` if the command is not in PATH. Also, ensure you're in a virtual environment or activate it first:

```powershell
# Create minimal venv (UV Cache Workflow)
python -m venv .venv --symlinks
.\.venv\Scripts\Activate.ps1

# Install with uv (uses global cache, minimal .venv)
uv pip install -e .  # or: pip install -e .

python -m agt start
```

## Verify Installation

```bash
# Check if agt command is available (may not work on Windows)
agt --help

# On Windows, use Python module instead:
python -m agt start

# Verify worktree creation
python -m agt start
# Extract and set AGENT_ID from output first: $env:AGENT_ID = "agent-xxxx"
# On Windows PowerShell (direct PowerShell command, not via agt run):
Get-ChildItem .work\  # or: dir .work\ on Windows
python -m agt clean
```

**Windows Note**: The `agt` command may not be in PATH. Always use `python -m agt` on Windows, or activate your virtual environment first.

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

**Status**: ✅ **Fixed in v0.1.0** - Package structure has been fixed in `pyproject.toml`

**Solution**: If you encounter this issue, update to the latest version:

```bash
cd .tools
git pull origin main
cd agt
uv pip install -e . --force-reinstall  # or: pip install -e . --force-reinstall
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

**Symptoms**: 
- `error: pathspec 'message' did not match any file(s) known to git` (quote parsing issue)
- `nothing to commit, working tree clean` (files not staged or not in worktree)

**Status**: 
- Quote parsing: ✅ **Fixed in v0.1.0** - Commit command now uses argument list instead of shell command
- File staging: The `commit` command runs `git add -A` automatically, but ensure files are created in the worktree directory

**Solutions**:

1. **Ensure files are in worktree directory**:
   ```powershell
   # Files created via agt run should be in .work/agent-xxxx/
   python -m agt run "echo test > file.txt"
   # Verify file exists in worktree
   python -m agt run "dir"
   ```

2. **Update to latest version** (if quote parsing issue):
   ```bash
   cd .tools
   git pull origin main
   cd agt
   pip install -e . --force-reinstall
   ```

3. **Manual commit** (if automatic staging fails):
   ```powershell
   cd .work/agent-xxxx  # Replace xxxx with your AGENT_ID
   git add -A
   git commit -m "your message"
   cd ../..
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
$env:AGENT_ID = "agent-xxxx"  # Use the ID from python -m agt start

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
python -m agt start
python -m agt run "your-commands"
python -m agt commit "feat: changes"
python -m agt push
```

**Benefits**:
- ✅ Consistent branch naming (`feat/agent-xxxx`)
- ✅ Automated workflow
- ✅ Less manual Git commands
- ✅ Isolated environment per agent

## Updating the Submodule

**Important**: Git submodules do NOT update automatically. When the `agent-ops` repository is updated, you need to manually update the submodule in each project that uses it.

### How to Update to Latest Version

#### Option 1: Update to Latest on Tracked Branch (Recommended)

```bash
# Update submodule to latest commit on the tracked branch (main)
git submodule update --remote .tools

# This fetches the latest changes and updates the submodule
# You need to commit this change in your main repository
git add .tools
git commit -m "chore: update agent-tools submodule"
```

#### Option 2: Update Manually

```bash
# Navigate to submodule directory
cd .tools

# Pull latest changes
git pull origin main

# Go back to main repository
cd ..

# Stage the submodule update
git add .tools
git commit -m "chore: update agent-tools submodule"
```

#### Option 3: Update to Specific Version/Tag

```bash
# Update to a specific tag (e.g., v0.1.0)
cd .tools
git fetch origin
git checkout v0.1.0  # or any tag/branch/commit
cd ..

# Commit the update
git add .tools
git commit -m "chore: update agent-tools to v0.1.0"
```

### After Updating

After updating the submodule, you may need to reinstall the package:

```bash
# Reinstall the package (recommended after update)
cd .tools/agt
uv pip install -e . --force-reinstall  # or: pip install -e . --force-reinstall
cd ../..
```

### Windows PowerShell

```powershell
# Update submodule to latest
git submodule update --remote .tools

# Commit the update
git add .tools
git commit -m "chore: update agent-tools submodule"

# Reinstall (if needed)
cd .tools/agt
uv pip install -e . --force-reinstall  # or: pip install -e . --force-reinstall
cd ../..
```

### Checking Current Version

```bash
# Check which commit the submodule is pointing to
cd .tools
git log -1 --oneline
git describe --tags  # If tags are available
cd ..
```

### Common Update Scenarios

**Scenario 1: Want latest features automatically**
- Use `git submodule update --remote` regularly
- Consider adding this to your CI/CD pipeline

**Scenario 2: Want stable version**
- Pin to a specific tag: `cd .tools && git checkout v0.1.0`
- Update manually when needed

**Scenario 3: Development/testing**
- Track `main` branch: `git submodule update --remote --merge .tools`
- Update frequently to get latest changes

### Important Notes

1. **Submodules track specific commits, not branches**
   - Even if you track a branch, the submodule points to a specific commit
   - `git submodule update --remote` updates to the latest commit on the tracked branch

2. **Each repository needs manual update**
   - If you use agent-tools in multiple repositories, update each one separately
   - There's no automatic sync across repositories

3. **Update frequency**
   - Update when you need new features or bug fixes
   - Consider setting up a reminder or automation

4. **Version pinning**
   - For production, consider pinning to specific tags/versions
   - For development, tracking `main` branch is fine

## Clean Up After Testing

### Remove submodule

```bash
# Remove submodule completely
git submodule deinit .tools
git rm .tools
rm -rf .git/modules/.tools

# Or keep it for future use (just update it)
git submodule update --remote
```

### Remove all agent worktrees

```bash
# List worktrees
git worktree list

# Remove each one
git worktree remove .work/agent-xxxx --force

# Or remove all at once (PowerShell - direct command, not via agt run)
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
- [ ] Installation completed (`uv pip install -e .` or `pip install -e .`)
- [ ] `python -m agt start` works (or `agt start` if in PATH)
- [ ] `python -m agt run` executes commands (use Windows-compatible commands)
- [ ] `python -m agt commit` creates commits
- [ ] `python -m agt push` pushes to remote
- [ ] Branch appears in remote repository
- [ ] `python -m agt clean` removes worktree
- [ ] (Optional) `python -m agt merge` works if permitted

## Getting Help

If you encounter issues:

1. Check the [CLI Reference](cli_reference.md) for command details
2. Review [Architecture](architecture.md) for understanding the system
3. Check test results in your repository
4. Ensure all prerequisites are met
5. Verify repository URL is correct and accessible

## Example: Complete Test Session

### Linux/Mac

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

### Windows PowerShell

```powershell
# Full test session (copy-paste ready)
$REPO_URL = "https://github.com/tnedr/agent-ops"
git submodule add -b main $REPO_URL .tools
git submodule update --init --recursive
cd .tools/agt
uv pip install -e .  # or: pip install -e .
cd ../..

# Activate virtual environment if using one
.\.venv\Scripts\Activate.ps1

# Start worktree
python -m agt start
# Note AGENT_ID from output (e.g., AGENT_ID=agent-xxxx)

# Set AGENT_ID from output
$env:AGENT_ID = "agent-xxxx"  # Replace xxxx with actual ID from start output

# Create test file (use cmd.exe-compatible commands, not PowerShell cmdlets)
python -m agt run "echo Agent tools test > test.txt"

# View file
python -m agt run "type test.txt"

# Commit
python -m agt commit "test: complete workflow test"

# Push
python -m agt push

# Clean up
python -m agt clean
```
