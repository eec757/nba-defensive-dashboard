# Verification source registry — 2026–27 NBA defensive dashboard

Updated 2026-11-01. **Review-only policy.** These are source candidates, not preapproved identity evidence. Preserve source URLs, retrieval date, season, licensing and the exact observed source value. Never treat a generic G/F/C label as PG/SG/SF/PF/C or infer NBA↔Basketball Reference identity equivalence from name alone.

## Priority 1 — identity and exact season-position evidence

| Source | Role | Caveat |
|---|---|---|
| https://www.nba.com/players | Official NBA player profile/roster, name and NBA ID corroboration | NBA.com's displayed position can be broad or reflect current rather than 2026–27 season |
| https://www.nba.com/stats/overview | Official NBA historical/season statistics and player identification | Check season, API access and accuracy for per-position defense |
| https://github.com/swar/nba_api | Python access to NBA.com player IDs, CommonPlayerInfo, CommonTeamRoster, PlayerIndex and game logs | Unofficial wrapper; availability and endpoint behavior need live tests; NBA IDs alone do not prove BRef IDs |
| https://www.basketball-reference.com/ | BRef ID and specific 2026–27 roster/position, when explicitly shown | Honor access limits; broad primary positions or missing season information are not exact-position proof |
| https://www.espn.com/nba/players | Secondary independent player names and roster positions | May use broad G/F labels or a current season |
| https://www.cbssports.com/nba/stats/ | Secondary roster/position cross-check | Confirm exact player and season context |

## Priority 2 — paid/provider cross-check or cross-system mapping

| Source | Role | Caveat |
|---|---|---|
| https://sportsdata.io/nba-api | Licensed player profiles, roster, position and provider IDs | API key/plan and mapping to NBA/BRef IDs must be confirmed |
| https://developer.sportradar.com/basketball/docs/nba-ig-id-handling | Cross-provider identifier mapping design | Sportradar UUID/SR IDs are **not** NBA/BRef IDs; translate only with documented explicit mappings |
| https://highlightly.net/nba-api/documentation/players/by-id/ | Player profiles as independent cross-check | Confirm coverage, entitlement and position specificity |
| https://rapidapi.com/Creativesdev/api/nba-api-free-data | Candidate player/roster enrichment | Verify provenance, stability and rate limits before use |
| https://documenter.getpostman.com/view/24232555/2s93shzpR3 | Additional provider documentation to assess | Provider, source data and ID semantics not established |
| http://nbasense.com/nba-api/ | Potential auxiliary NBA API | HTTP-only URL; do not put tokens/credentials in plain-HTTP requests |
| https://github.com/djblechn-su/nba-player-team-ids | Historical NBA player/team ID lookup candidate | Validate update date and exact IDs against NBA source; do not assume 2026–27 completeness |

## Priority 3 — context / analytics only, not authoritative crosswalk proof

| Source | Role | Caveat |
|---|---|---|
| https://www.statmuse.com/nba | Human-readable stats/name and season questions | Queries do not establish an independent dual-ID mapping |
| https://www.bball-index.com/ | Advanced player and defensive analytics | Definition, coverage and license require assessment; not direct ID proof |
| https://bigballsdata.com/docs/nba-player-stats | Box-score/game-log candidate | Published documentation currently describes game logs through 2025–26 and provider-specific UUIDs; not a 2026–27 source until confirmed |
| https://basketball.fantasysports.yahoo.com/ | Supplemental fantasy-position cross-check | Positions are fantasy eligibility rather than necessarily one exact primary NBA role; use canonical URL without referral parameters |

## Automated matching and approval gates

1. Match an NBA ID to an official NBA identity and retain the observed URL, response, and retrieval timestamp.
2. Match a Basketball Reference ID to that same player from independent, inspectable dual-ID evidence. Name similarity alone never auto-approves.
3. Verify exact **2026–27** PG/SG/SF/PF/C position using season-scoped evidence. Disagreements, multiple labels, or G/F/FC remain exceptions.
4. Compare all three identity/position records; record conflicts, missing access and rate-limit failures as exceptions. Never substitute unchecked values.
5. Stage only fully corroborated and explicitly reviewed records; independently rerun the strict leaguewide, per-team and team-position 95% coverage gates, with unknown rows in denominators.
6. Production crosswalk updates and publication still require explicit authorization; this registry grants no approvals.

## Access and licensing

Use official documented APIs where possible. Confirm terms, rate limits and commercial/reuse restrictions before crawling or bulk fetching. Keep API tokens in GitHub encrypted Actions secrets, never committed to repository files, reports or logs. Do not send credentials to HTTP-only endpoints. Record source health (authentication, season support, field availability and reproducibility) before a source is enabled for automated promotion.

Duplicate Basketball Reference link in the user-supplied list is intentionally deduplicated.
