#!/usr/bin/env python3
"""Restore the exact accepted large CSV from its versioned gzip copy."""
from pathlib import Path
import argparse, gzip, hashlib, json, os, shutil, tempfile

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    root=ap.parse_args().root.resolve()
    manifest=json.loads((root/'config/entry_reentry_github_packaging_v1.json').read_text())
    for item in manifest['compressed_files']:
        source=root/item['compressed_path'];target=root/item['restored_path']
        for p in [source,target]:
            if not p.resolve().is_relative_to(root):raise ValueError('Path outside package')
        if sha(source)!=item['compressed_sha256']:raise ValueError('Compressed SHA256 differs: '+str(source))
        if target.exists():
            if target.stat().st_size!=item['restored_bytes'] or sha(target)!=item['restored_sha256']:
                raise ValueError('Refusing to overwrite a differing file: '+str(target))
            print('ALREADY VERIFIED:',item['restored_path']);continue
        target.parent.mkdir(parents=True,exist_ok=True)
        fd,tmpname=tempfile.mkstemp(prefix='restore_',suffix='.tmp',dir=target.parent)
        tmp=Path(tmpname)
        try:
            with os.fdopen(fd,'wb') as out,gzip.open(source,'rb') as src:shutil.copyfileobj(src,out)
            if tmp.stat().st_size!=item['restored_bytes'] or sha(tmp)!=item['restored_sha256']:
                raise ValueError('Restored SHA256/size differs')
            os.replace(tmp,target)
        finally:tmp.unlink(missing_ok=True)
        print('RESTORED AND VERIFIED:',item['restored_path'])

if __name__=='__main__':main()
