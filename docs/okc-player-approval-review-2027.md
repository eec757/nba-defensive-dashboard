# Oklahoma City player identity approval review — 2026–27

**Status: pending human sign-off.** This checklist is a review queue, not a verification certificate. The [evidence ledger](identity-evidence-2027.md) records two primary provider profiles for each player, but the crosswalk has no reviewer/date entries and every `verified` flag remains `false`.

| Player | NBA ID | BRef ID | Staged position | Evidence | Approval blocker |
|---|---|---|---|---|---|
| Chet Holmgren | 1631096 | holmgch01 | C | [NBA](https://www.nba.com/player/1631096/chet-holmgren) · [BRef](https://www.basketball-reference.com/players/h/holmgch01.html) | 2026–27 roster position confirmed; human sign-off still required |
| Jalen Williams | 1631114 | willija06 | SG | [NBA](https://www.nba.com/player/1631114/jalen-williams) · [BRef](https://www.basketball-reference.com/players/w/willija06.html) | 2026–27 roster and per-game rows confirm SG; human sign-off still required |
| Cason Wallace | 1641717 | wallaca01 | SG | [NBA](https://www.nba.com/player/1641717/cason-wallace) · [BRef](https://www.basketball-reference.com/players/w/wallaca01.html) | Confirm 2026–27 season position and human sign-off |
| Ajay Mitchell | 1642349 | mitchaj01 | SG | [NBA](https://www.nba.com/player/1642349/ajay-mitchell) · [BRef](https://www.basketball-reference.com/players/m/mitchaj01.html) | Confirm 2026–27 season position and human sign-off |

## Required checks before any approval

- [ ] Confirm each NBA numeric ID and BRef ID refer to the same person using independent biographical attributes, not only a name/team match.
- [x] Confirm staged **2026–27 season-specific** positions against the [Basketball-Reference 2026–27 OKC roster](https://www.basketball-reference.com/teams/OKC/2027.html). Jalen Williams is **SG** in the 2026–27 per-game position column, although his career positions include SG and PF. Recheck if the source updates.
- [ ] Record the reviewer and ISO review date in `data/verified_player_ids_2027.csv`, with a documented evidence trail.
- [ ] Review the `verification_source` policy: the publisher currently rejects a single NBA or BRef profile as sufficient cross-source linkage. Do not replace it with an arbitrary third-party URL or a self-referential repo page to bypass this gate.
- [ ] Keep `verified=false` until all requirements have been independently checked and the automated tests pass.
- [ ] Re-run leaguewide and per-team coverage; **95% verified coverage for each** and all five position groups are required before publishing.

## Latest measured baseline

Combined audit run [40085243426](https://github.com/eec757/nba-defensive-dashboard/actions/runs/40085243426): 8 staged entries, 0 metadata-complete approvals, 0 verified entries, 4.13% staged game-log coverage, 0% approved coverage. The 97.67% name/team candidate coverage is **not** verified coverage.

## Season-position source check (2026-10-24)

Basketball-Reference's [2026–27 OKC roster and stats](https://www.basketball-reference.com/teams/OKC/2027.html) lists Holmgren **C**, Jalen Williams **SG**, Wallace **SG**, and Mitchell **SG**. [Jalen Williams's player season table](https://www.basketball-reference.com/players/w/willija06.html) independently shows **2026–27: SG** while the player header gives historical positions SG/PF. This resolves the season-specific position question, **not** the human cross-provider identity approval, independent linkage-source requirement, or 95% coverage gates.
