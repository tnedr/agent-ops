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
2. **Workflow Triggered**: The GitHub Action workflow starts
3. **Bot Runs**: The PR bot checks the PR status
4. **Wait Period**: Default 5 seconds (configurable via `--wait`)
5. **CI Check** (optional): If `ci: "true"`, waits for all checks to pass
6. **Merge**: Squash merges the PR
7. **Cleanup**: Deletes the source branch

## Permissions

The action requires the `GITHUB_TOKEN` secret, which is automatically available in GitHub Actions. Make sure your repository has the following permissions:

- **Contents**: Write (to merge PRs)
- **Pull requests**: Write (to merge and delete branches)

These are usually set automatically, but you can check in:
- Repository Settings → Actions → General → Workflow permissions

## Troubleshooting

### Bot Not Merging

1. Check workflow permissions
2. Verify `GITHUB_TOKEN` is set
3. Check workflow logs for errors
4. Ensure PR is not in draft mode

### CI Checks Not Passing

- If `ci: "true"`, the bot waits for all checks
- If checks fail, set `force: "true"` to override (requires admin permissions)

### Permission Errors

- Ensure the `GITHUB_TOKEN` has write permissions
- Check repository settings for workflow permissions

