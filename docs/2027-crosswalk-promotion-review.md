# Human-attested crosswalk promotion review

The 2026-10-25 audit (run 40167109077) validated 362 user-attested new player identities plus 4 previously approved identities with no staging exceptions.

**This branch is a review gate, not publication.** The audited artifact `reports/human_attested_crosswalk_2027.csv` contains the approved crosswalk, but is stored in the GitHub Actions artifact, not committed here. Before any live promotion, compare the artifact's 366 entries with the exact 362-ID review snapshot and 4 existing approvals. Reject extra records, missing reviewed IDs, mismatched positions, conflicting IDs, or absent evidence. Do not promote from a fresh unapproved proposal.

The same audit found proposed game coverage 772/791 (97.6%) but failed defending-team gates for MIA, OKC, PHO and SAC and many conservative team-position gates. Therefore **do not publish `data/position_defense_2027.json`**. The live publisher's 95% league/team/team-position checks must stay in force.

Source: https://github.com/eec757/nba-defensive-dashboard/actions/runs/40167109077
