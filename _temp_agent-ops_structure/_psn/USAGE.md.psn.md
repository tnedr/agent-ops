# === FILE: USAGE.md ===
# Path: USAGE.md
# Type: md
# Size: 3.3KB
# Modified: 2025-11-04T14:51:15.538346

# Using agent-ops Actions in Other Repositories

## Quick Start

Add this workflow to `.github/workflows/auto-merge.yml` in your repository:

```yaml
name: Auto-merge PR

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

jobs:
  merge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Auto-merge with PR-bot
        uses: tnedr/agent-ops/actions/pr-bot@main
        with:
          ci: "false"    # Set to "true" to wait for CI checks
          force: "false" # Set to "true" to merge even with failed checks
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Configuration Options

### Wait for CI Checks

If you want the bot to wait for all CI checks to pass before merging:

```yaml
with:
  ci: "true"  # Wait for green checks
```

### Force Merge (Admin Override)

If you want to merge even when checks fail (requires admin permissions):

```yaml
with:
  force: "true"  # Merge even with failed checks
```

## Versioning

### Using Latest (Main Branch)

```yaml
uses: tnedr/agent-ops/actions/pr-bot@main
```

⚠️ **Warning**: This uses the latest code, which may be unstable.

### Using Version Tags (Recommended)

```yaml
uses: tnedr/agent-ops/actions/pr-bot@v1
```

First, create a version tag in the agent-ops repository:

```bash
git tag v1
git push origin v1
```

Then use `@v1` in your workflow for stability.

## Testing

### Test in Your Repository

1. Create a test branch:
   ```bash
   git checkout -b test/pr-bot
   ```

2. Make a small change:
   ```bash
   echo "Test" >> test.txt
   git add test.txt
   git commit -m "test: PR bot"
   git push -u origin test/pr-bot
   ```

3. Create a PR on GitHub

4. The bot should automatically merge it after 5 seconds (if `ci: "false"`)

### Test in agent-ops Repository

The `agent-ops` repository has its own test workflow (`.github/workflows/test-pr-bot.yml`) that tests the bot locally.

## How It Works

1. **PR Created**: When a PR is opened/updated