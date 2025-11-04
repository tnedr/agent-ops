# Complete Workflow Syntax Reference

## Full Workflow File Structure

```yaml
name: Auto-merge PR                    # Workflow name (shown in Actions tab)

on:                                     # Trigger events
  pull_request:                         # PR events
    types:                              # Specific event types
      - opened                          # PR created
      - synchronize                     # New commits pushed
      - reopened                        # Closed PR reopened
      - ready_for_review                # Draft marked ready
      - labeled                         # Label added/removed

jobs:                                   # Job definitions
  merge:                                # Job ID (can be anything)
    if: contains(                      # Condition check
        github.event.pull_request.labels.*.name, 
        'automerge'
      )
    runs-on: ubuntu-latest              # Runner OS
    
    steps:                              # Execution steps
      - uses: actions/checkout@v4       # Checkout code
      
      - name: Auto-merge with PR-bot    # Step name (for logs)
        uses: tnedr/agent-ops/actions/pr-bot@main  # Action reference
        with:                           # Input parameters
          ci: "false"                   # Wait for CI? (string)
          force: "false"                # Force merge? (string)
        env:                            # Environment variables
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  # Auto-provided token
```

## Action Reference Syntax

### Basic Format

```
uses: <owner>/<repo>/<path>@<ref>
```

### Examples

```yaml
# From main branch (latest, may be unstable)
uses: tnedr/agent-ops/actions/pr-bot@main

# From specific tag (recommended for production)
uses: tnedr/agent-ops/actions/pr-bot@v1

# From specific commit (most stable)
uses: tnedr/agent-ops/actions/pr-bot@abc123def456

# Local path (same repository)
uses: ./actions/pr-bot
```

### Path to Action

- The action directory must contain `action.yml`
- Path is relative to repository root: `actions/pr-bot/`
- Full path: `tnedr/agent-ops/actions/pr-bot`

## Event Types Explained

### `opened`
- Triggered when PR is first created
- **Note**: If PR created without label, workflow won't run (condition fails)

### `synchronize`
- Triggered when new commits are pushed to PR branch
- **Note**: Only runs if PR already has `automerge` label

### `reopened`
- Triggered when a closed PR is reopened
- Useful if PR was closed and then reopened

### `ready_for_review`
- Triggered when draft PR is marked as ready
- **Note**: Only runs if PR has `automerge` label

### `labeled`
- **Most important!** Triggered when label is added
- This is how you manually trigger the workflow
- Add `automerge` label → workflow runs immediately

## Condition Syntax

### Label Check

```yaml
if: contains(github.event.pull_request.labels.*.name, 'automerge')
```

**How it works:**
- `github.event.pull_request.labels` - Array of label objects
- `.*.name` - Extract all `name` fields from labels
- `contains(..., 'automerge')` - Check if array contains 'automerge'

**Alternative syntax:**
```yaml
if: github.event.pull_request.labels.*.name == 'automerge'
```

But `contains()` is safer for arrays.

## Input Parameters

### CI Parameter

```yaml
with:
  ci: "false"  # Don't wait for CI checks
```

```yaml
with:
  ci: "true"   # Wait for all CI checks to pass
```

**Behavior:**
- `"false"`: Bot waits 5 seconds, then merges
- `"true"`: Bot polls CI status every 30 seconds, waits up to 30 minutes

### Force Parameter

```yaml
with:
  force: "false"  # Don't merge if checks fail
```

```yaml
with:
  force: "true"   # Merge even if checks fail (admin only)
```

**Behavior:**
- `"false"`: If CI checks fail, bot exits with error
- `"true"`: Bot merges even with failed checks (requires admin permissions)

## Environment Variables

### GITHUB_TOKEN

```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Automatic:**
- Provided by GitHub Actions automatically
- No need to create manually
- Has write permissions by default

**Custom token (optional):**
```yaml
env:
  GITHUB_TOKEN: ${{ secrets.MY_CUSTOM_TOKEN }}
```

## Complete Example

Here's a complete, production-ready workflow:

```yaml
name: Auto-merge PR

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review, labeled]

jobs:
  merge:
    # Only run if PR has 'automerge' label
    if: contains(github.event.pull_request.labels.*.name, 'automerge')
    runs-on: ubuntu-latest
    
    permissions:
      contents: write      # Needed to merge PR
      pull-requests: write # Needed to update PR status
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Auto-merge with PR-bot
        uses: tnedr/agent-ops/actions/pr-bot@main
        with:
          ci: "false"
          force: "false"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Common Mistakes

### ❌ Wrong: Missing `labeled` event
```yaml
on:
  pull_request:
    types: [opened]  # Missing 'labeled' - can't trigger by adding label!
```

### ✅ Correct: Include `labeled` event
```yaml
on:
  pull_request:
    types: [opened, labeled]  # Can trigger by adding label
```

### ❌ Wrong: Missing condition check
```yaml
jobs:
  merge:
    runs-on: ubuntu-latest  # Will run on EVERY PR!
```

### ✅ Correct: Add condition
```yaml
jobs:
  merge:
    if: contains(github.event.pull_request.labels.*.name, 'automerge')
    runs-on: ubuntu-latest
```

### ❌ Wrong: Wrong input type
```yaml
with:
  ci: false  # Boolean - wrong!
```

### ✅ Correct: Use string
```yaml
with:
  ci: "false"  # String - correct!
```

## Testing the Syntax

### Validate YAML Online

1. Copy your workflow file
2. Paste at https://www.yamllint.com/
3. Check for syntax errors

### Test Locally

```bash
# Install act (local GitHub Actions runner)
brew install act  # macOS
# or
choco install act-cli  # Windows

# Test workflow
act pull_request
```

## Next Steps

After creating the workflow:
1. Commit and push to repository
2. Create a test PR
3. Add `automerge` label
4. Watch it work!

