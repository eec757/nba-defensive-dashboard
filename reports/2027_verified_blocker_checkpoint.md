# 2027 publication blockers: verified checkpoint

Source: successful read-only combined audit [#40456515831](https://github.com/eec757/nba-defensive-dashboard/actions/runs/40456515831).

## Current approved baseline
- Approved player-game coverage: **920/969 = 94.94%**, below the required 95% leaguewide threshold.
- The hypothetical additional-evidence scenario reaches **964/969 = 99.48%**, but this is **not approved coverage** and does not authorize publication.
- The hypothetical scenario has **25 failed defending-team-position checks**, five each for LAL, MEM, OKC, PHO, and SAC. Publication remains blocked.

## Exact remaining hypothetical unknowns
| NBA ID | Player | Source rows | Defending teams | Missing independent evidence |
|---|---|---:|---|---|
| 1643633 | Graham Ike | 3 | LAL, MEM, PHO | Precise 2026–27 season-roster position |
| 1643568 | Nick Martinelli | 1 | SAC | Precise 2026–27 season-roster position |
| 1643813 | Alpha Diallo | 1 | OKC | Exact NBA-to-Basketball-Reference identity link and precise 2026–27 season-roster position |

## Interpretation and next actions
1. Keep these three players out of **player-level display** only. Do not delete their source rows or reduce coverage denominators.
2. The five unknown rows are the remaining blocker in the **hypothetical** scenario, not the only blocker in the actual approved baseline. Approval of the other hypothetically supported identities would still require the established independent review process.
3. Obtain independent season-specific precise position evidence; do not convert generic F/G labels to PF/SF/SG or infer positions from game context.
4. Re-run leaguewide, defending-team, and defending-team-position 95% gates after any documented, authorized approvals. Never waive gates, auto-approve, or publish from this report.

This checkpoint is diagnostic and does not modify production or main.
