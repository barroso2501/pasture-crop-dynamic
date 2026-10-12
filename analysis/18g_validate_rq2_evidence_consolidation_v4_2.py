"""Validate the compact v4.2 evidence update and its numerical provenance."""
from pathlib import Path
import argparse, csv, hashlib, json
import pandas as pd

PREVIOUS='outputs/summary/decision024_review_v1/canonical_integrated_evidence_matrix_v4_1.csv'
CURRENT='outputs/summary/rq2_evidence_consolidation_v4_2/canonical_integrated_evidence_matrix_v4_2.csv'
EVENT_OLD='outputs/validation/decision024_review_v1/canonical_evidence_status_events_v3.csv'
EVENT_NEW='outputs/validation/rq2_evidence_consolidation_v4_2/canonical_evidence_status_events_v4.csv'
OUTPUT='outputs/validation/rq2_evidence_consolidation_v4_2/canonical_rq2_evidence_consolidation_validation_v1.json'

def require(value,message):
    if not bool(value):raise ValueError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f);return r.fieldnames,list(r)
def close(actual,expected,label,tol=1e-10):
    require(abs(float(actual)-float(expected))<=tol,label)

def run(root):
    snapshots=json.loads((root/'config/rq2_evidence_v4_2_reference_snapshots_v1.json').read_text())
    for rec in snapshots['files']:
        require(sha(root/rec['relative_path'])==rec['sha256'],'Pinned predecessor/execution source differs: '+rec['relative_path'])
    old_fields,old=read(root/PREVIOUS)
    fields,current=read(root/CURRENT)
    require(fields==old_fields and len(current)==len(old)==35,'Evidence schema/population differs')
    require([r['finding_id'] for r in current]==[r['finding_id'] for r in old],'Finding IDs/order differ')
    require(len({r['finding_id'] for r in current})==35,'Duplicate finding')
    require((root/CURRENT).read_bytes().startswith(b'\xef\xbb\xbf'),'BOM missing')
    changed=[]
    source_fields=['source_relative_path','source_sha256','source_authenticated']
    for before,after in zip(old,current):
        diff=[k for k in fields if k!='evidence_matrix_version' and before[k]!=after[k]]
        if diff:changed.append(after['finding_id'])
        require(all(after[k]==before[k] for k in source_fields),'Canonical source anchor changed')
        require(after['evidence_status']==before['evidence_status'],'Evidence qualification changed')
        require(after['causal_claim_flag']=='0','Causal claim introduced')
        require(after['evidence_matrix_version']=='phase9-decision024-corrected-evidence-matrix-v4.2','Wrong current edition')
    require(changed==['P9A035','P9A036'],'Substantive changes extend beyond two authorized findings')
    for after in current:
        if after['finding_id'] in changed:
            require(after['evidence_status']=='qualified' and after['robustness_status']=='window_boundary_sensitive_full_domain_validated','Sensitivity/status qualification missing')
            require('not first-ever establishment' in after['interpretation_boundary'],'Entry semantics missing')
            require('does not identify an artifact fraction' in after['interpretation_boundary'],'Identification boundary missing')
            require('not been executed' not in after['interpretation_boundary'],'Obsolete sensitivity status')

    raw=(root/EVENT_OLD).read_bytes()
    new=(root/EVENT_NEW).read_bytes()
    require(new.startswith(raw),'Prior event bytes were edited')
    ef,er=read(root/EVENT_OLD);nf,nr=read(root/EVENT_NEW)
    require(ef==nf and len(er)==8 and len(nr)==10 and nr[:8]==er,'Event population/schema/history differs')
    require(len({r['event_id'] for r in nr})==10,'Duplicate event')
    require([r['finding_id'] for r in nr[8:]]==changed,'New event finding mismatch')
    for r in nr[8:]:
        require(r['event_status']=='supplemented_by_validated_window_sensitivity' and r['effective_date']=='2026-10-12','Wrong appended event')
        require(r['validation_record']==OUTPUT,'Event validation pointer differs')

    _,inventory=read(root/'config/rq2_evidence_v4_2_source_inventory_v1.csv')
    require(len(inventory)==9 and {r['finding_id'] for r in inventory}==set(changed),'Supplemental source inventory differs')
    for r in inventory:
        p=root/r['source_relative_path']
        require(sha(p)==r['source_sha256'] and p.stat().st_size==int(r['bytes']),'Source hash/size differs')
    sensitivity=root/'outputs/validation/window_origin_sensitivity_v1/full'
    native=json.loads((sensitivity/'canonical_window_origin_sensitivity_validation_v1.json').read_text())
    require(native['status']=='PASS' and native['scope']=='full' and native['whole_domain_sensitivity_complete'],'Native acceptance missing')
    require(native['normalized_rows']==472891 and native['fresh_rows']==423113 and native['early_1985_reference_rows_reused']==49778,'Native panel population differs')
    require(native['native_synthetic_cases']==30 and native['native_field_invariant_counts_zero'],'Native assurance differs')
    require(native['executed_script_sha256_operator_attested'] is None and not native['independently_verified_remote_script_identity'],'Unwarranted execution authentication')
    for filename,record in native['outputs'].items():
        p=sensitivity/filename
        if p.exists():require(sha(p)==record['sha256'],'Accepted compact output changed')
        else:require(filename=='canonical_window_origin_cell_panel_v1.csv','Missing compact numerical output')

    claims=json.loads((root/'outputs/summary/rq2_evidence_consolidation_v4_2/canonical_rq2_numerical_claims_v4_2.json').read_text())
    intervals=pd.read_csv(sensitivity/'canonical_window_origin_interval_summary_v1.csv',float_precision='round_trip')
    pools=pd.read_csv(sensitivity/'canonical_window_origin_pooled_summary_v1.csv',float_precision='round_trip')
    require(len(intervals)==19 and len(pools)==15,'Sensitivity summaries incomplete')
    anchor=root/'outputs/summary/pasture_spell_panel_v2/canonical_pas_tmp_origin_pooled_summary_v2.csv'
    primary=pd.read_csv(anchor,float_precision='round_trip').set_index('window').loc['primary_1985_2020']
    for k,v in primary.items():
        if isinstance(v,str):require(claims['P9A036']['canonical_primary'][k]==v,'Canonical primary label mismatch')
        else:close(claims['P9A036']['canonical_primary'][k],v,'Canonical primary value mismatch')
    require(claims['P9A035']['elapsed_years_to_interval_start']==15 and claims['P9A035']['interval_ordinal']==4,'Elapsed-time interpretation differs')
    require(claims['P9A036']['common_calendar']=='2000_2020','Calendar comparison differs')
    for b in [1985,1995,2000]:
        q=intervals.loc[intervals.baseline_year.eq(b)].sort_values('t0')
        first=q.iloc[0];close(first.initial_pct,100,'First interval construction',1e-8)
        close(claims['P9A035']['initial_pct_by_baseline_at_15_years'][str(b)],q.loc[q.elapsed_intervals.eq(3),'initial_pct'].iloc[0],'Lag-share claim mismatch')
        primary_cross=q.loc[q.diagnostic_interval.eq(0)&q.entry_pct.gt(50)]
        observed=q.loc[q.entry_pct.gt(50)]
        val=primary_cross.interval.iloc[0] if len(primary_cross) else None
        require(claims['P9A035']['first_primary_entry_crossing_by_baseline'][str(b)]==val,'Primary crossing claim mismatch')
        if b!=1985:require(observed.interval.iloc[0]=='2020_2025' and int(observed.diagnostic_interval.iloc[0])==1,'Later-window crossing not diagnostic')
        matched=pools.loc[pools.baseline_year.eq(b)&pools.comparison_window.eq('common_calendar_primary_2000_2020')].iloc[0]
        follow=pools.loc[pools.baseline_year.eq(b)&pools.comparison_window.eq('equal_followup_first_20_years')].iloc[0]
        close(claims['P9A036']['common_calendar_flow_ha'],matched.flow_pas_tmp_ha,'Matched denominator mismatch',1e-8)
        for name in ['initial','entry']:
            close(claims['P9A036'][f'common_calendar_{name}_pct_by_baseline'][str(b)],matched[name+'_pct'],'Calendar-share claim mismatch')
        close(claims['P9A036']['equal_followup_20years_initial_pct_by_baseline'][str(b)],follow.initial_pct,'Follow-up claim mismatch')
    text=(root/'manuscript/results/rq2_observed_pasture_spell_origins_v4_2.md').read_text()
    for n in ['46.91%','53.09%','38.10%','64.70%','78.07%','48.76%','59.90%','66.36%']:
        require(n in text,'Manuscript numerical statement missing: '+n)
    for phrase in ['100% initial by construction','not first-ever pasture establishment','not a process threshold','not deduplicated across intervals']:
        require(phrase in text,'Manuscript boundary missing: '+phrase)

    result={'status':'PASS','scope':'documentary_and_numerical_evidence_consolidation',
            'date':'2026-10-12','matrix_version':'v4.2','matrix_rows':35,
            'substantively_updated_findings':changed,'other_findings_substantively_unchanged':33,
            'P9A037_substantively_unchanged':True,'canonical_source_anchors_and_hashes_preserved':True,
            'qualified_statuses_preserved':True,'all_causal_claim_flags_zero':True,
            'historical_event_rows_and_bytes_preserved':8,'new_supplementary_event_rows':2,
            'supplementary_source_inventory_entries_authenticated':9,
            'numerical_claims_match_accepted_sources':True,
            'manuscript_numbers_and_key_boundaries_checked':True,
            'native_window_sensitivity_pass_reused':True,'new_native_execution_performed':False,
            'other_33_source_contents_reauthenticated_here':False,
            'remote_execution_script_identity_independently_verified':False,
            'matrix_csv_sha256':sha(root/CURRENT),'previous_matrix_csv_sha256':sha(root/PREVIOUS),
            'event_csv_sha256':sha(root/EVENT_NEW),'previous_event_csv_sha256':sha(root/EVENT_OLD),
            'native_sensitivity_validation_sha256':sha(sensitivity/'canonical_window_origin_sensitivity_validation_v1.json'),
            'source_inventory_sha256':sha(root/'config/rq2_evidence_v4_2_source_inventory_v1.csv'),
            'release_with_DOI_complete':False,
            'first_entry_reentry_decomposition_performed':False,
            'limits':['This is evidence consolidation, not a new native or causal analysis.',
                      'Canonical 1985 numerical evidence and all other finding contents are preserved.',
                      'The complete manuscript was not supplied; the manuscript file is a standalone proposed section.',
                      'Public DOI packaging remains pending.']}
    output=root/OUTPUT;output.parent.mkdir(parents=True,exist_ok=True)
    payload=(json.dumps(result,indent=2)+'\n').encode()
    require(not output.exists() or output.read_bytes()==payload,'Versioned validation output differs')
    if not output.exists():output.write_bytes(payload)
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    result=run(parser.parse_args().root)
    print('RQ2 EVIDENCE CONSOLIDATION v4.2 — PASS')
    print('35 findings; 2 updated; 33 unchanged. Historical events preserved; 2 appended.')
