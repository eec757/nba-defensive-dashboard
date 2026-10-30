# NBA defensive analytics morning update — October 30, 2026

**Game date:** October 29, 2026. **Seasons:** 2025–26 and 2026–27 regular seasons. **Publication:** quality-labeled reports only; no modifications to `data/summary.json`, player identity approvals, positional publication gate, or local HTML.

## October 29 — 3 verified final games

All three scores agree between [RealGM](https://basketball.realgm.com/nba/scores/2026-10-29) and [Sports.ws](https://www.sports.ws/nba/2026-10-29). The [NBA.com scoreboard](https://www.nba.com/games?date=2026-10-29) confirms all three final statuses; numeric scores were not exposed in its readable text.

| Away | Home | Final away–home | Points allowed |
|---|---|---|---|
| CLE | ATL | 111–114 | CLE: 114; ATL: 111 |
| SAC | NOP | 120–132 | SAC: 132; NOP: 120 |
| MEM | POR | 124–103 | MEM: 103; POR: 124 |

**Lowest points allowed:** Memphis (103), Atlanta (111), Cleveland (114). These are points allowed, not pace-adjusted defensive ratings.

## 2026–27 provisional scoring and defensive rankings

The repository's [`data/summary.json`](../data/summary.json) was last updated **2026-10-29T13:53:02.170068+00:00** and contains **68 games through October 28**. Appending three independently corroborated October 29 finals yields **71 completed games**. Existing 2-decimal averages were converted back to unambiguous integer totals using `round(GP × PPG)` (each baseline team has at most five games), then combined with verified scores. Rankings are points scored/allowed per game, not possession-adjusted ratings; tied averages share competition rank.

| Team | GP | Scored/game (rank) | Allowed/game (defense rank) |
|---|---:|---:|---:|
| TOR | 4 | 117.50 (#11) | 102.50 (#1) |
| DET | 5 | 109.80 (#24) | 103.40 (#2) |
| OKC | 5 | 108.20 (#27) | 104.60 (#3) |
| MEM | 5 | 118.20 (#8) | 106.20 (#4) |
| PHI | 5 | 110.80 (#21) | 107.40 (#5) |
| MIN | 5 | 120.40 (#4) | 107.80 (#6) |
| LAC | 4 | 106.50 (#29) | 108.00 (#7) |
| CHA | 5 | 101.00 (#30) | 108.20 (#8) |

**2025–26 (complete, unchanged 1,230 games):** Boston 107.16 allowed/game (#1; 114.85 scored/game #19); Oklahoma City 107.88 allowed/game (#2; 119.02 scored/game #5); Detroit 109.61 allowed/game (#3; 117.77 scored/game #8).

[Full two-season team snapshot](../reports/defensive-team-season-snapshot-2026-10-30.csv).

## Defensive metric quality and source access

- **Team points scored/allowed and league ranks:** 2025–26 complete 1,230-game repository source. 2026–27 provisional through October 29, 71 games. The 3 added finals are independently corroborated, not a direct official NBA.com Stats season export.
- **Opponent 3PM, 3PA, 3P% and FG%:** Latest available repository [BoxScore Lab NBA-derived](https://boxscorelab.com/downloads/) snapshot **through October 28**, covering 68 games. Excludes October 29 for all teams, including those that played October 29. This snapshot is newer than the shooting coverage in the prior day's separately compiled report.
- **Position defense PG/SG/SF/PF/C and positional three-point defense:** **Unavailable/unverified** pending validated player-game positional coverage and the 95% publication gate.
- **Paint defense and rim defense:** **Unavailable/unverified** at season-team level; no fabricated attempts, makes, points, or percentages.
- **NBA.com Stats:** [Traditional team stats](https://www.nba.com/stats/teams/traditional?Season=2026-27) could not be retrieved as a usable table. [NBA.com schedule](https://www.nba.com/games?date=2026-10-29) was readable for game final status, but its box score text did not expose numeric team statistics.
- **pbpstats:** [pbpstats](https://www.pbpstats.com/) exposed no readable statistics in text retrieval; no possession or shot-location measures published.
- **Dashboard protection:** `data/summary.json`, identity approval records, positional publication safeguards, and any local HTML dashboard file were not modified by this report.

## Artifacts

- [October 29 nightly team-game results](../reports/nightly-team-defense-2026-10-29.csv)
- [Two-season quality-labeled defensive team snapshot through October 29](../reports/defensive-team-season-snapshot-2026-10-30.csv)
