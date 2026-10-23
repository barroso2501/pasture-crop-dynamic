"""Derive supplementary RQ2 entry/re-entry tables and matrix v4.4; preserve native products."""
from pathlib import Path
import argparse,csv,hashlib,io,json,math

SUMMARY='outputs/validation/entry_reentry_v1/full/canonical_entry_reentry_full_v1_summary.csv'
NATIVE_REPORT='outputs/validation/entry_reentry_v1/full/canonical_entry_reentry_full_v1_validation.json'
OLD_MATRIX='outputs/summary/rq2_relative_conversion_v1/canonical_integrated_evidence_matrix_v4_3.csv'
OLD_EVENTS='outputs/validation/rq2_relative_conversion_v1/canonical_evidence_status_events_v5.csv'
OUT='outputs/summary/rq2_entry_reentry_v4_4'
VAL='outputs/validation/rq2_entry_reentry_v4_4'
KINDS=['first_observed_entry','observed_reentry','prior_history_uncertain']
FLOW=['flow_pas_tmp_ha','initial_ha','entry_ha','unresolved_ha']+[k+'_ha' for k in KINDS]
STOCK=['stock0_pas_ha','initial_pas_stock_ha','entry_pas_stock_ha','unresolved_pas_stock_ha']+[k+'_pas_stock_ha' for k in KINDS]

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):
 with Path(p).open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f);return r.fieldnames,list(r)
def payload(rows,fields=None):
 f=io.StringIO(newline='');w=csv.DictWriter(f,fieldnames=fields or list(rows[0]),lineterminator='\r\n');w.writeheader();w.writerows(rows)
 return f.getvalue().encode('utf-8-sig')
def save(root,name,data):
 p=root/name;p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists() and p.read_bytes()!=data:raise ValueError('Refusing different versioned output: '+name)
 if not p.exists():p.write_bytes(data)
def fraction(n,d):return n/d if d>0 else ''
def md_matrix(rows):
 lines=['# Integrated evidence matrix v4.4','','2026-10-23. 35 finding IDs retained; only P9A035/P9A036 supplemented. Qualified statuses, causal flags, canonical anchors and prior evidence retained. Supplemental chronology uses the accepted 1985-boundary full-domain exports.','']
 for r in rows:
  lines.extend(['## '+r['finding_id']+' — '+r['research_question']+' / '+r['topic'],'',r['main_result'],'','**Numerical evidence:** '+r['numeric_evidence'],'','**Interpretation boundary:** '+r['interpretation_boundary'],'','**Evidence status:** '+r['evidence_status']+'; **causal flag:** '+r['causal_claim_flag']+'.','', '**Canonical source:** `'+r['source_relative_path']+'`; SHA256 `'+r['source_sha256']+'`.','', '**Source locator:** '+r['source_locator'],''])
 return ('\n'.join(lines)+'\n').encode()

