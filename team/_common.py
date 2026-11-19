"""Shared helpers for the team scripts. Python 3.11+ standard library only.

One repo holds both the code and the team tooling. The task board is GitHub issues on this
repo (label `task`); topic rooms are issues titled `Room: <topic>`. Everything goes through
`gh api` (REST), so it works anywhere `gh auth login` works.

HERE = the checkout this script lives in (the main clone or a task worktree).
MAIN = the main clone (where `tasks/` and the shared identity live).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
CONFIG = json.loads((HERE / "team" / "team.config.json").read_text())
REPO = f"{CONFIG['gh_owner']}/{CONFIG['repo']}"


def _main_clone() -> Path:
    try:
        common = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                                cwd=HERE, capture_output=True, text=True, timeout=5).stdout.strip()
        return Path(common).parent if common else HERE
    except Exception:
        return HERE


MAIN = _main_clone()
TASKS_DIR = MAIN / "tasks"

# Files that wiring writes into a checkout; all are added to .git/info/exclude.
WIRED_FILES = [".team/", ".claude/settings.local.json"]


def run(cmd: list[str], cwd: Path | None = None, check: bool = True, timeout: float | None = 120,
        capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=check, timeout=timeout, text=True, capture_output=capture)


def gh_api(path: str, *args: str, method: str = "GET", timeout: float = 20, check: bool = True):
    """Call the GitHub REST API through gh. Returns parsed JSON (or None for empty bodies)."""
    p = run(["gh", "api", "-X", method, path, *args], timeout=timeout, check=check)
    out = (p.stdout or "").strip()
    return json.loads(out) if out else None


def identity_path(root: Path) -> Path:
    return root / ".team" / "identity.json"


def load_identity(root: Path | None = None) -> dict | None:
    for r in ([root] if root else []) + [HERE, MAIN]:
        p = identity_path(r)
        if p.exists():
            return json.loads(p.read_text())
    return None


def require_identity(root: Path | None = None) -> dict:
    ident = load_identity(root)
    if not ident:
        sys.exit("No identity yet. Run: python team/join.py --name <first-name> --machine <label>")
    return ident


def write_identity(root: Path, ident: dict) -> None:
    p = identity_path(root)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(ident, indent=2) + "\n")


def git_exclude_path(checkout: Path) -> Path:
    rel = run(["git", "rev-parse", "--git-path", "info/exclude"], cwd=checkout).stdout.strip()
    return (checkout / rel).resolve()


def hook_settings(checkout: Path, python: str) -> dict:
    hooks = checkout / "team" / "hooks.py"

    def cmd(mode: str) -> dict:
        return {"hooks": [{"type": "command", "command": f'"{python}" "{hooks}" {mode}', "timeout": 15}]}

    return {"hooks": {
        "SessionStart": [cmd("session")],
        "UserPromptSubmit": [cmd("prompt")],
        "PostToolUse": [{"matcher": "Bash", **cmd("posttool")}],
        "Stop": [cmd("stop")],
    }}


def wire_checkout(checkout: Path, ident: dict) -> None:
    """Write identity and hook settings into a checkout and exclude them from git."""
    write_identity(checkout, ident)
    (checkout / ".claude").mkdir(exist_ok=True)
    (checkout / ".claude" / "settings.local.json").write_text(
        json.dumps(hook_settings(checkout, sys.executable), indent=2) + "\n")
    excl = git_exclude_path(checkout)
    excl.parent.mkdir(parents=True, exist_ok=True)
    existing = excl.read_text().splitlines() if excl.exists() else []
    missing = [f for f in WIRED_FILES if f not in existing]
    if missing:
        with excl.open("a") as fh:
            fh.write("\n# team wiring (never commit)\n" + "\n".join(missing) + "\n")


def tasks() -> list[dict]:
    return json.loads((HERE / "plans" / "tasks.json").read_text())


def board_issues(state: str = "all") -> list[dict]:
    return gh_api(f"repos/{REPO}/issues?labels=task&state={state}&per_page=100") or []


def task_id_of(issue: dict) -> str | None:
    title = issue.get("title", "")
    return title.split(" ", 1)[0] if title[:1] == "T" else None


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
