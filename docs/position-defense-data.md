# Defense by position: data integration plan

Status: player-level position statistics **not yet connected**. Do not display invented values.

## Current working feed
BoxScore Lab team-game CSVs produce team PPG, opponent PPG, FG%, and 3-point defense for 2025-26 and 2026-27. Keep this daily workflow operational independently of player-level enrichment.

## Candidate player-game source
https://github.com/llimllib/nba_data
Its public documentation describes player-game logs, player metadata, game IDs, and season-partitioned Parquet files. Verify actual file availability, schema, 2025-26 and 2026-27 coverage, and licensing before connecting it to the dashboard. This source has **not** been integrated or validated.

## Required validation
1. Identify each player by stable player ID, with a documented position assignment for the season. Hybrid positions must not be silently forced into PG/SG/SF/PF/C.
2. Identify each game and both participating teams with stable IDs, not name matching alone.
3. For every player-game row, join to the *opponent* team, not the player's team.
4. Exclude playoffs when displaying regular-season data. Avoid duplicate player rows and traded-player double counting.
5. Reconcile total player points per game to the corresponding team-game points, with explicit treatment of team points not attributed to players.
6. Count games with coverage; if a season/team/position cannot be verified, show Unavailable.
7. Describe results as **opposing player production by listed position**, not points conceded while guarding that position.
8. Keep shot-location/paint/rim defense unavailable until separately validated.

## Next implementation
Inspect the candidate Parquet schema and a small current-season sample. Implement optional enrichment with independent error handling; publish position statistics only after reconciliation passes. Keep the existing collector and dashboard usable if enrichment fails.
