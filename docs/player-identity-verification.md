# Independent player-ID verification protocol

The dashboard must not label a Basketball-Reference player ID as verified merely because the player's name and team match an NBA game log, because an external crosswalk repeats the same mapping, or because an NBA.com player profile exists.

## What qualifies

For each `bref_id` ↔ `nba_player_id` pair, a reviewer must find an independently checkable source that **explicitly identifies both IDs as the same player**, or an auditable identity chain with a shared, independently assigned identifier and documented provenance. Record the exact evidence URL, what identifiers it shows, and the date reviewed. A link to a single-provider player page does not suffice. Name, team, draft class, or matching statistics alone do not establish an ID link.

## Review procedure

1. Open `reports/verification_priority_2027.csv` and review the highest-game-count players first.
2. Check the candidate's Basketball-Reference ID, NBA numeric ID, team, and position against the actual source records.
3. Find a source showing the **explicit ID association**. If none is available, keep `verified=false` and note why.
4. Check for duplicate BRef IDs, duplicate NBA IDs, conflicting evidence, and position changes.
5. Only after reviewing the evidence, update `data/verified_player_ids_2027.csv` with `verified=true` and the evidence URL. The publishing script still enforces numeric IDs, unique mappings, and minimum game-log coverage.

## Publication requirements

- At least 95% of all regular-season opponent player-game rows must be covered by verified identities.
- Each defending team must also meet 95% verified opponent player-game row coverage.
- All 30 teams must have a nonempty result for all five positions.
- The automated safety tests must pass.
- Compare a sample of resulting team/position totals against the original game logs before publishing.

**Important:** The publisher can enforce structural checks and coverage, but cannot prove that a linked webpage genuinely contains the claimed ID relationship. Independent human evidence review remains mandatory. Do not mark an identity verified just to reach the coverage threshold.
