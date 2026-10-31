# NBA defensive analytics morning update — October 31, 2026

**Game date:** October 30, 2026. **Seasons:** 2025–26 and 2026–27 regular seasons. **Publication:** quality-labeled reports only; no manual edits to `data/summary.json`, player identity approvals, positional publication gate, or local HTML.

## October 30 — 10 verified final games

All ten final scores were cross-checked against [Basketball-Reference October 30 scores](https://www.basketball-reference.com/boxscores/?month=10&day=30&year=2026); [NBA.com's October 30 scoreboard](https://www.nba.com/games?date=2026-10-30) confirms final status for all ten.

| Away | Home | Final away–home |
|---|---|---|
| CHA | WAS | 79–95 |
| CHI | BOS | 111–125 |
| DET | BKN | 110–94 |
| NYK | PHI | 93–98 |
| ORL | TOR | 121–114 |
| IND | MIA | 125–145 |
| HOU | DAL | 111–116 |
| LAC | MIN | 101–127 |
| LAL | GSW | 95–112 |
| DEN | PHX | 127–120 |

**Fewest points allowed October 30:** Washington 79, Philadelphia 93, Detroit 94, Charlotte 95, Golden State 95. Team-game points allowed is not pace-adjusted defensive rating.

## 2026–27 provisional defensive leaders

The successful [Daily NBA Update workflow](https://github.com/eec757/nba-defensive-dashboard/actions/runs/41206571639) refreshed [`data/summary.json`](../data/summary.json) at **2026-10-31T13:39:51.803020+00:00**, covering **81 completed 2026–27 games** through October 30 (71 prior games + 10 verified finals). Season ranks and shooting values are taken directly from the repository snapshot, not inferred from rounded averages.

| Team | GP | Scored/game (scoring rank) | Allowed/game (defense rank) | Opp 3PM/game | Opp 3PA/game | Opp 3P% | Opp FG% |
|---|---:|---:|---:|---:|---:|---:|---:|
| DET | 6 | 109.83 (#24) | 101.83 (#1) | 12.33 | 38.00 | 32.50% | 41.70% |
| OKC | 5 | 108.20 (#27) | 104.60 (#2) | 13.40 | 40.00 | 33.50% | 42.60% |
| PHI | 6 | 108.67 (#26) | 105.00 (#3) | 10.83 | 34.50 | 31.40% | 42.40% |
| CHA | 6 | 97.33 (#30) | 106.00 (#4) | 12.50 | 33.67 | 37.10% | 45.30% |
| MEM | 5 | 118.20 (#9) | 106.20 (#5) | 11.40 | 37.60 | 30.30% | 43.10% |

**2025–26 complete, unchanged (1,230 games):** Boston 114.85 scored/game (#19), 107.16 allowed/game (#1); Oklahoma City 119.02 scored/game (#5), 107.88 allowed/game (#2); Detroit 117.77 scored/game (#8), 109.61 allowed/game (#3).

[Full two-season snapshot](../reports/defensive-team-season-snapshot-2026-10-31.csv) contains all 30 teams in each season, scoring/defensive ranks, opponent three-point makes/attempts/percentage, opponent FG%, and per-category quality flags.

## Advanced defense and source quality

- **Team scoring and defensive ranks:** 2025–26 complete 1,230-game NBA-derived repository source; 2026–27 provisional 81-game NBA-derived repository source through October 30. Ten October 30 final scores independently corroborated. Rankings are raw points per game, not possession-adjusted.
- **Three-point defense and opponent FG%:** NBA-derived [BoxScore Lab](https://boxscorelab.com/downloads/) repository source has team shooting coverage for all 81 current-season games and all 1,230 2025–26 games. Values were not independently validated against direct NBA.com Stats tables in this run.
- **Position defense (PG/SG/SF/PF/C), including positional three-point defense:** **Unavailable/unverified** until approved player-game matching meets the 95% publication gate.
- **Paint defense:** Verified **single-game** example from the [official Houston–Dallas October 30 summary](https://www.nba.com/game/hou-vs-dal-0022600021): Houston and Dallas each scored 46 points in the paint, so each allowed 46 in that game. **Season-level paint points/attempts unavailable/unverified**; no extrapolation.
- **Rim defense:** **Unavailable/unverified** for team-season and position; no validated rim attempts, makes, percentages or points allowed.
- **NBA.com Stats:** [Team traditional stats](https://www.nba.com/stats/teams/traditional?Season=2026-27) did not return a usable table. NBA.com scoreboard was readable for game final statuses; the single-game summary supplied paint points.
- **pbpstats:** [pbpstats.com](https://www.pbpstats.com/) exposed no readable statistics, so possession and shot-location measures remain unavailable.
- **Dashboard safeguards:** GitHub's Daily NBA Update updated `data/summary.json`, and the [Pages deployment](https://github.com/eec757/nba-defensive-dashboard/actions/runs/41206588612) succeeded. This report adds quality-labeled artifacts only. No local HTML file was accessed or modified, and identity approvals and the 95% positional publication gate remain unchanged.

## Artifacts

- [October 30 nightly team-game results](../reports/nightly-team-defense-2026-10-30.csv)
- [Two-season defensive snapshot through October 30](../reports/defensive-team-season-snapshot-2026-10-31.csv)
