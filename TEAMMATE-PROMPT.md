# Send this to each teammate

## 1. Accept the GitHub invite (it expires, so do it first)
- https://github.com/vincentx20072/OAF_quant_bootcamp_project/invitations

## 2. Install the tools if missing
Python 3.11+, git, GitHub CLI (`gh auth login`, use the same GitHub account that got the invite), Claude Code.

## 3. Open Claude Code in the folder where you keep projects and paste this

```text
Set me up on my team's OAF Quant Bootcamp mini-project repo (Overnight vs Intraday). Do these steps in order, check each result, and stop and tell me if anything fails.

1. Check prerequisites: python3 --version (need 3.11+; on Windows try `py --version`), git --version, gh auth status (must be logged in; if not, tell me to run `gh auth login` and wait), claude --version.
2. Clone the repo here unless it already exists: gh repo clone vincentx20072/OAF_quant_bootcamp_project   then cd OAF_quant_bootcamp_project
   Create and activate a virtualenv in that folder: python3 -m venv .venv && source .venv/bin/activate   (Windows: py -m venv .venv then .venv\Scripts\activate). Use that venv's python for every step below.
3. Ask me for my first name (lowercase) and a short machine label (e.g. laptop). Then run: python team/join.py --name <name> --machine <machine>
   It records my GitHub login in the git-ignored .team/ folder. There is no token to handle.
4. Run: python team/setup.py   (checks out the develop branch, writes Claude Code hooks to the git-ignored .claude/settings.local.json, installs the Python dependencies)
5. Run: python team/doctor.py   and fix anything it flags until it says "All good". If "board reachable" fails, I have not accepted the collaborator invite: send me to https://github.com/vincentx20072/OAF_quant_bootcamp_project/invitations.
6. Read README.md, AGENTS.md, NOTES.md, plans/00-architecture.md and .claude/skills/challenge-rules/SKILL.md. Run python team/hooks.py board. Then summarise in 5 lines: what we are building, deadlines, the rooms, which tasks are open on the board, and which task you suggest for me.
7. Tell me to RESTART Claude Code inside the OAF_quant_bootcamp_project folder (or inside a tasks/<slug> folder). The session should open with a "TEAM HUB" block.

From then on always follow the team-hub skill (read the board, claim a task before editing, post START/COMMIT/PR/DONE on the task issue, put findings in the room issues and docs/research) and the challenge-rules skill (the hard rules and deadlines).
```

Shortcut instead of step 3: `claude plugin marketplace add vincentx20072/OAF_quant_bootcamp_project`, then `claude plugin install oaf-team@oaf-team`, then type `/oaf-team:setup` in Claude Code.

## 4. After the restart, say this in the new session

```text
Run the team-hub session start: read the TEAM HUB block, answer anything that needs my reply, and read AGENTS.md and NOTES.md. Then tell me which unclaimed task fits me, and claim it once I agree.
```

## 5. Start your task in its own folder

```bash
python team/new_task.py <slug>      # e.g. factor-split
cd tasks/<slug>
claude
```
Ready-made prompts for each task are in `prompts/agents/`. Paste the one for your task into that session.

## Deadlines (Europe/London)
| When | What |
|---|---|
| 2026-11-20 18:00 | Group roster sent to committee |
| 2026-11-22 20:00 | End-to-end loop on real data |
| 2026-11-27 20:00 | P1 analyses done |
| 2026-11-28 18:00 | Feature freeze, tag v1-numbers |
| 2026-11-29 20:00 | Final charts |
| 2026-11-30 20:00 | Deck draft |
| 2026-12-01 19:00 | Timed rehearsal |
| 2026-12-02 12:00 | Deck emailed (internal) |
| 2026-12-02 23:59 | **Deck due to committee** |
| 2026-12-03 09:00 | **Presentation (date and time TBC)** |

## Remembered automatically in every new session
You do not need to re-explain anything when you start a new Claude Code session or run `/clear`. Start it inside `OAF_quant_bootcamp_project` or a `tasks/<slug>` folder and these load by themselves:
- `CLAUDE.md` / `AGENTS.md` and the `team-hub` and `challenge-rules` skills (protocol, rules, deadlines).
- A session-start hook that injects the deadlines, the task board, who holds which task, open PRs and recent board comments, and pulls the latest `develop`.
- A hook before each prompt that shows new comments from teammates and their agents.
- `NOTES.md`, `plans/` and `docs/research/` hold decisions and findings; write there anything the team must keep.
If a session does not show the "TEAM HUB" block at the start, run `python team/doctor.py` and restart.
