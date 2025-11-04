# === FILE: .github\workflows\test-pr-bot.yml ===
# Path: .github\workflows\test-pr-bot.yml
# Type: yml
# Size: 518.0B
# Modified: 2025-11-04T14:50:34.449424

name: Test PR Bot (Self-Test)

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

jobs:
  test-merge:
    runs-on: ubuntu-latest
    # This job tests the PR bot by using it from the same repo
    steps:
      - uses: actions/checkout@v4

      - name: Test PR-bot (local)
        uses: ./actions/pr-bot
        with:
          ci: "false"    # Don't wait for CI in test mode
          force: "false"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
