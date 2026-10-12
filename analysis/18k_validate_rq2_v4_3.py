"""Check preservation, independent interval fractions and explicit pending work."""
from pathlib import Path
import argparse,csv,hashlib,json,math
import pandas as pd

def require(x,msg):
    if not bool(x):raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f);return r.fieldnames,list(r)

def run(root):
    prev=root/'outputs/summary/rq2_evidence_consolidation_v4_2/canonical_integrated_evidence_matrix_v4_2.csv'
    matrix=root/'outputs/summary/rq2_relative_conversion_v1/canonical_integrated_evidence_matrix_v4_3.csv'
    evold=root/'outputs/validation/rq2_evidence_consolidation_v4_2/canonical_evidence_status_events_v4.csv'
    evnew=root/'outputs/validation/rq2_relative_conversion_v1/canonical_evidence_status_events_v5.csv'
    native=root/'outputs/validation/window_origin_sensitivity_v1/full/canonical_window_origin_sensitivity_validation_v1.json'
    pins=json.loads((root/'config/rq2_v4_3_predecessor_pins_v1.json').read_text())
    require(sha(prev)==pins['previous_matrix_sha256'] and sha(evold)==pins['previous_events_sha256'] and sha(native)==pins['original_native_validation_sha256'],'Pinned predecessor changed')
    fields,old=read(prev);nf,new=read(matrix)
    require(fields==nf and len(old)==len(new)==35,'Matrix schema/population differs')
    require([r['finding_id'] for r in new]==[r['finding_id'] for r in old],'Finding ID/order differs')
    changed=[]
    for a,b in zip(old,new):
        if any(a[k]!=b[k] for k in fields if k!='evidence_matrix_version'):changed.append(b['finding_id'])
        require(all(a[k]==b[k] for k in ['source_relative_path','source_sha256','source_authenticated','evidence_status','causal_claim_flag']),'Source/status/causal flags changed')
        require(b['evidence_matrix_version'].endswith('v4.3'),'Wrong edition')
        if b['finding_id'] in ['P9A035','P9A036']:
            require('nesting' in b['main_result'] and 'fraction' in b['main_result'],'Short matrix statement lacks key qualification')
    require(changed==['P9A035','P9A036'],'Unexpected substantive finding changes')
    require(matrix.read_bytes().startswith(b'\xef\xbb\xbf'),'Matrix BOM lost')
    ef,old_events=read(evold);newf,new_events=read(evnew)
    require(ef==newf and len(old_events)==10 and len(new_events)==12,'Event schema/count differs')
    require(evnew.read_bytes().startswith(evold.read_bytes()) and new_events[:10]==old_events,'Historical event bytes/rows changed')
    require(len({r['event_id'] for r in new_events})==12,'Duplicate event ID')
    require([r['finding_id'] for r in new_events[10:]]==changed,'Event/finding mismatch')
    _,sources=read(root/'config/rq2_evidence_v4_3_source_inventory_v1.csv')
    require(len(sources)==13,'Source inventory incomplete')
    for rec in sources:require(sha(root/rec['source_relative_path'])==rec['source_sha256'],'Numerical source hash differs')
    src=pd.read_csv(root/'outputs/validation/window_origin_sensitivity_v1/full/canonical_window_origin_interval_summary_v1.csv',float_precision='round_trip').set_index(['baseline_year','t0'])
    q=pd.read_csv(root/'outputs/summary/rq2_relative_conversion_v1/canonical_relative_endpoint_conversion_fractions_v1.csv',float_precision='round_trip').set_index(['baseline_year','t0'])
    require(len(src)==len(q)==19 and set(src.index)==set(q.index),'Ratio population differs')
    first=0;estimable=0
    for key,row in q.iterrows():
        ref=src.loc[key]
        for origin in ['initial','entry','unresolved']:
            require(row[origin+'_conversion_ha']==ref[origin+'_ha'] and row[origin+'_stock_t0_ha']==ref[origin+'_pas_stock_ha'],'Copied area differs')
            stock=float(ref[origin+'_pas_stock_ha']);conversion=float(ref[origin+'_ha'])
            expected=conversion/stock if stock>0 else math.nan
            got=row[origin+'_endpoint_conversion_fraction_5y']
            require((math.isnan(expected) and pd.isna(got)) or abs(got-expected)<=1e-14,'Independent fraction calculation differs')
        if ref.entry_pas_stock_ha==0:
            first+=1;require(pd.isna(row.relative_fraction_ratio_initial_entry) and row.relative_ratio_status=='undefined_zero_entry_stock','Zero-entry-stock ratio fabricated')
        else:
            estimable+=1
            expected=(ref.initial_ha/ref.initial_pas_stock_ha)/(ref.entry_ha/ref.entry_pas_stock_ha)
            require(abs(row.relative_fraction_ratio_initial_entry-expected)<=1e-13,'Independent ratio differs')
            identity=ref.initial_ha/ref.entry_ha-(ref.initial_pas_stock_ha/ref.entry_pas_stock_ha)*expected
            require(abs(identity)<=1e-12,'Algebraic factorization differs')
    require(first==3 and estimable==16,'Missing/estimable ratio counts differ')
    summary=pd.read_csv(root/'outputs/summary/rq2_relative_conversion_v1/canonical_relative_endpoint_conversion_summary_v1.csv',float_precision='round_trip').set_index('baseline_year')
    for base,group in q.reset_index().groupby('baseline_year'):
        vals=group.loc[group.diagnostic_interval.eq(0),'relative_fraction_ratio_initial_entry'].dropna()
        require(abs(summary.loc[base,'primary_ratio_min']-vals.min())<1e-13 and abs(summary.loc[base,'primary_ratio_max']-vals.max())<1e-13,'Summary extrema differ')
    require(bool(summary.loc[2000,'primary_ratio_monotonic_increasing']),'b2000 three-point monotonicity incorrectly reported')
    require(not bool(summary.loc[1985,'primary_ratio_monotonic_increasing']) and not bool(summary.loc[1995,'primary_ratio_monotonic_increasing']),'Oscillating primary sequence mislabeled')
    n=json.loads(native.read_text())
    require(n['executed_script_sha256_operator_attested'] is None and not n['independently_verified_remote_script_identity'],'Historical execution authentication changed')
    protocol=json.loads((root/'config/plan009_joint_native_followup_protocol_v1.json').read_text())
    require(protocol['status']=='PREPARED_NOT_EXECUTED' and not protocol['age_201_and_boundary_native_executed'],'Pending native work mislabeled')
    release=json.loads((root/'outputs/validation/release_preparation_v2/known_release_file_byte_checks_v1.json').read_text())
    require(release['known_file_count']==86 and release['verified_file_count']==83 and release['missing_or_failed_files']==3,'Known-release check scope changed')
    require(not release['release_ready'] and not release['doi_assigned'],'Incomplete release claimed ready')
    require(all(r['status']=='MISSING' and r['source_relative_path'].endswith('.parquet') for r in release['results'] if r['status']!='PASS'),'Unexpected release failure hidden')
    manuscript=(root/'manuscript/results/rq2_observed_pasture_spell_origins_v4_3.md').read_text()
    for text in ['1.1674','1.3979','0.8164','1.1016','0.8072','0.7209','0.6712','undefined','set nesting','not time-integrated exposure']:
        require(text in manuscript,'Manuscript numerical/denominator wording missing: '+text)
    result={'status':'PASS','scope':'descriptive_derivative_and_documentary_update_v4.3','date':'2026-10-12',
            'matrix_rows':35,'substantively_updated_findings':changed,'other_findings_unchanged':33,
            'canonical_anchors_statuses_and_causal_flags_preserved':True,
            'historical_event_rows_preserved':10,'supplementary_event_rows_added':2,
            'source_inventory_entries_checked':13,'interval_ratios':19,'estimable_ratios':16,'undefined_first_interval_ratios':3,
            'independent_area_ratio_and_factorization_checks':'PASS',
            'no_new_native_execution':True,'operator_attestation_recorded':False,
            'native_extensions_status':'protocol_prepared_not_exporter_or_execution',
            'known_release_files_verified':83,'missing_parquets':3,'complete_stage0_inventory_accepted':False,'doi_assigned':False,
            'matrix_sha256':sha(matrix),'previous_matrix_sha256':sha(prev),'events_sha256':sha(evnew),
            'native_validation_sha256_unchanged':sha(native),
            'limits':['Fractions are national descriptive endpoint ratios, not time exposure, hazards or causal adjustments.',
                      'No pooled exposure-normalized ratio is estimated.',
                      'Native chronology/age/boundary/cross-tab extensions require a future GEE implementation and pilot.',
                      'The full manuscript was not edited; a complete proposed section is provided.',
                      'Known-product byte verification is partial; the full public-release scope is not frozen.']}
    out=root/'outputs/validation/rq2_relative_conversion_v1/canonical_rq2_v4_3_validation_v1.json';out.parent.mkdir(parents=True,exist_ok=True)
    payload=(json.dumps(result,indent=2)+'\n').encode()
    require(not out.exists() or out.read_bytes()==payload,'Versioned validation differs')
    if not out.exists():out.write_bytes(payload)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    record=run(p.parse_args().root)
    print('RQ2 v4.3 DESCRIPTIVE UPDATE — PASS; 2 findings updated, 33 preserved; native extensions pending.')
