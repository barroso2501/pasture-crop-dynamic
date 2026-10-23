"""Authenticate accepted bytes and independently audit the supplementary RQ2 v4.4 edition."""
from pathlib import Path
from array import array
import argparse,collections,csv,gzip,hashlib,io,json,math

BASE='outputs/validation/entry_reentry_v1/full'
OUT='outputs/summary/rq2_entry_reentry_v4_4'
VAL='outputs/validation/rq2_entry_reentry_v4_4'
FLOW=['flow_pas_tmp_ha','initial_ha','entry_ha','unresolved_ha','first_observed_entry_ha','observed_reentry_ha','prior_history_uncertain_ha']
STOCK=['stock0_pas_ha','initial_pas_stock_ha','entry_pas_stock_ha','unresolved_pas_stock_ha','first_observed_entry_pas_stock_ha','observed_reentry_pas_stock_ha','prior_history_uncertain_pas_stock_ha']
KINDS=['first_observed_entry','observed_reentry','prior_history_uncertain']
def require(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):
 with Path(p).open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f);return r.fieldnames,list(r)
def close(a,b,tol,msg):require(math.isfinite(float(a)) and abs(float(a)-float(b))<=tol,msg)
def check_ratio(actual,numerator,denominator):
 if denominator==0:require(actual=='','Zero-denominator fraction must be blank')
 else:close(actual,numerator/denominator,1e-13,'Ratio must divide summed areas with stated denominator')
def check_matrix_rows(fields,old,new):
 require(len(old)==len(new)==35,'Matrix population changed')
 require([r['finding_id'] for r in old]==[r['finding_id'] for r in new],'Finding IDs/order changed')
 changed=[]
 for a,b in zip(old,new):
  require(b['evidence_matrix_version'].endswith('v4.4'),'Wrong matrix edition')
  for k in ['source_relative_path','source_sha256','source_authenticated','evidence_status','causal_claim_flag']:
   require(a[k]==b[k],'Canonical anchor/status/causal field changed: '+k)
  if any(a[k]!=b[k] for k in fields if k!='evidence_matrix_version'):changed.append(b['finding_id'])
 require(changed==['P9A035','P9A036'],'Only P9A035/P9A036 may change substantive content')
 return changed
def check_event_bytes(old,new):
 require(new.startswith(old),'Historical event bytes changed')
 def parse(b):return list(csv.DictReader(io.StringIO(b.decode('utf-8-sig'),newline='')))
 a,b=parse(old),parse(new)
 require(len(a)==12 and len(b)==14 and b[:12]==a,'Event prefix/count changed')
 require(len({r['event_id'] for r in b})==14,'Duplicate event ID')
 require([r['finding_id'] for r in b[12:]]==['P9A035','P9A036'],'New event/finding mismatch')
 require(all(r['event_status']=='supplemented_by_validated_entry_reentry_decomposition' for r in b[12:]),'Event status promotion')

