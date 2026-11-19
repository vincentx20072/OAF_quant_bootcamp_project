# Research: data

- Source: yfinance, `auto_adjust=True`. Open must be adjusted too (T02 verifies).
- Expected quirks: early MTUM/VLUE/USMV/QUAL history starts ~2013; occasional stale opens on single stocks; ticker renames (META was FB before 2022 — yfinance serves history under META) [VERIFY].
- Cache: `data/cache/open.csv.gz`, `close.csv.gz`.
