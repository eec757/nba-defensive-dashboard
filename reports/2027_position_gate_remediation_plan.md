# 2026–27 position gate remediation plan

Evidence baseline: successful combined audit run https://github.com/eec757/nba-defensive-dashboard/actions/runs/40178924794 (artifact 12593835780).

## Current audited state

- 787 / 791 hypothetical player-game rows covered (99.49%); four unmatched game rows.
- 21 conservative team-position failures; zero team-level failures; publication_ready=false.
- Failures: LAL PG/SG/SF/PF/C, MEM PG/SG/SF/PF/C, OKC PG/SG/SF/PF/C, SAC PG/SG/SF/PF/C, PHO SG.

## Prioritized evidence actions

1. **Phoenix SG**: independently inspect the 2026–27 season roster position cache, per-game player position mapping and SG observation denominator. The baseline includes one unknown Phoenix opponent player-game row (NBA ID 1629057), but the hypothetical scenario supports that player's C position. Phoenix SG still has zero verified observations and cannot be fixed by assigning that Center row to SG. Check for missing source observations, position normalization and denominator definition; do not infer SG assignments.
2. **Graham Ike (1643633)**: Wikidata candidate `ikegr01` exists. Independently verify 2026–27 season-specific PF eligibility for two player-game rows against LAL and MEM.
3. **Nick Martinelli (1643568)**: Wikidata candidate `martini01` exists. Independently verify 2026–27 season-specific SF eligibility for one player-game row against SAC.
4. **Alpha Diallo (1643813)**: official NBA ID/name/team/G evidence propagated, but Wikidata BRef field blank; user-supplied `diallal01` and SG remain pending independent exact-ID and season-specific position checks. One player-game row against OKC.
5. **Recompute all conservative position denominators** after each evidence-backed correction. One unmatched player-game row can cause multiple position failures if the conservative policy treats it as potentially belonging to any position; do not equate 21 failures with 21 distinct missing players.

## Safeguards

No publication, automatic human approval, crosswalk modification, or relaxation of the 95% leaguewide/team/team-position gate. Re-run the combined identity and coverage workflow after source-backed changes.

## Artifact-verified Phoenix baseline (run 40178924794)

- `proposed_game_coverage_2027.json`: PHO has 13 total opponent player-game rows, 12 verified, one unknown. Verified positions: PG 5, SG **0**, SF 3, PF 1, C 3.
- `unmatched_player_games_2027.json`: the one PHO unknown is NBA ID `1629057`. This is a **baseline** unknown; the scenario's season-roster matching may support it at C. Do not confuse baseline unknown rows with the four remaining **hypothetical scenario** unknown rows.
- `missing_player_coverage_scenario_2027.json`: exactly **21** failing team-position pairs (5 each LAL, MEM, OKC, SAC; PHO SG only). The prior count of 22 was a documentation error.
- The conservative gate checks `verified/(verified+remaining_unknown)`, with an explicit nonzero-verified requirement. Thus even if all unknown PHO rows were resolved, PHO SG would still fail until a valid SG observation exists. Never fabricate one.

Next: trace the 13 PHO opponent-game rows through source game logs and position mapping to determine whether SG absence reflects actual observed games or a pipeline omission. Do not conflate the Phoenix team's own SG roster with opponent positions defended by Phoenix.

## User-provided source references for Phoenix review

- Robert Williams III: https://www.basketball-reference.com/players/w/williro04.html (user reports Portland center; direct source verification pending).
- Phoenix 2026–27 roster: https://www.basketball-reference.com/teams/PHO/2027.html (guard listings; Phoenix's own roster is not an opposing-player SG observation).
- Trace each Phoenix opponent game log back to its source game ID, opponent, NBA player ID, and original position; distinguish absent observations from dropped mappings. Do not assign an SG based on Phoenix's own roster.
