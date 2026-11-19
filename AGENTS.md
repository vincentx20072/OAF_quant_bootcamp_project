# AGENTS.md — read this first

**What we build.** OAF Quant Bootcamp mini-project: where does the US market earn its return, overnight or intraday?
P0 the split (one chart). P1 factor ETFs by time of day + switching strategy + break-even cost. P2 optional momentum WML.
Deck of 6 slides, 5-minute talk, Thu 3 Dec [VERIFY].

**Where things live.** One public repo, `vincentx20072/OAF_quant_bootcamp_project`.
- Code: `src/oi/`, `scripts/run_all.py`, `tests/`. Integration branch: `develop`. `main` = reviewed releases.
- Team tooling: `team/` (board scripts, config), `.claude/skills/`, `plans/`, `prompts/agents/`, `docs/research/`, `NOTES.md`.
- `tasks/<slug>/` = one git worktree per task inside your main clone, branch `<person>/<agent>/<slug>` (git-ignored).
- Board = issues labelled `task`; rooms = issues titled `Room: <topic>`.

**Protocol (full version: `team-hub` skill).**
1. Session start: read the TEAM HUB block; answer NEEDS REPLY first; read `NOTES.md`, `plans/00-architecture.md`.
2. `python team/new_task.py <slug>` → `cd tasks/<slug>` → `python team/post.py --claim <id> "<intent>"`.
3. Edit only your task's scope. Contract changes: post `CONTRACT ...`, wait for Dev 1.
4. Commit small; `git fetch && git rebase origin/develop`; `python -m pytest -q`; `gh pr create --base develop`; post `PR ...`.
5. After merge: `python team/post.py --done <id> <pr-url>`.
6. Findings → room issue + `docs/research/<topic>.md`; decisions → `NOTES.md`. Doc-only changes ride in your task PR,
   or go in a small `docs/<topic>` PR.

**Never.**
- Push to `develop` or `main` directly, or rewrite shared history.
- Commit `.team/`, `.claude/settings.local.json`, `.env*`, keys or tokens. The repo is **public**.
- Commit downloaded price data (`data/cache/*.csv.gz` is ignored on purpose).
- Put `--synthetic` numbers in the deck.
- Use unadjusted prices or simple returns; everything is adjusted log returns.
- Spend past the 20 man-hour group cap: cut P2 first, then P1 to one slide.

**Deadlines (Europe/London).**

| When | What |
|---|---|
| Sun 22 Nov 20:00 | End-to-end loop on real data |
| Fri 27 Nov 20:00 | P1 done |
| **Sat 28 Nov 18:00** | **Feature freeze, tag `v1-numbers`** |
| Mon 30 Nov 20:00 | Deck draft |
| Wed 2 Dec 12:00 | Deck emailed (internal) |
| **Wed 2 Dec 23:59** | **HARD: deck due** |
| **Thu 3 Dec** | **HARD: presentation** |

**Ownership map** (contract `src/oi/contract.py`).

| Path | Owner |
|---|---|
| `src/oi/contract.py`, `data.py`, `decompose.py`, `metrics.py`, `scripts/`, `tests/test_core.py`, `pyproject.toml`, `team/` | dev1 lead — vincent |
| `src/oi/momentum.py`, `tests/test_momentum.py` | dev2 momentum — TBD |
| `src/oi/factors.py`, `strategy.py`, `tests/test_strategy.py` | dev3 factors & strategy — TBD |
| `src/oi/plots.py`, `tests/test_plots.py`, `deck/` | dev4 charts & deck — TBD |
