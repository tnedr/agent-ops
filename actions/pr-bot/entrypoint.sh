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

