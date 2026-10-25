# 2026–27 position-defense identity approval runbook

**Status: NOT APPROVED FOR PUBLICATION.** This is a human-review procedure, not an authorization to change any `verified` flag.

## Scope and baseline

The latest successful [combined audit (run 40163429051)](https://github.com/eec757/nba-defensive-dashboard/actions/runs/40163429051) observed **642 actual player-game rows**. Only **8/642 (1.25%)** rows have approved identities in the existing crosswalk. The unapproved proposal baseline covers **626/642 (97.51%)** rows. A separate hypothetical scenario adds **12** rows to reach **638/642 (99.38%)**, but **25 defending-team/position coverage gates fail**. All automated proposal safety tests passed. Proposed identity links and cached roster positions are *not* approvals.

## Review sequence

1. Download the `combined-player-identity-audit-2027` artifact from [the successful audit](https://github.com/eec757/nba-defensive-dashboard/actions/runs/40163429051). Keep the source artifact unchanged for traceability.
2. For **every proposed identity**, compare the exact numeric NBA player ID against the official NBA player profile, the exact Basketball-Reference player ID against the corresponding player profile, and a genuinely independent source explicitly linking both IDs. A matching name alone is insufficient.
3. Check the player's **2026–27** team roster for one unambiguous `PG`, `SG`, `SF`, `PF`, or `C` assignment. Broad `G`/`F`, multiple conflicting positions, and depth-chart guesses are not sufficient. Record source URLs, review date, and the human reviewer's identifier.
4. **Do not batch-approve** the 366 proposed rows from a count or a script result. Each record requires human sign-off. Preserve rejected/ambiguous records as unverified.
5. For the remaining exceptions: NBA **1643633** (Graham Ike, 2 rows, `F`), **1643568** (Nick Martinelli, 1 row, `F`), and **1643813** (Alpha Diallo, 1 row, no exact BRef ID/position), obtain precise season-specific evidence or leave unverified.
6. Update `data/verified_player_ids_2027.csv` **only after** the individual evidence is checked. Never modify it based solely on a hypothetical coverage report.
7. Run the position-publication safety tests and combined identity audit. Confirm **at least 95% actual verified player-game coverage leaguewide, per defending team, and conservatively per defending team-position** before publishing. The production publisher must refuse to write output when any gate fails.

## Reviewer record

For each candidate record, document:

| Field | Required evidence |
| --- | --- |
| NBA player ID | Exact official NBA player URL |
| Basketball-Reference ID | Exact Basketball-Reference player URL |
| Independent linkage | External source explicitly connecting both IDs |
| 2026–27 position | Exact season roster source and one of PG/SG/SF/PF/C |
| Decision | Approve / reject / needs further evidence |
| Human reviewer | Identifier and ISO review date |
| Disagreement notes | Source conflicts, unresolved aliases, or position ambiguity |

**Stop conditions:** Missing identity linkage, missing reviewer attestation, ambiguous position, failed safety tests, or any coverage gate below 95% all block position-statistics publication. A successful GitHub Actions audit run means the audit executed; it does **not** mean the data is approved.
