"""Claude Code hook entry point: hooks.py session|prompt|posttool|stop|board.

Never fails and never takes more than ~10 s: every network call has a short timeout, and any
error just shortens the output. Exit code is always 0.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

START = time.monotonic()
BUDGET = 9.0

try:
    from _common import CONFIG, MAIN, REPO, load_identity
except Exception:  # config missing or broken: stay silent
    sys.exit(0)


def left() -> float:
    return max(0.5, BUDGET - (time.monotonic() - START))


def api(path: str):
    try:
        p = subprocess.run(["gh", "api", path], capture_output=True, text=True, timeout=min(4.0, left()))
        return json.loads(p.stdout) if p.returncode == 0 and p.stdout.strip() else None
    except Exception:
        return None


def root() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())


def ident() -> dict:
    return load_identity(root()) or {}


def state_path() -> Path:
    base = root() / ".team"
    if not base.exists():
        base = MAIN / ".team"
    return base / "hook-state.json"


def load_state() -> dict:
    try:
        return json.loads(state_path().read_text())
    except Exception:
        return {}


def save_state(s: dict) -> None:
    try:
        state_path().parent.mkdir(parents=True, exist_ok=True)
        state_path().write_text(json.dumps(s))
    except Exception:
        pass


def recent_comments(n: int = 30) -> list[dict]:
    return api(f"repos/{REPO}/issues/comments?sort=created&direction=desc&per_page={n}") or []


def issue_no(c: dict) -> str:
    return c.get("issue_url", "").rsplit("/", 1)[-1]


def needs_reply(comments: list[dict], me: dict) -> list[dict]:
    if not me:
        return []
    pat = re.compile(rf"(@{re.escape(me.get('github', '~'))}\b|to:\s*{re.escape(me.get('person', '~'))}\b)", re.I)
    out = []
    for c in comments:  # newest first
        if c["user"]["login"] == me.get("github"):
            continue
        if not pat.search(c.get("body", "")):
            continue
        later_mine = any(x["user"]["login"] == me.get("github") and issue_no(x) == issue_no(c)
                         and x["created_at"] > c["created_at"] for x in comments)
        if not later_mine:
            out.append(c)
    return out


def fmt(c: dict) -> str:
    body = " ".join(c.get("body", "").split())[:160]
    return f"  [#{issue_no(c)} {c['user']['login']} {c['created_at'][5:16]}] {body}"


def board_text() -> str:
    me = ident()
    lines = ["=== TEAM HUB (GitHub issues board) ===",
             f"You: {me.get('id', 'NO IDENTITY: run python team/join.py')}  |  Board: https://github.com/{REPO}/issues"]
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")
    upcoming = [d for d in CONFIG.get("deadlines", []) if d["at"] >= now][:3]
    if upcoming:
        lines.append("Next deadlines: " + "; ".join(f"{d['at'].replace('T', ' ')} {d['what']}{' (HARD)' if d['hard'] else ''}" for d in upcoming))
    issues = api(f"repos/{REPO}/issues?labels=task&state=all&per_page=100")
    if issues is None:
        lines.append("(board unreachable: check `gh auth status`; continuing without it)")
    else:
        lines.append("Tasks:")
        for i in sorted(issues, key=lambda x: x["title"]):
            who = ",".join(a["login"] for a in i.get("assignees", [])) or "unclaimed"
            mark = "done" if i["state"] == "closed" else who
            lines.append(f"  #{i['number']:<3} {i['title'][:60]:<60} {mark}")
    prs = api(f"repos/{REPO}/pulls?state=open&per_page=20")
    if prs:
        lines.append("Open PRs: " + "; ".join(f"#{p['number']} {p['title'][:40]} ({p['user']['login']})" for p in prs))
    comments = recent_comments()
    nr = needs_reply(comments, me)
    if nr:
        lines.append("NEEDS REPLY (answer these first):")
        lines += [fmt(c) for c in nr[:5]]
    if comments:
        lines.append("Recent messages:")
        lines += [fmt(c) for c in reversed(comments[:12])]
        s = load_state()
        s["last_seen"] = max(int(c["id"]) for c in comments)
        save_state(s)
    lines.append("Protocol: team-hub skill. Rules and deadlines: challenge-rules skill.")
    return "\n".join(lines)


def mode_session() -> None:
    try:
        subprocess.run(["git", "pull", "--ff-only", "-q"], cwd=MAIN, capture_output=True, timeout=min(4.0, left()))
    except Exception:
        pass
    print(board_text())


def mode_prompt() -> None:
    s = load_state()
    seen = int(s.get("last_seen", 0))
    comments = [c for c in recent_comments(20) if int(c["id"]) > seen]
    if not comments:
        return
    me = ident()
    new = [c for c in comments if c["user"]["login"] != me.get("github")]
    s["last_seen"] = max(int(c["id"]) for c in comments)
    save_state(s)
    if new:
        print("TEAM HUB: new messages since your last prompt:")
        print("\n".join(fmt(c) for c in reversed(new)))


def mode_posttool() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    cmd = (data.get("tool_input") or {}).get("command", "")
    tip = None
    if re.search(r"\bgh\s+pr\s+create\b|/pulls\b", cmd):
        tip = "Post `PR <url>: <title>. Needs review from <who>` on your task issue: python team/post.py --task <id> \"...\""
    elif re.search(r"\bgit\s+push\b", cmd):
        tip = "Pushed. If others depend on it, post COMMIT on your task issue; if ready, open the PR against develop."
    elif re.search(r"\bgit\s+commit\b", cmd):
        tip = "Committed. Read the inbox before pushing (python team/hooks.py board). Post `COMMIT <sha7> <branch>: <what>; affects <paths>` if others depend on it."
    if tip:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": tip}}))


def mode_stop() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    if data.get("stop_hook_active"):
        return
    nr = needs_reply(recent_comments(), ident())
    s = load_state()
    ids = sorted(str(c["id"]) for c in nr)
    if ids and ids != s.get("blocked_for"):
        s["blocked_for"] = ids
        save_state(s)
        reason = "Unanswered team messages addressed to you:\n" + "\n".join(fmt(c) for c in nr[:5])
        print(json.dumps({"decision": "block", "reason": reason + "\nReply on the issue (python team/post.py) or say why not, then stop."}))


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "board"
    try:
        {"session": mode_session, "prompt": mode_prompt, "posttool": mode_posttool,
         "stop": mode_stop, "board": lambda: print(board_text())}.get(mode, lambda: None)()
    except Exception:
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
