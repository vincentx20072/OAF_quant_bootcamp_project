# Onboarding

The fastest path is `TEAMMATE-PROMPT.md`: paste its block into Claude Code and it does everything below.

By hand:
1. Accept the collaborator invite to `vincentx20072/OAF_quant_bootcamp_project` (needed to push branches and edit issues).
2. Install Python 3.11+, git, GitHub CLI (`gh auth login`), Claude Code.
3. `gh repo clone vincentx20072/OAF_quant_bootcamp_project && cd OAF_quant_bootcamp_project`
4. `python3 -m venv .venv && source .venv/bin/activate` (Windows: `py -m venv .venv` then `.venv\Scripts\activate`)
5. `python team/join.py --name <you> --machine <label>`
6. `python team/setup.py`
7. `python team/doctor.py` until `All good`
8. Restart Claude Code inside the repo folder. The session should open with a `TEAM HUB` block.

The hooks live in `.claude/settings.local.json`, written by `team/setup.py` with the exact venv Python, so they work on macOS, Linux and Windows.
