# NBA defensive analytics morning update — October 29, 2026

**Game date:** October 28, 2026. **Seasons:** 2025–26 and 2026–27 regular seasons. **Publication:** quality-labeled reports only; no modifications to `data/summary.json`, player identity approvals, positional publication gate, or local HTML.

## October 28 — 12 verified final games

All 12 finals and numeric scores independently agree between [RealGM](https://basketball.realgm.com/scores/2026-10-28) and [Sports.ws](https://www.sports.ws/nba/2026-10-28). [NBA.com scoreboard](https://www.nba.com/games?date=2026-10-28) lists all 12 as final but does not expose numeric scores in the retrieved text.

| Away | Home | Final away–home | Points allowed |
|---|---|---|---|
| MIA | ATL | 129–117 | MIA: 117; ATL: 129 |
| WAS | CLE | 111–121 | WAS: 121; CLE: 111 |
| CHA | DET | 89–97 | CHA: 97; DET: 89 |
| PHI | IND | 114–109 | PHI: 109; IND: 114 |
| ORL | TOR | 99–129 | ORL: 129; TOR: 99 |
| DEN | NOP | 104–91 | DEN: 91; NOP: 104 |
| GSW | MIN | 119–114 | GSW: 114; MIN: 119 |
| HOU | MIL | 132–100 | HOU: 100; MIL: 132 |
| NYK | CHI | 133–127 | NYK: 127; CHI: 133 |
| SAS | UTA | 117–111 | SAS: 111; UTA: 117 |
| OKC | DAL | 96–120 | OKC: 120; DAL: 96 |
| LAL | LAC | 103–87 | LAL: 87; LAC: 103 |

**Lowest points allowed:** LA Lakers (87), Detroit (89), Denver (91), Dallas (96), Toronto (99), Houston (100).

## 2026–27 provisional scoring and defensive rankings

The repository's published `data/summary.json` was refreshed on October 28 at 13:50 UTC and contains **56 games through October 27**. Appending 12 corroborated October 28 finals yields **68 completed games**. New season totals use rounded `GP × PPG` from the baseline two-decimal source averages (the small 1–4 game baseline yields unambiguous integer totals). Rankings are **points scored/allowed per game**, not possession-adjusted defensive rating; ties share competition rank.

| Team | GP | Scored/game (rank) | Allowed/game (defense rank) |
|---|---:|---:|---:|
| TOR | 4 | 117.50 (#9) | 102.50 (#1) |
| DET | 5 | 109.80 (#23) | 103.40 (#2) |
| OKC | 5 | 108.20 (#26) | 104.60 (#3) |
| MEM | 4 | 116.75 (#10) | 107 (#4) |
| PHI | 5 | 110.80 (#21) | 107.40 (#5) |
| MIN | 5 | 120.40 (#4) | 107.80 (#6) |
| LAC | 4 | 106.50 (#29) | 108.00 (#7) |
| CHA | 5 | 101.00 (#30) | 108.20 (#8) |

**2025–26 (complete, unchanged 1,230 games):** BOS 107.16 allowed/game (#1; 114.85 scored/game #19); OKC 107.88 allowed/game (#2; 119.02 scored/game #5); DET 109.61 allowed/game (#3; 117.77 scored/game #8).

[Full two-season team snapshot](../reports/defensive-team-season-snapshot-2026-10-29.csv).

## Defensive metric quality and source access

- **Team points scored/allowed and league ranks:** 2025–26 full-season repository source; 2026–27 **provisional derived through October 28** using corroborated finals, 68 games. Not a direct official NBA.com Stats season export.
- **Opponent three-point makes/attempts/percentage and FG%:** Latest available repository BoxScore Lab NBA-derived snapshot **through October 26 only**; excludes October 27–28. Values retained unchanged rather than falsely presented as current.
- **Position defense PG/SG/SF/PF/C and positional three-point defense:** **Unavailable/unverified**, because validated position-specific player-game coverage is not available for publication.
- **Paint defense and rim defense:** **Unavailable/unverified** at season-team level. No estimates.
- **NBA.com Stats:** [Traditional team stats](https://www.nba.com/stats/teams/traditional?Season=2026-27) could not be retrieved. The NBA.com schedule was accessible and confirmed final statuses, but numeric scores were corroborated via independent scoreboards.
- **pbpstats:** [pbpstats](https://www.pbpstats.com/) returned no usable data in text retrieval; no possession or shot-location measures published.
- **Dashboard protection:** `data/summary.json`, identity approval records, positional publication safeguards and any local HTML dashboard file were not modified.

## Artifacts

- [October 28 nightly team-game results](../reports/nightly-team-defense-2026-10-28.csv)
- [Two-season quality-labeled defensive team snapshot through October 28](../reports/defensive-team-season-snapshot-2026-10-29.csv)
