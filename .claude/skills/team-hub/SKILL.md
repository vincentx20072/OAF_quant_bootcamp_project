---
name: team-hub
description: Team coordination protocol for the OAF_quant_bootcamp_project repo (overnight vs intraday). Use at the start of every session, before every commit or push, when blocked, when finishing a task, and whenever you need to know who owns a file or task.
---

# Team hub protocol (GitHub issues board)

There is no chat server. The **board** is GitHub issues on `vincentx20072/OAF_quant_bootcamp_project`:
- one issue per task, labelled `task`, `P0|P1|P2`, `role:devN`, titled `T05 factor-split: ...`
- one issue per topic room, labelled `room`, titled `Room: <topic>`
- the assignee of a task issue is its owner; a closed task issue is done

Git owns the code. The board owns awareness. Nothing blocks you; you are expected to check.

All commands below run from the repo root **or** your `tasks/<slug>` folder (each has its own `team/`).

## Session start
1. Read the `TEAM HUB` block the SessionStart hook injected (or run `python team/hooks.py board`).
2. Answer every **NEEDS REPLY** item first, on its issue.
3. Read `AGENTS.md`, `NOTES.md` and `plans/00-architecture.md`. Never re-decide anything written there.

## Rooms

| Room | Where | Use for |
|---|---|---|
| main | the task issues themselves | START / COMMIT / PR / BLOCKED / DONE / CONTRACT |
| data | issue `Room: data` + `docs/research/data.md` | yfinance quirks, universe choices, data checks |
| analysis | issue `Room: analysis` + `docs/research/analysis.md` | results, strategy and cost findings |
| deck | issue `Room: deck` + `docs/research/deck.md` | slides, charts, talk script |

Post findings to the room issue at once. Copy anything worth keeping into the matching `docs/research/*.md` or `NOTES.md` in your task branch, so it lands with your PR.

## Message prefixes (comments on your task issue)

| When | Command | Text |
|---|---|---|
| Starting | `python team/post.py --claim T05 "<intent>"` | assigns you and posts `START T05 on <branch>: <intent>` |
| Others depend on a commit | `python team/post.py --task T05 "..."` | `COMMIT <sha7> <branch>: <what>; affects <paths>` |
| PR opened | `python team/post.py --task T05 "..."` | `PR <url>: <title>. Needs review from @<owner>` |
| Stuck | `python team/post.py --task T05 "..."` | `BLOCKED T05: <need>, to:<person> @<github>` |
| Changing the contract | `python team/post.py --task T05 "..."` | `CONTRACT src/oi/contract.py: <old> -> <new>`; wait for Dev 1's reply |
| Merged | `python team/post.py --done T05 <pr-url>` | posts `DONE T05: <url>` and closes the issue |
| Finding | `python team/post.py --room data "..."` | free text |

## Rules
- Read the board (`python team/hooks.py board`) before every commit and push, when blocked, and when finishing.
- Reply only to items that need a reply. No "thanks" or "ok" comments.
- Before editing outside your task's **Scope** (listed on its issue): check the ownership map in `AGENTS.md` and ask the owner on your task issue.
- Work only in your own worktree `tasks/<slug>` on your own branch:
  `git fetch && git rebase origin/develop`, run `python -m pytest -q`, then `gh pr create --base develop`.
  Someone else approves and merges.
- The repo is public: never commit or post tokens, `.env` files, keys, `.team/` or downloaded price data.

## Hooks (installed by `team/setup.py` and `team/new_task.py`; you do not run them)

| Hook | What it does |
|---|---|
| SessionStart | `git pull --ff-only` on the main clone; injects the TEAM HUB block: deadlines, task board, open PRs, needs-reply, recent messages |
| UserPromptSubmit | shows new board comments since your last prompt |
| PostToolUse (Bash) | after `git commit`, `git push` or `gh pr create`, reminds you to post COMMIT / PR |
| Stop | blocks stopping once if a message addressed to you is unanswered |
