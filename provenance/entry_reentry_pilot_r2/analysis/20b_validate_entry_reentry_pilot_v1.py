#!/usr/bin/env python3
"""Validate operator-supplied entry/re-entry pilot CSVs. Standard library, Python >=3.10."""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_csv(path, fields=None):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        names = reader.fieldnames or []
        require(len(names) == len(set(names)), f'{path.name}: duplicate columns')
        if fields is not None:
            require(set(names) == set(fields), f'{path.name}: unexpected columns')
        rows = list(reader)
    require(all(None not in r and None not in r.values() for r in rows), f'{path.name}: malformed CSV')
    return rows


def number(value):
    n = float(value)
    require(math.isfinite(n) and n >= 0, f'invalid metric: {value}')
    return n


def integer(value):
    n = number(value)
    require(n.is_integer(), f'not an integer: {value}')
    return int(n)


def near(a, b, tolerance, context):
    require(abs(a-b) <= tolerance, f'{context}: {a:.12g} != {b:.12g}, tolerance={tolerance}')


def csv_bytes(rows, fields):
    f = io.StringIO(newline='')
    writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return f.getvalue().encode('utf-8-sig')


def check_identities(row, tol, context):
    for total, parts in [
        ('flow_pas_tmp_ha', ['initial_ha', 'entry_ha', 'unresolved_ha']),
        ('stock0_pas_ha', ['initial_pas_stock_ha', 'entry_pas_stock_ha', 'unresolved_pas_stock_ha']),
        ('entry_ha', ['first_observed_entry_ha', 'observed_reentry_ha', 'prior_history_uncertain_ha']),
        ('entry_pas_stock_ha', ['first_observed_entry_pas_stock_ha', 'observed_reentry_pas_stock_ha', 'prior_history_uncertain_pas_stock_ha'])]:
        near(row[total], math.fsum(row[k] for k in parts), tol, context+'/'+total)
    for kind in ['initial', 'entry', 'unresolved', 'first_observed_entry', 'observed_reentry', 'prior_history_uncertain']:
        require(row[kind+'_ha'] <= row[kind+'_pas_stock_ha']+tol, context+': flow exceeds stock/'+kind)
    require(row['domain_ha'] > 0, context+': no area support')
    require(row['flow_pas_tmp_ha'] <= row['stock0_pas_ha']+tol and row['stock0_pas_ha'] <= row['domain_ha']+tol,
            context+': support/stock/flow ordering')
    for kind in ['initial', 'entry', 'unresolved']:
        for suffix in ['_ha', '_pas_stock_ha']:
            near(row[kind+suffix], row['control_'+kind+suffix], tol, context+'/accepted engine/'+kind+suffix)


