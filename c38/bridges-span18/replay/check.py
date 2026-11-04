#!/usr/bin/env python3
"""Independent exact assembly. --run compiles and reruns all native enumerations.

Without --run, audit this job's native outputs; missing outputs mean PARTIAL.
No producer source, executable, receipt, or external baseline is used.
"""
from fractions import Fraction as Q
import argparse, hashlib, json, pathlib, subprocess, sys, re
sys.set_int_max_str_digits(100000)
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parent
D=1<<96
M=51081913
WIDTHS=[41,62,82,103,125,146,168,189,212,234,257,280,303,327,351,376,401,72]

def load(p):
    return json.loads(p.read_text())
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
    if not ok: raise ValueError(msg)
def rat(x): return Q(str(x))
def file_records(p):
    if not p.exists(): return []
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]
def extract_fork(out):
    """Reuse the independently enumerated h=18 terminal fork of the range-22 sweep."""
    log=out/'frame22_18_30.log'
    if not log.exists():log=out/'frame22_18_30.json.log'
    if not log.exists():return
    matches=re.findall(r'^terminal frame 22 span 18 lo (\d+) hi (\d+)$',log.read_text(),re.M)
    if not matches:return
    require(len(matches)==1,'duplicate terminal-fork receipt')
    lo,hi=matches[0]
    row={'frame_range':22,'span_min':18,'span_max':18,'crossing_cap':5,'M':M,'scale':96,
         'num_lo':lo,'num_hi':hi,'provenance':'h=18 terminal fork in frame22_18_30 sweep'}
    (out/'frame22_18_18.json').write_text(json.dumps(row,sort_keys=True)+'\n')

