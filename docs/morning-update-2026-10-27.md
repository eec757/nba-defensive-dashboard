# NBA defensive analytics morning update — October 27, 2026

**Game date:** October 26, 2026. **Seasons:** 2025–26 and 2026–27 regular seasons. **Publication:** Report and quality-labeled CSV files only; no changes to `data/summary.json`, player-identity approvals, positional gates, or local HTML.

## October 26 — all nine games final

[NBA.com official scoreboard](https://www.nba.com/games?date=2026-10-26) lists nine final games. Final score pairs cross-checked against [LunoSport October 26 scoreboard](https://www.lunosport.com/nba/2026-10-26) and [OnSportsNow October 26 scoreboard](https://onsportsnow.com/?date=2026-10-26&sport=all). The nightly CSV has 18 team-game records, with game IDs 0022600119–0022600127.

| Away | Home | Final away–home | Points allowed |
|---|---|---|---|
| WAS | CHA | 103–110 | WAS: 110; CHA: 103 |
| MIN | CLE | 125–127 | MIN: 127; CLE: 125 |
| CHI | BOS | 99–134 | CHI: 134; BOS: 99 |
| DAL | MIA | 113–109 | DAL: 109; MIA: 113 |
| IND | MIL | 102–110 | IND: 110; MIL: 102 |
| PHX | OKC | 114–125 | PHX: 125; OKC: 114 |
| ATL | HOU | 110–120 | ATL: 120; HOU: 110 |
| MEM | UTA | 110–105 | MEM: 105; UTA: 110 |
| GSW | DEN | 134–114 | GSW: 114; DEN: 134 |

**Lowest points allowed:** Boston held Chicago to 99, Utah allowed Memphis 110, Charlotte held Washington to 103, and Dallas allowed Miami 109. Note Boston's 99 was the fewest allowed across all nine games.

## Two-season scoring and defensive rankings

The repository's last successful `data/summary.json` update is **2026-10-26T15:09:13.336963+00:00**, with **1,230 completed 2025–26 games** and **43 completed 2026–27 games through October 25**. This report adds the nine verified October 26 finals to the 43-game team scoring base for **52 games through October 26**. Because the source stores PPG to two decimals, prior *integer team point totals* were recovered by rounding `gp × PPG` to the nearest integer (unique within the small 1–4-game sample); the nine final scores were added to those totals. Team averages and ranks below are **provisional derived** and are not a fresh NBA.com Stats season table. Rankings use points per game, **not** possession-adjusted ratings; equal values share rank.

### 2026–27 scoring and defense leaders through October 26

| Team | GP | Points scored/game (rank) | Points allowed/game (defense rank) |
|---|---:|---:|---:|
| OKC | 4 | 111.25 (#21) | 100.75 (#1) |
| POR | 2 | 126.00 (#2) | 101.50 (#2) |
| TOR | 3 | 113.67 (#15) | 103.67 (#3) |
| MIN | 4 | 122.00 (#4) | 105.00 (#4) |
| DET | 3 | 118.33 (#8) | 105.67 (#5) |
| MEM | 4 | 116.75 (#11) | 107.00 (#6) |
| PHI | 4 | 110.00 (#24) | 107.00 (#6) |
| BOS | 3 | 118.00 (#9) | 107.67 (#8) |

**Oklahoma City:** 4 GP, 111.25 scored/game (#21), 100.75 allowed/game (#1). On October 26 OKC beat Phoenix 125–114, allowing 114 points. All early-season rankings are highly sensitive to the small sample.

**2025–26 (full 1,230 games, unchanged):** BOS 107.16 (#1, scored 114.85 #19); OKC 107.88 (#2, scored 119.02 #5); DET 109.61 (#3, scored 117.77 #8). All 60 team-season rows with scoring and defensive ranks are in [defensive-team-season-snapshot-2026-10-27.csv](../reports/defensive-team-season-snapshot-2026-10-27.csv).

## Shooting, position, paint and rim data quality

- **Three-point defense, team level — SOURCE SNAPSHOT ONLY:** 2025–26 values cover the full season; 2026–27 opponent 3PM/game, 3PA/game, 3P%, and opponent FG% cover only **43 games through October 25** and **exclude October 26**. The source is [BoxScore Lab NBA-derived game data](https://boxscorelab.com/downloads/). OKC through October 25: opponent 3PM 11/game, 3PA 35/game, 3P% 31.4%, FG% 40.6%. These shooting stats must not be represented as through October 26.
- **Position-specific defense (PG/SG/SF/PF/C) and positional three-point defense — UNAVAILABLE / UNVERIFIED.** The validated player-game positional coverage/publication gate is not satisfied in the published dataset; no positions or matchups were guessed.
- **Paint defense / opponent paint attempts — UNAVAILABLE / UNVERIFIED** as comparable team-season and positional metrics.
- **Rim defense / shots and attempts at rim — UNAVAILABLE / UNVERIFIED** as comparable team-season and positional metrics.
- **Source access:** [NBA.com Stats team traditional table](https://www.nba.com/stats/teams/traditional?Season=2026-27) could not be retrieved in this run; [pbpstats](https://www.pbpstats.com/) returned no usable play-by-play statistics. NBA.com **game final statuses** were accessible; score pairs were independently corroborated.
- **LOCAL HTML / PUBLICATION:** No local HTML file was available or modified. This report does not modify `data/summary.json`, published dashboard data, player crosswalks, or position-specific publication safeguards.

## Artifacts

- [October 26 nightly team-game results](../reports/nightly-team-defense-2026-10-26.csv)
- [Two-season quality-labeled team snapshot through October 26](../reports/defensive-team-season-snapshot-2026-10-27.csv)
