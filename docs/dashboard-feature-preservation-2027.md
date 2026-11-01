# Dashboard feature preservation and player-prop expansion

## Non-negotiable foundation

The dashboard's primary features remain:

1. **All 30 NBA team defensive rankings:** team points scored per game and rank, points allowed per game and rank, defensive efficiency where verified, opponent FGM/FGA/FG%, 3PM/3PA/3P%, paint points and attempts allowed, and shots at the rim and attempts allowed. Include team-level per-game rates and league ranks.
2. **Defense versus position:** for each team, independently calculate opponent points, 3PM, 3PA, FG%, 3P%, paint points and attempts, and shots at the rim and attempts against **PG, SG, SF, PF and C**. Include per-game rates, rankings, game counts and coverage.
3. **Season separation:** keep 2025–26 and 2026–27 distinct; enable explicit season, team, position, metric and date-range filters. Do not mix denominators or silently combine seasons.
4. **Data quality:** retain player-ID and exact-position evidence checks, unknowns in denominators, 95% leaguewide publication gate, all 30 team gates and 150 team-position gates. Display freshness, source, verified-game coverage and missing-data warnings.

## Additive player-prop module

- Underdog Fantasy and PrizePicks market lines, when obtained by a permitted, documented method, belong in a **separate optional module**.
- Match platform players to canonical NBA IDs only after independent validation; never use platform-listed positions as exact PG/SG/SF/PF/C verification.
- Display source, collection time, event time, rule version, market, line, matchup, estimate and uncertainty. No unverified or stale line should appear as current.
- Link each player-prop analysis back to its opponent's team defense ranking and defense-vs-position profile.
- Historical backtesting must distinguish model predictions, platform lines and final outcomes; avoid claims of guaranteed picks.

## Recommended UI navigation

- **Team Defense** — league rankings, team trends, opponent shooting and paint/rim metrics.
- **Defense vs Position** — 30×5 matrix, sortable by metric, drill-down by team and position.
- **Player Matchup Explorer** — player history vs opponent defensive profile, with quality flags.
- **Player Props** — optional Underdog/PrizePicks comparisons after authorized access is established.

## Implementation priority

Finish trustworthy team and position defensive tables and coverage audits before integrating platform projections. Add prop comparisons without removing or reducing any existing defensive metric or gate. This document is planning only; it does not change production or claim new data coverage.
