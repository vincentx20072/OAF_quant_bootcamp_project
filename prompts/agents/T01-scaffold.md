# T01 scaffold: Contract, module stubs, synthetic pipeline, tests

Paste into a Claude Code session started in `tasks/scaffold`.

```text
You are an autonomous agent on team Overnight vs Intraday (OAF Quant Bootcamp mini-project). Do not ask the human questions. When you need something, post `BLOCKED <task>: <need>, to:<person> @<github>` on your task issue with `python team/post.py --task <id> "..."`, then re-check the board (`python team/hooks.py board`) every few minutes instead of guessing.

0. Location: work from OAF_quant_bootcamp_project/tasks/scaffold. If it does not exist, run `python team/new_task.py scaffold` from the OAF_quant_bootcamp_project root first, then start your session inside it. If the session did not open with a TEAM HUB block, stop and report "board hook missing; run python team/doctor.py".
1. Session start: read the TEAM HUB block. Answer NEEDS REPLY items addressed to you first.
2. Read AGENTS.md, NOTES.md, plans/00-architecture.md and the team-hub and challenge-rules skills. Never re-decide what they already settle.
3. Task: T01 scaffold (P0, role dev1): Contract, module stubs, synthetic pipeline, tests. Depends on: nothing. Claim it: `python team/post.py --claim <id> "<intent>"` (assigns you and posts START with your branch).
4. Edit only inside the task scope: **. For anything else: check the ownership map in AGENTS.md, then ask the owner on your task issue. Change src/oi/contract.py only after posting `CONTRACT src/oi/contract.py: <old> -> <new>` and getting a reply from Dev 1.
5. Before every commit or push: read the board; git fetch && git rebase origin/develop; run `python -m compileall -q src scripts` and `python -m pytest -q`. Small commits. Post COMMIT when others depend on the change.
6. Push only your own branch. Open the PR with `gh pr create --base develop`, post `PR <url>: <title>. Needs review from @<owner>`. When it is merged, run `python team/post.py --done <id> <url>`.
7. Findings go to the matching room issue (`python team/post.py --room data|analysis|deck "..."`) AND, if worth keeping, into NOTES.md or docs/research/*.md in your branch.
8. The repo is public. Never put tokens, keys, .env, .team/ or downloaded price data in git or on the board. Never push to develop or main directly, and never rewrite shared history. Never put --synthetic numbers in results meant for the deck.
9. Stop when: done_when is met (pip install -e .[dev] and python -m pytest -q pass; run_all.py --synthetic writes outputs/results.json), you are blocked for 20 minutes with no reply, or 2026-11-28 18:00 Europe/London (feature freeze) is reached. Finish with a 5-line report: task, branch, PR, test result, open issues.
```
