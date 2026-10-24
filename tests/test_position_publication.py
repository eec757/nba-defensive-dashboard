"""Offline safety tests: never publish from provisional player identities."""
import csv
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "publish_verified_positions.py"
spec = importlib.util.spec_from_file_location("position_publisher", SCRIPT)
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)

class PublicationSafetyTests(unittest.TestCase):
    def test_two_primary_urls_still_require_human_review(self):
        row = {
            "nba_player_id": "1631096", "bref_id": "holmgch01",
            "nba_profile_url": "https://www.nba.com/player/1631096/chet-holmgren",
            "bref_profile_url": "https://www.basketball-reference.com/players/h/holmgch01.html",
            "reviewed_by": "", "reviewed_on": ""
        }
        with self.assertRaisesRegex(ValueError, "reviewer"):
            publisher.validate_independent_evidence(row)
        row["reviewed_by"] = "human-reviewer"
        row["reviewed_on"] = "2026-10-24"
        self.assertTrue(publisher.validate_independent_evidence(row))

    def test_invalid_or_future_review_dates_rejected(self):
        row = {
            "nba_player_id": "1631096", "bref_id": "holmgch01",
            "nba_profile_url": "https://www.nba.com/player/1631096/chet-holmgren",
            "bref_profile_url": "https://www.basketball-reference.com/players/h/holmgch01.html",
            "reviewed_by": "human-reviewer", "reviewed_on": "not-a-date"
        }
        with self.assertRaisesRegex(ValueError, "valid ISO"):
            publisher.validate_independent_evidence(row)
        row["reviewed_on"] = "2099-01-01"
        with self.assertRaisesRegex(ValueError, "future"):
            publisher.validate_independent_evidence(row)

    def test_mismatched_primary_profile_ids_rejected(self):
        row = {
            "nba_player_id": "1631096", "bref_id": "holmgch01",
            "nba_profile_url": "https://www.nba.com/player/1631114/jalen-williams",
            "bref_profile_url": "https://www.basketball-reference.com/players/h/holmgch01.html",
            "reviewed_by": "human-reviewer", "reviewed_on": "2026-10-24"
        }
        with self.assertRaisesRegex(ValueError, "NBA player profile"):
            publisher.validate_independent_evidence(row)

    def test_opponent_aggregation_uses_defending_team_and_game_count(self):
        okc = publisher.TEAM_IDS["OKC"]
        bos = publisher.TEAM_IDS["BOS"]
        rows = [
            ("100", okc, "g1", 20, 5, 4, 8, 16, 2, 6),
            ("101", okc, "g1", 10, 3, 2, 4, 8, 1, 3),
            ("100", okc, "g2", 16, 7, 6, 6, 12, 2, 4),
            ("100", bos, "g3", 22, 8, 3, 9, 18, 3, 8),
        ]
        totals, games, covered, all_rows = publisher.summarize_position_rows(
            rows, {"100": "PG", "101": "SG"}, publisher.TEAM_IDS
        )
        self.assertEqual(len(games["OKC"]), 2)
        self.assertEqual(len(games["BOS"]), 1)
        self.assertEqual((covered["OKC"], all_rows["OKC"]), (3, 3))
        self.assertEqual(totals["OKC", "PG"][1], 36)
        self.assertEqual(totals["OKC", "SG"][1], 10)
        self.assertEqual(publisher.position_metrics(totals["OKC", "PG"], 2)["points_allowed"], 18.0)
        self.assertEqual(publisher.position_metrics(totals["BOS", "PG"], 1)["points_allowed"], 22.0)

    def test_opponent_aggregation_rejects_unknown_team(self):
        rows = [("100", "999", "g1", 2, 1, 0, 1, 2, 0, 0)]
        with self.assertRaisesRegex(ValueError, "Unknown opponent team"):
            publisher.summarize_position_rows(rows, {"100": "PG"}, publisher.TEAM_IDS)

    def test_position_metrics_use_all_defending_games(self):
        # Two games, with three verified opponent player appearances.
        # Totals: rows, PTS, REB, AST, FGM, FGA, 3PM, 3PA.
        result = publisher.position_metrics([3, 50, 20, 12, 18, 40, 6, 15], 2)
        self.assertEqual(result, {
            "points_allowed": 25.0,
            "rebounds_allowed": 10.0,
            "assists_allowed": 6.0,
            "fg_pct": 45.0,
            "three_pct": 40.0,
        })

    def test_position_metrics_handle_no_shot_attempts(self):
        result = publisher.position_metrics([1, 0, 3, 2, 0, 0, 0, 0], 1)
        self.assertIsNone(result["fg_pct"])
        self.assertIsNone(result["three_pct"])

    def test_position_metrics_reject_impossible_shooting(self):
        with self.assertRaisesRegex(ValueError, "Inconsistent shooting"):
            publisher.position_metrics([1, 20, 2, 1, 11, 10, 2, 4], 1)

    def test_canonical_team_id_mapping(self):
        self.assertEqual(len(publisher.TEAM_IDS), 30)
        self.assertEqual(len(set(publisher.TEAM_IDS.values())), 30)
        expected = {
            "ATL": "1610612737", "BOS": "1610612738",
            "BRK": "1610612751", "CHI": "1610612741",
            "CHO": "1610612766", "CLE": "1610612739",
            "DAL": "1610612742", "DEN": "1610612743",
            "DET": "1610612765", "GSW": "1610612744",
            "HOU": "1610612745", "IND": "1610612754",
            "LAC": "1610612746", "LAL": "1610612747",
            "MEM": "1610612763", "MIA": "1610612748",
            "MIL": "1610612749", "MIN": "1610612750",
            "NOP": "1610612740", "NYK": "1610612752",
            "OKC": "1610612760", "ORL": "1610612753",
            "PHI": "1610612755", "PHO": "1610612756",
            "POR": "1610612757", "SAC": "1610612758",
            "SAS": "1610612759", "TOR": "1610612761",
            "UTA": "1610612762", "WAS": "1610612764",
        }
        for abbreviation, team_id in expected.items():
            self.assertEqual(publisher.TEAM_IDS.get(abbreviation), team_id)

    def test_unverified_rows_cannot_publish(self):
        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            try:
                os.chdir(directory)
                Path("data").mkdir()
                with Path("data/verified_player_ids_2027.csv").open("w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["bref_id", "nba_player_id", "position", "verification_source", "verified"])
                    writer.writerow(["wilsoca01", "1643410", "PF", "https://www.nba.com/player/1643410", "false"])
                publisher.CROSSWALK = Path("data/verified_player_ids_2027.csv")
                publisher.OUTPUT = Path("data/position_defense_2027.json")
                publisher.main()
                self.assertFalse(publisher.OUTPUT.exists())
            finally:
                os.chdir(previous)

    def test_single_provider_profile_is_not_independent_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            try:
                os.chdir(directory)
                Path("data").mkdir()
                Path("data/verified_player_ids_2027.csv").write_text(
                    "bref_id,nba_player_id,position,verification_source,verified\n"
                    "wilsoca01,1643410,PF,https://www.nba.com/player/1643410,true\n",
                    encoding="utf-8")
                publisher.CROSSWALK = Path("data/verified_player_ids_2027.csv")
                publisher.OUTPUT = Path("data/position_defense_2027.json")
                with self.assertRaisesRegex(ValueError, "Single-provider"):
                    publisher.main()
                self.assertFalse(publisher.OUTPUT.exists())
            finally:
                os.chdir(previous)

    def test_invalid_verified_identity_rejected_before_database_access(self):
        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            try:
                os.chdir(directory)
                Path("data").mkdir()
                Path("data/verified_player_ids_2027.csv").write_text(
                    "bref_id,nba_player_id,position,verification_source,verified\n"
                    "wilsoca01,not-an-id,PF,https://example.org/evidence,true\n",
                    encoding="utf-8")
                publisher.CROSSWALK = Path("data/verified_player_ids_2027.csv")
                publisher.OUTPUT = Path("data/position_defense_2027.json")
                with self.assertRaises(ValueError):
                    publisher.main()
                self.assertFalse(publisher.OUTPUT.exists())
            finally:
                os.chdir(previous)

if __name__ == "__main__":
    unittest.main()
