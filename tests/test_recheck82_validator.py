"""Temporary synthetic integration checks, not native/scientific results."""
from pathlib import Path
import importlib.util,json,csv,tempfile,unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('new_validator',ROOT/'analysis/validate_pasture_v2_recheck82_v1.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
C=json.loads((ROOT/'config/pasture_v2_coverage_recheck_82_v1.json').read_text())
RUN='20261019150000'

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name)
        self.path=self.base/f'pasture_v2_coverage_recheck82_{RUN}_v1.csv'
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

if __name__=='__main__':unittest.main(verbosity=2)
