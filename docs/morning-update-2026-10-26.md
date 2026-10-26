# NBA defensive analytics morning update — October 26, 2026

**Game date:** October 25, 2026 (U.S. local date). **Seasons:** 2025–26 and 2026–27 regular seasons. **Publication status:** Separate, quality-labeled report and CSV only; no changes to the dashboard's published `data/summary.json` or positional-publication gates.

## Last night's seven completed games

The [NBA.com schedule](https://www.nba.com/games?date=2026-10-25) lists **7 games, all final**. Final scores are corroborated by [Reuters' October 26 NBA roundup](https://www.reuters.com/sports/nba-roundup-luka-doncic-explodes-52-lead-lakers-past-jazz--flm-2026-10-26/). There are **14 verified team-game rows** in [nightly-team-defense-2026-10-25.csv](../reports/nightly-team-defense-2026-10-25.csv).

| Away | Home | Final (away–home) | Defensive points allowed |
|---|---|---|---|
| LAL | UTA | 132–123 | LAL allowed 123; UTA allowed 132 |
| IND | BKN | 136–109 | IND allowed 109; BKN allowed 136 |
| LAC | OKC | 101–108 | LAC allowed 108; OKC allowed 101 |
| ORL | NYK | 111–102 | ORL allowed 102; NYK allowed 111 |
| TOR | MIN | 94–117 | TOR allowed 117; MIN allowed 94 |
| DET | PHI | 106–93 | DET allowed 93; PHI allowed 106 |
| MEM | SAC | 123–112 | MEM allowed 112; SAC allowed 123 |

**Lowest points allowed by winning teams:** Detroit 93 (at Philadelphia), Minnesota 94 (vs. Toronto), Oklahoma City 101 (vs. LA Clippers). This is raw points allowed, not pace-adjusted defensive rating.

## Season team scoring and defensive ranks

The last confirmed [published repository season snapshot](../data/summary.json) was refreshed **2026-10-25T13:26:38.950152+00:00**, containing **1,230 regular-season games for 2025–26** and **28 games through October 23 for 2026–27**. No later successful daily source refresh was confirmed during this report. This report separately reconciles all **8 games on October 24** and **7 games on October 25** with that 28-game snapshot: **43 games through October 25** (86 team-game appearances). **The main dashboard's season summary is not updated by this report.**

**Provisional 2026–27 team rankings through October 25** are derived from the 28-game source snapshot (which stores two-decimal PPG averages) plus the 15 verified final scores. Small rounding differences of the original source averages are possible. Ranks below are by **points scored per game** and **points allowed per game**, not offensive/defensive rating. Each team has played only 1–4 games.

| Team | GP | Points scored/game (rank) | Points allowed/game (defense rank) |
|---|---:|---:|---:|
| OKC | 3 | 106.67 (#28) | 96.33 (#1) |
| MIN | 3 | 121.00 (#6) | 97.67 (#2) |
| POR | 2 | 126.00 (#2) | 101.50 (#3) |
| TOR | 3 | 113.67 (#15) | 103.67 (#4) |
| DET | 3 | 118.33 (#10) | 105.67 (#5) |

**2025–26 full-season scoring defense (unchanged, 82 GP each):** Boston 107.16 allowed/game (#1; scored 114.85, #19); Oklahoma City 107.88 (#2; scored 119.02, #5); Detroit 109.61 (#3; scored 117.77, #8). All 30 teams in both seasons, including team scoring and defense ranks, are included in [defensive-team-season-snapshot-2026-10-26.csv](../reports/defensive-team-season-snapshot-2026-10-26.csv).

**Oklahoma City through October 25:** 3 GP, 106.67 points scored/game (#28), 96.33 points allowed/game (#1). The October 25 game against the Clippers was a 108–101 win; this new score is reflected only in the provisional report.

## Three-point, positional, paint and rim defense

- **Three-point defense and opponent FG% — available, but different freshness:** The 2025–26 full-season team values are included in the CSV. For 2026–27, the latest verified repository source values are **only through October 23**, and **exclude October 24–25**. For Oklahoma City, 2025–26 opponent 3PM 14.34/game, 3PA 38.89/game, 3P% 36.9%, opponent FG% 43.7%; 2026–27 through October 23 only: opponent 3PM 9.00/game, 3PA 33.50/game, 3P% 26.9%, opponent FG% 38.3%. Do not treat the latter as through October 25.
- **Positional defense and positional three-point defense (PG/SG/SF/PF/C): UNAVAILABLE / UNVERIFIED.** The source snapshot contains no validated breakdowns. Player identity/position approval and 95% coverage gates remain unchanged.
- **Paint defense and paint attempts: UNAVAILABLE / UNVERIFIED** as comparable season-level and positional statistics.
- **Rim defense / shots at rim and attempts: UNAVAILABLE / UNVERIFIED** as comparable season-level and positional statistics.

## Source and publication quality

- **VERIFIED FINAL:** October 25 team-game points, NBA.com final schedule and Reuters score roundup.
- **CALCULATED / DERIVED:** 2025–26 full-season team averages and ranks, from [BoxScore Lab NBA-derived source](https://boxscorelab.com/downloads/) in the repository snapshot.
- **PROVISIONAL DERIVED:** 2026–27 points/game and league ranks through October 25, calculated from two-decimal October 23 averages plus verified October 24 and October 25 scores; these are not a new NBA.com Stats feed pull.
- **STALE / PARTIAL:** 2026–27 three-point and opponent FG% values remain at the October 23 source snapshot.
- **UNAVAILABLE / UNVERIFIED:** All positional defense, paint and rim metrics noted above.
- **SOURCE ACCESS LIMITATION:** [NBA.com Stats team tables](https://www.nba.com/stats/teams/traditional?Season=2026-27) could not be retrieved; [pbpstats](https://www.pbpstats.com/) returned no usable statistics. NBA.com game schedules and Reuters scores were accessible. No unavailable values were fabricated.
- **LOCAL HTML:** No local HTML dashboard was accessible or modified. `data/summary.json` and identity/position publication safeguards remain untouched.