def derive(root):
 root=Path(root)
 pins=json.loads((root/'config/rq2_entry_reentry_v4_4_predecessor_pins_v1.json').read_text())
 for n,h in pins['sha256'].items():
  if sha(root/n)!=h:raise ValueError('Predecessor changed: '+n)
 report=json.loads((root/NATIVE_REPORT).read_text())
 if report['status']!='PASS' or not report['full_domain_decomposition_complete'] or not report['native_full_domain_auxiliary_age201_complete']:raise ValueError('Full native acceptance absent')
 if sha(root/SUMMARY)!=report['output_sha256'][Path(SUMMARY).name]:raise ValueError('Accepted summary changed')
 _,source=read(root/SUMMARY);intervals=[]
 for x in source:
  r={k:int(x[k]) for k in ['t0','t1','cells','diagnostic_interval','baseline_interval_by_construction']}
  r['interval']=f"{r['t0']}_{r['t1']}";r['scope']='canonical_24889_cells_boundary1985'
  r.update({k:float(x[k]) for k in FLOW+STOCK})
  for k in ['initial','entry','unresolved']+KINDS:r[k+'_fraction_of_total_flow']=fraction(r[k+'_ha'],r['flow_pas_tmp_ha'])
  for kind in KINDS:
   r[kind+'_fraction_of_entry_flow']=fraction(r[kind+'_ha'],r['entry_ha'])
   r[kind+'_fraction_of_entry_stock']=fraction(r[kind+'_pas_stock_ha'],r['entry_pas_stock_ha'])
  r['entry_denominator_status']='undefined_zero_entry_flow_and_stock' if not r['entry_ha'] and not r['entry_pas_stock_ha'] else 'positive_entry_flow_and_stock'
  intervals.append(r)
 pools=[]
 for label,selected,diagnostic in [('primary_1985_2020',[r for r in intervals if not r['diagnostic_interval']],0),('diagnostic_2020_2025',[r for r in intervals if r['diagnostic_interval']],1),('full_observed_1985_2025',intervals,1)]:
  r={'window':label,'intervals':len(selected),'includes_diagnostic_interval':diagnostic,'aggregation':'sum_of_interval_conversion_areas_not_unique_area'}
  r.update({k:math.fsum(x[k] for x in selected) for k in FLOW})
  for kind in ['initial','entry','unresolved']+KINDS:r[kind+'_fraction_of_total_flow']=fraction(r[kind+'_ha'],r['flow_pas_tmp_ha'])
  for kind in KINDS:r[kind+'_fraction_of_entry_flow']=fraction(r[kind+'_ha'],r['entry_ha'])
  pools.append(r)
 save(root,OUT+'/canonical_entry_reentry_interval_composition_v4_4.csv',payload(intervals))
 save(root,OUT+'/canonical_entry_reentry_pooled_composition_v4_4.csv',payload(pools))
 primary=pools[0];last=intervals[-2];diag=intervals[-1]
 claims={'date':'2026-10-23','boundary_year':1985,'cells':24889,'primary_intervals':7,'diagnostic_interval':[2020,2025],
         'primary':primary,'last_primary':last,'diagnostic':diag,
         'primary_reentry_flow_fraction_monotonic_non_decreasing':all(b>=a for a,b in zip([r['observed_reentry_fraction_of_entry_flow'] for r in intervals[1:7]],[r['observed_reentry_fraction_of_entry_flow'] for r in intervals[2:7]])),
         'undefined_conditional_entry_intervals':[r['interval'] for r in intervals if r['entry_denominator_status'].startswith('undefined')],
         'first_observed_not_first_ever':True,'pooled_stock_exposure_or_hazard_estimated':False,
         'source_summary_sha256':sha(root/SUMMARY),'native_full_validation_sha256':sha(root/NATIVE_REPORT)}
 save(root,OUT+'/canonical_rq2_entry_reentry_claims_v4_4.json',(json.dumps(claims,indent=2,allow_nan=False)+'\n').encode())
 fields,old=read(root/OLD_MATRIX);new=[];cross=[]
 for x in old:
  r=dict(x);r['evidence_matrix_version']='phase9-decision024-corrected-evidence-matrix-v4.4'
  if r['finding_id'] in ['P9A035','P9A036']:
   if r['finding_id']=='P9A035':
    r['main_result']+=' Full-domain chronology now separates first observed entry, observed re-entry and uncertain prior history within confirmed entry; the conditional re-entry share is descriptive and not monotonic over primary intervals.'
    r['numeric_evidence']+=f" Re-entry / confirmed-entry flow: 2.354410% in 1990-1995, {100*last['observed_reentry_fraction_of_entry_flow']:.6f}% in 2015-2020 and {100*diag['observed_reentry_fraction_of_entry_flow']:.6f}% in diagnostic 2020-2025. Corresponding last-primary and diagnostic re-entry / entry-stock shares: {100*last['observed_reentry_fraction_of_entry_stock']:.6f}% and {100*diag['observed_reentry_fraction_of_entry_stock']:.6f}%. The 1985-1990 conditional entry denominators are zero and fractions undefined."
   else:
    r['main_result']+=' The accepted confirmed-entry component is now subdivided: first observed entry accounts for 84.58% and observed re-entry for 15.42% of summed primary entry flow, with prior-history uncertainty retained separately.'
    r['numeric_evidence']+=f" Within primary entry flow ({primary['entry_ha']:.6f} ha), first observed = {primary['first_observed_entry_ha']:.6f} ha ({100*primary['first_observed_entry_fraction_of_entry_flow']:.6f}%); re-entry = {primary['observed_reentry_ha']:.6f} ha ({100*primary['observed_reentry_fraction_of_entry_flow']:.6f}%); prior-history uncertain = {primary['prior_history_uncertain_ha']:.6f} ha ({100*primary['prior_history_uncertain_fraction_of_entry_flow']:.9f}%). Relative to all primary PAS-to-TMP flow, first observed and re-entry are {100*primary['first_observed_entry_fraction_of_total_flow']:.6f}% and {100*primary['observed_reentry_fraction_of_total_flow']:.6f}%."
   r['interpretation_boundary']+=' First observed entry requires no earlier observed PAS and complete valid pre-entry coverage since 1985; it is not first-ever establishment. Re-entry requires any earlier observed PAS, and the label is frozen at entry. Prior-history uncertainty after a confirmed nonPAS reset differs from unresolved current-spell origin. Earlier PAS can identify re-entry despite intervening gaps; gaps alone never establish an exit or a new confirmed entry. Longer observable history and changing stock/cohort composition can change subclass shares; no inferential trend, renewal model, physical land-use-cycle identification or causal claim follows. Classification instability can contribute to observed recurrence. The auxiliary age-201 checks concern coverage-derived code, not complete numeric validation of the public pasture-age v2 asset.'
   r['source_id']+='_entry_reentry_full_v1'
   r['source_locator']+=' Entry/re-entry supplementary sources and derivatives: config/rq2_evidence_v4_4_source_inventory_v1.csv#'+r['finding_id']
   r['robustness_status']='window_boundary_sensitive_with_stock_normalization_and_validated_entry_reentry_decomposition'
  changed=any(r[k]!=x[k] for k in fields if k!='evidence_matrix_version')
  cross.append({'finding_id':r['finding_id'],'substantive_change':int(changed),'previous_version':'v4.3','current_version':'v4.4','canonical_source_unchanged':int(r['source_relative_path']==x['source_relative_path'] and r['source_sha256']==x['source_sha256']),'status_unchanged':int(r['evidence_status']==x['evidence_status'])})
  new.append(r)
 save(root,OUT+'/canonical_integrated_evidence_matrix_v4_4.csv',payload(new,fields))
 save(root,OUT+'/canonical_integrated_evidence_matrix_v4_4.md',md_matrix(new))
 save(root,OUT+'/canonical_evidence_matrix_v4_3_to_v4_4_crosswalk_v1.csv',payload(cross))
 ef,events=read(root/OLD_EVENTS);added=[]
 for finding in ['P9A035','P9A036']:
  added.append(dict(event_id=finding+'-ENTRY-REENTRY-20261023',finding_id=finding,event_status='supplemented_by_validated_entry_reentry_decomposition',effective_date='2026-10-23',reason='Accepted full-domain coverage-derived entry chronology incorporated into matrix v4.4. Conditional denominators, prior-history uncertainty and first-observed qualification retained; canonical anchors and qualified status unchanged.',governing_record='docs/results/rq2_entry_reentry_incorporation_v4_4.md',rescission_criteria='Not a suspension, rescission or status promotion; append-only supplementary descriptive evidence.',source_version='canonical_integrated_evidence_matrix_v4_4',validation_record=VAL+'/canonical_rq2_v4_4_validation_v1.json'))
 f=io.StringIO(newline='');w=csv.DictWriter(f,fieldnames=ef,quoting=csv.QUOTE_ALL,lineterminator='\r\n');w.writerows(added)
 save(root,VAL+'/canonical_evidence_status_events_v6.csv',(root/OLD_EVENTS).read_bytes()+f.getvalue().encode())
 sf,inventory=read(root/'config/rq2_evidence_v4_3_source_inventory_v1.csv')
 for finding in ['P9A035','P9A036']:
  for name,role,scope in [(SUMMARY,'supplemental_numerical','Eight accepted interval stock/flow partitions, canonical boundary 1985'),(NATIVE_REPORT,'execution_validation','Unchanged accepted full native exports and preserved pilot'),(OUT+'/canonical_entry_reentry_interval_composition_v4_4.csv','derived_numerical','Explicit interval total/entry-flow/entry-stock denominators'),(OUT+'/canonical_entry_reentry_pooled_composition_v4_4.csv','derived_numerical','Seven primary interval-area sums, separate diagnostic/full windows')]:
   inventory.append(dict(finding_id=finding,source_role=role,source_relative_path=name,source_sha256=sha(root/name),bytes=(root/name).stat().st_size,claim_scope=scope))
 save(root,'config/rq2_evidence_v4_4_source_inventory_v1.csv',payload(inventory,sf))
 uncertain='outputs/validation/uncertain_pair_crosstab_v1/full/canonical_uncertain_pairs_full_v1_validation.json'
 status={'date':'2026-10-23','version':'plan009-current-followup-status-v1','matrix_version':'v4.4','events_version':'v6','historical_protocol_unchanged':'config/plan009_joint_native_followup_protocol_v1.json',
         'historical_protocol_status_not_rewritten':True,
         'components':{
          'coverage_entry_reentry_full':{'status':'ACCEPTED_FULL','cells':24889,'rows':199112,'record':NATIVE_REPORT,'sha256':sha(root/NATIVE_REPORT)},
          'coverage_auxiliary_age201_full':{'status':'ACCEPTED_FULL_FOR_COVERAGE_DERIVED_ENGINE','record':NATIVE_REPORT,'sha256':sha(root/NATIVE_REPORT),'public_age_asset_full_numeric_validation':False},
          'pas_conditioned_uncertain_pairs_full':{'status':'ACCEPTED_FULL','cells':24889,'rows':49778,'record':uncertain,'sha256':sha(root/uncertain)},
          'original_seeded_pixel_sampling_protocol':{'status':'NOT_CLAIMED_COMPLETED','reason':'Full-domain aggregate native invariants and fixtures were accepted; the separate proposed seeded annual-pixel sample was not supplied and is not retroactively declared executed.'},
          'public_age_v2_complete_numeric_validation':{'status':'NOT_PERFORMED','reason':'Separate 21,869-cell targeted coding audit does not validate every numeric age or migrate canonical accounting.'},
          'remote_executed_text_attestation':{'status':'NOT_SUPPLIED','executed_script_sha256':None,'operator_attestation':None},
          'public_data_release':{'status':'NOT_DECLARED_READY','doi_assigned':False,'reason':'Earlier partial release inventory and byte-check record retain their dated scope; no new release/DOI verification in this update.'}},
         'no_new_gee_execution_this_update':True,'no_new_boundary_event_raster_comparison_this_update':True,'matrix_status_promotion':False}
 save(root,'config/plan009_followup_status_20261023_v1.json',(json.dumps(status,indent=2)+'\n').encode())
 return {'status':'DERIVED','interval_rows':len(intervals),'pooled_rows':len(pools),'matrix_rows':len(new),'events':len(events)+len(added)}

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);print(json.dumps(derive(ap.parse_args().root),indent=2))
