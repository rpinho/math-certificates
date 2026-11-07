"""Skeptic's controls, derived directly from the official TOPTW rules."""
from prepare import load,distances,replay
from ortools.sat.python import cp_model
from pathlib import Path
import time,json,random,copy

p=load('official_pr11.txt');d=distances(p);n=len(p)
def feasible(route):
    t=p[0][4]
    for i,j in zip(route,route[1:]):
        t=max(p[j][4],t+p[i][2]+d[i][j])
        if t>p[j][5]:return False
    return True

# A single deterministic greedy insertion run: best prize / added travel,
# considering every unvisited customer at every insertion position.
routes=[[0,0] for _ in range(3)];left=set(range(1,n))
while True:
    options=[]
    for j in sorted(left):
        for k,r in enumerate(routes):
            for h in range(1,len(r)):
                rr=r[:h]+[j]+r[h:]
                if feasible(rr):
                    cost=d[r[h-1]][j]+d[j][r[h]]-d[r[h-1]][r[h]]+p[j][2]
                    # integer cross product comparison performed below
                    options.append((p[j][3],max(cost,1),j,k,h))
    if not options:break
    best=options[0]
    for q in options[1:]:
        if q[0]*best[1]>best[0]*q[1]:best=q
    _,_,j,k,h=best;routes[k].insert(h,j);left.remove(j)
insertion=replay(p,routes);insertion['routes']=routes

# Fresh all-customers feasibility model. Each vehicle's circuit has loops
# exactly for customers it skips. Every customer belongs to exactly one circuit.
model=cp_model.CpModel();assigned=[]
for k in range(3):
    visit=[None]+[model.new_bool_var(f'v{k}_{i}') for i in range(1,n)]
    assigned.append(visit)
    t=[None]+[model.new_int_var(p[i][4],p[i][5],f't{k}_{i}') for i in range(1,n)]
    arcs=[]
    empty=model.new_bool_var(f'empty{k}');arcs.append((0,0,empty))
    for i in range(1,n):arcs.append((i,i,visit[i].Not()))
    for i in range(n):
        for j in range(n):
            if i==j:continue
            if j==0:
                if p[i][4]+p[i][2]+d[i][0]>p[0][5]:continue
            elif i==0:
                if max(p[j][4],p[0][4]+d[0][j])>p[j][5]:continue
            elif p[i][4]+p[i][2]+d[i][j]>p[j][5]:continue
            x=model.new_bool_var(f'x{k}_{i}_{j}');arcs.append((i,j,x))
            if j==0:model.add(t[i]+p[i][2]+d[i][0]<=p[0][5]).only_enforce_if(x)
            elif i==0:model.add(t[j]>=p[0][4]+d[0][j]).only_enforce_if(x)
            else:model.add(t[j]>=t[i]+p[i][2]+d[i][j]).only_enforce_if(x)
    model.add_circuit(arcs)
for i in range(1,n):model.add_exactly_one(assigned[k][i] for k in range(3))
solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
solver.parameters.max_time_in_seconds=120;solver.parameters.random_seed=613
st=time.monotonic();status=solver.solve(model)
result={'insertion':insertion,'mandatory_all_customers':{'status':solver.status_name(status),'wall_seconds':time.monotonic()-st,'response':solver.response_stats()},'note':'CP status is a corroborating control, not the exact certificate.'}

# Route validator attacks.
base=json.loads(Path('input/primal.json').read_text());attacks={}
bad=copy.deepcopy(base['routes']);bad.append([0,0]);attacks['fleet']=bad
bad=copy.deepcopy(base['routes']);bad[1].insert(1,bad[0][1]);attacks['repeat']=bad
bad=copy.deepcopy(base['routes']);bad[0][1]=99;attacks['range']=bad
bad=copy.deepcopy(base['routes']);bad[0][-1]=1;attacks['depot']=bad
bad=copy.deepcopy(base['routes']);bad[0]=[0,19,46,19,0];attacks['window']=bad
rejected=[]
for name,r in attacks.items():
    try:replay(p,r)
    except (AssertionError,IndexError):rejected.append(name)
assert len(rejected)==len(attacks)
result['rejected_primal_attacks']=rejected
Path('controls_receipt.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
