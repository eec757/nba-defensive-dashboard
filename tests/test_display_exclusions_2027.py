import unittest
from scripts.display_exclusions_2027 import EXCLUDED_PLAYER_IDS, visible_player_rows, assert_raw_denominator_preserved

class DisplayExclusionsTests(unittest.TestCase):
    def test_exact_three_ids(self):
        self.assertEqual(EXCLUDED_PLAYER_IDS, {"1643633","1643568","1643813"})

    def test_only_display_rows_filtered(self):
        raw=[{"nba_player_id":"1643633"},{"nba_player_id":"1643568"},{"nba_player_id":"1643813"},{"nba_player_id":"1629057"}]
        self.assertEqual(visible_player_rows(raw),[raw[-1]])
        self.assertEqual(len(raw),4)

    def test_denominator_cannot_use_filtered_rows(self):
        raw=[{"nba_player_id":"1643633"},{"nba_player_id":"1629057"}]
        assert_raw_denominator_preserved(raw,2)
        with self.assertRaises(ValueError):
            assert_raw_denominator_preserved(raw,1)

if __name__=="__main__": unittest.main()
