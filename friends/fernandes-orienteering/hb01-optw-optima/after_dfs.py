from pathlib import Path
import time,subprocess,json
root=Path('/workspace/ref_hugo_HB01')
while True:
    try:
        if len(json.load(open(root/'dfs.json')))==15:break
    except (FileNotFoundError,json.JSONDecodeError):pass
    time.sleep(2)
subprocess.run(['nice','-n','10','g++','-std=c++17','-O3','greedy.cpp','-o','greedy'],cwd=root,check=True)
subprocess.run(['nice','-n','10','python3','extra_audit.py'],cwd=root,check=True)
