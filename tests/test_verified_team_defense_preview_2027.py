import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from build_verified_team_defense_preview_2027 import calculate_team_preview

class TeamPreviewTests(unittest.TestCase):
    def test_unknown_rows_remain_denominator_and_do_not_contribute(self):
        teams={"AAA":"1"}
        rows=[("verified","1","g1",10,4,2),("unknown","1","g1",99,50,30)]
        result=calculate_team_preview(rows,{"verified"},teams)
        self.assertEqual(result["leaguewide_all_rows"],2)
        self.assertEqual(result["leaguewide_covered_rows"],1)
        self.assertFalse(result["leaguewide_gate_pass"])
        self.assertEqual(result["teams"]["AAA"]["unknown_player_game_rows"],1)
        self.assertIsNone(result["teams"]["AAA"]["verified_only_metrics"])
    def test_verified_only_passes_and_aggregates(self):
        result=calculate_team_preview([("p","1","g1",10,4,2)],{"p"},{"AAA":"1"})
        self.assertTrue(result["leaguewide_gate_pass"])
        self.assertEqual(result["teams"]["AAA"]["verified_only_metrics"]["points_allowed_per_game"],10)
        self.assertFalse(result["published"])
    def test_unrecognized_team_fails_closed(self):
        with self.assertRaises(ValueError):
            calculate_team_preview([("p","999","g",1,1,1)],{"p"},{"AAA":"1"})

if __name__=="__main__":unittest.main()
