# CLI Reference

## Commands

### `agt start [base-branch]`

Start a new agent worktree.

**Arguments:**
- `base-branch` (optional): Base branch to create worktree from (default: `main`)

**Example:**
```bash
agt start
agt start develop
```

**Output:**
- Creates `.work/agent-<id>/` directory
- Creates `feat/agent-<id>` branch
- Sets `AGENT_ID` environment variable
- Prints worktree path and branch name

---

### `agt run <command> [args...]`

Run a command in the agent worktree.

**Requirements:**
- Must run `agt start` first
- `AGENT_ID` environment variable must be set

**Arguments:**
- `command`: Command to execute (can include arguments)

**Examples:**
```bash
agt run python script.py
agt run "git add . && git status"
agt run npm install
agt run echo "Hello from worktree"
```

**Windows Note:** On Windows, `agt run` uses `cmd.exe` (not PowerShell) when `shell=True` is used. For best compatibility:
- Use Python commands: `python -m agt run "python -c \"print('test')\""`
- Use simple cmd.exe commands: `python -m agt run "dir"` or `python -m agt run "echo test > file.txt"`
- Avoid PowerShell-specific cmdlets (e.g., `Get-ChildItem`, `Set-Content`)

**Note:** The command runs in the worktree directory, so relative paths are relative to the worktree.

---

### `agt commit [--agent <id>] "<message>"`

Commit changes in the agent worktree.

**Requirements:**
- Must run `agt start` first
- Agent ID must be specified via `--agent` flag, working directory, or environment variable

**Arguments:**
- `--agent <id>` (optional): Explicitly specify agent ID (required when multiple worktrees exist)
- `message`: Commit message

**Agent ID Detection** (in priority order):
1. `--agent` flag (explicit)
2. Working directory (if inside `.work/agent-xxxx`)
3. Environment variable `AGENT_ID` (legacy)
4. Auto-detect (if only one worktree exists)

**Examples:**
```bash
# Using --agent flag (recommended for multiple agents)
agt commit --agent agent-xxxx "feat: add new feature"

# Working from within worktree directory (auto-detection)
cd .work/agent-xxxx
agt commit "feat: add new feature"
cd ../..

# Legacy: using environment variable (single agent only)
export AGENT_ID=agent-xxxx
agt commit "feat: add new feature"

# Single worktree (auto-detection)
agt commit "feat: add new feature"
```

**What it does:**
1. Stages all changes (`git add -A`)
2. Creates a commit with the provided message
3. Prints confirmation

---

### `agt push [--agent <id>] [remote]`

Push the agent branch to remote.

**Requirements:**
- Must run `agt start` first
- Must have commits to push (run `agt commit` first)
- Agent ID must be specified via `--agent` flag, working directory, or environment variable

**Arguments:**
- `--agent <id>` (optional): Explicitly specify agent ID (required when multiple worktrees exist)
- `remote` (optional): Remote name (default: `origin`)

**Agent ID Detection** (in priority order):
1. `--agent` flag (explicit)
2. Working directory (if inside `.work/agent-xxxx`)
3. Environment variable `AGENT_ID` (legacy)
4. Auto-detect (if only one worktree exists)

**Examples:**
```bash
# Using --agent flag (recommended for multiple agents)
agt push --agent agent-xxxx
agt push --agent agent-xxxx origin

# Working from within worktree directory (auto-detection)
cd .work/agent-xxxx
agt push
cd ../..

# Legacy: using environment variable (single agent only)
export AGENT_ID=agent-xxxx
agt push

# Single worktree (auto-detection)
agt push
```

**What it does:**
1. Pushes the branch to the remote repository
2. Sets upstream tracking (`git push -u`)
3. Prints confirmation message

**Note:** After pushing, open a PR manually in the GitHub UI.

---

### `agt clean`

Remove the agent worktree.

**Requirements:**
- Must run `agt start` first
- `AGENT_ID` environment variable must be set

**Examples:**
```bash
agt clean
```

**What it does:**
1. Removes the worktree directory
2. Cleans up Git worktree references
3. Prints confirmation

**Note:** The branch remains on the remote. Use this after your PR is merged or if you want to start fresh.

---

### `agt merge [--agent <id>]`

Merge agent branch into main using fast-forward merge (local only).

**Requirements:**
- Must run `agt start` first
- Must have pushed branch (run `agt push` first)
- Must have write access to `main` branch
- No branch protection rules (or admin override)
- Agent ID must be specified via `--agent` flag, working directory, or environment variable

**Arguments:**
- `--agent <id>` (optional): Explicitly specify agent ID (required when multiple worktrees exist)

**Agent ID Detection** (in priority order):
1. `--agent` flag (explicit)
2. Working directory (if inside `.work/agent-xxxx`)
3. Environment variable `AGENT_ID` (legacy)
4. Auto-detect (if only one worktree exists)

**Examples:**
```bash
# Using --agent flag (recommended for multiple agents)
agt merge --agent agent-xxxx

# Working from within worktree directory (auto-detection)
cd .work/agent-xxxx
agt merge
cd ../..

# Legacy: using environment variable (single agent only)
export AGENT_ID=agent-xxxx
agt merge

# Single worktree (auto-detection)
agt merge
```

**What it does:**
1. Fetches latest `main` from remote
2. Rebases agent branch onto `origin/main`
3. Switches to `main` branch in root repo
4. Performs fast-forward merge (`git merge --ff-only`)
5. Pushes `main` to remote

**Warning:** This command only works if you have direct write access to `main` and there are no branch protection rules. In most cases, use manual PR review instead.

---

## Error Handling

All commands exit with non-zero status on error:

- `1`: Missing or invalid arguments
- `2`: Worktree not found (run `agt start` first)

## Environment Variables

- `AGENT_ID`: Automatically set by `agt start`, required by `run`, `commit`, `push`, `merge`, and `clean`

## Exit Codes

- `0`: Success
- `1`: Usage error
- `2`: Worktree not found

---

## Agent CLI – Required Commands

Quick reference table for agents:

| Step | Command |
|------|---------|
| Create isolated worktree | `agt start` |
| Run task | `agt run "python task.py"` |
| Commit changes | `agt commit "feat: xyz"` |
| Push to remote | `agt push` |
| (optional) Merge locally | `agt merge` *(if permitted)* |
| Cleanup | `agt clean` |

**Note:** The `merge` command only works if you have write access to the `main` branch and there are no branch protection rules. Otherwise, use manual PR review in GitHub UI.

