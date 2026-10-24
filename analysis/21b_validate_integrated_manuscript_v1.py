"""Audit integrated-draft sources, claim coverage, plot data and explicit unfinished scope."""
from pathlib import Path
import argparse,collections,csv,hashlib,json,math,re,urllib.parse

def require(ok,message):
 if not ok:raise ValueError(message)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rows(p):
 with Path(p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def run(root):
 root=Path(root);config=root/'config/manuscript_integrated_v1';draft=root/'manuscript/integrated_v1'
 pins=json.loads((config/'baseline_pins_v1.json').read_text())
 for n,h in pins['sha256'].items():require(sha(root/n)==h,'Accepted source changed: '+n)
 implementation=json.loads((config/'draft_output_pins_v1.json').read_text())
 for n,h in implementation['sha256'].items():require(sha(root/n)==h,'Versioned draft/implementation changed: '+n)
 matrix_path='outputs/summary/rq2_entry_reentry_v4_4/canonical_integrated_evidence_matrix_v4_4.csv';matrix=rows(root/matrix_path);byid={x['finding_id']:x for x in matrix}
 require(len(matrix)==len(byid)==35,'Matrix population')
 require(collections.Counter(x['research_question'] for x in matrix)=={'RQ1':4,'RQ2':3,'RQ3':2,'RQ4':18,'RQ5':8},'Research-question coverage')
 require(all(x['causal_claim_flag']=='0' and x['evidence_matrix_version'].endswith('v4.4') for x in matrix),'Matrix status/causal edition changed')
 trace=rows(config/'claim_traceability_v1.csv');require(len(trace)==35 and {x['finding_id'] for x in trace}==set(byid),'Claim register incomplete')
 exact=0;fallback=0
 phase7_path='outputs/validation/phase7_biome_comparison_v1/canonical_phase7_biome_validation_v1.json';phase7=json.loads((root/phase7_path).read_text());require(phase7['validation_status']=='PASS','Phase 7 acceptance absent')
 for x in trace:
  old=byid[x['finding_id']]
  for a,b in [('evidence_status','evidence_status'),('main_result','main_result'),('numeric_evidence','numeric_evidence'),('interpretation_boundary','interpretation_boundary'),('canonical_anchor_as_recorded','source_relative_path'),('canonical_anchor_sha256_as_recorded','source_sha256')]:require(x[a]==old[b],'Finding content/anchor changed')
  require(x['primary_manuscript_home']=='analytical_manuscript' and x['allocation_status']=='proposed_not_stage0_scope_freeze','Allocation misrepresented as governance freeze')
  paths=x['resolved_support_paths'].split('|');hashes=x['resolved_support_sha256'].split('|');require(len(paths)==len(hashes),'Support list mismatch')
  for n,h in zip(paths,hashes):require(sha(root/n)==h,'Resolved support bytes changed')
  if x['canonical_anchor_found_by_hash']=='True':
   exact+=1;require(hashes==[old['source_sha256']],'Exact canonical hash mismatch')
  else:
   fallback+=1;require(x['finding_id'] in ['P9A018','P9A019','P9A020','P9A021'],'Undeclared missing canonical anchor')
   for n,h in zip(paths,hashes):require(h==phase7['outputs'][Path(n).name]['sha256'],'Numerical fallback not accepted Phase 7 output')
 require((exact,fallback)==(31,4),'Legacy-source resolution counts')
 # Recheck the biome arithmetic from accepted tables rather than relying only on the older matrix text.
 p7=root/'outputs/summary/phase7_biome_comparison_v1';process=rows(p7/'canonical_phase7_biome_process_summary_v1.csv');regional=rows(draft/'table_biome_process_totals_v1.csv')
 require(len(regional)==6,'Regional table population')
 for x in regional:
  actual=math.fsum(float(r['value_sum']) for r in process if r['boundary_scope']=='primary_assignment' and r['primary_biome']==x['primary_biome'] and r['metric']==x['metric'] and r['diagnostic_interval']=='0')
  require(actual==float(x['sum_interval_area_ha']),'Independent regional sum differs')
 audit=json.loads((config/'biome_direct_support_audit_v1.json').read_text());require(audit['status']=='PASS' and audit['legacy_narrative_anchor_missing'] and audit['current_matrix_unchanged'],'Biome exception hidden')
 cohort=rows(root/'outputs/validation/phase9_gap_resolution_v1/canonical_fixed_1985_pasture_cohort_summary_v1.csv');combined=[x for x in cohort if x['boundary_scope']=='combined_domain'];require(len(combined)==9,'Cohort date coverage')
 require(len({x['cohort_total_ha'] for x in combined})==1,'Fixed cohort denominator changed')
 for x in combined:
  total=math.fsum(float(x[k+'_share']) for k in ['nat','pas','tmp','oag','out','water','nodata','unexpected','masked'])
  require(abs(total-1)<1e-9,'Cohort plot partition does not close')
 y=next(x for x in combined if x['year']=='2020');require(round(float(y['pas_share'])*100,2)==63.13 and round(float(y['tmp_share'])*100,2)==19.94,'Cohort headline differs')
 document=(draft/'pasture_crop_dynamics_integrated_draft_v1.md').read_text()
 require(set(re.findall(r'P9A\d{3}',document))==set(byid),'Draft missing or inventing finding IDs')
 for section in ['## 2. Methods','## 3. Results','## 4. Discussion','### 3.1 RQ1','### 3.2 RQ2','### 3.3 RQ3','### 3.4 RQ4','### 3.7 RQ5']:
  require(section in document,'Integrated section missing: '+section)
 for term in ['6.51%','15.416026%','8.184336%','63.13%','19.94%','87.5%','120','192','48','not time-integrated exposure','first-ever','not a submission-ready','not a complete pixel partition','classification instability','universal','survival']:
  require(term in document,'Draft headline or boundary absent: '+term)
 bibliography=rows(config/'bibliography_verification_v1.csv');require(len(bibliography)==5 and len({x['doi'] for x in bibliography})==5,'Bibliography population/duplicates')
 body,reference_text=document.split('## References',1)
 uses={'Souza2020':'Souza Jr. et al., 2020','Macedo2012':'Macedo et al., 2012','Song2021':'Song et al., 2021','Anselin1995':'Anselin (1995)','StehmanFoody2019':'Stehman and Foody, 2019'}
 for x in bibliography:require(x['doi'] in reference_text and uses[x['key']] in body and x['access_scope'],'Orphan/unqualified bibliography entry')
 registry=rows(config/'figure_table_registry_v1.csv');require(len(registry)==13,'Display registry incomplete')
 main_fig=[x for x in registry if x['display_type']=='main_figure'];require(len(main_fig)==6,'Main-figure sequence')
 require({x['display_id'] for x in main_fig if x['readiness_status']=='planned_assembly'}=={'F1','F4'},'Unproduced main figures not declared')
 require(sum(x['readiness_status']=='draft_generated' for x in main_fig)==3 and sum(x['readiness_status']=='draft_existing_reuse' for x in main_fig)==1,'Produced/reused main figure states')
 for x in registry:
  require(sha(root/x['source_relative_path'])==x['source_sha256'],'Display source changed')
  if x['asset_relative_path']:require(sha(root/x['asset_relative_path'])==x['asset_sha256'],'Display asset changed')
  else:require(x['readiness_status'].startswith('planned'),'Missing asset mislabeled complete')
 fig_manifest=json.loads((root/'figures/manuscript_integrated_v1/figure_source_manifest_v1.json').read_text());require(not fig_manifest['new_analytical_fit'] and len(fig_manifest['outputs'])==9,'Figure scope/format count')
 for n,h in fig_manifest['sources'].items():require(sha(root/n)==h,'Figure source hash')
 for n,h in fig_manifest['outputs'].items():require(sha(root/n)==h,'Figure output hash')
 hh=rows(root/'outputs/validation/phase8e_maup_hh_cluster_v1/canonical_maup_hh_robustness_assessment_v1.csv');require(len(hh)==30 and sum(x['overall_prespecified_robustness_pass']=='True' for x in hh)==21,'HH figure count differs')
 for m,expected in [('replenishment_density_per_10kha',6),('net_cr_balance_density_per_10kha',6),('cr_balance_index',6),('consolidation_density_per_10kha',3),('nat_tmp_density_per_10kha',0)]:require(sum(x['overall_prespecified_robustness_pass']=='True' for x in hh if x['metric']==m)==expected,'Metric HH robustness differs')
 links=0
 for p in draft.glob('*.md'):
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
   if target.startswith(('http:','https:','#','mailto:')):continue
   path=urllib.parse.unquote(target.split('#')[0])
   if path:require((p.parent/path).exists(),'Local manuscript link broken: '+str(p)+' -> '+path);links+=1
 record={'status':'PASS_FOR_INTEGRATED_DRAFT','date':'2026-10-24','scope':'claim_source_coverage_and_descriptive_rendering_audit_not_new_native_or_spatial_inference','matrix_version':'v4.4','events_version':'v6','matrix_sha256_unchanged':sha(root/matrix_path),'accepted_findings':35,'RQ_coverage':dict(collections.Counter(x['research_question'] for x in matrix)),'direct_legacy_anchor_hash_matches':exact,'legacy_narrative_exceptions_with_authenticated_numeric_support':fallback,'accepted_project_sources_checked':len(pins['sha256']),'references_initially_verified':5,'reference_orphans':0,'main_figures_planned':6,'new_main_figures_generated':3,'main_existing_figure_reused':1,'main_figures_still_to_assemble':['F1','F4'],'new_figure_formats_verified':9,'main_tables_written':2,'display_registry_rows':13,'local_manuscript_links_checked':links,'new_gee_or_spatial_fit':False,'scientific_matrix_or_events_changed':False,'submission_ready':False,'stage0_governance_frozen':False,'doi_assigned':False,'word_count_main_draft':len(re.findall(r"\b[\w’-]+\b",document)),'limitations':['Text is a first integrated draft; this audit does not certify every scientific interpretation or replace author review.','Four historic Phase 7 narrative anchors are absent; accepted direct numerical support is checked and the exception remains explicit.','Initial bibliography is not a systematic or complete literature review; access scope is recorded.','F1/F4 and supplementary table assembly remain editorial tasks.','Public release, official dataset citation, licensing/attribution and contribution-based authorship are not finalized here.']}
 out=root/'outputs/validation/manuscript_integrated_v1';out.mkdir(parents=True,exist_ok=True);p=out/'integrated_manuscript_draft_validation_v1.json';data=(json.dumps(record,indent=2)+'\n').encode()
 require(not p.exists() or p.read_bytes()==data,'Refusing different versioned draft audit')
 if not p.exists():p.write_bytes(data)
 return record

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);r=run(ap.parse_args().root);print(json.dumps(r,indent=2))
