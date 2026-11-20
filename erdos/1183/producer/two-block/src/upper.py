"""Replay the earlier scalar rank witness and exclusion trees in this packet."""
import json
from pathlib import Path
from rank_tree_replay import witness,tree
p=Path("data/upper")
record=json.loads((p/"upper_n23.json").read_text())
word="001001110010110001101101"
assert record["word"]==word and record["n"]==23 and len(record["colours"])==2
for c,row in enumerate(record["colours"]):
    assert row["colour"]==c and len(row["witness"])==row["maximum"]==14
    witness(23,word,c,14,row["witness"])
    nodes=tree(p/Path(row["proof"]).name,word,c,15)
    print("rank word",word,"colour",c,"maximum",14,"no-at-15 nodes",nodes)
