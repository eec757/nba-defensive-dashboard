# Exact seven-player attestation blockers — audit artifact review

Source: [GitHub Actions #40560875344](https://github.com/eec757/nba-defensive-dashboard/actions/runs/40560875344), artifact `combined-player-identity-audit-2027`, file `2027_seven_player_attestation_readiness.csv`.

All seven have **one identical blocker**: `not_in_verified_crosswalk`.

| NBA ID | BRef ID | Position | Reported blocker |
|---|---|---|---|
| 1626171 | portibo01 | PF | not_in_verified_crosswalk |
| 1641713 | jacksgg01 | PF | not_in_verified_crosswalk |
| 1641842 | hollaro01 | SF | not_in_verified_crosswalk |
| 1643515 | anderch02 | PG | not_in_verified_crosswalk |
| 1629057 | williro04 | C | not_in_verified_crosswalk |
| 1642383 | claytwa01 | PG | not_in_verified_crosswalk |
| 1641747 | holmeda01 | PF | not_in_verified_crosswalk |

**Interpretation:** This is a baseline-membership finding, not proof that each row already meets independent evidence and provenance requirements. The read-only checker short-circuits when the player is absent, so it has **not** validated their evidence URL, review metadata, or precise crosswalk fields. The next change should generate **unapproved, fully sourced candidate rows** and validate them with existing `publish_verified_positions.py` rules in a staging report, rather than directly inserting verified rows.

User review attestation exists, but formal approval provenance is not yet machine-validated. No change to `data/verified_player_ids_2027.csv`, no main/production update, and no 95% gate waiver.
