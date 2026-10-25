# 2026–27 position gate remediation plan

Evidence baseline: successful combined audit run https://github.com/eec757/nba-defensive-dashboard/actions/runs/40178924794 (artifact 12593835780).

## Current audited state

- 787 / 791 hypothetical player-game rows covered (99.49%); four unmatched game rows.
- 22 conservative team-position failures; zero team-level failures; publication_ready=false.
- Failures: LAL PG/SG/SF/PF/C, MEM PG/SG/SF/PF/C, OKC PG/SG/SF/PF/C, SAC PG/SG/SF/PF/C, PHO SG.

## Prioritized evidence actions

1. **Phoenix SG**: independently inspect the 2026–27 season roster position cache, per-game player position mapping and SG observation denominator. This failure has no known unresolved player-game row and cannot be fixed by resolving Ike, Martinelli or Diallo alone. Check for missing source observations, position normalization and denominator definition; do not infer SG assignments.
2. **Graham Ike (1643633)**: Wikidata candidate `ikegr01` exists. Independently verify 2026–27 season-specific PF eligibility for two player-game rows against LAL and MEM.
3. **Nick Martinelli (1643568)**: Wikidata candidate `martini01` exists. Independently verify 2026–27 season-specific SF eligibility for one player-game row against SAC.
4. **Alpha Diallo (1643813)**: official NBA ID/name/team/G evidence propagated, but Wikidata BRef field blank; user-supplied `diallal01` and SG remain pending independent exact-ID and season-specific position checks. One player-game row against OKC.
5. **Recompute all conservative position denominators** after each evidence-backed correction. One unmatched player-game row can cause multiple position failures if the conservative policy treats it as potentially belonging to any position; do not equate 22 failures with 22 distinct missing players.

## Safeguards

No publication, automatic human approval, crosswalk modification, or relaxation of the 95% leaguewide/team/team-position gate. Re-run the combined identity and coverage workflow after source-backed changes.
