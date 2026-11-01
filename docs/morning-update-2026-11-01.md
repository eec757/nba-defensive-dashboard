# NBA defensive analytics morning update — November 1, 2026

**Game date:** October 31, 2026. **Seasons:** 2025–26 and 2026–27 regular seasons. **Publication:** quality-labeled report files only. No manual change to `data/summary.json`, local HTML, identity approvals or the 95% positional gate.

## October 31 — seven verified final games

Seven of seven October 31 games were final, cross-checked against [Sports.ws](https://sports.ws/nba/2026-10-31) and [Basketball-Reference's October 31 box scores](https://www.basketball-reference.com/boxscores/?month=10&day=31&year=2026). Six NBA.com official game summaries were readable and independently confirmed those scores; the Minnesota–San Antonio NBA.com page was not fully readable.

| Away | Home | Final away–home |
|---|---|---|
| POR | UTA | 112–90 |
| PHI | CHA | 109–104 |
| ATL | NOP | 99–121 |
| SAC | MEM | 105–136 |
| CLE | MIL | 136–111 |
| MIN | SAS | 111–121 |
| OKC | HOU | 98–119 |

**Fewest points allowed:** Portland 90, New Orleans 99, Houston 98, Philadelphia 104, Memphis 105. (Sorted numerical order: Portland 90, Houston 98, New Orleans 99, Philadelphia 104, Memphis 105.)

## Provisional 2026–27 defensive leaders through October 31

The [Daily NBA Update](https://github.com/eec757/nba-defensive-dashboard/actions/runs/41312475677) completed successfully on November 1 and refreshed [`data/summary.json`](../data/summary.json) at **2026-11-01T13:41:37.676713+00:00**, but the NBA-derived source still covers **81 completed games through October 30**. The separate report combines those 81 games with the **seven independently verified October 31 finals**, totaling **88 games**. The scoring/defense averages below are **provisional approximations**, computed from previously rounded team averages plus exact new scores; ranks may change when the upstream source includes October 31.

| Team | GP | Points scored/game (scoring rank) | Points allowed/game (defense rank) |
|---|---:|---:|---:|
| DET | 6 | 109.83 (#22) | 101.83 (#1) |
| PHI | 7 | 108.72 (#25) | 104.86 (#2) |
| MEM | 6 | 121.17 (#1) | 106.00 (#3) |
| TOR | 5 | 116.80 (#11) | 106.20 (#4) |
| CHA | 7 | 98.28 (#30) | 106.43 (#5) |

2025–26 remains a complete 1,230-game season: Boston **114.85 scored/game (#19)** and **107.16 allowed/game (#1)**; Oklahoma City **119.02 scored/game (#5)** and **107.88 allowed/game (#2)**; Detroit **117.77 scored/game (#8)** and **109.61 allowed/game (#3)**.

[Full two-season snapshot](../reports/defensive-team-season-snapshot-2026-11-01.csv) includes all 30 teams each season, provisional scoring and defense ranks, opponent three-point and FG defense, and category-specific quality labels.

## Three-point defense, paint defense, rim defense and positional defense

- **Opponent three-point defense (3PM/3PA/3P%) and FG%:** Available in the NBA-derived [BoxScore Lab](https://boxscorelab.com/downloads/) repository source for **81 current-season games through October 30**, plus the full 2025–26 season. These season shooting figures **exclude all seven October 31 games** and were not independently cross-checked against direct NBA.com Stats tables.
- **Verified October 31 single-game three-point example:** In [Oklahoma City at Houston](https://www.nba.com/game/okc-vs-hou-0022600153), Houston made **18 of 41** three-point attempts, so Oklahoma City allowed **18/41 (43.9%)**; Oklahoma City made **10 of 32**, so Houston allowed **10/32 (31.3%)**. Do not mix these into stale season shooting averages.
- **Verified October 31 single-game paint defense:** NBA.com's official game summaries show **Portland 28 / Utah 26; Philadelphia 48 / Charlotte 50; Atlanta 66 / New Orleans 52; Sacramento 54 / Memphis 36; Cleveland 46 / Milwaukee 60; Oklahoma City 30 / Houston 44** points in the paint allowed. These are defensive values, reversing the opponent's offensive PITP. Minnesota–San Antonio paint points were not independently retrievable. [Source summaries](https://www.nba.com/game/okc-vs-hou-0022600153) and [nightly game file](../reports/nightly-team-defense-2026-10-31.csv). **Season paint points/attempts and paint shot efficiency remain unavailable.**
- **Rim defense (attempts, makes, percentages, points allowed):** Unavailable/unverified at both team-season and position level.
- **PG/SG/SF/PF/C positional defense**, including three-point, paint and rim breakdowns: Unavailable/unverified. The 95% validated player-game identity and position coverage publication gate remains in force.
- **Direct NBA.com Stats season tables:** [NBA.com team traditional statistics](https://www.nba.com/stats/teams/traditional?Season=2026-27) were not accessible as usable tabular data; official individual NBA.com game summaries did supply final scores, game-level paint totals and the one confirmed shooting example.
- **pbpstats:** [pbpstats.com](https://www.pbpstats.com/teams/nba) did not yield a usable team or play-by-play table, so no shot-location or possession estimates were invented.

## Repository and dashboard status

[Daily NBA Update run](https://github.com/eec757/nba-defensive-dashboard/actions/runs/41312475677) and [GitHub Pages deployment](https://github.com/eec757/nba-defensive-dashboard/actions/runs/41312496907) both succeeded on November 1. The automated source snapshot remains 81 games; this report provides a separate **88-game provisional scoring update**. This report does **not** change `data/summary.json`, publish unverified positional statistics, or access/modify any local HTML dashboard.

## Artifacts

- [October 31 final scores, verified game-level paint and limited three-point defense](../reports/nightly-team-defense-2026-10-31.csv)
- [Full 2025–26 and provisional 2026–27 team defensive snapshot](../reports/defensive-team-season-snapshot-2026-11-01.csv)
