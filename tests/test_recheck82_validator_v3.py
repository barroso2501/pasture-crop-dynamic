"""Temporary synthetic integration checks, not native/scientific results."""
from pathlib import Path
import importlib.util,json,csv,tempfile,unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('new_validator',ROOT/'analysis/validate_pasture_v2_recheck82_v3.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
C=json.loads((ROOT/'config/pasture_v2_coverage_recheck_82_v3.json').read_text())
RUN='20261019150000'

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name)
        self.path=self.base/f'pasture_v2_coverage_recheck82_{RUN}_v3.csv'
        self.rows=[]
        for c in C['cells']:
            r=dict(c,script_version=C['version'],parent_run=C['parent_run'],
                   parent_validation_sha256=C['parent_validation_sha256'],run_id=RUN,
                   generated_at_utc='2026-10-19T15:00:00.000Z',expected_cells=82,year_start=1985,year_end=2025,
                   coverage_asset=C['coverage'],new_asset=C['age'],grid_asset=C['grid'],
                   known_codes_json=json.dumps(C['known_coverage_codes']),prior_known_codes_json=json.dumps(C['previous_known_coverage_codes']),
                   crs=C['crs'],crs_transform=json.dumps(C['crs_transform']),tile_scale=16,
                   legacy_coverage_unknown_present=1,remaining_unknown_max_code=-1000000000,
                   remaining_unknown_negative_min_code=-1000000000)
            r.update({'new_'+k:int(k in ['has_pasture','has_code100','has_2xx','has_valid_coverage']) for k in v.old.FLAGS})
            r.update({f'coverage_code_{code}_present':int(code==26) for code in C['newly_recognized_codes']})
            self.rows.append(r)
    def tearDown(self):self.tmp.cleanup()
    def run_validation(self):
        fields=['new_'+k for k in v.old.FLAGS]+['legacy_coverage_unknown_present']+[
            f'coverage_code_{c}_present' for c in C['newly_recognized_codes']]+[
            'remaining_unknown_max_code','remaining_unknown_negative_min_code','native_grid_support']
        for r in self.rows:
            r.setdefault('native_fixture_method','two_explicit_halves_native_4x4_reduceRegions_v1')
            r.setdefault('native_constant_test_status','PASS')
            r.setdefault('native_partition_test_json',json.dumps({
                'covered_min':1,'covered_max':1,'left_min':0,'left_max':1,'right_min':0,'right_max':1}))
            t=C['crs_transform']
            r.setdefault('native_fixture_region_json',json.dumps([t[2],t[5]+4*t[4],t[2]+4*t[0],t[5]]))
            r.setdefault('native_grid_support',1)
            r.setdefault('native_schema_test_status','PASS')
            r.setdefault('native_schema_test_fields',26)
            r.setdefault('native_schema_expected_json',json.dumps({k:i+1 for i,k in enumerate(fields)}))
            r.setdefault('image_band_names_json',json.dumps(fields))
            r.setdefault('reducer_missing_count',0)
            r.setdefault('reducer_missing_fields','')
            r['reducer_properties_json']=json.dumps({k:r[k] for k in fields})
            r['reducer_property_names_json']=json.dumps(fields)
        sample=min(self.rows,key=lambda r:r['audit_id'])
        values={k:sample[k] for k in fields}
        for r in self.rows:
            r.setdefault('materialized_cells',82)
            r.setdefault('finite_window_buffer_m',1000)
            r.setdefault('native_geometry_area_m2',200000000)
            r.setdefault('finite_window_coordinates_json',json.dumps([[[-61,-25],[-40,-25],[-40,-2],[-61,-2],[-61,-25]]]))
            r.setdefault('real_preflight_audit_id',min(c['audit_id'] for c in C['cells']))
            r.setdefault('real_preflight_status','PASS_SELECTED_METHOD')
            r.setdefault('reduction_strategy','mapped_direct_reduceRegion_finite_image')
            r.setdefault('real_preflight_direct_valid',1)
            r.setdefault('real_preflight_table_valid',1)
            r.setdefault('real_preflight_values_json',json.dumps(values))
            r.setdefault('real_preflight_diagnostics_json',json.dumps({'direct':values,'table':values}))
        self.path.write_bytes(v.encoded_csv(self.rows,list(self.rows[0])))
        return v.validate(self.path,ROOT,self.base/'out')
    def test_complete_combination(self):
        r=self.run_validation()
        self.assertEqual(r['combined_cells'],21869)
        self.assertEqual(r['parent_cells_reused_unchanged'],21787)
        self.assertEqual(r['affected_cells']['coverage_unknown_code'],0)
        self.assertEqual(r,self.run_validation())
    def test_missing_cell(self):
        self.rows.pop()
        with self.assertRaisesRegex(ValueError,'incomplete'):self.run_validation()
        self.assertFalse((self.base/'out').exists())
    def test_false_explanation(self):
        self.rows[0]['coverage_code_26_present']=0
        with self.assertRaisesRegex(ValueError,'not explained'):self.run_validation()
    def test_still_unknown_is_pending(self):
        self.rows[0].update(new_coverage_unknown_code=1,remaining_unknown_max_code=99,remaining_unknown_negative_min_code=-99)
        r=self.run_validation()
        self.assertIn('coverage_unknown_code',r['pending_controls'])
        self.assertEqual(r['verdicts']['code1'],'NAO_DETECTADO_COM_PENDENCIAS')
    def test_binary_and_identity_rejection(self):
        self.rows[0]['new_code1']=2
        with self.assertRaisesRegex(ValueError,'Nonbinary'):self.run_validation()
        self.rows[0]['new_code1']=0;self.rows[0]['GRID_ID']='wrong'
        with self.assertRaisesRegex(ValueError,'crosswalk'):self.run_validation()
    def test_genuine_positive_is_reported(self):
        self.rows[0].update(new_invalid100_after_nonpas=1,new_code100_without_confirmed_initial=1)
        r=self.run_validation()
        self.assertEqual(r['verdicts']['invalid100_after_nonpas'],'PRESENTE_NO_ESCOPO')
        self.assertIn('code100_without_confirmed_initial',r['pending_controls'])

    def test_empty_actual_result_pattern_rejected(self):
        for row in self.rows:
            for key in list(row):
                if key.startswith('new_') or key.startswith('coverage_code_') or key.startswith('remaining_unknown_') or key=='legacy_coverage_unknown_present':
                    if key!='new_asset':row[key]=''
        with self.assertRaises(ValueError):
            self.run_validation()
        self.assertFalse((self.base/'out').exists())
    def test_native_transport_guard_rejected(self):
        self.rows[0]['reducer_missing_count']=1
        self.rows[0]['reducer_missing_fields']='new_code1'
        with self.assertRaisesRegex(ValueError,'Missing native reductions'):self.run_validation()
    def test_native_schema_failure_rejected(self):
        self.rows[0]['native_schema_test_status']='FAIL'
        with self.assertRaisesRegex(ValueError,'schema self-test'):self.run_validation()
    def test_native_geometry_support_required(self):
        self.rows[0]['native_grid_support']=0
        with self.assertRaises(ValueError):self.run_validation()

    def test_unexercised_half_rejected(self):
        self.rows[0]['native_partition_test_json']=json.dumps({
            'covered_min':1,'covered_max':1,'left_min':0,'left_max':0,'right_min':1,'right_max':1})
        with self.assertRaisesRegex(ValueError,'both spatial halves'):self.run_validation()
    def test_fixture_grid_size_rejected(self):
        self.rows[0]['native_fixture_region_json']='[-47,-16,-46.9,-15.9]'
        with self.assertRaisesRegex(ValueError,'4x4'):self.run_validation()


    def test_table_null_direct_valid(self):
        self.run_validation()
        for r in self.rows:
            d=json.loads(r['real_preflight_diagnostics_json']);d['table']={}
            r['real_preflight_diagnostics_json']=json.dumps(d)
            r['real_preflight_table_valid']=0
        # A new isolated output dir avoids conflicting immutable report bytes.
        self.path=self.base/f'pasture_v2_coverage_recheck82_{RUN}_v3.csv'
        import shutil
        shutil.rmtree(self.base/'out')
        self.assertEqual(self.run_validation()['status'],'PASS')
    def test_both_real_methods_null(self):
        self.run_validation()
        for r in self.rows:r['real_preflight_diagnostics_json']='{"direct":{},"table":{}}'
        with self.assertRaisesRegex(ValueError,'No valid real-cell'):self.run_validation()
    def test_methods_disagree(self):
        self.run_validation()
        for r in self.rows:
            d=json.loads(r['real_preflight_diagnostics_json']);d['table']['new_code1']=1
            r['real_preflight_diagnostics_json']=json.dumps(d)
        with self.assertRaisesRegex(ValueError,'methods disagree'):self.run_validation()
    def test_real_geometry_empty(self):
        self.rows[0]['native_geometry_area_m2']=0
        with self.assertRaisesRegex(ValueError,'real geometry'):self.run_validation()
    def test_preflight_not_reproduced(self):
        self.run_validation()
        min(self.rows,key=lambda r:r['audit_id'])['new_code1']=1
        with self.assertRaisesRegex(ValueError,'does not reproduce'):self.run_validation()

if __name__=='__main__':unittest.main(verbosity=2)
