# 2026–27 identity verification review checklist

## Current baseline (Combined Player Identity Audit run 40084696794)

- 30 teams, 512 roster entries, 336 single-name candidates.
- 378 / 387 player-game rows (97.67%) have **name/team candidates**, not verified identities.
- 8 staged crosswalk IDs cover 16 / 387 player-game rows (4.13%).
- 0 approved crosswalk IDs; approved game-row coverage is 0%.
- All five positions for all 30 defending teams remain unpublished.

## Review workflow

1. Download the `combined-player-identity-audit-2027` artifact from https://github.com/eec757/nba-defensive-dashboard/actions/runs/40084696794.
2. Use `reports/game_log_identity_priority_2027.csv` to prioritize frequent player-game IDs; use `reports/player_matching_2027.csv` for additional candidates.
3. For each candidate, independently open the official NBA profile identified by numeric NBA ID and the Basketball-Reference profile identified by BRef ID. Check multiple biographical identifiers (name, birth date, team, college/draft), and save **both exact profile URLs** in `docs/identity-evidence-2027.md`.
4. Verify the **2026–27 season-specific** Basketball-Reference position (PG, SG, SF, PF, or C), and note ambiguous/multiple positions. Do not silently substitute a career or current general position.
5. Only after reviewing evidence and the publication gate's source-validation requirements, approve a crosswalk row. A single-provider profile URL is explicitly insufficient for the current automated gate. Do not set `verified=true` merely because name/team match.
6. Run `Test Position Publication Safety` and `Diagnose Real NBA Game Logs`; check independently approved row coverage both leaguewide and for every defending team.
7. Only use the existing guarded publication workflow once coverage reaches 95% leaguewide **and** per defending team, with all five position groups represented. Until then, leave position-defense statistics unavailable.

## Audit limitations

Name/team matching is not cross-provider identity verification. A 97.67% candidate coverage result does not mean the 95% verified-publication threshold has been met. The current crosswalk uses a single `verification_source` URL; a future reviewed multi-source evidence schema and explicit approval test are needed before automated approval can be safely enabled.
