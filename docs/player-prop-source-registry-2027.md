# Player-prop source registry (2026–27)

Purpose: add Underdog Fantasy and PrizePicks as **market/projection context**, not as authoritative player identity, exact position, or defensive-stat sources.

| Source | Intended data | Identity authority | Access status | Automated ingestion |
| --- | --- | --- | --- | --- |
| NBA.com / NBA Stats | Official player and game stats | Primary NBA ID source | Existing validation workflow | Only approved methods |
| Basketball Reference | Candidate crosswalk / historical statistics | Corroboration; independently confirm dual IDs | Existing review workflow | Respect site restrictions |
| ESPN / CBS Sports | Additional profile and roster corroboration | Secondary | Discovery / manual review | Not yet approved |
| Underdog Fantasy | Available pick'em projections, selection categories, rules, timestamps | No | **Permission and access method not verified** | **Disabled** |
| PrizePicks | Available pick'em projections, selection categories, rules, timestamps | No | **Permission and access method not verified** | **Disabled** |

## Data separation

- `player_identity`: canonical NBA player ID, independently verified BRef crosswalk, team and exact 2026–27 PG/SG/SF/PF/C position.
- `platform_projection`: platform, source player label, mapped canonical NBA ID **only after verification**, market type, line, observation timestamp and timezone, event start, status, scoring/rule version, evidence URL, collection method and access authorization.
- `model_estimate`: versioned estimate, uncertainty, features and data quality, distinct from any platform line.
- `evaluation`: settled results, platform-specific grading, historical error/calibration, no look-ahead bias.

## Release safeguards

1. Do not scrape either platform or use undocumented endpoints. Obtain documented, permitted access and confirm applicable terms before automated retrieval.
2. Do not infer a canonical player identity or exact position from a platform listing.
3. Never treat a projection as an actual result or a verified defensive statistic.
4. Preserve the existing **95% leaguewide coverage** and **30 team / 150 team-position** gates. Missing records remain in denominators.
5. Do not publish recommendations until data freshness, identity mapping, rules and backtesting are validated. Any probabilities are estimates, not guarantees.

## Next implementation gate

Identify authorized Underdog and PrizePicks data access (official API, licensed vendor, or manual user-provided exports), then implement a **disabled-by-default importer** with schema validation, provenance and timestamp checks. Do not ingest live lines before access is approved.
