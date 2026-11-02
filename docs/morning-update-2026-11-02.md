# NBA defensive analytics morning update — November 2, 2026

**Game date:** November 1, 2026. **Seasons:** 2025–26 and 2026–27 regular seasons. **Scope:** verified finals, refreshed NBA-derived team-season analytics, official NBA.com game-level paint points. **Source update:** 2026-11-02T14:05:00.394206+00:00. **Publication:** quality-labeled report files; positional data remains gated.

## November 1 — all four final games verified

Official [NBA.com game summaries](https://www.nba.com/games?date=2026-11-01) agree with the [Basketball-Reference November 1 scoreboard](https://www.basketball-reference.com/boxscores/?month=11&day=1&year=2026) and [RealGM](https://basketball.realgm.com/scores/2026-11-01).

| Away | Home | Final away–home | NBA.com source |
|---|---|---|---|
| BOS | ORL | 108–97 | [Game summary](https://www.nba.com/game/bos-vs-orl-0022600154) |
| BKN | IND | 98–90 | [Game summary](https://www.nba.com/game/bkn-vs-ind-0022600155) |
| LAC | GSW | 112–124 | [Game summary](https://www.nba.com/game/lac-vs-gsw-0022600156) |
| TOR | LAL | 125–131 | [Game summary](https://www.nba.com/game/tor-vs-lal-0022600157) |

**Fewest points allowed:** Brooklyn 90, Boston 97, Indiana 98, Orlando 108. These are points allowed in individual games, not defensive ratings.

## 2026–27 team defense through November 1 — 92 games

The repository's [`data/summary.json`](../data/summary.json) was updated **2026-11-02T14:05:00.394206+00:00** from [BoxScore Lab](https://boxscorelab.com/downloads/) NBA-derived game data. It contains **92** games and 184 team-game records. Compared with yesterday's 88-game report, exactly eight team GP counts increased by one, corresponding to all four verified November 1 games. **Team averages and ranks below come directly from the refreshed repository snapshot, not from rounded-average estimates.** Ranks by points allowed/game (fewest = #1); scoring ranks by points scored/game (most = #1).

| Team | GP | Scored/game (rank) | Allowed/game (defense rank) |
|---|---:|---:|---:|
| DET | 6 | 109.83 (#21) | 101.83 (#1) |
| PHI | 7 | 108.71 (#23) | 104.86 (#2) |
| MEM | 6 | 121.17 (#1) | 106.00 (#3) |
| CHA | 7 | 98.29 (#30) | 106.43 (#4) |
| OKC | 6 | 106.50 (#29) | 107.00 (#5) |

**2025–26 complete 1,230-game season:**

| Team | GP | Scored/game (rank) | Allowed/game (defense rank) |
|---|---:|---:|---:|
| BOS | 82 | 114.85 (#19) | 107.16 (#1) |
| OKC | 82 | 119.02 (#5) | 107.88 (#2) |
| DET | 82 | 117.77 (#8) | 109.61 (#3) |
| HOU | 82 | 115.23 (#18) | 110.01 (#4) |
| NYK | 82 | 116.45 (#10) | 110.12 (#5) |

[Full 60-team-season snapshot](../reports/defensive-team-season-snapshot-2026-11-02.csv) includes scoring/defense ranks, opponent 3PM/3PA/3P%, opponent FG% and quality labels for both seasons.

## Advanced defense and quality

- **Three-point and FG defense:** NBA-derived repository source includes opponent 3PM, 3PA, 3P%, FG% for all **92** 2026–27 games through November 1 and all **1,230** 2025–26 games. These were **not independently reconciled** to direct NBA.com Stats tables. Examples for 2026–27: Detroit opponent 3PM **12.33/game**, 3PA **38.00/game**, 3P% **32.5%**, opponent FG% **41.7%**; Philadelphia **11.29**, **35.14**, **32.1%**, **43.3%**. 
- **Official November 1 game-level paint defense (points allowed):** Boston **36**, Orlando **38**; Brooklyn **26**, Indiana **30**; Clippers **44**, Golden State **48**; Toronto **48**, Lakers **46**. These reverse the opponent's offensive PITP on each NBA.com game summary. [Game-level CSV](../reports/nightly-team-defense-2026-11-01.csv). **Season paint points/attempts and paint shooting efficiency remain unavailable.**
- **Rim defense:** Attempts, makes, percentage and points allowed at the rim unavailable/unverified at season and position levels.
- **PG/SG/SF/PF/C positional defense:** All position-specific points, three-point, paint and rim statistics unavailable/unverified. The **95% validated player-game identity and position coverage gate remains in force**.
- **Direct NBA.com Stats:** [Team traditional stats](https://www.nba.com/stats/teams/traditional?Season=2026-27) were inaccessible as usable tables; official NBA.com game summaries provided all four finals and game-level paint totals.
- **pbpstats:** [Teams](https://www.pbpstats.com/teams/nba) was inaccessible as a usable play-by-play dataset. No shot-location, positional or possession statistics were inferred.

## Repository and dashboard status

The automated source snapshot already contains all **92** current-season games. This report and its two CSVs are supplementary; they do **not** manually overwrite `data/summary.json`, change player identity approvals, bypass the 95% publication gate, or access/modify any local HTML dashboard. The success/failure status of the November 2 GitHub Actions workflow was not independently confirmed.

## Artifacts

- [November 1 verified scores and official game-level paint defense](../reports/nightly-team-defense-2026-11-01.csv)
- [Two-season scoring, defense, shooting and quality snapshot](../reports/defensive-team-season-snapshot-2026-11-02.csv)
