#!/usr/bin/env bash
# Demo: Local agent workflow using agt

set -e

echo "🚀 Starting agent workflow demo..."

# 1. Start agent worktree
echo "Step 1: Creating worktree..."
agt start

# 2. Run some commands in the worktree
echo "Step 2: Running commands in worktree..."
agt run "echo 'Hello from agent worktree' > test.txt"
agt run "cat test.txt"

# 3. Commit changes
echo "Step 3: Committing changes..."
agt commit "feat: add demo test file"

# 4. Push to remote
echo "Step 4: Pushing to remote..."
agt push

echo "✅ Demo complete! Open a PR in GitHub UI."
echo "💡 After PR is merged, run 'agt clean' to remove the worktree."

