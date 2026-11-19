"""Start a task in its own worktree: python team/new_task.py <slug>.  No slug: list open tasks.

Creates tasks/<slug> (inside the main clone, gitignored) on branch <person>/<agent>/<slug> from
origin/<integration branch>, with identity <person>.<machine>.<agent>-<slug>, wired for Claude Code.
"""

from __future__ import annotations

import sys

from _common import CONFIG, MAIN, TASKS_DIR, board_issues, require_identity, run, task_id_of, tasks, wire_checkout


def list_open() -> None:
    issues = {task_id_of(i): i for i in board_issues("all")}
    done = {tid for tid, i in issues.items() if i["state"] == "closed"}
    print("Open tasks whose dependencies are done:")
    for t in tasks():
        i = issues.get(t["id"])
        if t["id"] in done or (i and i.get("assignees")):
            continue
        if all(d in done for d in t["depends"]):
            num = f"#{i['number']}" if i else "(not seeded)"
            print(f"  {t['id']} {t['slug']:<14} {t['priority']} {t['role']:<5} {num:<6} {t['title']}")
    print("\nStart one with: python team/new_task.py <slug>")


def main() -> None:
    if len(sys.argv) < 2:
        list_open()
        return
    slug = sys.argv[1]
    if slug not in {t["slug"] for t in tasks()} and slug != "smoke":
        print(f"warning: '{slug}' is not in plans/tasks.json")
    ident = require_identity(MAIN)
    branch = CONFIG["branch_template"].format(person=ident["person"], agent=ident["agent"], slug=slug)
    dest = TASKS_DIR / slug
    if dest.exists():
        print(f"tasks/{slug} already exists")
    else:
        run(["git", "fetch", "origin"], cwd=MAIN)
        run(["git", "worktree", "add", "-b", branch, str(dest), f"origin/{CONFIG['integration_branch']}"], cwd=MAIN)
    wire_checkout(dest, {**ident, "id": f"{ident['id']}-{slug}", "task": slug, "branch": branch})
    print(f"Ready: cd tasks/{slug} && claude   (branch {branch})")
    print('Claim it first (from that folder): python team/post.py --claim <task-id> "<intent>"')


if __name__ == "__main__":
    main()
