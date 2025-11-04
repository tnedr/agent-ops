# === FILE: actions\pr-bot\entrypoint.sh ===
# Path: actions\pr-bot\entrypoint.sh
# Type: sh
# Size: 270.0B
# Modified: 2025-11-04T13:39:24.391117

#!/bin/sh
set -e

# Build arguments array based on inputs
ARGS=""

if [ "$INPUT_CI" = "true" ]; then
    ARGS="$ARGS --ci"
fi

if [ "$INPUT_FORCE" = "true" ]; then
    ARGS="$ARGS --force"
fi

# Execute the Python script with arguments
exec python /app/pr_bot.py $ARGS
