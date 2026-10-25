"""Offline safety tests for Wikidata evidence staging."""
import unittest
from scripts.stage_wikidata_exact_evidence import classify

def candidate(nba="123",bref="smithjo01"):
    return {"priority":"1","team":"OKC","roster_name":"Example Player",
            "nba_player_id":nba,"bref_id":bref,"position":"PG",
            "regular_season_games":"2",
            "nba_profile_url":"https://www.nba.com/player/"+nba,
            "bref_profile_url":"https://www.basketball-reference.com/players/s/"+bref+".html",
            "season_position_source":"https://www.basketball-reference.com/teams/OKC/2027.html"}

def binding(nba="123",bref="smithjo01",item="Q123"):
    result={"nba":{"value":nba},"item":{"value":"https://www.wikidata.org/entity/"+item}}
    if bref is not None:
        result["bref"]={"value":bref}
    return result

class EvidenceStagingTests(unittest.TestCase):
    def test_exact_pair_stages_but_never_approves(self):
        matches,exceptions=classify([candidate()],[binding()])
        self.assertEqual(len(matches),1)
        self.assertEqual(exceptions,[])
        self.assertEqual(matches[0]["verified"],"false")
        self.assertEqual(matches[0]["verification_source"],"https://www.wikidata.org/entity/Q123")

    def test_mismatch_remains_exception(self):
        matches,exceptions=classify([candidate()],[binding(bref="wrong01")])
        self.assertEqual(matches,[])
        self.assertEqual(exceptions[0]["reason"],"bref_id_mismatch_or_ambiguous")

    def test_missing_bref_remains_exception(self):
        matches,exceptions=classify([candidate()],[binding(bref=None)])
        self.assertEqual(matches,[])
        self.assertEqual(exceptions[0]["reason"],"missing_bref_id")

    def test_ambiguous_entities_are_not_approved(self):
        matches,exceptions=classify([candidate()],[binding(),binding(item="Q456")])
        self.assertEqual(matches,[])
        self.assertEqual(exceptions[0]["reason"],"ambiguous_wikidata_items")

    def test_no_wikidata_match(self):
        matches,exceptions=classify([candidate()],[])
        self.assertEqual(matches,[])
        self.assertEqual(exceptions[0]["reason"],"missing_wikidata_nba_id")

if __name__=="__main__":
    unittest.main()
