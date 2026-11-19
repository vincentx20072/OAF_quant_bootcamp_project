---
name: oaf-team-onboard
description: Set a teammate up on the OAF_quant_bootcamp_project repo (clone, venv, identity, hooks, doctor, briefing). Use when someone asks to be set up or onboarded on this project.
---

# Onboard a teammate

Do these steps in order, check each result, and stop and tell the person if anything fails.

1. Check prerequisites: python3 --version (need 3.11+; on Windows try `py --version`), git --version, gh auth status (must be logged in; if not, tell me to run `gh auth login` and wait), claude --version.
2. Clone the repo here unless it already exists: gh repo clone vincentx20072/OAF_quant_bootcamp_project   then cd OAF_quant_bootcamp_project
   Create and activate a virtualenv in that folder: python3 -m venv .venv && source .venv/bin/activate   (Windows: py -m venv .venv then .venv\Scripts\activate). Use that venv's python for every step below.
3. Ask me for my first name (lowercase) and a short machine label (e.g. laptop). Then run: python team/join.py --name <name> --machine <machine>
   It records my GitHub login in the git-ignored .team/ folder. There is no token to handle.
4. Run: python team/setup.py   (checks out the develop branch, writes Claude Code hooks to the git-ignored .claude/settings.local.json, installs the Python dependencies)
5. Run: python team/doctor.py   and fix anything it flags until it says "All good". If "board reachable" fails, I have not accepted the collaborator invite: send me to https://github.com/vincentx20072/OAF_quant_bootcamp_project/invitations.
6. Read README.md, AGENTS.md, NOTES.md, plans/00-architecture.md and .claude/skills/challenge-rules/SKILL.md. Run python team/hooks.py board. Then summarise in 5 lines: what we are building, deadlines, the rooms, which tasks are open on the board, and which task you suggest for me.
7. Tell me to RESTART Claude Code inside the OAF_quant_bootcamp_project folder (or inside a tasks/<slug> folder). The session should open with a "TEAM HUB" block.
