# === FILE: .github\workflows\pull_request.yml ===
# Path: .github\workflows\pull_request.yml
# Type: yml
# Size: 580.0B
# Modified: 2025-11-04T13:36:47.203918

name: PR Pipeline (only bot demo)

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

jobs:
  merge-gate:
    runs-on: ubuntu-latest
    # nincsenek needs -> közvetlenül fut
    steps:
      - uses: actions/checkout@v4

      - name: Auto-merge with PR-bot
        uses: ./actions/pr-bot          # lokális path, nem kell publikus tag
        with:
          ci: "false"                   # ha átírod "true"-ra, zöld check-et vár
          force: "false"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
