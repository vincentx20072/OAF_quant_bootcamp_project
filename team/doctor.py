"""Check this machine is ready. Prints one fix per problem, then `All good` or `N problems`."""

from __future__ import annotations

import shutil
import sys

from _common import CONFIG, MAIN, REPO, TASKS_DIR, WIRED_FILES, gh_api, identity_path, run

problems: list[str] = []


def check(ok: bool, label: str, fix: str) -> None:
    print(("  ok   " if ok else "  FAIL ") + label)
    if not ok:
        problems.append(fix)


def main() -> None:
    print("doctor:")
    check(sys.version_info >= (3, 11), f"python {sys.version.split()[0]} (need 3.11+)", "Install Python 3.11+")
    check(sys.prefix != sys.base_prefix, "running inside a virtualenv",
          "python -m venv .venv && source .venv/bin/activate (Windows: .venv\\Scripts\\activate)")
    for tool in ("git", "gh"):
        check(shutil.which(tool) is not None, f"{tool} installed", f"Install {tool}")
    check(shutil.which("claude") is not None, "claude (Claude Code) installed", "Install Claude Code")
    try:
        check(True, f"gh logged in as {gh_api('user')['login']}", "")
    except Exception:
        check(False, "gh logged in", "Run: gh auth login")
    try:
        gh_api(f"repos/{REPO}/issues?per_page=1")
        check(True, f"board reachable ({REPO} issues)", "")
    except Exception:
        check(False, "board reachable", f"Accept the invite: https://github.com/{REPO}/invitations")
    check(identity_path(MAIN).exists(), "identity", "Run: python team/join.py --name <first-name> --machine <label>")
    branch = run(["git", "branch", "--show-current"], cwd=MAIN).stdout.strip()
    check(branch == CONFIG["integration_branch"], f"main clone on {CONFIG['integration_branch']} (is {branch or 'detached'})",
          "Run: python team/setup.py")
    try:
        import matplotlib, numpy, pandas, pytest, yfinance  # noqa: F401
        check(True, "dependencies importable", "")
    except Exception as e:
        check(False, f"dependencies importable ({e})", "Run: python team/setup.py inside your venv")
    checkouts = [MAIN] + (sorted(p for p in TASKS_DIR.iterdir() if (p / ".git").exists()) if TASKS_DIR.exists() else [])
    for co in checkouts:
        rel = "main clone" if co == MAIN else f"tasks/{co.name}"
        check((co / ".claude" / "settings.local.json").exists() and identity_path(co).exists(), f"{rel} wired",
              "Run: python team/setup.py" if co == MAIN else f"Run: python team/new_task.py {co.name}")
        status = run(["git", "status", "--porcelain"], cwd=co).stdout
        leaked = [l for l in status.splitlines() if any(w.rstrip("/") in l for w in WIRED_FILES + ["tasks/"])]
        check(not leaked, f"{rel}: wired files and tasks/ invisible to git", f"git status shows {leaked[:2]}")
    print("All good" if not problems else f"{len(problems)} problems")
    for f in problems:
        print("  fix:", f)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
