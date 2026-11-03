"""Create an empty, separate replay queue from the frozen exact range plan.
The historical receipts are never copied into this new replay directory.
"""
import argparse,json,pathlib
parser=argparse.ArgumentParser();parser.add_argument('directory');args=parser.parse_args()
root=pathlib.Path(__file__).resolve().parent
work=root/args.directory
assert not pathlib.Path(args.directory).is_absolute() and '..' not in pathlib.Path(args.directory).parts
assert not work.exists(),'choose a new replay directory'
plan=json.loads((root/'RANGE_PLAN.json').read_text())
work.mkdir();(work/'receipts').mkdir();(work/'logs').mkdir()
jobs=[]
for item in plan['jobs']:
    row=dict(item)
    row.update(status='pending',receipt=str(pathlib.Path(args.directory)/'receipts'/(row['id']+'.json')),log=str(pathlib.Path(args.directory)/'logs'/(row['id']+'.log')))
    jobs.append(row)
queue=work/'QUEUE.json';queue.write_text(json.dumps(dict(jobs=jobs),indent=2)+'\n')
print('Fresh queue:',queue.relative_to(root),';',len(jobs),'ranges; no prior receipts used')
