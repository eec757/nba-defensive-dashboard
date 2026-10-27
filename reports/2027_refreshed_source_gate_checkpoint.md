# 2027 refreshed-source gate checkpoint

Source: [combined audit run 40450375172](https://github.com/eec757/nba-defensive-dashboard/actions/runs/40450375172), commit f48ec36; source checked 2026-10-27 04:38 UTC.

## Observed source improvement

- Source player-game rows: 969 (previously 791); distinct games: 43 (previously 35).
- Phoenix reference game 0022600111 is now present with Phoenix-opponent rows. Source-reference freshness passes; this does not establish full season completeness.
- Phoenix opponent position trace: 24 rows across 2 games, verified PG 8, SG 2, SF 5, PF 3, C 4; unmatched 2. Previously SG had zero rows.
- Upstream metadata records updated times: games 2026-10-26 21:12:07 UTC, player_box 2026-10-26 21:12:04 UTC, game_rotations 2026-10-26 17:32:20 UTC. These are dataset timestamps, not a verified refresh schedule.

## Publication remains blocked

- Approved identity coverage: 920 / 969 = 94.94%, below the 95% leaguewide threshold. 49 player-game rows unmatched across 34 player IDs.
- Read-only proposed game coverage: 947 / 969 = 97.73%; team coverage failures MIA, OKC, PHO, SAC, plus multiple team-position failures. Proposal coverage is not approval.
- Hypothetical additional matches: 964 / 969 = 99.48%, 5 unknown rows; no team gate failures but 25 team-position failures (all positions for LAL, MEM, OKC, PHO, SAC). These are conservative scenario failures, not 25 player identities.
- No approvals, crosswalk modifications, production publication, or relaxation of 95% leaguewide/team/team-position gates is authorized by this report.

## Next actions

1. Produce an exact exception queue from the 49 unmatched player-game rows / 34 IDs, with defending-team and game provenance, without auto-approval.
2. Independently validate missing NBA-to-BRef IDs and 2026-27 season roster positions; keep game-specific roles separate.
3. Re-run all three coverage gates against refreshed source and reviewed identities; do not publish unless each independently passes.
