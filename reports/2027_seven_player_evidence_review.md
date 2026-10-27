# Seven-player independent evidence review — pending approvals

Source: combined audit [#40458682249](https://github.com/eec757/nba-defensive-dashboard/actions/runs/40458682249), artifact `combined-player-identity-audit-2027`, `missing_player_position_evidence_2027.json` and `2027_supported_identity_review_queue.csv`.

| NBA ID | Basketball Reference ID | Candidate position | 2026–27 roster evidence | Wikidata identity | Game rows |
|---|---|---|---|---|---:|
| 1626171 | portibo01 | PF | [MIA roster](https://www.basketball-reference.com/teams/MIA/2027.html) | [Q19667582](https://www.wikidata.org/wiki/Q19667582) | 3 |
| 1641713 | jacksgg01 | PF | [MEM roster](https://www.basketball-reference.com/teams/MEM/2027.html) | [Q115492105](https://www.wikidata.org/wiki/Q115492105) | 3 |
| 1641842 | hollaro01 | SF | [DET roster](https://www.basketball-reference.com/teams/DET/2027.html) | [Q116407941](https://www.wikidata.org/wiki/Q116407941) | 3 |
| 1643515 | anderch02 | PG | [CHO roster](https://www.basketball-reference.com/teams/CHO/2027.html) | [Q133691210](https://www.wikidata.org/wiki/Q133691210) | 3 |
| 1629057 | williro04 | C | [POR roster](https://www.basketball-reference.com/teams/POR/2027.html) | [Q28151848](https://www.wikidata.org/wiki/Q28151848) | 2 |
| 1642383 | claytwa01 | PG | [DAL roster](https://www.basketball-reference.com/teams/DAL/2027.html) | [Q117262884](https://www.wikidata.org/wiki/Q117262884) | 2 |
| 1641747 | holmeda01 | PF | [DEN roster](https://www.basketball-reference.com/teams/DEN/2027.html) | [Q115492041](https://www.wikidata.org/wiki/Q115492041) | 1 |

**Review status: pending for all seven.** These are evidence references extracted from the audit, not newly independently revalidated live pages. Confirm exact identity and the precise season-specific position against the cited sources and record the established independent approval evidence before any crosswalk promotion. The audit reported no official NBA identity evidence for these seven in this source report. The 17 game rows are hypothetical additions only.

**Explicit exclusions:** NBA IDs 1643633, 1643568, 1643813 remain outside this queue; their five raw rows stay in coverage denominators. No auto-approval, gate waiver, publication, or main-branch change is authorized.

## Live source spot-check (2026-10-27)

Independent web lookup corroborated precise 2026–27 roster positions for **Bobby Portis (MIA PF)** and **Ron Holland (DET SF)** from Basketball Reference roster pages. A Memphis roster result lists **GG Jackson II (PF)** but came from an unofficial mirror; recheck the canonical Basketball Reference page before signoff. Other candidates' precise positions and all exact NBA↔BRef identity pairs still require individually documented live validation. Generic G/F labels do not suffice.

- Bobby Portis: https://www.basketball-reference.com/teams/MIA/2027.html and https://www.basketball-reference.com/players/p/portibo01.html
- Ron Holland: https://www.basketball-reference.com/teams/DET/2027.html
- GG Jackson II: https://www.basketball-reference.com/teams/MEM/2027.html (canonical source not confirmed in this spot-check)

**No approvals granted.** Partial corroboration only; strict publication gates remain.

## Canonical-source checks — 2026-10-27 (additional)

Direct Basketball Reference 2026–27 roster pages independently corroborate these **candidate season positions**:

| NBA ID | Player | 2026–27 position | Canonical roster |
|---|---|---|---|
| 1643515 | Christian Anderson Jr. | PG | https://www.basketball-reference.com/teams/CHO/2027.html |
| 1642383 | Walter Clayton | PG | https://www.basketball-reference.com/teams/DAL/2027.html |
| 1641747 | DaRon Holmes | PF | https://www.basketball-reference.com/teams/DEN/2027.html |
| 1641713 | GG Jackson II | PF | https://www.basketball-reference.com/teams/MEM/2027.html |
| 1629057 | Robert Williams | C | https://www.basketball-reference.com/teams/POR/2027.html |

Christian Anderson's Wikidata item https://www.wikidata.org/wiki/Q133691210 independently exposes both NBA ID `1643515` and Basketball Reference ID `a/anderch02`; this is an exact identity match, not human approval. Other identity mappings remain candidates until their respective evidence is checked explicitly. The older claim that GG Jackson's position was only found via a mirror is superseded by the canonical MEM roster check above.

**Review status remains pending for all seven.** No approvals, publication, source-row deletions, or gate changes. Live sources may evolve; retain source URL and audit date for subsequent human signoff.

## Additional independent identity cross-check — 2026-10-27

- **Bobby Portis (NBA 1626171):** NBA player profile https://www.nba.com/player/1626171 names Bobby Portis Jr. and Miami Heat. Basketball Reference player profile https://www.basketball-reference.com/players/p/portibo01.html names Bobby Portis and Miami Heat. These are corroborating player/team references, **not a machine-verifiable exact NBA-ID-to-BRef-ID assertion** on their own; preserve pending exact-link review.
- **Walter Clayton Jr. (NBA 1642383):** NBA G League player profile https://gleague.nba.com/player/1642383 names Walter Clayton Jr.; Basketball Reference player page https://www.basketball-reference.com/players/c/claytwa01.html names Walter Clayton and displays 2026–27 DAL PG. Dallas's Oct 21, 2026 signing release https://gleague.nba.com/news/mavericks-sign-walter-clayton-jr-to-two-way-contract confirms team affiliation, but labels him only as a guard. These independently corroborate identity context and the specific Basketball Reference position, **not the exact NBA↔BRef ID linkage by themselves**.

Both cases remain **pending human evidence approval**. Do not infer exact identity links from similar names and teams; do not alter verified crosswalk or 95% coverage gates.

## Exact dual-identifier Wikidata verification — 2026-10-27

Direct Wikidata item lookups confirmed **both** NBA.com player ID (P3647) and Basketball Reference NBA player ID (P2685) on the **same item** for the following candidates. Basketball Reference values include the single-letter path prefix; the crosswalk uses the basename.

| Player | Wikidata item | P3647 NBA ID | P2685 Basketball Reference NBA ID | Status |
|---|---|---|---|---|
| Bobby Portis | https://www.wikidata.org/wiki/Q19667582 | 1626171 | p/portibo01 | exact dual-ID match, human approval pending |
| GG Jackson | https://www.wikidata.org/wiki/Q115492105 | 1641713 | j/jacksgg01 | exact dual-ID match, human approval pending |
| Robert Williams III | https://www.wikidata.org/wiki/Q28151848 | 1629057 | w/williro04 | exact dual-ID match, human approval pending |
| Walter Clayton Jr. | https://www.wikidata.org/wiki/Q117262884 | 1642383 | c/claytwa01 | exact dual-ID match, human approval pending |

These four are corroborated at the exact identifier level. The other three candidates (Ron Holland, Christian Anderson Jr., DaRon Holmes II) are not yet recorded as fully checked in this review. Wikidata assertions are third-party evidence, not human signoff. No approval, crosswalk change, or publication authorized.
