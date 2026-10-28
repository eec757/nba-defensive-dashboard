# Candidate propagation audit — run 40177048492

Source: https://github.com/eec757/nba-defensive-dashboard/actions/runs/40177048492 (successful); artifact `combined-player-identity-audit-2027` ID 12592987198, report `2027_targeted_candidate_propagation.json`.

**10 of 11** targeted candidates match the generated Wikidata game-log staging candidate IDs. All 11 remain `approval_status=pending`.

- Graham Ike (NBA 1643633): expected `ikegr01`; staged `ikegr01`; candidate match.
- Nick Martinelli (NBA 1643568): expected `martini01`; staged `martini01`; candidate match.
- Alpha Diallo (NBA 1643813): expected `diallal01`; staged ID list empty; **candidate_not_propagated**.

**Root cause:** `scripts/stage_missing_game_log_identity_evidence.py` derives candidate BRef IDs from Wikidata NBA-ID matches; the returned Diallo item has no BRef ID. The human-supplied BRef candidate is recorded in the targeted review but is not part of the upstream Wikidata result. This is an evidence gap, not proof that `diallal01` is incorrect.

**Safe next action:** independently corroborate the exact NBA-ID ↔ BRef-ID link (not merely the player name or position), then add a separately sourced, reviewed mapping to the staging pipeline. Do not silently override Wikidata, mark identity approved, or change the 95% publication gate. Position evidence for all three players must separately satisfy the 2026-27 season roster requirements.

No crosswalk changes; no publication authorization.
