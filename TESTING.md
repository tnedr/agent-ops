# Testing PR Bot in Another Repository

## Quick Test Steps

### 1. Copy the Workflow

Copy the `example-workflow.yml` file to your target repository:

```bash
# In your target repository
mkdir -p .github/workflows
cp /path/to/agent-ops/example-workflow.yml .github/workflows/auto-merge.yml
```

Or manually create `.github/workflows/auto-merge.yml` with this content:

```yaml
name: Auto-merge PR

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review, labeled]

jobs:
  merge:
    if: contains(github.event.pull_request.labels.*.name, 'automerge')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Auto-merge with PR-bot
        uses: tnedr/agent-ops/actions/pr-bot@main
        with:
          ci: "false"
          force: "false"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 2. Commit and Push

```bash
git add .github/workflows/auto-merge.yml
git commit -m "test: add PR bot workflow"
git push
```

### 3. Create a Test PR

```bash
# Create a test branch
git checkout -b test/pr-bot

# Make a small change
echo "# Test PR Bot" >> test-bot.md
git add test-bot.md
git commit -m "test: PR bot auto-merge"
git push -u origin test/pr-bot
```

### 4. Create PR on GitHub

1. Go to your repository on GitHub
2. You should see a banner suggesting to create a PR
3. Click "Compare & pull request"
4. **IMPORTANT: Add the `automerge` label** to the PR
5. Click "Create pull request"

### 5. Watch It Work

- The workflow will start running (check the "Actions" tab)
- After 5 seconds, the bot should automatically merge the PR
- The branch will be deleted automatically

## Verification

### Check Workflow Run

1. Go to the "Actions" tab in your repository
2. Click on the "Auto-merge PR" workflow
3. Check the logs to see:
   - ✅ PR bot started
   - ✅ PR merged successfully
   - ✅ Branch deleted

### Check PR Status

- The PR should be marked as "Merged"
- The source branch should be deleted
- The commit should be in the main branch

## Troubleshooting

### Workflow Not Running

- **Check**: Did you add the `automerge` label? (Required!)
- **Check**: Is the workflow file in `.github/workflows/` directory?
- **Check**: Is the workflow file named correctly (`.yml` or `.yaml`)?

### Bot Not Merging

- **Check**: Workflow logs for errors
- **Check**: GITHUB_TOKEN permissions (should be automatic)
- **Check**: PR is not in draft mode
- **Check**: PR has no merge conflicts

### Permission Errors

If you see permission errors:
1. Go to Repository Settings → Actions → General
2. Under "Workflow permissions", ensure "Read and write permissions" is selected
3. Save and retry

## Advanced Testing

### Test with CI Checks

To test waiting for CI checks:

```yaml
with:
  ci: "true"  # Wait for green checks
```

Then create a PR with the `automerge` label - the bot will wait for all checks to pass.

### Test Force Merge

To test admin override:

```yaml
with:
  force: "true"  # Merge even with failed checks
```

**Note**: This requires admin permissions and should only be used for testing.

## Clean Up After Testing

After testing, you can:
1. Remove the workflow file if you don't want auto-merge
2. Keep it for future use (just add `automerge` label when needed)
3. Modify the label condition to use a different label name

