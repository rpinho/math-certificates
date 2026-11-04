"""Separately written (same agent), exact finite diagram verifier.

No search modules or floating-point arithmetic. This checks an abstract
braid closure diagram, not a spatial embedding or thickness certificate.
"""
import json,sys,pathlib
class Reject(Exception):pass
def need(cond,code):
    if not cond:raise Reject(code)
def diagram(d):
    need(isinstance(d,dict) and set(d)=={'m','word','repeat','crossings'},'E_SCHEMA')
    m=d['m'];n=d['repeat'];word=d['word'];C=d['crossings']
    need(type(m) is int and type(n) is int and type(C) is int,'E_INTEGER')
    need(m>=2 and n>=1 and isinstance(word,list) and len(word)>0,'E_PARAMETERS')
    for g in word:
        need(type(g) is int,'E_INTEGER')
        need(0<abs(g)<m,'E_GENERATOR_RANGE')
    need(C==len(word)*n,'E_CROSSING_COUNT')
    lanes=list(range(m));visits=[[] for _ in range(m)]
    vertex=0
    for _ in range(n):
        for g in word:
            i=abs(g)-1;left,right=lanes[i:i+2]
            over=1 if g>0 else -1
            visits[left].append((vertex,over));visits[right].append((vertex,-over))
            lanes[i],lanes[i+1]=right,left;vertex+=1
    follow=[None]*m
    for lane,label in enumerate(lanes):follow[label]=lane
    seen=set();components=[]
    for first in range(m):
        if first in seen:continue
        cur=first;component=[]
        while cur not in seen:
            seen.add(cur);component+=visits[cur];cur=follow[cur]
        need(cur==first,'E_CLOSURE_PERMUTATION')
        need(len(component)>0,'E_UNUSED_STRAND')
        components.append(component)
    need(sum(map(len,components))==2*C,'E_EVENT_COVERAGE')
    graph=[set() for _ in range(C)];loops=False
    for comp in components:
        for (v,over),(w,nextover) in zip(comp,comp[1:]+comp[:1]):
            need(over!=nextover,'E_NOT_ALTERNATING')
            if v==w:loops=True
            graph[v].add(w);graph[w].add(v)
    def connected_without(deleted=None):
        nodes=set(range(C))-{deleted}
        if not nodes:return True
        reached={next(iter(nodes))};todo=list(reached)
        while todo:
            v=todo.pop()
            for w in graph[v]:
                if w!=deleted and w not in reached:reached.add(w);todo.append(w)
        return reached==nodes
    need(connected_without(),'E_DISCONNECTED_PROJECTION')
    need(not loops,'E_NUGATORY')
    for v in range(C):need(connected_without(v),'E_NUGATORY')
    return {'m':m,'repeat':n,'crossings':C,'components':len(components),'alternating':True,'no_self_loops_or_cut_vertices':True}
def check(packet):
    need(isinstance(packet,dict) and set(packet)=={'kind','cases'},'E_PACKET_SCHEMA')
    need(packet['kind']=='finite_alternating_braid_diagrams_v1','E_PACKET_KIND')
    need(isinstance(packet['cases'],list) and packet['cases'],'E_EMPTY_CASES')
    return [diagram(d) for d in packet['cases']]
if __name__=='__main__':
    try:
        data=json.loads(pathlib.Path(sys.argv[1]).read_text());rows=check(data)
        print(json.dumps({'verdict':'EXACT_FINITE_DIAGRAMS_PASS_CANDIDATE_UNREFEREED','qualification':'abstract topology only; no spatial geometry or C22b bound','cases':rows},indent=2))
    except Reject as e:print(str(e));sys.exit(1)
