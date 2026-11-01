# Three-player independent verification queue (2026–27)

These players are **pending review**, not permanently excluded. Keep every raw player-game row in coverage denominators. Do not treat an ambiguous roster position as an exact PG/SG/SF/PF/C label.

| NBA player ID | Player | BRef candidate | Exact position proposed | Pending evidence | Current verified metric status |
| --- | --- | --- | --- | --- | --- |
| 1643633 | Graham Ike | ikegr01 | PF | Independent 2026–27 exact position evidence (source currently says F / Forward-Center) | Excluded from exact-position metrics |
| 1643568 | Nick Martinelli | martini01 | SF | Independent 2026–27 exact position evidence (source currently says F / Forward) | Excluded from exact-position metrics |
| 1643813 | Alpha Diallo | diallal01 | SG | Independent NBA↔BRef identity linkage **and** exact 2026–27 position evidence (source labels conflict) | Excluded from identity-dependent and exact-position metrics |

## Independent promotion checks

1. Verify the NBA player ID and Basketball-Reference player ID correspond to the same person using independently inspectable evidence.
2. Record the 2026–27 exact position as one of PG, SG, SF, PF, C, with source URL, retrieval date, and reviewer approval. A generic G, F, G-F, or F-C label is insufficient.
3. For identity-only team analytics, permit a player with independently verified identity to advance to a separate *identity-verified / position-pending* state; do **not** promote that player to the exact-position crosswalk.
4. Re-run all coverage audits after any promotion. Maintain leaguewide, team, and team-position 95% publication gates. UNKNOWN rows remain in all denominators.
5. Do not invent source evidence or reviewer signatures. No changes to production files, `main`, or PR merges without explicit approval.

## Review outcomes

Current state: all three **pending**. No new independent verification or owner approval is claimed by this queue.
