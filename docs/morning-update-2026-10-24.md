# NBA defensive analytics morning update — October 24, 2026

**Snapshot:** previous NBA game date October 23, 2026; seasons 2025–26 and 2026–27; regular season only.

## October 23 completed games

NBA.com's [October 23 scoreboard](https://www.nba.com/games?date=2026-10-23) marks **12 games final**. Final point totals were checked against [theScore's dated scoreboard](https://www.thescore.com/nba/events/2026-10-23). The 24 team-game records are in [nightly-team-defense-2026-10-23.csv](../reports/nightly-team-defense-2026-10-23.csv). Each record includes points scored, points allowed, opponent, status, and provenance.

| Away | Home | Final |
|---|---|---|
| Chicago | Milwaukee | 132–125 |
| New York | Boston | 103–107 |
| Atlanta | Charlotte | 128–81 |
| Toronto | Washington | 112–102 |
| Minnesota | Orlando | 115–93 |
| Dallas | Indiana | 121–105 |
| Detroit | Miami | 128–111 |
| Houston | San Antonio | 114–110 |
| New Orleans | Utah | 119–120 |
| LA Clippers | LA Lakers | 117–125 |
| Memphis | Golden State | 111–108 |
| Portland | Sacramento | 128–120 |

**Single-game defense highlights:** Atlanta allowed 81 points, Minnesota 93, Toronto 102, Boston 103. These are *one-night* point totals, not season defensive ranks.

## Season-level team summary

The repository's [data/summary.json](../data/summary.json) was updated at **2026-10-24 13:26 UTC** by the successful [Daily NBA Update](https://github.com/eec757/nba-defensive-dashboard/actions/runs/40098144862). Source: [BoxScore Lab](https://boxscorelab.com/downloads/) NBA-derived team-game CSVs (CC BY 4.0). These are **calculated/derived** statistics, not direct NBA.com Stats API responses.

| Season | Regular-season games | Teams | Best scoring defenses by opponent PPG |
|---|---:|---:|---|
| 2025–26 | 1,230 | 30 | Boston 107.16 (#1); Oklahoma City 107.88 (#2); Detroit 109.61 (#3) |
| 2026–27 through Oct 23 | 28 | 30 | Oklahoma City 94.00 (#1, 2 GP); Denver 96.00 (#2, 1 GP); Toronto 97.00 (#3, 2 GP) |

### Oklahoma City detail

| Season | GP | PPG (scoring rank) | Opponent PPG (defense rank) | Opponent 3PM/G | Opponent 3PA/G | Opponent 3P% | Opponent FG% |
|---|---:|---|---|---:|---:|---:|---:|
| 2025–26 | 82 | 119.02 (#5) | 107.88 (#2) | 14.34 | 38.89 | 36.9% | 43.7% |
| 2026–27 | 2 | 106.00 (#25) | 94.00 (#1) | 9.00 | 33.50 | 26.9% | 38.3% |

**Quality and limitations:** Team scoring, opponent scoring, shooting and ranks are **derived from BoxScore Lab game results** and should be interpreted with small-sample caution in 2026–27. NBA.com's game schedule and finals were accessible, but NBA.com Stats team-stat pages were not accessible in this run; pbpstats did not expose retrievable data. Therefore no direct NBA.com Stats/pbpstats-derived enrichment was added. All five opponent-position groups (PG/SG/SF/PF/C), position-specific 3-point defense, paint defense, and rim defense remain **Unavailable / unverified**. No missing values have been estimated.

**Publication protection:** No player-identity approvals or position-publication gates were changed. This report does not assert that any local HTML dashboard file was modified.
