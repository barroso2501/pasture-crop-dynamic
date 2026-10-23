"""Synthetic 8-cell/8-interval integration tests. No temporary exports are scientific evidence."""
from pathlib import Path
import copy,csv,collections,hashlib,importlib.util,json,shutil,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('full_validator',ROOT/'analysis/20d_validate_entry_reentry_full_v1.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

def read(p):return list(v.csv_rows(p))
def write(p,rows,fields):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(v.csv_bytes(rows,fields))
def pins(root):
 files=[p for folder in ['config','analysis','gee','provenance'] for p in (root/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='entry_reentry_full_source_snapshots_v1.json']
 (root/'config/entry_reentry_full_source_snapshots_v1.json').write_text(json.dumps({'sha256':{str(p.relative_to(root)):v.sha(p) for p in files}},indent=2)+'\n')

def create_exports(root,folder):
 C=json.loads((root/'config/entry_reentry_full_v1.json').read_text());S=json.loads((root/'config/entry_reentry_full_schema_v1.json').read_text())
 p_root=root/C['accepted_pilot_root'];pilot={(r['cell_id'],r['t0']):r for r in read(p_root/'outputs/native/entry_reentry_v1/pilot_r2/canonical_entry_reentry_pilot_v1.csv')}
 pilot_audit={r['cell_id']:r for r in read(p_root/'outputs/native/entry_reentry_v1/pilot_r2/canonical_entry_reentry_history_audit_pilot_v1.csv')}
 groups={}
 for ref in read(root/'config/entry_reentry_full_reference_v1.csv'):
  row={k:ref[k] for k in ['cell_id','GRID_ID','source_batch_id','t0','t1','diagnostic_interval']}
  row.update(scope='full',output_version=C['version'],run_id=C['run_tag']+'_full')
  row.update({k:0 for k in S['area_fields']+S['cell_error_fields']});row['domain_ha']=next((float(p['domain_ha']) for p in pilot.values() if p['cell_id']==row['cell_id']),25000)
  for k in S['historical_comparison_fields']:row[k]=float(ref[k])
  for kind in ['initial','entry','unresolved']:
   for suffix in ['_ha','_pas_stock_ha']:row['control_'+kind+suffix]=row[kind+suffix]
  for kind,fraction in [('first_observed_entry',.35),('observed_reentry',.45),('prior_history_uncertain',.2)]:
   for suffix in ['_ha','_pas_stock_ha']:row[kind+suffix]=row['entry'+suffix]*(dict(first_observed_entry=.9,observed_reentry=.1,prior_history_uncertain=0)[kind] if row['cell_id'] in ['18081','32173'] else fraction)
  key=(row['cell_id'],row['t0'])
  if key in pilot:
   for k in S['area_fields']+S['cell_error_fields']:row[k]=float(pilot[key][k])
  groups.setdefault(f"canonical_entry_reentry_{row['t0']}_{row['t1']}_b{int(row['source_batch_id']):02d}_v1.csv",[]).append(row)
 for name,rows in groups.items():write(folder/name,rows,S['cell_fields'])
 for c in read(root/'config/entry_reentry_full_crosswalk_v1.csv'):
  row=dict(c,start_year=1985,end_year=2025,years_checked=41,scope='full',output_version=C['version'],run_id=C['run_tag']+'_full')
  row.update({k:0 for k in S['audit_count_fields']+S['error_fields']+S['boundary_fields']})
  row.update(history_support_pixel_equivalents=10.125,confirmed_entry_pixel_years=6.5,confirmed_reentry_pixel_years=2.5,first_observed_entry_pixel_years=3,prior_history_uncertain_entry_pixel_years=1)
  if c['cell_id'] in pilot_audit:
   for k in S['audit_count_fields']+S['error_fields']+S['boundary_fields']:row[k]=float(pilot_audit[c['cell_id']][k])
  write(folder/f"canonical_entry_reentry_history_audit_b{int(c['source_batch_id']):02d}_v1.csv",[row],S['audit_fields'])
 manifest=dict(scope='full',output_version=C['version'],run_id=C['run_tag']+'_full',source_script='20c_export_entry_reentry_full_v1.js',expected_cells=C['expected_cells'],expected_rows=C['expected_rows'],expected_audit_rows=C['expected_cells'],expected_cell_files=64,expected_audit_files=8,config_json=json.dumps(S['runtime_config']),coverage_band_count=41,coverage_bands_csv='|'.join(f'classification_{y}' for y in range(1985,2026)),native_projections_json=json.dumps({str(y):{'crs':C['crs'],'transform':C['crs_transform']} for y in range(1985,2026)}),audit_start_year=1985,audit_end_year=2025,audit_years_checked=41,runtime_grid_cells=C['expected_cells'])
 for b in C['expected_batches']:manifest[f'runtime_b{b:02d}_cells']=C['expected_batch_cells'][str(b)]
 write(folder/'canonical_entry_reentry_manifest_full_v1.csv',[manifest],S['manifest_fields'])

class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.template_temp=tempfile.TemporaryDirectory();cls.template=Path(cls.template_temp.name)/'root'
  shutil.copytree(ROOT,cls.template,ignore=lambda d,n:[x for x in n if x in ['__pycache__','entry_reentry_full_reference_v1.csv','entry_reentry_full_source_snapshots_v1.json','outputs']])
  # The accepted native pilot outputs are genuine immutable references, not generated test data.
  target=cls.template/'provenance/entry_reentry_pilot_r2/outputs'
  shutil.copytree(ROOT/'provenance/entry_reentry_pilot_r2/outputs',target)
  C=json.loads((ROOT/'config/entry_reentry_full_v1.json').read_text());S=json.loads((ROOT/'config/entry_reentry_full_schema_v1.json').read_text())
  cross=read(ROOT/'config/entry_reentry_full_crosswalk_v1.csv');selected={}
  for row in cross:selected.setdefault(row['source_batch_id'],row)
  for row in cross:
   if row['cell_id'] in ['18081','32173']:selected[row['source_batch_id']]=row
  ids={x['cell_id'] for x in selected.values()};reference=[r for r in v.csv_rows(ROOT/'config/entry_reentry_full_reference_v1.csv') if r['cell_id'] in ids]
  C.update(expected_cells=8,expected_rows=64,expected_batch_cells={str(b):1 for b in range(8)},software_test_fixture_only=True)
  C['reference_provenance']['data_source_rows']=dict(collections.Counter(r['data_source'] for r in reference));C['reference_provenance']['selected_rows']=64
  S['runtime_config']['expected_cells']=8
  (cls.template/'config/entry_reentry_full_v1.json').write_text(json.dumps(C,indent=2)+'\n');(cls.template/'config/entry_reentry_full_schema_v1.json').write_text(json.dumps(S,indent=2)+'\n')
  write(cls.template/'config/entry_reentry_full_crosswalk_v1.csv',sorted(selected.values(),key=lambda x:int(x['cell_id'])),['cell_id','GRID_ID','source_batch_id'])
  write(cls.template/'config/entry_reentry_full_reference_v1.csv',reference,list(reference[0]));pins(cls.template)
 @classmethod
 def tearDownClass(cls):cls.template_temp.cleanup()
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.base=Path(self.temp.name);self.root=self.base/'root';shutil.copytree(self.template,self.root)
  self.exports=self.base/'exports';self.exports.mkdir();self.output=self.base/'out';create_exports(self.root,self.exports)
  self.C=json.loads((self.root/'config/entry_reentry_full_v1.json').read_text());self.S=json.loads((self.root/'config/entry_reentry_full_schema_v1.json').read_text())
 def tearDown(self):self.temp.cleanup()
 def validate(self):return v.validate(self.root,self.exports,self.output)
 def change(self,name,fn,fields=None):
  p=self.exports/name;r=read(p);fn(r);write(p,r,fields or list(r[0]))
 def cells(self,fn,t0=2015,b=0):self.change(f'canonical_entry_reentry_{t0}_{t0+5}_b{b:02d}_v1.csv',fn,self.S['cell_fields'])
 def audit(self,fn,b=0):self.change(f'canonical_entry_reentry_history_audit_b{b:02d}_v1.csv',fn,self.S['audit_fields'])
 def manifest(self,fn):self.change('canonical_entry_reentry_manifest_full_v1.csv',fn,self.S['manifest_fields'])
 def rejected(self):
  with self.assertRaises((ValueError,KeyError,TypeError,IndexError)):self.validate()
 def test_complete_full_validation_and_immutable_reuse(self):
  r=self.validate();self.assertEqual(r['rows'],64);self.assertTrue(r['full_domain_decomposition_complete']);self.assertTrue(r['native_full_domain_auxiliary_age201_complete']);self.assertEqual(r,self.validate())
  summary=read(self.output/'canonical_entry_reentry_full_v1_summary.csv');self.assertEqual(summary[0]['first_observed_entry_fraction_of_entry_flow'],'')
 def test_missing_file(self):
  (self.exports/'canonical_entry_reentry_history_audit_b07_v1.csv').unlink();self.rejected()
 def test_extra_retry_csv(self):
  (self.exports/'retry.csv').write_text('x\n1\n');self.rejected()
 def test_duplicate_cell(self):self.cells(lambda r:r.append(copy.deepcopy(r[0])));self.rejected()
 def test_empty_batch(self):self.cells(lambda r:r.clear());self.rejected()
 def test_foreign_cell(self):self.cells(lambda r:r[0].update(cell_id='999999'));self.rejected()
 def test_wrong_grid(self):self.cells(lambda r:r[0].update(GRID_ID='wrong'));self.rejected()
 def test_wrong_batch(self):self.cells(lambda r:r[0].update(source_batch_id=7));self.rejected()
 def test_wrong_interval(self):self.cells(lambda r:r[0].update(t0=2010));self.rejected()
 def test_wrong_diagnostic(self):self.cells(lambda r:r[0].update(diagnostic_interval=0),t0=2020);self.rejected()
 def test_pixel_origin_error(self):self.cells(lambda r:r[0].update(accepted_origin_mismatch_pixel_equivalents=.0001));self.rejected()
 def test_auxiliary_partition(self):self.cells(lambda r:r[0].update(first_observed_entry_ha=float(r[0]['first_observed_entry_ha'])+1));self.rejected()
 def test_nan(self):self.cells(lambda r:r[0].update(domain_ha='NaN'));self.rejected()
 def test_negative(self):self.cells(lambda r:r[0].update(observed_reentry_ha=-1));self.rejected()
 def test_historical_control(self):self.cells(lambda r:r[0].update(control_entry_ha=float(r[0]['control_entry_ha'])+1));self.rejected()
 def test_baseline_construction(self):self.cells(lambda r:r[0].update(entry_ha=.0001),t0=1985);self.rejected()
 def test_aggregate_stricter_than_cell_tolerance(self):
  def change(rows):
   for k in ['initial_ha','control_initial_ha','flow_pas_tmp_ha','initial_pas_stock_ha','control_initial_pas_stock_ha','stock0_pas_ha']:rows[0][k]=float(rows[0][k])+.002
  for b in range(8):self.cells(change,b=b)
  self.rejected()
 def test_history_age201_error(self):self.audit(lambda r:r[0].update(reentry_age201_error_pixel_years=.001));self.rejected()
 def test_history_frozen_label_error(self):self.audit(lambda r:r[0].update(frozen_label_error_pixel_years=.001));self.rejected()
 def test_history_support(self):self.audit(lambda r:r[0].update(history_support_pixel_equivalents=0));self.rejected()
 def test_history_partition(self):self.audit(lambda r:r[0].update(confirmed_entry_pixel_years=7));self.rejected()
 def test_history_years(self):self.audit(lambda r:r[0].update(years_checked=40));self.rejected()
 def test_positive_stock_without_event_support(self):self.audit(lambda r:r[0].update(confirmed_entry_pixel_years=0,confirmed_reentry_pixel_years=0,first_observed_entry_pixel_years=0,prior_history_uncertain_entry_pixel_years=0),b=1);self.rejected()
 def test_pilot_auxiliary_flow_identity(self):
  def change(rows):
   r=rows[0];delta=min(float(r['first_observed_entry_ha']),float(r['observed_reentry_pas_stock_ha'])-float(r['observed_reentry_ha']))/2
   self.assertGreater(delta,.01);r['first_observed_entry_ha']=float(r['first_observed_entry_ha'])-delta;r['observed_reentry_ha']=float(r['observed_reentry_ha'])+delta
  self.cells(change,b=1);self.rejected()
 def test_pilot_history_boundary(self):self.audit(lambda r:r[0].update(entry_2024_ha=float(r[0]['entry_2024_ha'])+1),b=1);self.rejected()
 def test_run_identity(self):self.cells(lambda r:r[0].update(run_id='er1_20261021_r2_pilot'));self.rejected()
 def test_projection(self):
  def change(r):
   d=json.loads(r[0]['native_projections_json']);d['1999']['transform'][0]=.01;r[0]['native_projections_json']=json.dumps(d)
  self.manifest(change);self.rejected()
 def test_runtime(self):
  def change(r):
   d=json.loads(r[0]['config_json']);d['valid_source_codes'].remove(1);r[0]['config_json']=json.dumps(d)
  self.manifest(change);self.rejected()
 def test_manifest_runtime_grid(self):self.manifest(lambda r:r[0].update(runtime_grid_cells=9));self.rejected()
 def test_manifest_batch_size(self):self.manifest(lambda r:r[0].update(runtime_b07_cells=2));self.rejected()
 def test_reference_tampering(self):
  p=self.root/'config/entry_reentry_full_reference_v1.csv';p.write_bytes(p.read_bytes()+b'\n');self.rejected()
 def test_step_compatibility_beyond_hashes(self):
  p=self.root/'gee/20c_export_entry_reentry_full_v1.js';p.write_text(p.read_text().replace('.where(initial,100)','.where(initial,101)',1));pins(self.root);self.rejected()
 def test_immutable_output_refusal(self):
  self.validate();(self.output/'canonical_entry_reentry_full_v1_summary.csv').write_text('changed');self.rejected()

if __name__=='__main__':unittest.main(verbosity=2)
