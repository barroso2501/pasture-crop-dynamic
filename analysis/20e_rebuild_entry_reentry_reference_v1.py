#!/usr/bin/env python3
"""Reproduce compact controls from the exact previously accepted window-sensitivity data ZIP."""
import argparse,csv,hashlib,io,json,tempfile
from pathlib import Path
from zipfile import ZipFile

FIELDS=['cell_id','GRID_ID','source_batch_id','t0','t1','diagnostic_interval','flow_pas_tmp_ha','stock0_pas_ha','initial_ha','entry_ha','unresolved_ha','initial_pas_stock_ha','entry_pas_stock_ha','unresolved_pas_stock_ha','data_source']

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()

def rebuild(root,source_zip,output_dir):
 root,source_zip,output_dir=map(Path,(root,source_zip,output_dir))
 C=json.loads((root/'config/entry_reentry_full_v1.json').read_text());p=C['reference_provenance']
 if sha(source_zip)!=p['source_archive_sha256']:raise ValueError('Source data ZIP hash differs')
 with tempfile.TemporaryDirectory() as temp:
  directory=Path(temp);cross={};seen=set();n=0
  with ZipFile(source_zip) as z:
   member=p['source_panel_member'];h=hashlib.sha256()
   with z.open(member) as f:
    for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
   if h.hexdigest()!=p['source_panel_sha256']:raise ValueError('Source panel hash differs')
   with (directory/'entry_reentry_full_reference_v1.csv').open('w',encoding='utf-8-sig',newline='') as out,z.open(member) as raw:
    w=csv.DictWriter(out,fieldnames=FIELDS,lineterminator='\n');w.writeheader()
    for row in csv.DictReader(io.TextIOWrapper(raw,encoding='utf-8-sig')):
     if row['baseline_year']!='1985':continue
     key=(row['cell_id'],row['t0'])
     if key in seen:raise ValueError('Duplicate historical reference')
     seen.add(key);n+=1;identity={k:row[k] for k in ['cell_id','GRID_ID','source_batch_id']}
     if row['cell_id'] in cross and cross[row['cell_id']]!=identity:raise ValueError('Inconsistent canonical identity')
     cross[row['cell_id']]=identity;w.writerow({k:row[k] for k in FIELDS})
  if n!=C['expected_rows'] or len(cross)!=C['expected_cells']:raise ValueError('Historical population differs')
  with (directory/'entry_reentry_full_crosswalk_v1.csv').open('w',encoding='utf-8-sig',newline='') as f:
   w=csv.DictWriter(f,fieldnames=['cell_id','GRID_ID','source_batch_id'],lineterminator='\n');w.writeheader();w.writerows(sorted(cross.values(),key=lambda x:int(x['cell_id'])))
  names=['entry_reentry_full_reference_v1.csv','entry_reentry_full_crosswalk_v1.csv']
  for name in names:
   target=output_dir/name
   if target.exists() and target.read_bytes()!=(directory/name).read_bytes():raise ValueError('Refusing to replace different reference: '+name)
  output_dir.mkdir(parents=True,exist_ok=True)
  for name in names:
   if not (output_dir/name).exists():(output_dir/name).write_bytes((directory/name).read_bytes())
  return {'status':'REFERENCE_REPRODUCTION_PASS','cells':len(cross),'rows':n,'native_execution_performed':False,'sha256':{name:sha(directory/name) for name in names}}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--source-data-zip',type=Path,required=True);p.add_argument('--output-dir',type=Path)
 a=p.parse_args();print(json.dumps(rebuild(a.root,a.source_data_zip,a.output_dir or a.root/'config'),indent=2))

if __name__=='__main__':main()
