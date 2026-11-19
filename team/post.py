"""Post to the board.

    python team/post.py --claim T02 "intent"        assign yourself + START comment
    python team/post.py --task T02 "COMMIT abc1234 ..."   comment on a task issue
    python team/post.py --room data "finding"       comment on the 'Room: data' issue
    python team/post.py --done T02 <pr-url>         DONE comment + close the issue
    add --file path to send a file's contents instead of text
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from _common import REPO, board_issues, gh_api, load_identity, require_identity, task_id_of


def find_task(tid: str) -> dict:
    for i in board_issues("all"):
        if task_id_of(i) == tid:
            return i
    sys.exit(f"No board issue for {tid}. Has the board been seeded (team/seed.py)?")


def find_room(topic: str) -> dict:
    for i in gh_api(f"repos/{REPO}/issues?labels=room&state=open&per_page=50") or []:
        if i["title"].lower() == f"room: {topic}".lower():
            return i
    sys.exit(f"No 'Room: {topic}' issue.")


def comment(number: int, body: str) -> str:
    payload = json.dumps({"body": body})
    p = subprocess.run(["gh", "api", "-X", "POST", f"repos/{REPO}/issues/{number}/comments", "--input", "-"],
                       input=payload, text=True, capture_output=True, check=True)
    return json.loads(p.stdout)["html_url"]


def main() -> None:
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--task")
    g.add_argument("--claim")
    g.add_argument("--done")
    g.add_argument("--room")
    p.add_argument("--file")
    p.add_argument("text", nargs="?", default="")
    a = p.parse_args()
    here = load_identity(Path.cwd()) or require_identity()
    text = Path(a.file).read_text() if a.file else a.text
    sign = f"\n\n— `{here['id']}`"
    if a.claim:
        issue = find_task(a.claim)
        gh_api(f"repos/{REPO}/issues/{issue['number']}/assignees", "-f", f"assignees[]={here['github']}",
               method="POST")
        branch = here.get("branch", "<branch>")
        url = comment(issue["number"], f"START {a.claim} on {branch}: {text}{sign}")
    elif a.done:
        issue = find_task(a.done)
        url = comment(issue["number"], f"DONE {a.done}: {text}{sign}")
        gh_api(f"repos/{REPO}/issues/{issue['number']}", "-f", "state=closed", method="PATCH")
    elif a.task:
        url = comment(find_task(a.task)["number"], text + sign)
    else:
        url = comment(find_room(a.room)["number"], text + sign)
    print(url)


if __name__ == "__main__":
    main()
