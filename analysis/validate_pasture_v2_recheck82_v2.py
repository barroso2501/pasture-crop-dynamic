#!/usr/bin/env python3
"""Validate v2 native transport and 82 cells; missing data are never zeros."""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('parent_validator',Path(__file__).with_name('validar_auditoria_pasture_v2_v1_2.py'))
old=importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
require=old.require


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def encoded_csv(rows,fields):
    out=io.StringIO(newline='')
    w=csv.DictWriter(out,fieldnames=fields,lineterminator='\n')
    w.writeheader();w.writerows(rows)
    return out.getvalue().encode('utf-8-sig')


def validate(path,root=ROOT,output_dir=None):
    root=Path(root);path=Path(path)
    config_path=root/'config/pasture_v2_coverage_recheck_82_v2.json'
    config=json.loads(config_path.read_text())
    parent_dir=root/'outputs/native/pasture_v2_v1_2/domain_new'
    parent_report_path=root/'outputs/validation/pasture_v2_v1_2/domain_new'/f"pasture_v2_mem12_domain_new_{config['parent_run']}_validation.json"
    require(sha(parent_report_path)==config['parent_validation_sha256'],'Parent validation hash changed')
    parent_report=json.loads(parent_report_path.read_text())
    require(parent_report['status']=='PASS' and parent_report['rows_validated']==21869,'Parent report differs')
    parent=[]
    for name,h in parent_report['input_sha256'].items():
        require(sha(parent_dir/name)==h,'Parent native bytes changed: '+name)
        parent.extend(old.read(parent_dir/name))
    parent_map={r['audit_id']:r for r in parent}
    selected={c['audit_id']:c for c in config['cells']}
    require(len(parent_map)==len(parent)==21869 and len(selected)==82,'Parent/selection inventory differs')
    require({r['audit_id'] for r in parent if old.integer(r['new_coverage_unknown_code'])==1}==set(selected),
            'Selected cells do not exactly match parent uncertainty')
    match=re.fullmatch(r'pasture_v2_coverage_recheck82_(\d{14})_v2\.csv',path.name)
    require(match is not None,'Unexpected recheck filename')
    run=match[1]
    rows=old.read(path)
    require(len(rows)==82 and {r['audit_id'] for r in rows}==set(selected),'Recheck incomplete/duplicated')
    binaries=['new_'+k for k in old.FLAGS]+['legacy_coverage_unknown_present']+[
        f'coverage_code_{c}_present' for c in config['newly_recognized_codes']]
    exact={'script_version':config['version'],'parent_run':config['parent_run'],
           'parent_validation_sha256':config['parent_validation_sha256'],'run_id':run,
           'coverage_asset':config['coverage'],'new_asset':config['age'],'grid_asset':config['grid'],
           'crs':config['crs']}
    required={'audit_id','cell_id','GRID_ID','generated_at_utc','expected_cells','year_start','year_end',
              'known_codes_json','prior_known_codes_json','crs_transform','tile_scale',
              'remaining_unknown_max_code','remaining_unknown_negative_min_code','native_grid_support'}|set(exact)|set(binaries)|set(config['required_transport_controls'])
    require(set(rows[0])==required,'Recheck columns differ')
    require(len({r['generated_at_utc'] for r in rows})==1,'Mixed execution times')
    changes=[]
    result_fields=['new_'+k for k in old.FLAGS]+['legacy_coverage_unknown_present']+[
        f'coverage_code_{c}_present' for c in config['newly_recognized_codes']]+[
        'remaining_unknown_max_code','remaining_unknown_negative_min_code','native_grid_support']
    expected_schema={k:i+1 for i,k in enumerate(result_fields)}
    for r in rows:
        require(all(r[k]==v for k,v in exact.items()),'Runtime identity differs')
        require(r['native_schema_test_status']=='PASS' and old.integer(r['native_schema_test_fields'])==26,
                'Native schema self-test did not pass')
        require(json.loads(r['native_schema_expected_json'])==expected_schema,'Native schema fixture outputs differ')
        require(json.loads(r['image_band_names_json'])==result_fields,'Native image bands/order differ')
        require(old.integer(r['reducer_missing_count'])==0 and r['reducer_missing_fields']=='',
                'Missing native reductions: '+r['reducer_missing_fields'])
        raw_properties=json.loads(r['reducer_properties_json'])
        raw_keys=json.loads(r['reducer_property_names_json'])
        require(isinstance(raw_properties,dict) and isinstance(raw_keys,list),'Raw native diagnostics invalid')
        for field in result_fields:
            require(r[field]!='','Empty native metric '+field+' / '+r['audit_id'])
            require(field in raw_properties and field in raw_keys and raw_properties[field] is not None,
                    'Native property absent/null: '+field)
            actual=float(r[field]);raw_value=raw_properties[field]
            require(not isinstance(raw_value,bool) and isinstance(raw_value,(int,float)) and
                    math.isfinite(actual) and math.isfinite(raw_value) and actual==raw_value,
                    'CSV/raw native property disagree: '+field)
        require(old.integer(r['native_grid_support'])==1,'No native geometry support')
        require(re.sub(r'[^0-9]','',r['generated_at_utc'])[:14]==run,'Run/time differ')
        require(old.integer(r['expected_cells'])==82 and old.integer(r['year_start'])==1985 and
                old.integer(r['year_end'])==2025 and old.integer(r['tile_scale'])==16,'Scope/parameters differ')
        require(json.loads(r['known_codes_json'])==config['known_coverage_codes'] and
                json.loads(r['prior_known_codes_json'])==config['previous_known_coverage_codes'],'Coverage rules differ')
        transform=json.loads(r['crs_transform'])
        require(len(transform)==6 and all(math.isfinite(x) and abs(x-y)<=1e-13
                for x,y in zip(transform,config['crs_transform'])),'Projection differs')
        expected=selected[r['audit_id']]
        require(r['cell_id']==expected['cell_id'] and r['GRID_ID']==expected['GRID_ID'],'Cell crosswalk differs')
        for k in binaries:
            r[k]=old.integer(r[k]);require(r[k] in [0,1],'Nonbinary: '+k)
        require(r['legacy_coverage_unknown_present']==1,'Legacy unknown not reproduced')
        require(r['new_reused100_after_exit']<=r['new_invalid100_after_nonpas']<=r['new_code100_without_confirmed_initial'],
                'Temporal subsets inconsistent')
        require(r['new_code100_after_gap_only']<=r['new_code100_without_confirmed_initial'],'Gap subset inconsistent')
        hi=float(r['remaining_unknown_max_code']);negative_lo=float(r['remaining_unknown_negative_min_code'])
        require(all(math.isfinite(x) and x.is_integer() for x in [hi,negative_lo]),'Unknown-code range invalid')
        if r['new_coverage_unknown_code']==0:
            require(hi==negative_lo==-1000000000,'Absent unknown must retain explicit sentinels')
            require(any(r[f'coverage_code_{c}_present'] for c in config['newly_recognized_codes']),
                    'Legacy unknown not explained by expanded codes')
        else:
            lo=-negative_lo
            require(lo<=hi and hi!=-1000000000 and negative_lo!=-1000000000,'Unknown range missing')
            require(lo not in config['known_coverage_codes']+[0,27] and
                    hi not in config['known_coverage_codes']+[0,27],'Unknown extrema classified as known')
        for k in old.FLAGS:
            before=old.integer(parent_map[r['audit_id']]['new_'+k]);after=r['new_'+k]
            if before!=after:
                changes.append({'audit_id':r['audit_id'],'cell_id':r['cell_id'],'GRID_ID':r['GRID_ID'],
                                'flag':k,'parent_value':before,'rechecked_value':after})
    subset={r['audit_id']:r for r in rows}
    combined=[]
    for prior in parent:
        current=subset.get(prior['audit_id'])
        row={k:prior[k] for k in ['audit_id','cell_id','GRID_ID']}
        row['evidence_source']='native_recheck82_v2' if current else 'accepted_parent_v1.2_unaffected'
        for k in old.FLAGS:
            row['new_'+k]=current['new_'+k] if current else old.integer(prior['new_'+k])
        combined.append(row)
    combined.sort(key=lambda r:r['audit_id'])
    totals={k:sum(r['new_'+k] for r in combined) for k in old.FLAGS}
    controls=[k for k in ['pasture_age_masked','pasture_age_zero','unexpected_age_code','coverage_unknown_code',
        'age100_outside_pas','age_positive_outside_pas','code100_without_confirmed_initial','code100_after_gap_only'] if totals[k]>0]
    if totals['has_valid_coverage']!=21869:controls.append('cells_without_valid_coverage')
    if totals['has_pasture']==0:controls.append('no_pasture_in_domain')
    def verdict(k):
        return 'PRESENTE_NO_ESCOPO' if totals[k] else ('NAO_DETECTADO_COM_PENDENCIAS' if controls
                                                   else 'NAO_DETECTADO_NO_DOMINIO_COMPLETO')
    report={'status':'PASS','version':config['version'],'recheck_run':run,'parent_run':config['parent_run'],
            'native_transport_controls':'PASS','native_output_fixture_fields':26,'native_cells_rechecked':82,'parent_cells_reused_unchanged':21787,'combined_cells':21869,
            'affected_cells':totals,'pending_controls':controls,'changed_flag_values':len(changes),
            'newly_recognized_code_cell_counts':{str(c):sum(r[f'coverage_code_{c}_present'] for r in rows)
                for c in config['newly_recognized_codes']},
            'verdicts':{k:verdict(k) for k in ['code1','invalid100_after_nonpas','reused100_after_exit']},
            'input_sha256':{'config':sha(config_path),'recheck_csv':sha(path),'parent_validation':sha(parent_report_path),
                            **parent_report['input_sha256']},
            'provenance_rule':'Only cells with observed parent unknown code are replaced. Elsewhere the expanded known list cannot change coverage states: any added observed code would have set the parent unknown flag.',
            'limitations':['Same referenced coverage/age asset IDs; remote asset bytes are not independently hashed.',
                           'No full-domain raster re-export is claimed for the 21,787 reused cells.',
                           'Cell occurrence flags, not pixel counts or hectares; not validation of all numeric ages.',
                           'Executed script text has no operator hash attestation.'],
            'executed_script_sha256':None}
    prefix=f'pasture_v2_coverage_recheck82_{run}_v2'
    products={prefix+'_combined_cells.csv':encoded_csv(combined,list(combined[0])),
              prefix+'_flag_changes.csv':encoded_csv(changes,['audit_id','cell_id','GRID_ID','flag','parent_value','rechecked_value'])}
    report['output_sha256']={name:hashlib.sha256(data).hexdigest() for name,data in products.items()}
    products[prefix+'_validation.json']=(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    output=Path(output_dir) if output_dir else root/'outputs/validation/pasture_v2_coverage_recheck82_v2'
    for name,data in products.items():
        require(not (output/name).exists() or (output/name).read_bytes()==data,'Refusing to overwrite different output')
    output.mkdir(parents=True,exist_ok=True)
    for name,data in products.items():
        if not (output/name).exists():(output/name).write_bytes(data)
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('csv',type=Path);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--output-dir',type=Path)
    args=p.parse_args()
    try:print(json.dumps(validate(args.csv,args.root,args.output_dir),ensure_ascii=False,indent=2))
    except (ValueError,KeyError,TypeError,OSError) as e:p.exit(1,f'RECHECK INCONCLUSIVE: {e}\n')
