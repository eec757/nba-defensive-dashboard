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
