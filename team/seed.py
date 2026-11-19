"""Seed the board (idempotent): labels, one issue per task in plans/tasks.json, one issue per topic room.

    python team/seed.py
"""

from __future__ import annotations

import json
import subprocess

from _common import CONFIG, HERE, REPO, gh_api, task_id_of, tasks

LABELS = {
    "task": "0e8a16", "room": "5319e7", "contract": "d93f0b", "blocked": "b60205",
    "P0": "b60205", "P1": "fbca04", "P2": "c5def5",
    **{f"role:{r['id']}": "1d76db" for r in CONFIG["roles"]},
}


def post(path: str, payload: dict, method: str = "POST") -> dict:
    p = subprocess.run(["gh", "api", "-X", method, path, "--input", "-"], input=json.dumps(payload),
                       text=True, capture_output=True, check=True)
    return json.loads(p.stdout) if p.stdout.strip() else {}


def main() -> None:
    have = {l["name"] for l in gh_api(f"repos/{REPO}/labels?per_page=100") or []}
    for name, color in LABELS.items():
        if name not in have:
            post(f"repos/{REPO}/labels", {"name": name, "color": color})

    existing = {task_id_of(i): i for i in gh_api(f"repos/{REPO}/issues?labels=task&state=all&per_page=100") or []}
    owners = {r["id"]: r for r in CONFIG["roles"]}
    created = 0
    for t in tasks():
        if t["id"] in existing:
            continue
        role = owners[t["role"]]
        body = (f"**Role:** {t['role']} ({role['title']}, {role['person']})  \n**Priority:** {t['priority']}  \n"
                f"**Depends on:** {', '.join(t['depends']) or 'nothing'}\n\n**Scope (edit only these):**\n"
                + "\n".join(f"- `{s}`" for s in t["scope"])
                + f"\n\n**Done when:** {t['done_when']}\n\n**Agent prompt:** `prompts/agents/{t['id']}-{t['slug']}.md`\n\n"
                "Claim with `python team/post.py --claim " + t["id"] + " \"<intent>\"`. "
                "Post START / COMMIT / PR / BLOCKED / DONE here.")
        issue = post(f"repos/{REPO}/issues", {"title": f"{t['id']} {t['slug']}: {t['title']}", "body": body,
                                              "labels": ["task", t["priority"], f"role:{t['role']}"]})
        existing[t["id"]] = issue
        created += 1
    print(f"tasks: {created} created, {len(existing)} on the board")

    rooms = {i["title"] for i in gh_api(f"repos/{REPO}/issues?labels=room&state=open&per_page=50") or []}
    slug = CONFIG["project"]
    for room in CONFIG["rooms"][1:]:
        topic = room["name"].removeprefix(slug + "-")
        title = f"Room: {topic}"
        if title in rooms:
            continue
        doc = HERE / "docs" / "research" / f"{topic}.md"
        body = f"Topic room for **{topic}**: {room['purpose']}.\n\nPost findings here AND in `docs/research/{topic}.md`.\n\n"
        if doc.exists():
            body += "---\n" + doc.read_text()
        post(f"repos/{REPO}/issues", {"title": title, "body": body, "labels": ["room"]})
        print("room:", title)


if __name__ == "__main__":
    main()
