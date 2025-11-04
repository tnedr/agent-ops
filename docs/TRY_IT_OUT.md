# Try It Out in Another Project

Quick guide to test `agent-tools` in a different repository.

## Prerequisites

- Git repository with `main` branch
- Python 3.11+ installed
- Git worktree support

## Quick Test (5 minutes)

### 1. Add as Submodule

```bash
# In your target project repository
git submodule add -b main https://github.com/<ORG>/agent-tools .tools
git submodule update --init --recursive
```

### 2. Install

```bash
cd .tools/agt
pip install -e .
# or
python -m pip install -e .
```

### 3. Test Basic Workflow

```bash
# Go back to project root
cd ../..

# Start an isolated worktree
agt start

# Create a test file
agt run "echo '# Test from agent-tools' > test_agent.txt"

# Commit the change
agt commit "test: verify agent-tools workflow"

# Push to remote (creates branch feat/agent-xxxx)
agt push

# Verify: Check that branch was created
git branch -a | grep feat/agent

# Optional: Clean up
agt clean
```

## Full Workflow Test

```bash
# 1. Start worktree
agt start

# 2. Create/modify files
agt run "python -c \"print('Hello from agent')\" > output.txt"
agt run "ls -la"

# 3. Commit changes
agt commit "feat: add test output"

# 4. Push to remote
agt push

# 5. Open PR manually in GitHub UI
# (or use: gh pr create --title "Test PR" --body "Testing agent-tools")

# 6. Optional: Merge locally (if permitted)
agt merge

# 7. Clean up
agt clean
```

## Verify Installation

```bash
# Check if agt command is available
agt --help

# Check version
python -m agt --help

# Verify worktree creation
agt start
ls -la .work/
agt clean
```

## Troubleshooting

### Command not found

```bash
# Make sure you're in the right directory
cd .tools/agt
pip install -e .

# Or use Python module directly
python -m agt start
```

### Worktree errors

```bash
# Check if .work directory exists
ls -la .work/

# Manually remove stuck worktrees
git worktree list
git worktree remove .work/agent-xxxx --force
```

### Permission errors

```bash
# Ensure you have write access to the repository
git status

# Check remote permissions
git remote -v
```

## Next Steps

- Set up VS Code tasks (see `docs/quick_start.md`)
- Integrate into your agent workflow
- Use version tags for stability: `git submodule add -b v0.1.0 ...`

## Clean Up After Testing

```bash
# Remove submodule
git submodule deinit .tools
git rm .tools
rm -rf .git/modules/.tools

# Or keep it for future use
git submodule update --remote
```

