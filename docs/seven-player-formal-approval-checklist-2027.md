# Seven-player formal approval checklist — 2026–27

The automated checks passed in [run 40634584926](https://github.com/eec757/nba-defensive-dashboard/actions/runs/40634584926): seven exact Wikidata dual-identifier matches, seven exact Basketball Reference 2026–27 roster-position matches, and zero attestation reconciliation inconsistencies. These checks do not themselves authorize approval.

The repository records the owner's prior statement, “i have reviewed and they are correct,” in `reports/2027_seven_player_user_review_attestation.csv`. This is a recorded conversational attestation, **not** a signed GitHub approval or a fabricated per-player signoff.

| NBA ID | BRef ID | Season position | Formal approval |
|---|---|---|---|
| 1626171 | portibo01 | PF | Pending |
| 1641713 | jacksgg01 | PF | Pending |
| 1641842 | hollaro01 | SF | Pending |
| 1643515 | anderch02 | PG | Pending |
| 1629057 | williro04 | C | Pending |
| 1642383 | claytwa01 | PG | Pending |
| 1641747 | holmeda01 | PF | Pending |

## Approval evidence to provide

A reviewer must explicitly record an attributable identity (for example, an authenticated GitHub review), actual review date, the seven exact NBA↔BRef ID pairs, and the seven season-primary positions. Preserve the exact independent Wikidata entity URLs and 2026–27 Basketball Reference roster URLs already staged in the candidate CSV and workflow artifacts. Verify the evidence still matches at signoff. Do not infer or backdate approval from the chat statement.

Once attributable approval evidence exists, prepare a **separate reviewable crosswalk promotion**; validate all required fields with `validate_independent_evidence`, rerun live checks, and keep the three excluded players in coverage denominators. Do not modify `main` or publish automatically. The strict leaguewide, defending-team and team-position 95% gates remain mandatory; the last audit still reported 30 failed team-position checks.
