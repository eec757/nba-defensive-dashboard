"""Fail-closed classification of season-roster position labels.

Never infer a five-position primary role from broad G/F or hybrid labels.
"""
EXACT=frozenset(("PG","SG","SF","PF","C"))
AMBIGUOUS=frozenset(("G","F","G-F","F-G","F-C","C-F","G/F","F/G","F/C","C/F","GUARD","FORWARD","FORWARD-CENTER","GUARD-FORWARD"))

def classify_roster_position(raw):
    label=str(raw or "").strip().upper().replace("–","-").replace("—","-")
    if label in EXACT:
        return {"raw":str(raw or ""),"position":label,"status":"exact"}
    if label in AMBIGUOUS:
        return {"raw":str(raw or ""),"position":None,"status":"ambiguous"}
    return {"raw":str(raw or ""),"position":None,"status":"unknown"}

if __name__=="__main__":
    import json
    for value in ("PG","SG","SF","PF","C","G","F","F-C","G-F","Forward","Forward-Center",""):
        print(json.dumps(classify_roster_position(value)))
