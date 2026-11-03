"""Aggregate an actual completed fresh replay with the unchanged checker."""
import argparse,json,pathlib
from verify_c57c_forest import aggregate,require
parser=argparse.ArgumentParser();parser.add_argument('directory');args=parser.parse_args()
root=pathlib.Path(__file__).resolve().parent
work=root/args.directory
require(not pathlib.Path(args.directory).is_absolute() and '..' not in pathlib.Path(args.directory).parts,'relative replay path required')
queue=json.loads((work/'QUEUE.json').read_text())
require(all(row['status']=='done' for row in queue['jobs']),'fresh replay queue incomplete')
receipts=[root/row['receipt'] for row in queue['jobs']]
aggregate(root/'C57_FOREST_V2.json',receipts,work/'complete_verification.json')
