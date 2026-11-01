import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from classify_roster_position_2027 import classify_roster_position

class PositionClassifierTests(unittest.TestCase):
    def test_exact_positions(self):
        for p in ("PG","SG","SF","PF","C"):
            self.assertEqual(classify_roster_position(p)["position"],p)
            self.assertEqual(classify_roster_position(p)["status"],"exact")
    def test_broad_and_hybrid_never_inferred(self):
        for p in ("G","F","F-C","C-F","G-F","F-G","Forward","Forward-Center","G/F","F/C"):
            self.assertIsNone(classify_roster_position(p)["position"])
            self.assertEqual(classify_roster_position(p)["status"],"ambiguous")
    def test_unknown_fails_closed(self):
        for p in ("","wing","PF/ C",None):
            self.assertIsNone(classify_roster_position(p)["position"])
            self.assertEqual(classify_roster_position(p)["status"],"unknown")

if __name__=="__main__":
    unittest.main()
