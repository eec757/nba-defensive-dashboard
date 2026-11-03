# NBA Defensive Morning Update — 2026-11-03

## November 2 results
All 15 scheduled games finished. Scores independently agree between [Sports.ws](https://www.sports.ws/nba/2026-11-02) and [West42Sports](https://www.west42sports.com/nba-schedule-game-results-2026-27/); [NBA scoreboard](https://www.nba.com/games?date=2026-11-02) lists finals. See [nightly CSV](../reports/nightly-team-defense-2026-11-02.csv).

Lowest points allowed: Detroit 91, Washington 94, San Antonio 97, Minnesota 100, Sacramento 100.

## Season source and coverage
The GitHub `data/summary.json` file fetched during this run was refreshed 2026-11-03 14:04 UTC, but still reports **92 games for 2026–27 through November 1**; the 15 November 2 games are **not yet included**. Combined verified scoreboard coverage is 107 games, not an updated season-level statistical dataset. The 2025–26 NBA-derived source contains 1,230 games.

### 2026–27 repository leaders (through November 1, provisional)
| Team | GP | Scored/game | Allowed/game | Defense rank | Opponent 3P% |
|---|---:|---:|---:|---:|---:|
| DET | 6 | 109.83 | 101.83 | 1 | 32.5% |
| PHI | 7 | 108.71 | 104.86 | 2 | 32.1% |
| MEM | 6 | 121.17 | 106.00 | 3 | 30.1% |
| CHA | 7 | 98.29 | 106.43 | 4 | 37.6% |
| OKC | 6 | 106.50 | 107.00 | 5 | 35.3% |

### 2025–26 leaders (full regular season)
BOS: 114.85 scored/game, 107.16 allowed/game (#1 defense); OKC: 119.02 scored, 107.88 allowed (#2); DET: 117.77 scored, 109.61 allowed (#3).

## Data quality
- **Verified finals:** November 2 team points scored/allowed; not yet incorporated into repository season rankings.
- **NBA-derived repository:** Through November 1 for 2026–27; 2025–26 complete. Opponent 3PM, 3PA, 3P%, and FG% are in `data/summary.json`, not independently verified against NBA.com Stats tables.
- **Unavailable/unverified:** PG/SG/SF/PF/C defense, position-specific three-point defense, season paint points/attempts allowed, and rim defense. No pbpstats-derived tables were retrievable in this run. The 95% approved positional coverage gate must remain in force.
- No changes were made to `data/summary.json`, player identity approvals, publication safeguards, or a local HTML dashboard.
