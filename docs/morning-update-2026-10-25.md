# NBA defensive analytics morning update — October 25, 2026

**Game date:** October 24, 2026 (U.S. local game dates). **Seasons:** 2025–26 and 2026–27 regular seasons. **Publication:** Team-game results compiled separately from the lagging season summary; no position-publication gates changed.

## October 24: eight completed NBA games

The [NBA.com October 24 schedule](https://www.nba.com/games?date=2026-10-24) shows **8 of 8 games final**. Scores for six games were corroborated by [GMA News](https://www.gmanetwork.com/news/sports/basketball/1007080/nba-scores-76ers-vs-bucks-mavericks-vs-spurs-hornets-vs-heat-suns-vs-warriors-and-other-games/story/); the Dallas–San Antonio result was corroborated by [NBA.com's Spurs box score](https://www.nba.com/spurs/game/0022600109-spurs-vs-mavericks-dallas-tx-10-24-2026/box-score), the Denver–New Orleans result by the [NBA game recap](https://www.nba.com/game/nop-vs-den-0022600110), and Phoenix–Golden State by an [AP game recap](https://www.cbsnews.com/sanfrancisco/news/booker-scores-43-points-in-suns-131-122-win-over-warriors-who-fall-to-0-3/). Scores are recorded in [nightly-team-defense-2026-10-24.csv](../reports/nightly-team-defense-2026-10-24.csv) as 16 team-game records.

| Away | Home | Final | Defensive note |
|---|---|---|---|
| MIA | CHA | 110–115 | CHA allowed 110 |
| BKN | CLE | 121–125 | CLE allowed 121 |
| MIL | PHI | 116–127 | PHI allowed 116 |
| HOU | ATL | 121–114 | HOU allowed 114 |
| WAS | CHI | 124–120 | WAS allowed 120 |
| SAS | DAL | 122–106 | SAS allowed 106 |
| NOP | DEN | 135–141 (OT) | DEN allowed 135 |
| GSW | PHX | 122–131 | PHX allowed 122 |

**Lowest points allowed among the eight winning teams:** San Antonio 106 (against Dallas), Charlotte 110 (against Miami), Houston 114 (against Atlanta). Denver allowed 135 in an overtime win, so its game result should not be interpreted as elite defense.

**Game-level paint defense, limited verified example:** [NBA.com's Pelicans–Nuggets game summary](https://www.nba.com/game/nop-vs-den-0022600110) lists points in the paint as **New Orleans 70** and **Denver 56**. Therefore Denver allowed 70 paint points and New Orleans allowed 56 in that one game. This is **not** a season paint-defense average or position breakdown.

## Season snapshots and ranks — important lag

The successful [Daily NBA Update run on October 25](https://github.com/eec757/nba-defensive-dashboard/actions/runs/40197618919) updated [data/summary.json](../data/summary.json) at **2026-10-25 13:26 UTC**, but its NBA-derived BoxScore Lab feed still contains **1,230 games for 2025–26 and only 28 games for 2026–27**, the same 2026–27 count as yesterday's report. Consequently, **October 24's eight games are NOT incorporated into the published season averages or ranks below**. Do not interpret these as through-October-24 rankings; keep the 16 verified team-game results separate until source data catches up.

| Season (coverage) | Team | GP | Scored / game (rank) | Allowed / game (defense rank) |
|---|---|---:|---|---|
| 2025–26 (complete) | BOS | 82 | 114.85 (#19) | 107.16 (#1) |
| 2025–26 (complete) | OKC | 82 | 119.02 (#5) | 107.88 (#2) |
| 2025–26 (complete) | DET | 82 | 117.77 (#8) | 109.61 (#3) |
| 2026–27 (through Oct 23 in feed) | OKC | 2 | 106.00 (#25) | 94.00 (#1) |
| 2026–27 (through Oct 23 in feed) | DEN | 1 | 84.00 (#29) | 96.00 (#2) |
| 2026–27 (through Oct 23 in feed) | TOR | 2 | 123.50 (#5) | 97.00 (#3) |

**Three-point defense — Oklahoma City, source-derived (not NBA.com Stats API):**

| Season | Opponent 3PM/game | Opponent 3PA/game | Opponent 3P% | Opponent FG% |
|---|---:|---:|---:|---:|
| 2025–26 | 14.34 | 38.89 | 36.9% | 43.7% |
| 2026–27 (2 games) | 9.00 | 33.50 | 26.9% | 38.3% |

## Data-quality labels and source access

- **Verified final — game-level points:** 8 NBA.com-marked final games, 16 scored/allowed team-game rows, with supporting score citations in CSV. Includes overtime where applicable.
- **Calculated / derived — team season stats:** 2025–26 full season; 2026–27 feed through October 23 only. Source: [BoxScore Lab downloads](https://boxscorelab.com/downloads/) (NBA-derived; CC BY 4.0). Ranks are based on points per game, not defensive rating; early-season ranks are preliminary.
- **Unavailable / unverified:** Position-specific defense (PG, SG, SF, PF, C), position-specific threes, season paint defense, and shots-at-rim / rim defense. No estimated values or invented player-position data.
- **Source access limitation:** [NBA.com Stats team tables](https://www.nba.com/stats/teams/traditional) and [pbpstats](https://www.pbpstats.com/) were inaccessible to this run; NBA.com's schedule and some individual game summaries were accessible. The one verified game-level paint-points example does not resolve season-level paint coverage.
- **Local dashboard:** No local HTML file was accessed or modified. Repository season summary and publication gates were not changed by this report.
