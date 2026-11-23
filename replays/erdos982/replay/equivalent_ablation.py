"""Check that omitting one of two identical families preserves the exact CNF."""
from collections import Counter
import json
from pathlib import Path
import sys

from run_case import build

reference = Path(sys.argv[1]).resolve()
source = json.loads((reference/"result.json").read_text())
for name in sys.argv[2:]:
    folder = reference.with_name(reference.name+"-no-"+name)
    folder.mkdir()
    _, families_file, digest = build(folder, source["n"], source["k"],
                                     [name], source.get("fan",False))
    assert digest == source["cnf_sha256"]
    families = dict(line.split("\t") for line in families_file.read_text().splitlines())
    counts = Counter()
    with (reference/"core_families.tsv").open() as inputs, \
            (folder/"core_families.tsv").open("w") as output:
        output.write(next(inputs))
        for line in inputs:
            cid, _ = line.split("\t")
            names = families[cid]
            print(cid,names,sep="\t",file=output)
            counts.update(names.split(","))
    result = dict(source, omitted=[name], core_families=counts, proof_case=reference.name)
    (folder/"result.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(folder.name, "both encoders match certified input", digest)