def run_native(out,threads):
    out.mkdir(parents=True,exist_ok=True)
    for name in ('strip','literal','rectangle','literal_rectangle'):
        args=['nice','-n','10','g++','-O3','-std=c++17']
        if name=='strip': args+=['-fopenmp']
        subprocess.run(args+[str(HERE/(name+'.cpp')),'-o',str(out/name)],check=True)
    def run(name,args,path):
        with (out/path).open('w') as f,(out/(path+'.log')).open('w') as log:
            p=subprocess.Popen(['nice','-n','10',str(out/name),*map(str,args)],stdout=f,stderr=log)
            with (out/'checker.pids').open('a') as ids:ids.write(str(p.pid)+'\n')
            try: require(p.wait()==0,'native execution failed: '+path)
            finally:
                if p.poll() is None:p.terminate();p.wait()
    run('literal',[],'literal.jsonl')
    run('literal_rectangle',[],'literal_rectangle.jsonl')
    for W in range(5):run('rectangle',[W,2,5,5],f'control_frame{W}.json')
    for h,w in enumerate(WIDTHS,1):
        run('strip',[h,w,0 if h==18 else 12,1 if h==18 else 2,threads],f'span{h}.jsonl')
    for W,mn,mx in ((22,18,30),(21,18,30),(23,18,18)):
        run('rectangle',[W,mn,mx,5],f'frame{W}_{mn}_{mx}.json')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--native-dir',type=pathlib.Path,default=ROOT/'pod')
    ap.add_argument('--run',action='store_true')
    ap.add_argument('--threads',type=int,default=28,help='OpenMP threads for a fresh strip run (1–28)')
    ap.add_argument('--output',type=pathlib.Path,default=HERE/'RESULTS.json')
    args=ap.parse_args()
    require(1<=args.threads<=28,'thread limit')
    if args.run:run_native(args.native_dir,args.threads)
    extract_fork(args.native_dir)
    inp=ROOT/'inputs'; hashes={}
    for line in (ROOT/'INPUTS_SHA256SUMS').read_text().splitlines():
        expected,rel=line.split();p=inp/rel
        require(digest(p)==expected,'input hash mismatch: '+rel)
        hashes[str(p.relative_to(ROOT))]=expected
    cert=load(inp/'EXACT_ENCLOSURES.json');packet=load(inp/'frozen/c38_finite_strip/packet.json')
    require(packet['M']==M and packet['L']==18 and packet['terminal_span_mode']=='FINITE_LAST_SPAN_LOWER_ONLY','main parameters')
    require([(s['l'],s['w']) for s in packet['spans']]==list(enumerate(WIDTHS,1)),'widths')
    require(packet['max_degree']==max(h*w for h,w in enumerate(WIDTHS,1))==6817,'degree')
    expected_a=[Q(0)]; expected_b=[Q(0)]; expected_B=[Q(0)]; expected_U=[Q(0)]
    # Recover the uniquely implied bridge enclosures, without adopting them as computations.
    for h,s in enumerate(cert['main_spans'],1):
        require((s['l'],s['w'])==(h,WIDTHS[h-1]),'enclosure family mismatch')
        require(s['mode']==('FULL_WIDTH_CERTIFIED' if h<18 else 'FINITE_LAST_SPAN_LOWER_ONLY'),'enclosure mode')
        a=rat(s['finite_irreducible_lower']); require(a>0,'cannot invert a clamped lower')
        b=a+sum(expected_b[j]*expected_U[h-j] for j in range(1,h))
        expected_a.append(a);expected_B.append(b)
        if h<18:
            beta=rat(s['full_irreducible_upper'])
            u=beta+sum(expected_a[j]*expected_B[h-j] for j in range(1,h))
            expected_b.append(beta);expected_U.append(u)
        else:
            require(s['full_irreducible_upper'] is None,'span18 full upper must be absent')
    sec=cert['secant']; require(sec['M']==M,'secant point'); L17=sum(expected_a[1:18]); L18=expected_a[18]; U=rat(sec['U'])
    require(L17==rat(sec['L17']) and L18==rat(sec['L18']),'secant lower derivation')
    require(L17+L18==rat(packet['P_lower']),'packet sum')
    require(sec['degree18']==18*WIDTHS[17]==1296,'last degree')
    seeds={name:load(inp/f'frozen/{name}/input/seed.json') for name in
           ('c38_span_degree','c38_secant_rescale','c38_disjoint_extension','c38_power_secant')}
    sd=seeds['c38_span_degree']; T=sum(h*WIDTHS[h-1]*expected_a[h] for h in range(1,19))
    require(rat(sd['L'])==L17+L18 and rat(sd['T'])==T,'span-degree seed')
    require(rat(sd['S'])==L17+L18-Q(sd['k'],M)*T,'span-degree arithmetic')
    require(len(sd['spans'])==18,'span-degree coverage')
    for h,item in enumerate(sd['spans'],1):
        require((item['h'],item['w'],item['degree'])==(h,WIDTHS[h-1],h*WIDTHS[h-1]) and rat(item['alpha'])==expected_a[h],'span-degree family')
    for seed in seeds.values():
        require(seed['M']==M and seed['new_M']==M-seed['k'] and rat(seed['mu'])==Q(1<<27,M-seed['k']),'seed grid/reciprocal')
    for name in ('c38_secant_rescale','c38_power_secant'):
        seed=seeds[name]
        require(all(rat(seed[k])==v for k,v in [('L17',L17),('L18',L18),('U',U)]),name+' enclosures')
    p22=cert['point22'];p23=cert['point23']
    for point,path,params in [(p22,'w22_h18_30_c5',(22,18,30)),(p23,'w23_h18_18_c5_parallel',(23,18,18))]:
        search=load(inp/f'frozen/rectangle_point/{path}/input/search.json')
        require(all(point[k]==search[k] for k in ('W','span_min','span_max','crossing_cap','M','S','num_lo','num_hi')),'rectangle search mismatch')
        require((point['W'],point['span_min'],point['span_max'])==params and point['crossing_cap']==5 and point['M']==M and point['S']==96,'rectangle family')
    lo22=Q(int(p22['num_lo']),D);hi23=Q(int(p23['num_hi']),D);e=max(Q(0),lo22-hi23)
    require(e>0 and e==rat(cert['supplement']['extra_lower']),'supplement lower')
    require(lo22==rat(cert['supplement']['lower22']) and hi23==rat(cert['supplement']['upper23']),'supplement endpoints')
    require(cert['supplement']['extra_degree']==30*23==690,'supplement degree')
    dis=seeds['c38_disjoint_extension'];require(e==rat(dis['extra_lower']),'disjoint seed')
    require((dis['extra_span_min'],dis['extra_span_max'],dis['extra_range'],dis['extra_crossing_cap'],dis['extra_degree'])==(19,30,22,5,690),'disjoint family')
    sc=seeds['c38_secant_rescale'];require(sc['upper_point_M']==M+314,'secant upper point');j=sc['k'];slope=(U-L17)/314+Q(1296,M)*L18
    require(rat(sc['slope'])==slope and rat(sc['S'])==L17+L18-j*slope,'secant linear arithmetic')
    j=dis['k'];require(rat(dis['S'])==L17+L18+e-j*(slope+Q(690,M)*e),'disjoint linear arithmetic')
    require(lo22==rat(dis['lower22']) and hi23==rat(dis['upper23']),'disjoint endpoints')
    def S(k):
        r=Q(M-k,M)
        return (1+Q(k,314))*L17-Q(k,314)*U+r**1296*L18+r**690*e
    power=seeds['c38_power_secant']; k=1353;value=Q(1<<27,M-k);s=S(k)
    require(value==Q(8388608,3192535),'reciprocal')
    require(s==rat(cert['power']['S'])==rat(power['S']),'full frozen S rational')
    require(k==cert['power']['k']==power['k'] and value==rat(power['mu'])==rat(cert['power']['mu']) and cert['power']['new_M']==M-k,'power parameters')
    require(s>=1 and S(k+1)<1,'power exact inequality')
    require(value>Q(1051,400),'target comparison')
    result={'status':'PARTIAL','value':str(value),'input_hashes':hashes,
            'certificate_arithmetic':{'S_equal':True,'S_ge_1':True,'next_S_lt_1':True,
                                      'S_minus_1':str(s-1)},'native_comparisons':[],'missing':[]}
    # All full-point forward and tail values are regenerated by our component graph.
    records={}
    for h,w in enumerate(WIDTHS,1):
        rows=file_records(args.native_dir/f'span{h}.jsonl')
        for row in rows:
            require(row['span']==h and row['width']==w and row['scale']==96,'native strip parameters')
            require(row['M'] in (M,M+314),'native point')
            require((h,row['M']) not in records,'duplicate native record')
            require(row['states']>0 and row['edges']>0,'empty native graph')
            require(row['tail_bits']==(0 if h==18 else 12),'tail precision')
            require(h==18 or row['cycles']>0,'no stabilized upper potential')
            records[h,row['M']]=row
        for point in ([M] if h==18 else [M,M+314]):
            if (h,point) not in records:result['missing'].append(f'span {h}, M={point}')
    fresh={}
    for point in (M,M+314):
        aa=[Q(0)];bb=[Q(0)];lower=[Q(0)];upper=[Q(0)]
        for h in range(1,19 if point==M else 18):
            if (h,point) not in records:break
            row=records[h,point];bl=Q(int(row['num_lo']),D);bh=Q(int(row['num_hi']),D);tail=Q(int(row['num_tail']),D)
            require(0<=bl<=bh and tail>=0,'invalid native interval')
            a=max(Q(0),bl-sum(bb[j]*upper[h-j] for j in range(1,h)))
            lower.append(bl);aa.append(a)
            if h<18:
                up=bh+tail;beta=up-sum(aa[j]*lower[h-j] for j in range(1,h))
                require(0<=a<=beta,'native renewal interval');upper.append(up);bb.append(beta)
            else:require(tail==0,'unused span18 tail marker')
            if point==M:
                require(bl==expected_B[h],f'span {h} finite bridge lower mismatch')
                require(a==expected_a[h],f'span {h} irreducible lower mismatch')
                if h<18:require(upper[h]==expected_U[h] and bb[h]==expected_b[h],f'span {h} full upper mismatch')
                else:require(bh==rat(cert['main_spans'][-1]['finite_irreducible_upper']),'span18 finite upper mismatch')
            result['native_comparisons'].append({'span':h,'M':point,'states':row['states'],'comparison':'exact per-span main bounds' if point==M else 'included in auxiliary upper-sum comparison'})
        fresh[point]=(aa,bb)
    if len(fresh[M+314][1])==18:
        require(sum(fresh[M+314][1][1:])==U,'auxiliary point upper sum mismatch')
        result['auxiliary_upper_exact_match']=True
    normalized_points={}
    for W,mn,mx,frozen in ((22,18,30,p22),(23,18,18,p23)):
        pair=[]
        for frame in (W,W-1):
            path=args.native_dir/f'frame{frame}_{mn}_{mx}.json'
            if not path.exists() or not path.read_text().strip():
                result['missing'].append(path.name);break
            row=load(path);require((row['frame_range'],row['span_min'],row['span_max'],row['crossing_cap'],row['M'],row['scale'])==(frame,mn,mx,5,M,96),'native rectangle parameters');pair.append(row)
        if len(pair)==2:
            alo,ahi=int(pair[0]['num_lo']),int(pair[0]['num_hi']);blo,bhi=int(pair[1]['num_lo']),int(pair[1]['num_hi'])
            require(0<=alo<=ahi and 0<=blo<=bhi,'frame interval')
            lo=max(0,alo-bhi);hi=ahi-blo;normalized_points[W]=(lo,hi)
            require(lo==int(frozen['num_lo']) and hi==int(frozen['num_hi']),f'rectangle range {W} endpoints mismatch')
            result['native_comparisons'].append({'rectangle_range':W,'span_min':mn,'span_max':mx,'exact_match':True})
    literal=file_records(args.native_dir/'literal.jsonl')
    require(len(literal)==36 and all(x['match'] for x in literal),'missing literal controls')
    require({(x['span'],x['width']) for x in literal}=={(h,w) for h in range(1,13) for w in range(1,4)},'literal coverage')
    result['literal_controls']=36
    literal_rect=file_records(args.native_dir/'literal_rectangle.jsonl')
    if len(literal_rect)!=5:result['missing'].append('literal_rectangle.jsonl')
    else:
        for row in literal_rect:
            W=row['frame_range'];p=args.native_dir/f'control_frame{W}.json'
            if not p.exists():result['missing'].append(p.name);continue
            got=load(p);x=Q(M,1<<27);v=sum(int(c)*x**n for n,c in enumerate(row['coefficients']))
            require(Q(int(got['num_lo']),D)<=v<=Q(int(got['num_hi']),D),'rectangle literal enclosure')
        result['rectangle_literal_controls']=5
    if not result['missing']:
        la=sum(fresh[M][0][1:18]);lg=fresh[M][0][18];uc=sum(fresh[M+314][1][1:]);r=Q(M-k,M)
        fresh_e=max(Q(0),Q(normalized_points[22][0]-normalized_points[23][1],D))
        require(fresh_e==e,'independent supplemental lower')
        recomputed=(1+Q(k,314))*la-Q(k,314)*uc+r**1296*lg+r**690*fresh_e
        require(recomputed==s and recomputed>=1,'independent final assembly')
        result['independent_S_equal']=True;result['status']='PASS'
    result['native_output_hashes']={p.name:digest(p) for p in sorted(args.native_dir.glob('*.json*')) if p.name.startswith(('span','frame','literal','control_frame')) and p.read_text().strip()}
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ('status','value','missing')},indent=2))
    return 0 if result['status']=='PASS' else 2
if __name__=='__main__':
    try:sys.exit(main())
    except Exception as exc:
        print('FAIL:',exc,file=sys.stderr);sys.exit(1)
