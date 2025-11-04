FROM python:3.11-slim

WORKDIR /app

# Install GitHub CLI
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pr_bot.py entrypoint.sh .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# függőségek, ha a script használ valamit (pl. click, PyYAML)
RUN pip install --no-cache-dir click PyYAML

ENTRYPOINT ["/app/entrypoint.sh"]

