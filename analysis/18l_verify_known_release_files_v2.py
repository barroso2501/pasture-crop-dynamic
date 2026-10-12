"""Verify the partial known-product inventory; never declare a full DOI release.

Read-only byte/row checks. Missing files remain explicit. Independent Stage 0,
licensing, metadata, claim allocation and deposition are outside this tool.
"""
from pathlib import Path
import argparse,csv,hashlib,json

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def run(inventory,repo_root,data_root):
    with inventory.open(encoding='utf-8-sig',newline='') as f:items=list(csv.DictReader(f))
    results=[]
    for rec in items:
        rel=Path(rec['source_relative_path'])
        if rel.is_absolute() or '..' in rel.parts:raise ValueError('Nonportable source path')
        base=repo_root if rec['source_root']=='repo_root' else data_root
        path=base/rel
        out={'product':rec['product'],'source_relative_path':rel.as_posix(),
             'source_root':rec['source_root'],'expected_sha256':rec['sha256'],
             'expected_rows':rec['expected_rows'] or None,'status':'MISSING'}
        if path.is_file():
            out['bytes']=path.stat().st_size;out['actual_sha256']=digest(path)
            if out['actual_sha256']!=out['expected_sha256']:out['status']='HASH_MISMATCH'
            else:
                out['status']='PASS'
                if rec['expected_rows']:
                    if rec['format']=='csv':
                        with path.open(encoding='utf-8-sig',newline='') as f:
                            reader=csv.reader(f);next(reader);rows=sum(1 for _ in reader)
                    elif rec['format']=='parquet':
                        try:
                            import pyarrow.parquet as pq
                            parquet=pq.ParquetFile(path);rows=parquet.metadata.num_rows
                            out['parquet_schema_columns']=parquet.schema.names
                        except ImportError:
                            out['status']='PARQUET_ROWS_NOT_CHECKED_INSTALL_PYARROW';rows=None
                    else:rows=None
                    out['actual_rows']=rows
                    if rows is not None and rows!=int(rec['expected_rows']):out['status']='ROW_MISMATCH'
        results.append(out)
    failures=[r for r in results if r['status']!='PASS']
    return {'status':'PARTIAL_MISSING_OR_FAILED_FILES' if failures else 'KNOWN_FILE_BYTES_AND_ROWS_PASS',
            'scope':'partial_known_decision024_window_sensitivity_and_relative_fraction_products_only',
            'inventory_sha256':digest(inventory),'known_file_count':len(results),
            'verified_file_count':len(results)-len(failures),'missing_or_failed_files':len(failures),
            'all_known_file_bytes_and_rows_pass':not failures,
            'complete_stage0_inventory_accepted':False,'release_ready':False,'doi_assigned':False,
            'release_gate_limits':['Other accepted Phase1-9 products and full Stage0 allocation are not inventoried by this partial tool.',
                                  'Licensing, complete dictionaries, portable examples and deposit remain separate gates.'],
            'results':results}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inventory',type=Path,default=Path(__file__).resolve().parents[1]/'config/public_release_known_products_v2.csv')
    p.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument('--data-root',type=Path,required=True)
    p.add_argument('--output-json',type=Path,required=True)
    a=p.parse_args();record=run(a.inventory,a.repo_root,a.data_root)
    if a.output_json.exists():raise ValueError('Choose a new output report path; existing reports are not replaced')
    a.output_json.parent.mkdir(parents=True,exist_ok=True);a.output_json.write_text(json.dumps(record,indent=2)+'\n')
    print(record['status']);print('Verified:',record['verified_file_count'],'Missing/failed:',record['missing_or_failed_files'])
    raise SystemExit(0 if record['all_known_file_bytes_and_rows_pass'] else 2)
