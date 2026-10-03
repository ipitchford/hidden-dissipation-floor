#!/usr/bin/env python3
"""Read-only manifest-bound replay. Run from any directory."""
import hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def check_manifest():
    lines=(ROOT/'SHA256SUMS').read_text().splitlines()
    for line in lines:
        digest,name=line.split('  ',1)
        if sha(ROOT/name)!=digest: raise RuntimeError('Manifest mismatch: '+name)
    return {n:sha(ROOT/n) for _,n in (x.split('  ',1) for x in lines)}
def main():
    before=check_manifest()
    with tempfile.TemporaryDirectory(prefix='hidden-dissipation-replay-') as d:
        target=Path(d)/'evidence'; shutil.copytree(ROOT/'evidence',target,ignore=shutil.ignore_patterns('__pycache__'))
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
        for opt in [[],['-O']]:
            for stem in ['exact','extensions','symbolic','numerical']:
                subprocess.run([sys.executable,*opt,str(target/('verify_'+stem+'.py'))],check=True,env=env)
            for name in ['exact_results.json','extension_results.json']:
                if json.loads((target/name).read_text())!=json.loads((ROOT/'evidence'/name).read_text()):
                    raise RuntimeError('Exact output mismatch: '+name)
            for name in ['symbolic_results.json','numerical_results.json']:
                if json.loads((target/name).read_text())['status']!='PASS':
                    raise RuntimeError('Diagnostic failed: '+name)
    if check_manifest()!=before: raise RuntimeError('Released bytes changed')
    print('PASS: manifest-bound read-only replay; normal and optimized checks; exact result parity')
if __name__=='__main__':main()
