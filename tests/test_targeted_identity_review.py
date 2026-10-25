"""Safety tests for the read-only targeted identity review validator."""
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "targeted_review", Path(__file__).resolve().parents[1] / "scripts" / "validate_targeted_identity_review.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def row(pid="1641724", decision="pending", bref="", position="", url="", notes=""):
    return {"nba_player_id": pid, "review_decision": decision,
            "verified_bref_id": bref, "verified_2026_27_position": position,
            "evidence_url": url, "review_notes": notes}

class TargetedReviewSafetyTests(unittest.TestCase):
    def test_pending_is_not_automatically_approved(self):
        self.assertEqual(module.validate([row()], {"1641724"}), [])

    def test_unverified_evidence_rejected(self):
        problems = module.validate([row(decision="verified")], {"1641724"})
        self.assertTrue(problems)

    def test_disallowed_evidence_host_rejected(self):
        problems = module.validate([row(decision="verified", bref="example01",
            position="PG", url="https://www.nba.com/player/1641724", notes="checked")], {"1641724"})
        self.assertTrue(any("independent HTTPS" in p["reason"] for p in problems))

    def test_complete_fields_only_pass_syntax_checks(self):
        self.assertEqual(module.validate([row(decision="verified", bref="example01",
            position="PG", url="https://www.wikidata.org/wiki/Q123", notes="reviewed")], {"1641724"}), [])

    def test_missing_player_rejected(self):
        self.assertTrue(module.validate([row()], {"1641724", "1643515"}))

    def test_duplicate_player_rejected(self):
        self.assertTrue(module.validate([row(), row()], {"1641724"}))

if __name__ == "__main__":
    unittest.main()
