# Priority unmatched players — independent evidence review (2026–27)

This is a **review packet**, not a crosswalk approval or published dataset. The team-gate gains from the unmatched-player audit are hypothetical and use a different coverage basis from the staged audit.

## NBA ID 1643515 — Christian Anderson Jr.

- NBA official profile: https://www.nba.com/player/1643515/christian-anderson — Christian Anderson, Charlotte Hornets, broad position **Guard**.
- Basketball-Reference profile: https://www.basketball-reference.com/players/a/anderch02.html — Christian Anderson Jr., Charlotte Hornets, **Point Guard**.
- 2026–27 Charlotte roster: https://www.basketball-reference.com/teams/CHO/2027.html — Christian Anderson Jr., **PG**.
- Existing repository candidate: `anderch02`, proposed **PG**, pending approval.
- Name, team, draft, and birthdate are consistent between provider profiles, but each profile independently naming the same player does **not** by itself satisfy the project's independent NBA-ID ↔ BRef-ID linkage evidence rule.
- **Status:** pending independent cross-provider linkage evidence and human review. Do not downgrade to G to shortcut the exact PG verification.

## NBA ID 1626171 — Bobby Portis Jr.

- NBA official profile: https://www.nba.com/player/1626171 — Bobby Portis Jr., Miami Heat, broad position **Forward**.
- Basketball-Reference profile: https://www.basketball-reference.com/players/p/portibo01.html — Bobby Portis, Miami Heat, **Power Forward / Center**; 2026–27 season position **PF**.
- Existing repository candidate: `portibo01`, proposed **PF**, pending approval.
- Name, team, birthday, draft year and pick align, but the cross-provider ID linkage must still meet the independent-evidence rule.
- **Status:** pending independent cross-provider linkage evidence and human review. Do not downgrade to F to shortcut exact PF verification.

## Audit implications

The most recent unmatched-player scenario showed seven and six player-game rows for these two IDs respectively, with each hypothetically capable of adding one team gate **in that scenario's coverage basis**. Those gains are not additive guarantees and do not modify the staged baseline of 8/30 team gates. No verification flags, position labels, or publication gates were changed.

## 2026-11-01 exact cross-provider ID verification

- **Christian Anderson Jr.**: Wikidata https://www.wikidata.org/wiki/Q133691210 explicitly lists NBA.com player ID `1643515` and Basketball Reference NBA player ID `a/anderch02` on the same item. Basketball-Reference https://www.basketball-reference.com/players/a/anderch02.html lists 2026–27 **PG**. NBA https://www.nba.com/player/1643515/christian-anderson identifies the same name and team but uses broad **Guard**. Exact ID linkage **supported**; exact 2026–27 PG source **supported**. Human crosswalk approval still pending.
- **Bobby Portis Jr.**: Wikidata https://www.wikidata.org/wiki/Q19667582 explicitly lists NBA.com player ID `1626171` and Basketball Reference NBA player ID `p/portibo01` on the same item. Wikidata lists power forward; the existing 2026–27 Basketball-Reference team roster candidate https://www.basketball-reference.com/teams/MIA/2027.html proposes **PF**. NBA https://www.nba.com/player/1626171 identifies the same player as broad **Forward**. Exact ID linkage **supported**; 2026–27 PF is **pending fresh direct season-roster confirmation** (Basketball-Reference player page returned HTTP 403 during this check). Human crosswalk approval still pending.
- **Action**: No `verified=true` flags changed, no human review was fabricated, and no coverage or publication gate was altered. Do not promote either record automatically.
