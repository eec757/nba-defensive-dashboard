# Latest combined audit blockers — run 40176525631

Source: successful GitHub Actions run https://github.com/eec757/nba-defensive-dashboard/actions/runs/40176525631, artifact 12593175748. This report describes **hypothetical** coverage only, not production approval.

- 787/791 hypothetical covered player-game rows (99.49%); four unresolved rows.
- 0 defending-team gate failures; **22 conservative team-position gate failures** across LAL, MEM, OKC, PHO and SAC.
- Publication ready: **false**; verified crosswalk modified: **false**.

| NBA player ID | Player | Rows | Defending teams | Remaining generated audit blockers |
|---|---|---:|---|---|
| 1643633 | Graham Ike | 2 | LAL, MEM | 2026-27 season-specific position evidence not consumed by coverage pipeline |
| 1643568 | Nick Martinelli | 1 | SAC | 2026-27 season-specific position evidence not consumed by coverage pipeline |
| 1643813 | Alpha Diallo | 1 | OKC | Exact BRef identity link and 2026-27 position evidence not consumed by coverage pipeline |

The review branch separately records user-approved PF, SF, SG respectively and the corrected Diallo BRef **candidate** `diallal01`. The generated game-log exception report still has an empty BRef ID for Diallo, demonstrating that changing a candidate report did **not** update the authoritative identity-matching pipeline. Do not treat the candidate edits as verified crosswalk approvals.

Next engineering step: add independently verified source evidence to the inputs used by `scripts/audit_missing_player_positions.py` and the exact-ID staging pipeline, with tests and without weakening the conservative 95% publication gate. Phoenix SG zero-sample must be resolved separately. Do not publish based on hypothetical 99.49%.
