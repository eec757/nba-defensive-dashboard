"""Fail-closed display filter for unresolved 2026-27 positions.

Never use this filter to change raw source rows or coverage denominators.
"""
EXCLUDED_PLAYER_IDS = frozenset({"1643633", "1643568", "1643813"})


def visible_player_rows(rows, id_field="nba_player_id"):
    """Return display-only rows, retaining input unchanged."""
    return [row for row in rows if str(row[id_field]) not in EXCLUDED_PLAYER_IDS]


def assert_raw_denominator_preserved(raw_rows, coverage_denominator):
    """Reject coverage calculated from display-filtered data."""
    if len(raw_rows) != coverage_denominator:
        raise ValueError("Coverage denominator must include all raw player-game rows")
