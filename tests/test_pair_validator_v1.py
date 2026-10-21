"""Synthetic file-integration checks; never emit scientific outputs outside temp dirs."""
import copy
import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validator', ROOT / 'analysis/19b_validate_uncertain_pair_crosstab_v1.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
C = json.loads((ROOT / 'config/uncertain_pair_crosstab_v1.json').read_text())


def write(path, rows, fields=None):
    path.write_bytes(v.csv_bytes(rows, fields or list(rows[0])))


def create_exports(directory, scope):
    directory.mkdir()
    cross = v.load_csv(ROOT / 'config' / C['crosswalk']['filename'])
    selected = [r for r in cross if scope == 'full' or r['cell_id'] in C['pilot_cell_ids']]
    reference = v.load_csv(ROOT / 'config' / C['accepted_boundary_summary']['filename'])
    grouped = {}
    for cell in selected:
        for year in [2024, 2025]:
            ref = [r for r in reference if int(r['episode_boundary_year']) == year]
            p = {k: 0.0 for k in v.PAIR}
            p['p00_ha'], p['p11_ha'] = 1000.0, 2000.0
            p['p10_ha'] = float(next(r['event_area_ha'] for r in ref if r['event_type']=='entry')) / 24889
            p['p01_ha'] = float(next(r['event_area_ha'] for r in ref if r['event_type']=='termination')) / 24889
            uncertain = float(ref[0]['uncertain_pair_ha']) / 24889
            # All three conditional groups have nonzero support.
            p['p02_ha'], p['p30_ha'], p['p44_ha'] = uncertain/4, uncertain/4, uncertain/2
            row = dict(cell, previous_year=year-1, event_year=year, diagnostic_interval=1,
                       scope=scope, output_version=C['version'], run_id=C['run_tag']+'_'+scope)
            row.update(p)
            row.update(domain_ha=sum(p.values()), valid_pair_ha=p['p00_ha']+p['p01_ha']+p['p10_ha']+p['p11_ha'],
                       uncertain_pair_ha=uncertain, uncertain_previous_PAS_ha=uncertain/4,
                       uncertain_current_PAS_ha=uncertain/4, uncertain_no_observed_PAS_ha=uncertain/2,
                       entry_ha=p['p10_ha'], termination_ha=p['p01_ha'])
            row.update({k: 0 for k in v.ERROR})
            name = 'canonical_uncertain_pairs_pilot_v1.csv' if scope == 'pilot' else f"canonical_uncertain_pairs_b{int(cell['source_batch_id']):02d}_v1.csv"
            grouped.setdefault(name, []).append(row)
    for name, rows in grouped.items():
        write(directory/name, rows, v.KEYS+v.PAIR+v.AREA+v.ERROR)
    manifest = dict(scope=scope, output_version=C['version'], run_id=C['run_tag']+'_'+scope,
                    source_script=C['gee_scripts'][scope]['filename'], expected_cells=len(selected), expected_rows=2*len(selected),
                    config_json=json.dumps(v.runtime(C)), pilot_cell_ids_json=json.dumps(C['pilot_cell_ids']),
                    native_projections_json=json.dumps({str(y): {'crs': C['crs'], 'transform': C['crs_transform']} for y in [2023,2024,2025]}),
                    coverage_band_count=41, coverage_bands_csv='|'.join(f'classification_{y}' for y in range(1985,2026)))
    write(directory/f'canonical_uncertain_pairs_manifest_{scope}_v1.csv', [manifest], v.MANIFEST)
    fixtures = json.loads((ROOT / 'config/uncertain_pair_native_cases_v1.json').read_text())
    native = [dict(case_id=r['case_id'], scope='native_synthetic', output_version=C['version'],
                   run_id=C['run_tag']+'_pilot_synthetic', expected_previous=r['expected_previous'],
                   expected_current=r['expected_current'], test_pixel_equivalents=10,
                   **{k: 0 for k in v.NATIVE_ERRORS}) for r in fixtures]
    write(directory/'canonical_uncertain_pairs_native_synthetic_v1.csv', native, v.NATIVE_KEYS)


class Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.exports = self.base/'pilot'
        create_exports(self.exports, 'pilot')
        self.output = self.base/'out'

    def tearDown(self):
        self.temp.cleanup()

    def run_pilot(self):
        return v.validate(ROOT, 'pilot', self.exports, self.output)

    def mutate(self, name, callback):
        path = self.exports/name
        rows = v.load_csv(path)
        callback(rows)
        write(path, rows)

    def test_pilot_and_immutable_reuse(self):
        report = self.run_pilot()
        self.assertEqual(report['rows'], 4)
        self.assertFalse(report['scientific_full_domain_complete'])
        self.assertIsNone(report['execution_identity']['executed_script_sha256'])
        self.assertEqual(report, self.run_pilot())

    def test_full_end_to_end_and_boundary_rejection(self):
        self.run_pilot()
        full = self.base/'full'
        create_exports(full, 'full')
        pilot = self.output/'canonical_uncertain_pairs_pilot_v1_validation.json'
        with self.assertRaisesRegex(ValueError, 'full requires'):
            v.validate(ROOT, 'full', full, self.base/'fullout')
        report = v.validate(ROOT, 'full', full, self.base/'fullout', pilot)
        self.assertEqual(report['rows'], 49778)
        self.assertTrue(report['scientific_full_domain_complete'])
        # Internally consistent perturbation of entry, domain and valid total must still fail legacy control.
        path = full/'canonical_uncertain_pairs_b00_v1.csv'
        rows = v.load_csv(path)
        for key in ['p10_ha', 'entry_ha', 'valid_pair_ha', 'domain_ha']:
            rows[0][key] = float(rows[0][key])+1
        write(path, rows)
        with self.assertRaisesRegex(ValueError, 'accepted boundary'):
            v.validate(ROOT, 'full', full, self.base/'rejected', pilot)
        self.assertFalse((self.base/'rejected').exists())

    def test_partition_rejected(self):
        self.mutate('canonical_uncertain_pairs_pilot_v1.csv', lambda r: r[0].update(p44_ha='100000'))
        with self.assertRaisesRegex(ValueError, 'domain_ha'):
            self.run_pilot()
        self.assertFalse(self.output.exists())

    def test_error_counter_exact_zero(self):
        self.mutate('canonical_uncertain_pairs_pilot_v1.csv', lambda r: r[0].update(partition_error_pixel_equivalents='0.000000001'))
        with self.assertRaisesRegex(ValueError, 'raster mismatch'):
            self.run_pilot()

    def test_native_support_and_inventory(self):
        name = 'canonical_uncertain_pairs_native_synthetic_v1.csv'
        self.mutate(name, lambda r: r[0].update(test_pixel_equivalents='0'))
        with self.assertRaisesRegex(ValueError, 'no support'):
            self.run_pilot()
        self.mutate(name, lambda r: r.pop())
        with self.assertRaisesRegex(ValueError, 'inventory'):
            self.run_pilot()

    def test_duplicate_export(self):
        (self.exports/'canonical_uncertain_pairs_pilot_v1 (1).csv').write_text('duplicate')
        with self.assertRaisesRegex(ValueError, 'CSV inventory'):
            self.run_pilot()

    def test_projection_and_nonfinite_rejected(self):
        self.mutate('canonical_uncertain_pairs_manifest_pilot_v1.csv', lambda r: r[0].update(native_projections_json='{}'))
        with self.assertRaisesRegex(ValueError, 'projection metadata'):
            self.run_pilot()

    def test_nonfinite_area_rejected(self):
        self.mutate('canonical_uncertain_pairs_pilot_v1.csv', lambda r: r[0].update(p00_ha='nan'))
        with self.assertRaisesRegex(ValueError, 'non-finite'):
            self.run_pilot()

    def test_missing_cell_pair_rejected(self):
        self.mutate('canonical_uncertain_pairs_pilot_v1.csv', lambda r: r.pop())
        with self.assertRaisesRegex(ValueError, 'inventory incomplete'):
            self.run_pilot()

    def test_refuse_different_output(self):
        self.run_pilot()
        path = self.output/'canonical_uncertain_pairs_pilot_v1_summary.csv'
        path.write_text('do not overwrite')
        with self.assertRaisesRegex(ValueError, 'refusing to overwrite'):
            self.run_pilot()
        self.assertEqual(path.read_text(), 'do not overwrite')


if __name__ == '__main__':
    unittest.main(verbosity=2)
