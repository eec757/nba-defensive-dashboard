# 2026–27 Oklahoma City identity sign-off worksheet

**Status: awaiting independent human review.** This worksheet is not an approval, and it must not be used to flip any `verified` flag automatically.

## Review queue

| Player | NBA ID | BRef ID | Wikidata linkage record | 2026–27 BRef roster position | Human-reviewed both IDs? |
|---|---|---|---|---|---|
| Chet Holmgren | 1631096 | holmgch01 | [Q88234141](https://www.wikidata.org/wiki/Q88234141) | C | Pending |
| Jalen Williams | 1631114 | willija06 | [Q100957464](https://www.wikidata.org/wiki/Q100957464) | SG | Pending |
| Cason Wallace | 1641717 | wallaca01 | [Q114414145](https://www.wikidata.org/wiki/Q114414145) | SG | Pending |
| Ajay Mitchell | 1642349 | mitchaj01 | [Q105925605](https://www.wikidata.org/wiki/Q105925605) | SG | Pending |

Position source: [Basketball-Reference 2026–27 Oklahoma City roster](https://www.basketball-reference.com/teams/OKC/2027.html). These are season roster positions, **not measured defensive matchup assignments**.

## Required review procedure

1. Open each Wikidata entity and inspect its **NBA player ID (P3647)** and **Basketball-Reference.com NBA player ID (P2685)** statements. Confirm both values exactly match the table. Check statement references and the entity's name; a URL's domain alone is not proof.
2. Independently inspect the linked [NBA player profiles](https://www.nba.com/players) and Basketball-Reference player profiles already recorded in `data/verified_player_ids_2027.csv`. Check biographical attributes (e.g. birth date, college, draft year) and reject ambiguous same-name matches.
3. Verify the season-position classification and record any source disagreement. Do not treat roster position as on-court defensive assignment.
4. Record the **actual human reviewer's identity** in `reviewed_by` and the actual ISO date in `reviewed_on`, only after the evidence is checked. Do not fabricate reviewer names or dates.
5. Set `verified=true` only for individually approved mappings, then run the safety tests and coverage audit. **Do not publish position defense** unless verified leaguewide and per-team game-row coverage are each at least 95% and all five position groups are represented.

## Audit baseline

The [combined audit run 40086881554](https://github.com/eec757/nba-defensive-dashboard/actions/runs/40086881554) reported **4 eligible evidence URLs, 0 metadata-complete records, 0 approved identities, and 0% approved game-log coverage**. Eligible URL syntax does not establish correct identity linkage.

**Reviewer:** _Pending_

**Review date:** _Pending_

**Decision:** _Pending; all four remain unapproved_
