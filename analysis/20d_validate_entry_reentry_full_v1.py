#!/usr/bin/env python3
"""Validate the 73 full-domain exports against preserved native pilot and accepted historical areas."""
import argparse
import collections
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path


def require(ok,message):
    if not ok:raise ValueError(message)


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def csv_rows(path,fields=None):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);names=reader.fieldnames or []
        require(len(names)==len(set(names)),f'{path.name}: duplicate columns')
        if fields is not None:require(set(names)==set(fields),f'{path.name}: columns differ')
        for row in reader:
            require(None not in row and None not in row.values(),f'{path.name}: malformed CSV')
            yield row


def number(value):
    n=float(value);require(math.isfinite(n) and n>=0,'nonfinite/negative metric: '+str(value));return n


def integer(value):
    n=number(value);require(n.is_integer(),'not an integer: '+str(value));return int(n)


def near(a,b,tol,context):require(abs(a-b)<=tol,f'{context}: {a:.12g} != {b:.12g}, tol={tol}')


def csv_bytes(rows,fields):
    f=io.StringIO(newline='');w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
    return f.getvalue().encode('utf-8-sig')


def validate(root,export_dir,output_dir):
    root,export_dir,output_dir=map(Path,(root,export_dir,output_dir))
    snapshot=json.loads((root/'config/entry_reentry_full_source_snapshots_v1.json').read_text())
    for name,h in snapshot['sha256'].items():require(sha(root/name)==h,'pinned file changed: '+name)
    C=json.loads((root/'config/entry_reentry_full_v1.json').read_text())
    S=json.loads((root/'config/entry_reentry_full_schema_v1.json').read_text())
    # Revalidate the preserved native pilot with its original supplied validator and exact bytes.
    p_root=root/C['accepted_pilot_root']
    spec=importlib.util.spec_from_file_location('accepted_entry_pilot',p_root/'analysis/20b_validate_entry_reentry_pilot_v1.py')
    pilot_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(pilot_module)
    pilot=pilot_module.validate(p_root,p_root/'outputs/native/entry_reentry_v1/pilot_r2',p_root/'outputs/validation/entry_reentry_v1/pilot_r2')
    require(pilot['status']=='PASS' and pilot['scope']=='pilot','accepted pilot not PASS')
    accepted_pilot=json.loads((p_root/C['accepted_pilot_validation']).read_text());require(pilot==accepted_pilot,'accepted pilot report differs')
    # Only the chronology orchestration expands; the tested scientific step remains exact.
    supplied=(root/'gee/20c_export_entry_reentry_full_v1.js').read_text()
    prior=(p_root/'gee/20a_export_entry_reentry_pilot_v1.js').read_text()
    def block(text,label):return text.split('// BEGIN_'+label+'\n')[1].split('// END_'+label)[0]
    require(block(supplied,'ENTRY_REENTRY_ENGINE')==block(prior,'ENTRY_REENTRY_ENGINE'),'accepted step changed')
    require(block(supplied,'ACCEPTED_REFERENCE_ENGINE')==block(prior,'ACCEPTED_REFERENCE_ENGINE'),'historical categorical reference changed')
    accepted_audit=prior.split('// BEGIN_SERVER_ITERATION_R2\n')[1].split('function fixtureRaw')[0]
    require(block(supplied,'ACCEPTED_R2_HISTORY_AUDIT')==accepted_audit,'accepted r2 history audit changed')
    cross=list(csv_rows(root/'config/entry_reentry_full_crosswalk_v1.csv'))
    cell_map={x['cell_id']:x for x in cross};require(len(cell_map)==len(cross)==C['expected_cells'],'crosswalk incomplete/duplicate')
    require(len({x['GRID_ID'] for x in cross})==len(cross),'duplicate GRID_ID')
    batch_sets={b:{x['cell_id'] for x in cross if integer(x['source_batch_id'])==b} for b in C['expected_batches']}
    require(set().union(*batch_sets.values())==set(cell_map),'crosswalk batch mismatch')
    require(all(len(cells)==C['expected_batch_cells'][str(b)] and bool(cells) for b,cells in batch_sets.items()),'batch populations differ')
    reference={};source_counts=collections.Counter()
    comparison_fields=S['historical_comparison_fields'];interval_map={a:b for a,b in C['intervals']}
    for row in csv_rows(root/'config/entry_reentry_full_reference_v1.csv'):
        cell=row['cell_id'];t0=integer(row['t0']);key=(cell,t0)
        require(cell in cell_map and t0 in interval_map and integer(row['t1'])==interval_map[t0] and key not in reference,'historical reference inventory')
        require(row['GRID_ID']==cell_map[cell]['GRID_ID'] and integer(row['source_batch_id'])==integer(cell_map[cell]['source_batch_id']),'reference identities')
        require(integer(row['diagnostic_interval'])==int(t0==2020),'reference diagnostic flag')
        source_counts[row['data_source']]+=1
        reference[key]={k:number(row[k]) for k in comparison_fields}
    expected_keys={(c,t0) for c in cell_map for t0 in interval_map}
    require(set(reference)==expected_keys and len(reference)==C['expected_rows'],'historical reference incomplete')
    require(dict(source_counts)==C['reference_provenance']['data_source_rows'],'historical reference provenance counts differ')
    historical_acceptance=json.loads((root/'config/window_origin_full_validation_v1.json').read_text())
    require(historical_acceptance['status']=='PASS' and historical_acceptance['scope']=='full','historical window report not accepted')
    require(C['reference_provenance']['source_panel_sha256']==historical_acceptance['outputs']['canonical_window_origin_cell_panel_v1.csv']['sha256'],'normalized historical panel hash provenance differs')
    cells_names=[(f'canonical_entry_reentry_{t0}_{t1}_b{b:02d}_v1.csv',t0,t1,b) for t0,t1 in C['intervals'] for b in C['expected_batches']]
    audit_names=[(f'canonical_entry_reentry_history_audit_b{b:02d}_v1.csv',b) for b in C['expected_batches']]
    manifest_name='canonical_entry_reentry_manifest_full_v1.csv'
    expected_names={x[0] for x in cells_names+audit_names}|{manifest_name}
    actual_names={p.name for p in export_dir.glob('*.csv')}
    require(actual_names==expected_names,f'CSV inventory differs: missing={sorted(expected_names-actual_names)}; extra={sorted(actual_names-expected_names)}')
    input_hashes={n:sha(export_dir/n) for n in sorted(expected_names)}
    input_hashes['accepted_pilot_validation']=sha(p_root/C['accepted_pilot_validation'])
    input_hashes['critical_input_snapshot']=sha(root/'config/entry_reentry_full_source_snapshots_v1.json')
    manifest=list(csv_rows(export_dir/manifest_name,S['manifest_fields']));require(len(manifest)==1,'manifest must have one row');manifest=manifest[0]
    meta={'scope':'full','output_version':C['version'],'run_id':C['run_tag']+'_full'}
    require(all(manifest[k]==v for k,v in meta.items()),'manifest identity')
    require(manifest['source_script']=='20c_export_entry_reentry_full_v1.js','manifest source script')
    for field,value in {'expected_cells':len(cell_map),'expected_rows':len(expected_keys),'expected_audit_rows':len(cell_map),'expected_cell_files':len(cells_names),'expected_audit_files':len(audit_names),'coverage_band_count':41,'audit_start_year':1985,'audit_end_year':2025,'audit_years_checked':41,'runtime_grid_cells':len(cell_map)}.items():
        require(integer(manifest[field])==value,'manifest/'+field)
    for b,selected in batch_sets.items():require(integer(manifest[f'runtime_b{b:02d}_cells'])==len(selected),'manifest runtime batch population')
    require(json.loads(manifest['config_json'])==S['runtime_config'],'runtime constants differ')
    require(manifest['coverage_bands_csv'].split('|')==[f'classification_{y}' for y in range(1985,2026)],'band inventory differs')
    projections=json.loads(manifest['native_projections_json']);require(set(projections)=={str(y) for y in range(1985,2026)},'projection inventory')
    for y,p in projections.items():
        require(p['crs']==C['crs'] and len(p['transform'])==6,'projection/'+y)
        for a,b in zip(p['transform'],C['crs_transform']):
            require(isinstance(a,(int,float)) and math.isfinite(a),'invalid affine value');near(a,b,1e-13,'affine/'+y)
    def identity(row,batch):
        cell=row['cell_id'];require(cell in batch_sets[batch],'cell outside expected batch')
        require(row['GRID_ID']==cell_map[cell]['GRID_ID'] and integer(row['source_batch_id'])==batch,'cell/grid/batch mismatch')
        require(all(row[k]==v for k,v in meta.items()),'row execution identity differs')
    row_map={};by_interval={t0:[] for t0 in interval_map};domain={};maxima={(t0,k):(0.0,'') for t0 in interval_map for k in comparison_fields}
    inventory=[]
    for name,t0,t1,batch in cells_names:
        seen=set()
        for row in csv_rows(export_dir/name,S['cell_fields']):
            identity(row,batch);cell=row['cell_id'];require(cell not in seen,'duplicate cell in interval/batch');seen.add(cell)
            require(integer(row['t0'])==t0 and integer(row['t1'])==t1 and integer(row['diagnostic_interval'])==int(t0==2020),'wrong interval/diagnostic flag in file')
            for k in S['area_fields']+S['cell_error_fields']:row[k]=number(row[k])
            require(all(row[k]==0 for k in S['cell_error_fields']),'accepted origin pixel mismatch')
            pilot_module.check_identities(row,C['per_cell_tolerance_ha'],str((cell,t0)))
            if t0==1985:
                near(row['initial_ha'],row['flow_pas_tmp_ha'],C['per_cell_tolerance_ha'],'baseline by construction')
                require(all(row[k]==0 for k in ['entry_ha','unresolved_ha','entry_pas_stock_ha','unresolved_pas_stock_ha']),'noninitial origin at 1985 baseline')
            if cell in domain:near(row['domain_ha'],domain[cell],C['per_cell_tolerance_ha'],'fixed cell-area support')
            else:domain[cell]=row['domain_ha']
            for k in comparison_fields:
                expected=reference[(cell,t0)][k];near(row[k],expected,C['per_cell_tolerance_ha'],f'historical/{cell}/{t0}/{k}')
                diff=abs(row[k]-expected)
                if diff>maxima[(t0,k)][0]:maxima[(t0,k)]=(diff,cell)
            row_map[(cell,t0)]=row;by_interval[t0].append(row)
        require(seen==batch_sets[batch],name+': incomplete cell inventory')
        inventory.append(dict(file=name,kind='cell_interval',rows=len(seen),batch=batch,t0=t0,t1=t1,sha256=input_hashes[name]))
    require(set(row_map)==expected_keys,'complete cell/interval inventory differs')
    audit_map={}
    for name,batch in audit_names:
        seen=set()
        for row in csv_rows(export_dir/name,S['audit_fields']):
            identity(row,batch);cell=row['cell_id'];require(cell not in seen,'duplicate history row');seen.add(cell)
            require([integer(row[k]) for k in ['start_year','end_year','years_checked']]==[1985,2025,41],'history year coverage')
            for k in S['audit_count_fields']+S['error_fields']+S['boundary_fields']:row[k]=number(row[k])
            require(row['history_support_pixel_equivalents']>0,'history has no support')
            require(all(row[k]==0 for k in S['error_fields']),'real history invariant mismatch')
            near(row['confirmed_entry_pixel_years'],math.fsum(row[k] for k in ['confirmed_reentry_pixel_years','first_observed_entry_pixel_years','prior_history_uncertain_entry_pixel_years']),C['pixel_equivalent_tolerance'],'entry-event partition')
            require(all(row[k]<=domain[cell]+C['per_cell_tolerance_ha'] for k in S['boundary_fields']),'boundary area exceeds domain')
            for kind,event in [('first_observed_entry','first_observed_entry_pixel_years'),('observed_reentry','confirmed_reentry_pixel_years'),('prior_history_uncertain','prior_history_uncertain_entry_pixel_years')]:
                if any(row_map[(cell,t0)][kind+'_pas_stock_ha']>C['per_cell_tolerance_ha'] for t0 in interval_map):require(row[event]>0,'positive stock without matching history event')
            audit_map[cell]=row
        require(seen==batch_sets[batch],name+': incomplete history inventory')
        inventory.append(dict(file=name,kind='history_audit',rows=len(seen),batch=batch,t0=1985,t1=2025,sha256=input_hashes[name]))
    require(set(audit_map)==set(cell_map),'full audit incomplete')
    pilot_controls=[]
    for row in csv_rows(p_root/'outputs/native/entry_reentry_v1/pilot_r2/canonical_entry_reentry_pilot_v1.csv'):
        full=row_map[(row['cell_id'],integer(row['t0']))]
        for k in S['area_fields']+S['cell_error_fields']:
            actual,expected=full[k],number(row[k]);near(actual,expected,C['per_cell_tolerance_ha'],'accepted pilot cell/'+k)
            pilot_controls.append(dict(cell_id=row['cell_id'],population='endpoint',t0=row['t0'],field=k,actual=actual,reference=expected,difference=actual-expected))
    for row in csv_rows(p_root/'outputs/native/entry_reentry_v1/pilot_r2/canonical_entry_reentry_history_audit_pilot_v1.csv'):
        full=audit_map[row['cell_id']]
        for k in S['audit_count_fields']+S['error_fields']+S['boundary_fields']:
            actual,expected=full[k],number(row[k]);tol=C['per_cell_tolerance_ha'] if k in S['boundary_fields'] else C['pixel_equivalent_tolerance']
            near(actual,expected,tol,'accepted pilot history/'+k)
            pilot_controls.append(dict(cell_id=row['cell_id'],population='history',t0=1985,field=k,actual=actual,reference=expected,difference=actual-expected))
    summaries=[];historical_controls=[]
    for t0,t1 in C['intervals']:
        selected=by_interval[t0];total={k:math.fsum(row[k] for row in selected) for k in S['area_fields']}
        pilot_module.check_identities(total,C['aggregate_tolerance_ha'],f'domain/{t0}')
        for k in comparison_fields:
            expected=math.fsum(reference[(cell,t0)][k] for cell in cell_map)
            near(total[k],expected,C['aggregate_tolerance_ha'],f'aggregate historical/{t0}/{k}')
            historical_controls.append(dict(t0=t0,t1=t1,field=k,actual_ha=total[k],reference_ha=expected,difference_ha=total[k]-expected,max_cell_difference_ha=maxima[(t0,k)][0],max_difference_cell_id=maxima[(t0,k)][1]))
        total.update(t0=t0,t1=t1,cells=len(selected),scope='full',diagnostic_interval=int(t0==2020),baseline_interval_by_construction=int(t0==1985))
        for kind in ['first_observed_entry','observed_reentry','prior_history_uncertain']:
            total[kind+'_fraction_of_entry_flow']=total[kind+'_ha']/total['entry_ha'] if total['entry_ha'] else ''
            total[kind+'_fraction_of_entry_stock']=total[kind+'_pas_stock_ha']/total['entry_pas_stock_ha'] if total['entry_pas_stock_ha'] else ''
        summaries.append(total)
    all_rows=sorted(row_map.values(),key=lambda x:(int(x['cell_id']),integer(x['t0'])))
    all_audit=sorted(audit_map.values(),key=lambda x:int(x['cell_id']))
    prefix='canonical_entry_reentry_full_v1'
    products={prefix+'_cells.csv':csv_bytes(all_rows,S['cell_fields']),prefix+'_summary.csv':csv_bytes(summaries,list(summaries[0])),prefix+'_history_audit.csv':csv_bytes(all_audit,S['audit_fields']),prefix+'_historical_controls.csv':csv_bytes(historical_controls,list(historical_controls[0])),prefix+'_pilot_controls.csv':csv_bytes(pilot_controls,list(pilot_controls[0])),prefix+'_inventory.csv':csv_bytes(inventory,list(inventory[0]))}
    report={'status':'PASS','scope':'full','version':C['version'],'cells':len(cell_map),'rows':len(row_map),'history_audit_rows':len(audit_map),'new_export_files':len(expected_names),'audit_years':[1985,2025],'preserved_native_fixtures':pilot['native_fixture_cases'],'preserved_fixture_steps':pilot['native_fixture_steps'],'historical_cell_field_comparisons':len(row_map)*len(comparison_fields),'aggregate_historical_controls':len(historical_controls),'pilot_comparisons':len(pilot_controls),'max_historical_per_cell_difference_ha':max(x[0] for x in maxima.values()),'full_domain_decomposition_complete':True,'native_full_domain_auxiliary_age201_complete':True,'input_sha256':input_hashes,'output_sha256':{n:hashlib.sha256(b).hexdigest() for n,b in products.items()},'reference_provenance':C['reference_provenance'],'execution_identity':{'supplied_script_sha256':snapshot['sha256']['gee/20c_export_entry_reentry_full_v1.js'],'executed_script_sha256':None,'operator_attestation':None,'independently_verified_remote_execution':False},'limitations':['First observed entry is window-specific from 1985, not first-ever establishment.','Prior PAS under masks is unknown; no gap bridging.','The 1985 baseline interval has only initial origin by construction; entry fractions have zero denominator and remain blank.','2020–2025 is diagnostic. Annual event counts are weighted pixel-years, not unique area or complete historical spell counts.','Earlier historical reference rows retain their accepted native/reused provenance; no native error counters are invented for reused references.','Operator-supplied exports, with preserved pilot fixtures; no new event-raster asset comparison or pasture-age asset migration.']}
    products[prefix+'_validation.json']=(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    for name,b in products.items():
        p=output_dir/name;require(not p.exists() or p.read_bytes()==b,'refusing to overwrite differing output: '+name)
    output_dir.mkdir(parents=True,exist_ok=True)
    for name,b in products.items():
        p=output_dir/name
        if not p.exists():p.write_bytes(b)
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope',choices=['full'],required=True)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--export-dir',type=Path,required=True);parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args()
    try:report=validate(args.root,args.export_dir,args.output_dir)
    except (ValueError,KeyError,OSError,TypeError,IndexError) as error:parser.exit(1,'FAIL: '+str(error)+'\n')
    print(json.dumps({k:report[k] for k in ['status','scope','cells','rows','history_audit_rows','new_export_files','full_domain_decomposition_complete']},indent=2))

if __name__=='__main__':main()
