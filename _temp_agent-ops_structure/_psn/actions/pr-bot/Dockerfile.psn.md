# === FILE: actions\pr-bot\Dockerfile ===
# Path: actions\pr-bot\Dockerfile
# Type: [no-ext]
# Size: 1.1KB
# Modified: 2025-11-04T13:40:24.515519

FROM python:3.11-slim

WORKDIR /app

# Install GitHub CLI and UV
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add UV to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

COPY pr_bot.py entrypoint.sh pyproject.toml .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Install dependencies using UV (follows UV Cache Guidelines)
# No external dependencies needed - script uses only standard library
# But we use uv pip sync to ensure proper dependency management
RUN uv pip install --system -e .

ENTRYPOINT ["/app/entrypoint.sh"]
