"""Regression tests for unapproved identity proposal staging."""
import csv
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("proposal", ROOT / "scripts" / "propose_verified_identity_crosswalk.py")
import sys
sys.path.insert(0, str(ROOT / "scripts"))
proposal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proposal)

class ProposalSafetyTests(unittest.TestCase):
    def test_new_candidates_have_no_synthetic_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            old = Path.cwd()
            try:
                os.chdir(directory)
                Path("data").mkdir()
                Path("reports").mkdir()
                fields = ["bref_id","nba_player_id","position","verification_source","verified",
                          "nba_profile_url","bref_profile_url","reviewed_by","reviewed_on","position_source"]
                with open("data/verified_player_ids_2027.csv","w",newline="") as handle:
                    writer=csv.DictWriter(handle,fieldnames=fields)
                    writer.writeheader()
                with open("reports/wikidata_exact_matches_2027.csv","w",newline="") as handle:
                    writer=csv.DictWriter(handle,fieldnames=fields)
                    writer.writeheader()
                    for i in range(362):
                        writer.writerow({
                            "bref_id":f"candidate{i:05d}","nba_player_id":str(1900000+i),
                            "position":"PG","verification_source":f"https://www.wikidata.org/wiki/Q{100000+i}",
                            "verified":"false","nba_profile_url":f"https://www.nba.com/player/{1900000+i}",
                            "bref_profile_url":f"https://www.basketball-reference.com/players/c/candidate{i:05d}.html",
                            "position_source":"https://www.basketball-reference.com/teams/OKC/2027.html"})
                proposal.main()
                with open("reports/proposed_verified_player_ids_2027.csv",newline="") as handle:
                    rows=list(csv.DictReader(handle))
                self.assertEqual(len(rows),362)
                self.assertTrue(all(r["verified"]=="false" and not r["reviewed_by"] and not r["reviewed_on"] for r in rows))
                with open("data/verified_player_ids_2027.csv",newline="") as handle:
                    self.assertEqual(len(list(csv.DictReader(handle))),0)
            finally:
                os.chdir(old)

if __name__=="__main__":
    unittest.main()
