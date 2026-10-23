"""Synthetic file integration only. Test exports/results live in TemporaryDirectory."""
import copy
import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('entry_validator',ROOT/'analysis/20b_validate_entry_reentry_pilot_v1.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
C=json.loads((ROOT/'config/entry_reentry_v1.json').read_text())
S=json.loads((ROOT/'config/entry_reentry_schema_v1.json').read_text())
F=json.loads((ROOT/'config/entry_reentry_native_cases_v1.json').read_text())

def write(path,rows,fields): path.write_bytes(v.csv_bytes(rows,fields))

def create_exports(folder):
    ref=v.load_csv(ROOT/'config/entry_reentry_pilot_reference_v1.csv')
    rows=[]
    meta=dict(scope='pilot',output_version=C['version'],run_id=C['run_tag']+'_pilot')
    for x in ref:
        row={k:x[k] for k in ['cell_id','GRID_ID','source_batch_id','t0','t1','diagnostic_interval']}
        row.update(meta)
        row.update({k:0 for k in S['area_fields']+S['cell_error_fields']})
        for k in S['historical_comparison_fields']: row[k]=float(x[k])
        row['domain_ha']=25000.0
        for kind in ['initial','entry','unresolved']:
            for suffix in ['_ha','_pas_stock_ha']: row['control_'+kind+suffix]=row[kind+suffix]
        for name,fraction in [('first_observed_entry',.4),('observed_reentry',.4),('prior_history_uncertain',.2)]:
            row[name+'_ha']=row['entry_ha']*fraction
            row[name+'_pas_stock_ha']=row['entry_pas_stock_ha']*fraction
        rows.append(row)
    write(folder/S['filenames']['cells'],rows,S['cell_fields'])
    audit=[]
    for c in C['pilot_cells']:
        r=dict(c,**meta,start_year=1985,end_year=2025,years_checked=41)
        r.update({k:0 for k in S['audit_count_fields']+S['error_fields']+S['boundary_fields']})
        r.update(history_support_pixel_equivalents=10.125,confirmed_entry_pixel_years=6.5,
                 confirmed_reentry_pixel_years=2.5,first_observed_entry_pixel_years=3,prior_history_uncertain_entry_pixel_years=1)
        audit.append(r)
    write(folder/S['filenames']['audit'],audit,S['audit_fields'])
    native=[]
    for f in F:
        r=dict(case_id=f['case_id'],start_year=f['start_year'],end_year=f['start_year']+len(f['values'])-1,steps=len(f['values']),
               scope='native_synthetic',output_version=C['version'],run_id=C['run_tag']+'_pilot_native_synthetic',
               expected_final_state=f['expected_state'][-1],expected_final_age=f['expected_age'][-1],
               expected_final_kind=f['expected_entry_kind'][-1],expected_final_count=f['expected_confirmed_entry_count'][-1],
               expected_final_entry_year=f['expected_entry_year'][-1],test_pixel_equivalents=10.125)
        r.update({k:0 for k in S['native_error_fields']});native.append(r)
    write(folder/S['filenames']['native'],native,S['native_fields'])
    m=dict(meta,source_script='20a_export_entry_reentry_pilot_v1.js',expected_cells=2,expected_rows=4,expected_audit_rows=2,
           expected_native_cases=len(F),expected_native_steps=sum(len(f['values']) for f in F),
           config_json=json.dumps(S['runtime_config']),coverage_band_count=41,
           coverage_bands_csv='|'.join(f'classification_{y}' for y in range(1985,2026)),
           native_projections_json=json.dumps({str(y):{'crs':C['crs'],'transform':C['crs_transform']} for y in range(1985,2026)}),
           audit_start_year=1985,audit_end_year=2025,audit_years_checked=41)
    write(folder/S['filenames']['manifest'],[m],S['manifest_fields'])

class Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.base=Path(self.temp.name)
        self.exports=self.base/'exports';self.exports.mkdir();self.output=self.base/'output';create_exports(self.exports)
    def tearDown(self): self.temp.cleanup()
    def validate(self): return v.validate(ROOT,self.exports,self.output)
    def mutate(self,kind,callback):
        p=self.exports/S['filenames'][kind];rows=v.load_csv(p);callback(rows);write(p,rows,{'cells':S['cell_fields'],'audit':S['audit_fields'],'native':S['native_fields'],'manifest':S['manifest_fields']}[kind])
    def rejected(self):
        with self.assertRaises((ValueError,KeyError,TypeError)): self.validate()
    def test_valid_and_immutable_reuse(self):
        r=self.validate();self.assertEqual(r['status'],'PASS');self.assertFalse(r['full_domain_decomposition_complete']);self.assertEqual(r,self.validate())
    def test_missing_file(self):
        (self.exports/S['filenames']['audit']).unlink();self.rejected()
    def test_extra_csv(self):
        (self.exports/'retry.csv').write_text('x\n1\n');self.rejected()
    def test_duplicate_cell(self):
        self.mutate('cells',lambda r:r.append(copy.deepcopy(r[0])));self.rejected()
    def test_missing_interval(self):
        self.mutate('cells',lambda r:r.pop());self.rejected()
    def test_reject_r1_run_identity(self):
        self.mutate('cells',lambda r:r[0].update(run_id='er1_20261021_pilot'));self.rejected()
    def test_wrong_grid(self):
        self.mutate('cells',lambda r:r[0].update(GRID_ID='wrong'));self.rejected()
    def test_wrong_batch(self):
        self.mutate('cells',lambda r:r[0].update(source_batch_id=7));self.rejected()
    def test_wrong_diagnostic(self):
        self.mutate('cells',lambda r:r[0].update(diagnostic_interval=1));self.rejected()
    def test_partition_failure(self):
        self.mutate('cells',lambda r:r[0].update(first_observed_entry_ha=float(r[0]['first_observed_entry_ha'])+1));self.rejected()
    def test_origin_reference_mismatch(self):
        self.mutate('cells',lambda r:r[0].update(accepted_origin_mismatch_pixel_equivalents=.00001));self.rejected()
    def test_negative(self):
        self.mutate('cells',lambda r:r[0].update(observed_reentry_ha=-1));self.rejected()
    def test_nan(self):
        self.mutate('cells',lambda r:r[0].update(domain_ha='nan'));self.rejected()
    def test_historical_mismatch_with_internal_closure(self):
        def change(rows):
            r=rows[0]
            for k in ['flow_pas_tmp_ha','initial_ha','control_initial_ha']:r[k]=float(r[k])+1
        self.mutate('cells',change);self.rejected()
    def test_flow_exceeds_stock(self):
        def change(rows):
            r=rows[0];entry=float(r['entry_ha'])
            r['first_observed_entry_ha']=entry;r['observed_reentry_ha']=0;r['prior_history_uncertain_ha']=0
            r['first_observed_entry_pas_stock_ha']=0;r['observed_reentry_pas_stock_ha']=float(r['entry_pas_stock_ha']);r['prior_history_uncertain_pas_stock_ha']=0
        self.mutate('cells',change);self.rejected()
    def test_age201_native_error(self):
        self.mutate('native',lambda r:r[0].update(entry_age201_error_pixel_years=1));self.rejected()
    def test_native_expectation_tampering(self):
        self.mutate('native',lambda r:r[0].update(expected_final_age=201));self.rejected()
    def test_native_zero_support(self):
        self.mutate('native',lambda r:r[0].update(test_pixel_equivalents=0));self.rejected()
    def test_native_fixture_missing(self):
        self.mutate('native',lambda r:r.pop());self.rejected()
    def test_native_fixture_duplicate(self):
        self.mutate('native',lambda r:r.append(copy.deepcopy(r[0])));self.rejected()
    def test_real_frozen_label_error(self):
        self.mutate('audit',lambda r:r[0].update(frozen_label_error_pixel_years=.01));self.rejected()
    def test_real_age201_error(self):
        self.mutate('audit',lambda r:r[0].update(reentry_age201_error_pixel_years=.01));self.rejected()
    def test_missing_history_audit(self):
        self.mutate('audit',lambda r:r.pop());self.rejected()
    def test_zero_history_for_positive_entry_stock(self):
        self.mutate('audit',lambda r:r[0].update(confirmed_entry_pixel_years=0,confirmed_reentry_pixel_years=0,first_observed_entry_pixel_years=0,prior_history_uncertain_entry_pixel_years=0));self.rejected()
    def test_audit_year_coverage(self):
        self.mutate('audit',lambda r:r[0].update(end_year=2024));self.rejected()
    def test_runtime_mismatch(self):
        def change(rows):
            c=json.loads(rows[0]['config_json']);c['valid_source_codes'].remove(1);rows[0]['config_json']=json.dumps(c)
        self.mutate('manifest',change);self.rejected()
    def test_projection_mismatch(self):
        def change(rows):
            c=json.loads(rows[0]['native_projections_json']);c['1999']['transform'][0]=.001;rows[0]['native_projections_json']=json.dumps(c)
        self.mutate('manifest',change);self.rejected()
    def test_fractional_pixel_equivalents_are_valid(self):
        self.assertEqual(self.validate()['status'],'PASS')
    def test_refuse_overwrite(self):
        self.validate();p=self.output/'canonical_entry_reentry_pilot_v1_summary.csv';p.write_text('changed');self.rejected()
    def test_duplicate_columns(self):
        p=self.exports/S['filenames']['cells'];b=p.read_text(encoding='utf-8-sig');lines=b.splitlines();lines[0]=lines[0].replace('GRID_ID','cell_id');p.write_text('\n'.join(lines));self.rejected()

if __name__=='__main__': unittest.main(verbosity=2)