def run(root):
 root=Path(root)
 for filename in ['config/rq2_entry_reentry_v4_4_predecessor_pins_v1.json','config/rq2_entry_reentry_v4_4_implementation_pins_v1.json']:
  pins=json.loads((root/filename).read_text())
  for name,h in pins['sha256'].items():require(sha(root/name)==h,'Pinned bytes changed: '+name)
 native=json.loads((root/BASE/'canonical_entry_reentry_full_v1_validation.json').read_text())
 require(native['status']=='PASS' and native['cells']==24889 and native['rows']==199112,'Native acceptance population')
 require(native['full_domain_decomposition_complete'] and native['native_full_domain_auxiliary_age201_complete'],'Native component flags')
 require(native['execution_identity']['executed_script_sha256'] is None and native['execution_identity']['operator_attestation'] is None and not native['execution_identity']['independently_verified_remote_execution'],'Remote authentication scope changed')
 critical=json.loads((root/'config/entry_reentry_full_source_snapshots_v1.json').read_text())['sha256']
 for name,h in critical.items():require(sha(root/name)==h,'Original full critical source changed: '+name)
 inputs=root/'outputs/native/entry_reentry_v1/full';C=json.loads((root/'config/entry_reentry_full_v1.json').read_text())
 for name,h in native['input_sha256'].items():
  p=root/C['accepted_pilot_root']/C['accepted_pilot_validation'] if name=='accepted_pilot_validation' else root/'config/entry_reentry_full_source_snapshots_v1.json' if name=='critical_input_snapshot' else inputs/name
  require(sha(p)==h,'Accepted native input changed: '+name)
 # Full normalized panel remains compressed in the repository; authenticate the exact restored bytes without writing it.
 for name,h in native['output_sha256'].items():
  p=root/BASE/name
  if p.exists():require(sha(p)==h,'Accepted derived native product changed: '+name)
  else:
   require(name=='canonical_entry_reentry_full_v1_cells.csv','Missing accepted output: '+name)
   zipped=root/'data/entry_reentry_full_v1'/ (name+'.gz');digest=hashlib.sha256();count=0
   with gzip.open(zipped,'rb') as f:
    for block in iter(lambda:f.read(1024*1024),b''):digest.update(block);count+=len(block)
   require(digest.hexdigest()==h,'Compressed normalized panel does not restore accepted hash')
 # Reaggregate actual native cell/interval inputs independently of the new derivative builder.
 groups={t:{k:array('d') for k in FLOW+STOCK} for t in range(1985,2025,5)};seen=collections.defaultdict(set);errors=0
 for p in sorted(inputs.glob('canonical_entry_reentry_????_????_b??_v1.csv')):
  with p.open(encoding='utf-8-sig',newline='') as f:
   for x in csv.DictReader(f):
    t=int(x['t0']);key=x['cell_id'];require(key not in seen[t],'Duplicate raw cell/interval');seen[t].add(key)
    require(float(x['accepted_origin_mismatch_pixel_equivalents'])==0,'Native origin mismatch');errors+=1
    for k in FLOW+STOCK:groups[t][k].append(float(x[k]))
 require(all(len(s)==24889 for s in seen.values()) and len(seen)==8 and errors==199112,'Raw native interval inventory')
 _,source=read(root/BASE/'canonical_entry_reentry_full_v1_summary.csv');source={int(r['t0']):r for r in source}
 max_raw=0.
 for t,metrics in groups.items():
  for k,vals in metrics.items():
   actual=math.fsum(vals);ref=float(source[t][k]);close(actual,ref,1e-7,'Independent native area aggregate differs');max_raw=max(max_raw,abs(actual-ref))
 schema=json.loads((root/'config/entry_reentry_full_schema_v1.json').read_text());audit_n=0
 for p in sorted(inputs.glob('canonical_entry_reentry_history_audit_b??_v1.csv')):
  with p.open(encoding='utf-8-sig',newline='') as f:
   for x in csv.DictReader(f):
    require(all(float(x[k])==0 for k in schema['error_fields']),'Actual native history mismatch');audit_n+=1
 require(audit_n==24889,'Actual audit population')
 _,derived=read(root/OUT/'canonical_entry_reentry_interval_composition_v4_4.csv')
 require([int(r['t0']) for r in derived]==list(range(1985,2025,5)),'Derivative interval inventory')
 for r in derived:
  t=int(r['t0']);ref=source[t]
  require(int(r['diagnostic_interval'])==int(t==2020) and int(r['baseline_interval_by_construction'])==int(t==1985),'Interval flags')
  for k in FLOW+STOCK:close(r[k],float(ref[k]),0,'Copied native area changed')
  for kind in ['initial','entry','unresolved']+KINDS:check_ratio(r[kind+'_fraction_of_total_flow'],float(ref[kind+'_ha']),float(ref['flow_pas_tmp_ha']))
  for kind in KINDS:
   check_ratio(r[kind+'_fraction_of_entry_flow'],float(ref[kind+'_ha']),float(ref['entry_ha']))
   check_ratio(r[kind+'_fraction_of_entry_stock'],float(ref[kind+'_pas_stock_ha']),float(ref['entry_pas_stock_ha']))
  if t==1985:require(r['entry_denominator_status']=='undefined_zero_entry_flow_and_stock','Baseline missing-value reason')
 _,pools=read(root/OUT/'canonical_entry_reentry_pooled_composition_v4_4.csv')
 require([r['window'] for r in pools]==['primary_1985_2020','diagnostic_2020_2025','full_observed_1985_2025'],'Pooled windows')
 for r in pools:
  selected=[x for t,x in source.items() if t<2020] if r['window'].startswith('primary') else [source[2020]] if r['window'].startswith('diagnostic') else list(source.values())
  require(int(r['intervals'])==len(selected) and r['aggregation']=='sum_of_interval_conversion_areas_not_unique_area','Pool denominator/scope')
  totals={k:math.fsum(float(x[k]) for x in selected) for k in FLOW}
  for k,v in totals.items():close(r[k],v,0,'Pooled area differs')
  for kind in ['initial','entry','unresolved']+KINDS:check_ratio(r[kind+'_fraction_of_total_flow'],totals[kind+'_ha'],totals['flow_pas_tmp_ha'])
  for kind in KINDS:check_ratio(r[kind+'_fraction_of_entry_flow'],totals[kind+'_ha'],totals['entry_ha'])
  require(not any('stock' in k for k in r),'Pooled stock/exposure ratio fabricated')
 # Retain the canonical previous origin partition within its accepted aggregate tolerance.
 _,canonical=read(root/'outputs/summary/pasture_spell_panel_v2/canonical_pas_tmp_origin_interval_summary_v2.csv');max_canonical=0.
 for x in canonical:
  t=int(x['interval'].split('_')[0])
  for a,b in [('flow_pas_tmp_ha','flow_pas_tmp_ha'),('initial_ha','initial_ha'),('entry_ha','new_ha'),('unresolved_ha','unresolved_ha')]:
   delta=abs(float(source[t][a])-float(x[b]));require(delta<=.001,'Canonical origin/flow anchor changed');max_canonical=max(max_canonical,delta)
 fields,old=read(root/'outputs/summary/rq2_relative_conversion_v1/canonical_integrated_evidence_matrix_v4_3.csv')
 nf,new=read(root/OUT/'canonical_integrated_evidence_matrix_v4_4.csv');require(nf==fields,'Matrix schema');changed=check_matrix_rows(fields,old,new)
 old_events=(root/'outputs/validation/rq2_relative_conversion_v1/canonical_evidence_status_events_v5.csv').read_bytes();new_events=(root/VAL/'canonical_evidence_status_events_v6.csv').read_bytes();check_event_bytes(old_events,new_events)
 sf,old_inventory=read(root/'config/rq2_evidence_v4_3_source_inventory_v1.csv');_,inventory=read(root/'config/rq2_evidence_v4_4_source_inventory_v1.csv')
 require(inventory[:len(old_inventory)]==old_inventory and len(inventory)==21,'Previous supplemental inventory changed or new sources incomplete')
 for x in inventory:require(sha(root/x['source_relative_path'])==x['source_sha256'],'Source-to-claim inventory hash')
 status=json.loads((root/'config/plan009_followup_status_20261023_v1.json').read_text());comp=status['components']
 require(comp['coverage_entry_reentry_full']['status']=='ACCEPTED_FULL' and comp['coverage_auxiliary_age201_full']['status']=='ACCEPTED_FULL_FOR_COVERAGE_DERIVED_ENGINE','Accepted component status')
 require(comp['original_seeded_pixel_sampling_protocol']['status']=='NOT_CLAIMED_COMPLETED' and comp['public_age_v2_complete_numeric_validation']['status']=='NOT_PERFORMED','Assurance scope expanded')
 protocol=json.loads((root/'config/plan009_joint_native_followup_protocol_v1.json').read_text());require(protocol['status']=='PREPARED_NOT_EXECUTED','Historical protocol overwritten')
 uncertain=json.loads((root/comp['pas_conditioned_uncertain_pairs_full']['record']).read_text());require(uncertain['status']=='PASS' and uncertain['scientific_full_domain_complete'],'Uncertain-pair acceptance')
 claims=json.loads((root/OUT/'canonical_rq2_entry_reentry_claims_v4_4.json').read_text())
 require(claims['undefined_conditional_entry_intervals']==['1985_1990'] and not claims['primary_reentry_flow_fraction_monotonic_non_decreasing'],'Incorrect baseline/trend description')
 require(claims['first_observed_not_first_ever'] and not claims['pooled_stock_exposure_or_hazard_estimated'],'Claim boundary')
 manuscript=(root/'manuscript/results/rq2_observed_pasture_spell_origins_v4_4.md').read_text()
 for word in ['15.416026','84.583066','19.117876','32.488051','first-ever','not time-integrated exposure','set nesting','classification instability','undefined']:
  require(word in manuscript,'Manuscript omits numerical/boundary wording: '+word)
 artifacts=[OUT+'/'+n for n in ['canonical_entry_reentry_interval_composition_v4_4.csv','canonical_entry_reentry_pooled_composition_v4_4.csv','canonical_integrated_evidence_matrix_v4_4.csv','canonical_integrated_evidence_matrix_v4_4.md','canonical_rq2_entry_reentry_claims_v4_4.json','canonical_evidence_matrix_v4_3_to_v4_4_crosswalk_v1.csv']]+[VAL+'/canonical_evidence_status_events_v6.csv']
 result={'status':'PASS','date':'2026-10-23','scope':'supplementary_descriptive_incorporation_rq2_v4.4','matrix_rows':35,'substantively_updated_findings':changed,'other_substantive_findings_preserved':33,'previous_event_rows_preserved_byte_for_byte':12,'new_events':2,'total_events':14,'original_native_csvs_authenticated':73,'original_critical_source_pins_checked':len(critical),'native_cell_interval_records_independently_reaggregated':errors,'native_actual_history_rows_rechecked':audit_n,'native_actual_error_counter_values_zero':errors+audit_n*len(schema['error_fields']),'max_independent_raw_aggregate_difference_ha':max_raw,'max_canonical_interval_anchor_difference_ha':max_canonical,'source_to_claim_entries_checked':21,'interval_derivative_rows':8,'pooled_derivative_rows':3,'canonical_source_anchors_statuses_causal_flags_preserved':True,'all_original_full_derived_bytes_authenticated_including_lossless_compressed_panel':True,'no_new_native_gee_run':True,'operator_attestation_recorded':False,'public_age_asset_full_numeric_validation_claimed':False,'original_seeded_pixel_sampling_claimed_completed':False,'doi_or_release_readiness_claimed':False,'output_sha256':{n:sha(root/n) for n in artifacts},'limitations':['First observed since 1985 is not first-ever establishment.','Conditional entry-flow shares differ from total-flow shares and entry-stock shares.','Pool sums interval areas; no spatial deduplication or pooled stock-exposure ratio.','2020-2025 is diagnostic; primary reentry shares are not monotonic.','Native age201 assurance applies to the coverage-derived engine, not all numeric public-age values.','No new remote execution, independent event-raster comparison, causal effect or hazard estimate.']}
 path=root/VAL/'canonical_rq2_v4_4_validation_v1.json';path.parent.mkdir(parents=True,exist_ok=True);data=(json.dumps(result,indent=2)+'\n').encode()
 require(not path.exists() or path.read_bytes()==data,'Refusing different validation report')
 if not path.exists():path.write_bytes(data)
 return result

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);result=run(ap.parse_args().root)
 print(json.dumps({k:result[k] for k in ['status','matrix_rows','substantively_updated_findings','other_substantive_findings_preserved','native_cell_interval_records_independently_reaggregated','native_actual_error_counter_values_zero']},indent=2))
