"""Create this machine's identity: python team/join.py --name vincent --machine laptop [--agent claude]."""

from __future__ import annotations

import argparse
import re

from _common import MAIN, gh_api, write_identity


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True, help="first name, lowercase")
    p.add_argument("--machine", required=True, help="short machine label, e.g. laptop")
    p.add_argument("--agent", default="claude")
    a = p.parse_args()
    for v in (a.name, a.machine, a.agent):
        if not re.fullmatch(r"[a-z0-9-]+", v):
            raise SystemExit(f"'{v}' must be lowercase letters, digits or '-'")
    login = gh_api("user")["login"]
    ident = {"id": f"{a.name}.{a.machine}.{a.agent}", "person": a.name, "machine": a.machine,
             "agent": a.agent, "github": login}
    write_identity(MAIN, ident)
    print(f"Joined as {ident['id']} (GitHub: {login}). Saved in .team/identity.json (git-ignored).")


if __name__ == "__main__":
    main()
