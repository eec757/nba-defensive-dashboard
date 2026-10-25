# 2026–27 Source Refresh Investigation

## Confirmed evidence

- Combined audit run [40181330577](https://github.com/eec757/nba-defensive-dashboard/actions/runs/40181330577) succeeded and produced `2027_source_readiness.json`.
- Current source catalog: `https://basketball-data.billmill.org/nba/nba.duckdb` (read-only in our audits).
- Last inspected snapshot: 791 regular-season player-game rows, 35 game IDs, one PHO-defended game (`0022600092`).
- Completed Oct 24 PHO–GSW reference game `0022600111` absent. `requires_source_refresh=true`; `source_reference_freshness_pass=false`.
- A reference-game freshness pass would not prove full-season completeness; it is only a minimum witness.

## Source architecture

- `scripts/audit_proposed_game_coverage.py`, `scripts/audit_source_freshness_2027.py`, and `scripts/trace_phoenix_opponent_positions.py` attach the external DuckDB catalog read-only. No repository script currently updates that upstream catalog.
- `scripts/collect.py` uses a separate BoxScore Lab team-game CSV source for team scoring summaries. It does not produce verified opponent player-game positions and must not be used as a substitute for position coverage.

## Next engineering decision

1. Identify the external DuckDB source's published refresh schedule and ingestion provenance. No verified refresh cadence has been established yet.
2. If upstream lags, develop an **independent staging-only** official-game-log ingestion path with strict game/player ID checks, schema validation, deduplication, and provenance timestamps.
3. Keep newly staged data out of the published dashboard until identity, team, team-position and 95% conservative coverage audits pass.
4. Keep season-roster position as primary; game-specific roles are separate and cannot backfill season SG rows.

**No production changes, no automatic approvals, no publication gate exceptions.**