def validate(root, export_dir, output_dir):
    root, export_dir, output_dir = map(Path, (root, export_dir, output_dir))
    pinned = json.loads((root/'config/entry_reentry_source_snapshots_v1.json').read_text())
    for name, expected in pinned['sha256'].items():
        require(sha(root/name) == expected, 'pinned file changed: '+name)
    config = json.loads((root/'config/entry_reentry_v1.json').read_text())
    schema = json.loads((root/'config/entry_reentry_schema_v1.json').read_text())
    cases = json.loads((root/'config/entry_reentry_native_cases_v1.json').read_text())
    expected_names = set(schema['filenames'].values())
    require({p.name for p in export_dir.glob('*.csv')} == expected_names, 'CSV inventory differs: expected exactly four pilot CSVs')
    inputs = {n: sha(export_dir/n) for n in sorted(expected_names)}
    inputs.update({n:h for n,h in pinned['sha256'].items()})
    accepted = json.loads((root/'config/reference_validation/window_origin_full_validation_v1.json').read_text())
    require(accepted['status'] == 'PASS' and accepted['scope'] == 'full', 'historical sensitivity not accepted')
    ref_hashes = {x['filename']:x['sha256'] for x in accepted['fresh_export_inputs']}
    reference = []
    cell_map = {x['cell_id']:x for x in config['pilot_cells']}
    # Re-extract exact baseline-1985 rows from original, accepted, hash-pinned native files.
    for item in config['reference_sources']:
        path = root/'config/reference_native'/item['filename']
        require(sha(path) == item['sha256'] == ref_hashes[item['filename']], 'historical native reference changed')
        rows = load_csv(path)
        reference.extend(r for r in rows if r['baseline_year']=='1985' and r['cell_id'] in cell_map)
    ref_map = {(r['cell_id'], integer(r['t0'])):r for r in reference}
    expected_keys = {(c,t0) for c in cell_map for t0,_ in config['intervals']}
    require(len(reference) == len(ref_map) == len(expected_keys) and set(ref_map) == expected_keys, 'historical reference inventory')
    subset = load_csv(root/'config/entry_reentry_pilot_reference_v1.csv')
    require(subset == reference, 'historical subset not reproduced from native sources')
    manifest_rows = load_csv(export_dir/schema['filenames']['manifest'], schema['manifest_fields'])
    require(len(manifest_rows)==1, 'manifest must have one row')
    manifest = manifest_rows[0]
    expected_meta = {'scope':'pilot','output_version':config['version'],'run_id':config['run_tag']+'_pilot'}
    require(all(manifest[k]==v for k,v in expected_meta.items()), 'manifest identity')
    require(manifest['source_script']=='20a_export_entry_reentry_pilot_v1.js', 'manifest source script')
    for key,value in {'expected_cells':2,'expected_rows':4,'expected_audit_rows':2,
                      'expected_native_cases':len(cases),'expected_native_steps':sum(len(c['values']) for c in cases),
                      'coverage_band_count':41,'audit_start_year':1985,'audit_end_year':2025,'audit_years_checked':41}.items():
        require(integer(manifest[key])==value, 'manifest/'+key)
    require(json.loads(manifest['config_json'])==schema['runtime_config'], 'runtime constants differ')
    require(manifest['coverage_bands_csv'].split('|')==[f'classification_{y}' for y in range(1985,2026)], 'annual bands differ')
    projections = json.loads(manifest['native_projections_json'])
    require(set(projections)=={str(y) for y in range(1985,2026)}, 'native projection inventory')
    for y,p in projections.items():
        require(p['crs']==config['crs'] and len(p['transform'])==6, 'projection/'+y)
        for a,b in zip(p['transform'], config['crs_transform']):
            require(isinstance(a,(int,float)) and math.isfinite(a), 'nonfinite native transform')
            near(a,b,1e-13,'transform/'+y)
    def identity(row):
        require(all(row[k]==v for k,v in expected_meta.items()), 'row identity differs')
        require(row['cell_id'] in cell_map, 'unexpected cell')
        ref = cell_map[row['cell_id']]
        require(row['GRID_ID']==ref['GRID_ID'] and integer(row['source_batch_id'])==ref['source_batch_id'], 'cell/grid/batch differs')
    rows=load_csv(export_dir/schema['filenames']['cells'],schema['cell_fields'])
    seen=set();comparisons=[]
    for row in rows:
        identity(row)
        t0,t1=integer(row['t0']),integer(row['t1'])
        require([t0,t1] in config['intervals'] and integer(row['diagnostic_interval'])==int(t0==2020),'interval/diagnostic flag')
        key=(row['cell_id'],t0)
        require(key not in seen, 'duplicate cell/interval');seen.add(key)
        for k in schema['area_fields']+schema['cell_error_fields']: row[k]=number(row[k])
        require(all(row[k]==0 for k in schema['cell_error_fields']), 'accepted origin pixel mismatch')
        check_identities(row,config['per_cell_tolerance_ha'],str(key))
        ref=ref_map[key]
        for field in schema['historical_comparison_fields']:
            actual,target=row[field],number(ref[field])
            near(actual,target,config['per_cell_tolerance_ha'],str(key)+'/historical/'+field)
            comparisons.append(dict(cell_id=key[0],t0=t0,field=field,actual_ha=actual,reference_ha=target,difference_ha=actual-target))
    require(len(rows)==4 and seen==expected_keys,'cell/interval inventory incomplete')
    rows.sort(key=lambda r:(int(r['cell_id']),integer(r['t0'])))
    audit=load_csv(export_dir/schema['filenames']['audit'],schema['audit_fields'])
    seen_audit=set()
    for row in audit:
        identity(row)
        require(row['cell_id'] not in seen_audit,'duplicate history audit');seen_audit.add(row['cell_id'])
        require([integer(row[k]) for k in ['start_year','end_year','years_checked']]==[1985,2025,41],'audit year coverage')
        for k in schema['audit_count_fields']+schema['error_fields']+schema['boundary_fields']: row[k]=number(row[k])
        require(row['history_support_pixel_equivalents']>0,'audit has no support')
        require(all(row[k]==0 for k in schema['error_fields']),'history invariant error')
        near(row['confirmed_entry_pixel_years'],math.fsum(row[k] for k in ['confirmed_reentry_pixel_years','first_observed_entry_pixel_years','prior_history_uncertain_entry_pixel_years']),1e-6,'entry-count partition')
        cell_rows=[r for r in rows if r['cell_id']==row['cell_id']]
        for kind,event_count in [('first_observed_entry','first_observed_entry_pixel_years'),
                                 ('observed_reentry','confirmed_reentry_pixel_years'),
                                 ('prior_history_uncertain','prior_history_uncertain_entry_pixel_years')]:
            if any(r[kind+'_pas_stock_ha']>config['per_cell_tolerance_ha'] for r in cell_rows):
                require(row[event_count]>0, 'positive entry stock without corresponding history event/'+kind)
        domain=min(r['domain_ha'] for r in rows if r['cell_id']==row['cell_id'])
        require(all(row[k]<=domain+config['per_cell_tolerance_ha'] for k in schema['boundary_fields']),'boundary area exceeds domain')
    require(len(audit)==2 and seen_audit==set(cell_map),'audit inventory incomplete')
    native=load_csv(export_dir/schema['filenames']['native'],schema['native_fields'])
    case_map={c['case_id']:c for c in cases};seen_native=set()
    for row in native:
        name=row['case_id'];require(name in case_map and name not in seen_native,'native fixture inventory');seen_native.add(name)
        case=case_map[name];steps=len(case['values'])
        require(row['scope']=='native_synthetic' and row['output_version']==config['version'] and row['run_id']==config['run_tag']+'_pilot_native_synthetic','native identity')
        required={'start_year':case['start_year'],'end_year':case['start_year']+steps-1,'steps':steps,
                  'expected_final_state':case['expected_state'][-1],'expected_final_age':case['expected_age'][-1],
                  'expected_final_kind':case['expected_entry_kind'][-1],'expected_final_count':case['expected_confirmed_entry_count'][-1],
                  'expected_final_entry_year':case['expected_entry_year'][-1]}
        require(all(integer(row[k])==v for k,v in required.items()),'native expectation metadata changed')
        require(number(row['test_pixel_equivalents'])>0,'native fixture has no support')
        require(all(number(row[k])==0 for k in schema['native_error_fields']),'native mismatch')
    require(len(native)==len(cases) and seen_native==set(case_map),'native fixtures missing')
    summaries=[]
    for t0,t1 in config['intervals']:
        selected=[r for r in rows if integer(r['t0'])==t0]
        total={k:math.fsum(r[k] for r in selected) for k in schema['area_fields']}
        check_identities(total,config['aggregate_tolerance_ha'],f'pilot total/{t0}')
        for field in schema['historical_comparison_fields']:
            target=math.fsum(number(ref_map[(c,t0)][field]) for c in cell_map)
            near(total[field],target,config['aggregate_tolerance_ha'],f'pilot total/historical/{t0}/{field}')
        total.update(t0=t0,t1=t1,cells=2,scope='pilot',diagnostic_interval=int(t0==2020))
        for kind in ['first_observed_entry','observed_reentry','prior_history_uncertain']:
            total[kind+'_fraction_of_entry_flow']=total[kind+'_ha']/total['entry_ha'] if total['entry_ha'] else ''
            total[kind+'_fraction_of_entry_stock']=total[kind+'_pas_stock_ha']/total['entry_pas_stock_ha'] if total['entry_pas_stock_ha'] else ''
        summaries.append(total)
    prefix='canonical_entry_reentry_pilot_v1'
    products={prefix+'_cells.csv':csv_bytes(rows,schema['cell_fields']),
              prefix+'_summary.csv':csv_bytes(summaries,list(summaries[0])),
              prefix+'_historical_controls.csv':csv_bytes(comparisons,list(comparisons[0])),
              prefix+'_history_audit.csv':csv_bytes(audit,schema['audit_fields'])}
    report={'status':'PASS','scope':'pilot','version':config['version'],'cells':2,'rows':4,
            'history_audit_rows':2,'audit_years':[1985,2025],'native_fixture_cases':len(cases),
            'native_fixture_steps':sum(len(c['values']) for c in cases),
            'full_domain_decomposition_complete':False,'native_full_domain_auxiliary_age201_complete':False,
            'historical_comparisons':len(comparisons),
            'max_historical_per_cell_difference_ha':max(abs(x['difference_ha']) for x in comparisons),
            'input_sha256':inputs,'output_sha256':{n:hashlib.sha256(b).hexdigest() for n,b in products.items()},
            'execution_identity':{'supplied_script_sha256':pinned['sha256']['gee/20a_export_entry_reentry_pilot_v1.js'],
                                  'executed_script_sha256':None,'operator_attestation':None,
                                  'independently_verified_remote_execution':False},
            'limitations':['Two-cell pilot; no domain-wide shares or rare-event absence inference.',
                           'First observed entry refers to the window beginning in 1985, not first-ever establishment.',
                           'Prior PAS under masks is unknown; gaps are not bridged.',
                           'Entry counts are observed confirmed entry counts, not total historical spell counts.',
                           'Pixel equivalents and pixel-years are reduction-weighted and may be fractional.',
                           'No new boundary-raster asset comparison or pasture-age source migration.']}
    products[prefix+'_validation.json']=(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    for name,b in products.items():
        p=output_dir/name
        require(not p.exists() or p.read_bytes()==b, 'refusing to overwrite differing result: '+name)
    output_dir.mkdir(parents=True,exist_ok=True)
    for name,b in products.items():
        p=output_dir/name
        if not p.exists(): p.write_bytes(b)
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--scope',required=True,choices=['pilot'])
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument('--export-dir',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    args=p.parse_args()
    try:
        result=validate(args.root,args.export_dir,args.output_dir)
    except (ValueError,KeyError,OSError,TypeError) as e:
        p.exit(1,'FAIL: '+str(e)+'\n')
    print(json.dumps({k:result[k] for k in ['status','scope','cells','rows','history_audit_rows','native_fixture_cases','native_fixture_steps','full_domain_decomposition_complete']},indent=2))

if __name__=='__main__':
    main()
