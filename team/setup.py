"""Put the main clone on the integration branch, wire it for Claude Code, install deps. Safe to re-run.

Run inside a virtualenv from the repo root:
    python -m venv .venv && source .venv/bin/activate && python team/setup.py
"""

from __future__ import annotations

import sys

from _common import CONFIG, MAIN, require_identity, run, wire_checkout


def main() -> None:
    ident = require_identity(MAIN)
    branch = CONFIG["integration_branch"]
    run(["git", "fetch", "origin"], cwd=MAIN)
    current = run(["git", "branch", "--show-current"], cwd=MAIN).stdout.strip()
    if current != branch:
        run(["git", "checkout", branch], cwd=MAIN)
    run(["git", "pull", "--ff-only"], cwd=MAIN, check=False)
    wire_checkout(MAIN, ident)
    print(f"Main clone on {branch}, wired as {ident['id']}")
    run([sys.executable, "-m", "pip", "install", "-q", "-e", f"{MAIN}[dev]"], capture=False, timeout=900)
    print("Installed dependencies into", sys.executable)


if __name__ == "__main__":
    main()
