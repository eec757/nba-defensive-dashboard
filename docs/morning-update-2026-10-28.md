# NBA defensive analytics morning update — October 28, 2026

**Game date:** October 27, 2026. **Seasons:** 2025–26 and 2026–27 regular seasons. **Publication:** Report and quality-labeled CSV files only; no modifications to `data/summary.json`, identity approvals, positional gates, or local HTML.

## October 27 — four final games

Final scores cross-checked against [Sports.ws October 27 scoreboard](https://sports.ws/nba/2026-10-27) and [RealGM October 27 scoreboard](https://basketball.realgm.com/scores/2026-10-27); NBA.com game pages confirm game date and fixture, although their dynamically rendered box-score values were not available in text extraction.

| Away | Home | Final away–home | Points allowed |
|---|---|---|---|
| BKN | BOS | 124–125 | BKN: 125; BOS: 124 |
| DET | NYK | 97–111 | DET: 111; NYK: 97 |
| SAC | SAS | 103–130 | SAC: 130; SAS: 103 |
| POR | LAL | 136–129 | POR: 129; LAL: 136 |

**Lowest points allowed:** New York allowed 97, San Antonio 103, Boston 124, and Portland 129. The first two teams held opponents below 105 points.

## Season scoring and defense rankings

The current repository `data/summary.json` was refreshed **2026-10-27T13:45:18.475609+00:00**, with **1,230 games in 2025–26** and **52 games in 2026–27 through October 26**. The four October 27 verified finals are appended to the existing team scoring totals, yielding **56 games through October 27**. Integer points were recovered by rounding `gp × PPG` from the repository's two-decimal source averages, then new game points were added. With only 1–4 games per team in the baseline, this uniquely identifies the prior integer total. Rankings below are **provisional derived points-per-game ranks**, not possession-adjusted defensive ratings. Ties share rank.

### 2026–27 defensive leaders

| Team | GP | Points scored/game (rank) | Points allowed/game (defense rank) |
|---|---:|---:|---:|
| OKC | 4 | 111.25 (#22) | 100.75 (#1) |
| TOR | 3 | 113.67 (#16) | 103.67 (#2) |
| MIN | 4 | 122.00 (#4) | 105.00 (#3) |
| NYK | 4 | 104.00 (#29) | 105.25 (#4) |
| DET | 4 | 113.00 (#17) | 107.00 (#5) |
| MEM | 4 | 116.75 (#10) | 107.00 (#5) |
| PHI | 4 | 110.00 (#24) | 107.00 (#5) |
| LAC | 3 | 113.00 (#17) | 109.67 (#8) |

**2025–26 (unchanged, complete 1,230 games):** BOS 107.16 (#1; scored 114.85 #19); OKC 107.88 (#2; scored 119.02 #5); DET 109.61 (#3; scored 117.77 #8). Full 60-team-season quality-labeled table: [snapshot](../reports/defensive-team-season-snapshot-2026-10-28.csv).

## Advanced defensive data and quality

- **Team scoring / points allowed and ranks:** Derived through **October 27**, 56 completed games. New game scores are independently corroborated, but the season averages are computed from a previously published NBA-derived repository snapshot, not a newly retrieved official NBA.com Stats season table.
- **Three-point defense and opponent FG%:** Repository's BoxScore Lab NBA-derived source through **October 26** only; **October 27 excluded**. The snapshot preserves opponent 3PM/game, 3PA/game, 3P%, and opponent FG% as source-snapshot values, not as through-October-27 metrics.
- **Position-specific defense (PG/SG/SF/PF/C) and positional three-point defense:** **Unavailable / unverified**. The position-specific player-game coverage publication gate has not been satisfied in the published data.
- **Paint defense:** **Unavailable / unverified** at comparable team-season level.
- **Rim defense:** **Unavailable / unverified** at comparable team-season level.
- **NBA.com Stats direct tables:** [Team traditional stats](https://www.nba.com/stats/teams/traditional?Season=2026-27) not accessible through the retrieval tool. NBA.com game pages were accessible but rendered no extractable box-score statistics.
- **pbpstats:** [pbpstats](https://www.pbpstats.com/) produced no usable text or play-by-play metrics in this run.
- **Dashboard:** No local HTML file was available or modified; `data/summary.json` and publication/identity safeguards were left unchanged.

## Artifacts

- [October 27 nightly team-game results](../reports/nightly-team-defense-2026-10-27.csv)
- [Two-season quality-labeled team snapshot through October 27](../reports/defensive-team-season-snapshot-2026-10-28.csv)
