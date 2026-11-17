# run_guard.py LOG -- cmd...  : nice 10, /usr/bin/time -l, kill if RSS of the process tree > 7.6 GB
import sys, subprocess, time, os, signal
log=sys.argv[1]; cmd=sys.argv[3:]; LIM=7.6e9
t0=time.time(); f=open(log,'w')
p=subprocess.Popen(['nice','-n','10','/usr/bin/time','-l']+cmd,stdout=f,stderr=subprocess.STDOUT)
peak=0; killed=False
while p.poll() is None:
    try:
        o=subprocess.run(['ps','-axo','pid=,ppid=,rss='],capture_output=True,text=True).stdout.split()
        rows=[(int(o[i]),int(o[i+1]),int(o[i+2])*1024) for i in range(0,len(o),3)]
        kids={p.pid}; ch=True
        while ch:
            ch=False
            for a,b,r in rows:
                if b in kids and a not in kids: kids.add(a); ch=True
        rss=sum(r for a,b,r in rows if a in kids); peak=max(peak,rss)
        if rss>LIM and not killed:
            killed=True
            for a in kids:
                try: os.kill(a,signal.SIGKILL)
                except Exception: pass
    except Exception: pass
    time.sleep(0.5)
f.close()
with open(log,'a') as f: f.write(f"\n# guard: exit={p.returncode} wall={time.time()-t0:.1f}s sampled_peak_rss={peak} killed_by_guard={killed}\n")
print(f"{' '.join(cmd)[:120]} -> exit={p.returncode} wall={time.time()-t0:.1f}s peak={peak/1e9:.2f}GB killed={killed}")
