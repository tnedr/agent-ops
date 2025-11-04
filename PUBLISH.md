# Publishing to GitHub

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `agent-ops`
3. Description: "Modular PR-bot and Agent/Doc-Ops GitHub Actions"
4. Choose visibility:
   - **Public** (recommended for reusable actions)
   - **Private** (if you want to keep it private)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **Create repository**

## Step 2: Add Remote and Push

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add the remote (replace <username> with your GitHub username)
git remote add origin https://github.com/<username>/agent-ops.git

# Or if you prefer SSH:
# git remote add origin git@github.com:<username>/agent-ops.git

# Push to GitHub
git push -u origin main
```

## Step 3: Verify

1. Go to https://github.com/<username>/agent-ops
2. Check that all files are uploaded
3. The workflow file should be visible in `.github/workflows/`

## Step 4: Test the Action

Create a test PR to verify the bot works:

```bash
# Create a test branch
git checkout -b test/pr-bot

# Make a small change
echo "# Test" >> test.md

# Commit and push
git add test.md
git commit -m "test: PR bot workflow"
git push -u origin test/pr-bot
```

Then create a PR on GitHub - the bot should automatically merge it after 5 seconds!

## Optional: Publish to GitHub Marketplace

If you want to make the action available to others:

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Click **Publish to GitHub Marketplace** (if available)
4. Fill in the details
5. Submit for review

## Using the Action in Other Repos

Once published, others (or you) can use it like this:

```yaml
- uses: <username>/agent-ops/actions/pr-bot@main
  with:
    ci: "false"
    force: "false"
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

