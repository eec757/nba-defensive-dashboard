"""Safety regression tests for source freshness readiness; no network or publishing."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from audit_source_readiness_2027 import evaluate

BASE={"season":2027,"checked_at_utc":"2026-10-25T00:00:00Z","catalog":"read-only","expected_completed_phoenix_game_id":"0022600111"}

class SourceReadinessTests(unittest.TestCase):
    def test_missing_reference_game_blocks_freshness(self):
        result=evaluate({**BASE,"expected_game_present_in_regular_season_catalog":False,"expected_game_has_phoenix_opponent_rows":False})
        self.assertTrue(result["requires_source_refresh"])
        self.assertFalse(result["source_reference_freshness_pass"])
        self.assertFalse(result["publication_ready"])

    def test_game_without_phoenix_opponents_still_stale(self):
        result=evaluate({**BASE,"expected_game_present_in_regular_season_catalog":True,"expected_game_has_phoenix_opponent_rows":False})
        self.assertTrue(result["requires_source_refresh"])
        self.assertFalse(result["publication_ready"])

    def test_reference_present_does_not_authorize_publication(self):
        result=evaluate({**BASE,"expected_game_present_in_regular_season_catalog":True,"expected_game_has_phoenix_opponent_rows":True})
        self.assertFalse(result["requires_source_refresh"])
        self.assertTrue(result["source_reference_freshness_pass"])
        self.assertFalse(result["publication_ready"])

    def test_missing_boolean_fields_fail_closed(self):
        result=evaluate(BASE)
        self.assertTrue(result["requires_source_refresh"])
        self.assertFalse(result["publication_ready"])

if __name__=="__main__":unittest.main()
