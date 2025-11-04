# === FILE: actions\pr-bot\pr_bot.py ===
# Path: actions\pr-bot\pr_bot.py
# Type: py
# Size: 10.2KB
# Modified: 2025-11-04T13:39:24.392117

#!/usr/bin/env python3
"""
pr_bot.py – One‑shot GitHub PR automator (v2.3)

==============================================

⬆️ *NEW in 2.3*

• **--force flag** – Admin override-dal merge-el, akkor is ha piros check-ek vannak

• **Configurable CI polling** – CI_POLL_INTERVAL beállítható PR_BOT_POLL env változóval

• **Token check** – Ellenőrzi a GitHub authentication-t indításkor

⬆️ *NEW in 2.2*

• **Simplified workflow** – Alapértelmezetten kikapcsolva a CI polling, azonnal merge-el

• **--ci** zászló: Ha szükséges, be lehet kapcsolni a CI pollingot

• **Reduced wait time** – Alapértelmezett várakozási idő 60 másodpercről 5 másodpercre csökkentve

Működés: branch létrehozás → commit → PR megnyitása → rövid várakozás → squash‑merge → branch törlés.

Ha a --ci flag meg van adva, akkor CI polling is történik a merge előtt.

"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import time
from typing import Any, List

CI_POLL_INTERVAL = int(os.getenv("PR_BOT_POLL", "30"))  # seconds per poll (configurable via env)
CI_POLL_TIMEOUT  = 30 * 60 # give up after 30 minutes

# ---------------- helpers ----------------

def run(cmd: str, capture: bool = False) -> str | None:
    """Run shell command, optionally return stdout."""
    if capture:
        proc = subprocess.run(cmd, shell=True, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if proc.returncode != 0:
            raise subprocess.CalledProcessError(proc.returncode, cmd, proc.stdout)
        return proc.stdout.strip()
    subprocess.check_call(cmd, shell=True)
    return None

def check_auth() -> None:
    """Check GitHub authentication status with friendly error message."""
    # In GitHub Actions, GITHUB_TOKEN is automatically available
    if "GITHUB_TOKEN" in os.environ:
        # Set up gh CLI with token