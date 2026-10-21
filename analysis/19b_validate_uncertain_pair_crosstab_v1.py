#!/usr/bin/env python3
"""Read-only validation of actual 19a exports. Python >=3.10; standard library only."""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path

PAIR = [f'p{i}{j}_ha' for i in range(5) for j in range(5)]
AREA = ['domain_ha', 'valid_pair_ha', 'uncertain_pair_ha',
        'uncertain_previous_PAS_ha', 'uncertain_current_PAS_ha',
        'uncertain_no_observed_PAS_ha', 'entry_ha', 'termination_ha']
ERROR = ['partition_error_pixel_equivalents', 'legacy_uncertain_error_pixel_equivalents',
         'conditional_partition_error_pixel_equivalents']
KEYS = ['cell_id', 'GRID_ID', 'source_batch_id', 'previous_year', 'event_year',
        'diagnostic_interval', 'scope', 'output_version', 'run_id']
NATIVE_ERRORS = ['previous_state_error', 'current_state_error', 'cross_classification_error',
                 'partition_error', 'legacy_uncertain_error', 'conditional_partition_error']
NATIVE_KEYS = ['case_id', 'scope', 'output_version', 'run_id', 'expected_previous',
               'expected_current', 'test_pixel_equivalents'] + NATIVE_ERRORS
MANIFEST = ['scope', 'output_version', 'run_id', 'source_script', 'expected_cells', 'expected_rows',
            'config_json', 'pilot_cell_ids_json', 'native_projections_json',
            'coverage_band_count', 'coverage_bands_csv']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_csv(path, fields=None):
    with Path(path).open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        names = reader.fieldnames or []
        require(len(names) == len(set(names)), f'{path.name}: duplicate columns')
        if fields is not None:
            require(set(names) == set(fields), f'{path.name}: columns differ: {set(names) ^ set(fields)}')
        rows = list(reader)
        require(all(None not in row and None not in row.values() for row in rows),
                f'{path.name}: malformed CSV')
        return rows


def number(value):
    result = float(value)
    require(math.isfinite(result) and result >= 0, f'non-finite/negative metric: {value}')
    return result


def integer(value):
    result = number(value)
    require(result.is_integer(), f'not an integer: {value}')
    return int(result)


def runtime(config):
    return {key: config[key] for key in ['version', 'coverage_asset', 'grid_asset', 'constants_module',
            'valid_source_codes', 'class_groups', 'crs', 'crs_transform', 'pairs', 'footprint_convention']} | {
            'observation_classes': config['classes'], 'square_metres_per_hectare': 10000}


def near(actual, expected, tolerance, context):
    require(abs(actual - expected) <= tolerance,
            f'{context}: {actual:.12g} != {expected:.12g} (tol {tolerance})')


def identities(row, tolerance, context):
    p = lambda i, j: row[f'p{i}{j}_ha']
    expected = {
        'domain_ha': math.fsum(row[k] for k in PAIR),
        'valid_pair_ha': math.fsum(p(i, j) for i in range(2) for j in range(2)),
        'uncertain_pair_ha': math.fsum(p(i, j) for i in range(5) for j in range(5) if i >= 2 or j >= 2),
        'uncertain_previous_PAS_ha': math.fsum(p(0, j) for j in range(2, 5)),
        'uncertain_current_PAS_ha': math.fsum(p(i, 0) for i in range(2, 5)),
        'uncertain_no_observed_PAS_ha': math.fsum(p(i, j) for i in range(1, 5) for j in range(1, 5) if i >= 2 or j >= 2),
        'entry_ha': p(1, 0), 'termination_ha': p(0, 1)}
    for key, value in expected.items():
        near(row[key], value, tolerance, context + '/' + key)
    near(row['domain_ha'], row['valid_pair_ha'] + row['uncertain_pair_ha'], tolerance, context + '/support')
    near(row['uncertain_pair_ha'], sum(row[k] for k in AREA[3:6]), tolerance, context + '/conditional partition')
    require(row['domain_ha'] > 0, context + ': no spatial support')
    require(all(row[k] == 0 for k in ERROR), context + ': raster mismatch counter is nonzero')


def csv_bytes(rows, fields):
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode('utf-8-sig')


def validate(root, scope, export_dir, output_dir, pilot_validation=None):
    root, export_dir, output_dir = map(Path, (root, export_dir, output_dir))
    config_path = root / 'config/uncertain_pair_crosstab_v1.json'
    config = json.loads(config_path.read_text())
    inputs = {'config': sha(config_path)}
    for key in ['crosswalk', 'accepted_boundary_summary', 'accepted_boundary_validation']:
        reference = root / 'config' / config[key]['filename']
        require(sha(reference) == config[key]['sha256'], f'{key}: reference hash mismatch')
        inputs[key] = sha(reference)
    source = root / 'gee' / config['gee_scripts'][scope]['filename']
    require(sha(source) == config['gee_scripts'][scope]['sha256'], 'supplied GEE script changed')
    inputs['supplied_script'] = sha(source)
    crosswalk = load_csv(root / 'config' / config['crosswalk']['filename'])
    cell_map = {r['cell_id']: r for r in crosswalk}
    require(len(cell_map) == len(crosswalk) == config['expected_cells'], 'crosswalk incomplete/duplicate')
    require(len({r['GRID_ID'] for r in crosswalk}) == len(crosswalk), 'crosswalk GRID_ID duplicate')
    selected = set(config['pilot_cell_ids']) if scope == 'pilot' else set(cell_map)
    names = (['canonical_uncertain_pairs_pilot_v1.csv'] if scope == 'pilot' else
             [f'canonical_uncertain_pairs_b{b:02d}_v1.csv' for b in config['expected_batches']])
    manifest_name = f'canonical_uncertain_pairs_manifest_{scope}_v1.csv'
    native_name = 'canonical_uncertain_pairs_native_synthetic_v1.csv'
    expected_names = set(names + [manifest_name, native_name])
    actual_names = {p.name for p in export_dir.glob('*.csv')}
    require(actual_names == expected_names,
            f'CSV inventory differs; missing={expected_names-actual_names}; extra={actual_names-expected_names}')
    for name in sorted(expected_names):
        inputs[name] = sha(export_dir / name)
    manifests = load_csv(export_dir / manifest_name, MANIFEST)
    require(len(manifests) == 1, 'manifest must contain exactly one row')
    manifest = manifests[0]
    expected_meta = {'scope': scope, 'output_version': config['version'],
                     'run_id': config['run_tag'] + '_' + scope,
                     'source_script': source.name}
    require(all(manifest[k] == v for k, v in expected_meta.items()), 'manifest identity mismatch')
    require(integer(manifest['expected_cells']) == len(selected) and
            integer(manifest['expected_rows']) == len(selected) * 2, 'manifest population mismatch')
    require(json.loads(manifest['config_json']) == runtime(config), 'runtime constants differ')
    require(json.loads(manifest['pilot_cell_ids_json']) == config['pilot_cell_ids'], 'pilot cells differ')
    require(integer(manifest['coverage_band_count']) == 41 and manifest['coverage_bands_csv'].split('|') ==
            [f'classification_{y}' for y in range(1985, 2026)], 'coverage band inventory differs')
    projections = json.loads(manifest['native_projections_json'])
    require(set(projections) == {'2023', '2024', '2025'}, 'projection metadata incomplete')
    for year, projection in projections.items():
        require(projection['crs'] == config['crs'] and len(projection['transform']) == 6,
                f'{year}: native projection differs')
        for actual, expected in zip(projection['transform'], config['crs_transform']):
            require(math.isfinite(actual), 'non-finite native transform')
            near(actual, expected, 1e-13, f'{year}/transform')
    fixture_path = root / 'config/uncertain_pair_native_cases_v1.json'
    fixtures = json.loads(fixture_path.read_text())
    inputs['native_case_definitions'] = sha(fixture_path)
    expected_cases = {r['case_id']: r for r in fixtures}
    native = load_csv(export_dir / native_name, NATIVE_KEYS)
    require(len(native) == config['native_fixture_cases'] and
            {r['case_id'] for r in native} == set(expected_cases), 'native fixture inventory differs')
    for row in native:
        case = expected_cases[row['case_id']]
        require(row['scope'] == 'native_synthetic' and row['output_version'] == config['version'] and
                row['run_id'] == config['run_tag'] + '_pilot_synthetic', 'native fixture identity mismatch')
        require(integer(row['expected_previous']) == case['expected_previous'] and
                integer(row['expected_current']) == case['expected_current'], 'fixture expected state differs')
        require(number(row['test_pixel_equivalents']) > 0, 'native fixture has no support')
        require(all(number(row[k]) == 0 for k in NATIVE_ERRORS), 'native fixture mismatch')
    if scope == 'full':
        require(pilot_validation is not None, 'full requires accepted pilot validation JSON')
        pilot = json.loads(Path(pilot_validation).read_text())
        require(pilot['status'] == 'PASS' and pilot['scope'] == 'pilot', 'pilot is not accepted')
        for key in ['config', 'native_case_definitions', native_name]:
            require(pilot['input_sha256'][key] == inputs[key], f'pilot/full identity differs: {key}')
        require(pilot['input_sha256']['supplied_script'] == config['gee_scripts']['pilot']['sha256'],
                'pilot source snapshot differs')
        inputs['accepted_pilot_validation'] = sha(pilot_validation)
    rows, seen = [], set()
    for name in names:
        chunk = load_csv(export_dir / name, KEYS + PAIR + AREA + ERROR)
        require(bool(chunk), f'{name}: empty export')
        batch = int(name.split('_b')[1][:2]) if scope == 'full' else None
        for row in chunk:
            cell = row['cell_id']
            require(cell in selected, f'{name}: unexpected cell {cell}')
            require(row['GRID_ID'] == cell_map[cell]['GRID_ID'] and
                    integer(row['source_batch_id']) == integer(cell_map[cell]['source_batch_id']),
                    f'{name}/{cell}: grid/batch differs')
            require(batch is None or integer(row['source_batch_id']) == batch, 'wrong batch file')
            year = integer(row['event_year'])
            require([integer(row['previous_year']), year] in config['pairs'] and
                    integer(row['diagnostic_interval']) == 1, 'unexpected pair or diagnostic flag')
            require(all(row[k] == expected_meta[k] for k in ['scope', 'output_version', 'run_id']), 'row identity differs')
            key = (cell, year)
            require(key not in seen, f'duplicate cell/pair: {key}')
            seen.add(key)
            for metric in PAIR + AREA + ERROR:
                row[metric] = number(row[metric])
            row['previous_year'], row['event_year'] = year - 1, year
            identities(row, config['area_tolerance_ha_per_cell'], str(key))
            rows.append(row)
    require(seen == {(c, y) for c in selected for y in [2024, 2025]}, 'cell/pair inventory incomplete')
    rows.sort(key=lambda r: (int(r['cell_id']), r['event_year']))
    national = []
    for year in [2024, 2025]:
        selected_rows = [r for r in rows if r['event_year'] == year]
        total = {k: math.fsum(r[k] for r in selected_rows) for k in PAIR + AREA + ERROR}
        total.update(previous_year=year-1, event_year=year, cells=len(selected_rows), scope=scope)
        identities(total, config['area_tolerance_ha_aggregate'], f'national/{year}')
        national.append(total)
    controls = []
    if scope == 'full':
        reference = load_csv(root / 'config' / config['accepted_boundary_summary']['filename'])
        require(len(reference) == 4, 'boundary reference inventory differs')
        for row in reference:
            total = next(r for r in national if r['event_year'] == integer(row['episode_boundary_year']))
            for field, actual in [('event_area_ha', total[row['event_type'] + '_ha']),
                                  ('uncertain_pair_ha', total['uncertain_pair_ha'])]:
                target = number(row[field])
                near(actual, target, config['area_tolerance_ha_aggregate'], 'accepted boundary/' + field)
                controls.append({'event_year': total['event_year'], 'event_type': row['event_type'],
                                 'field': field, 'actual_ha': actual, 'reference_ha': target,
                                 'difference_ha': actual-target})
    def conditional(row):
        result = {k: row[k] for k in ['event_year', 'scope']}
        if 'cell_id' in row:
            result.update({k: row[k] for k in ['cell_id', 'GRID_ID', 'source_batch_id']})
        denominators = {'previous_PAS_support_ha': math.fsum(row[f'p0{j}_ha'] for j in range(5)),
                        'current_PAS_support_ha': math.fsum(row[f'p{i}0_ha'] for i in range(5))}
        result.update(denominators)
        result.update({k: row[k] for k in AREA[2:6]})
        for side in ['previous', 'current']:
            den = denominators[side + '_PAS_support_ha']
            result[side + '_PAS_uncertain_fraction'] = row['uncertain_' + side + '_PAS_ha'] / den if den else ''
        den = row['uncertain_pair_ha']
        result['uncertain_no_observed_PAS_fraction'] = row['uncertain_no_observed_PAS_ha'] / den if den else ''
        return result
    conditioned = [conditional(r) for r in rows]
    conditioned_national = [conditional(r) for r in national]
    long = [{'previous_year': r['previous_year'], 'event_year': r['event_year'], 'scope': scope,
             'previous_state': config['classes'][i], 'current_state': config['classes'][j],
             'area_ha': r[f'p{i}{j}_ha']} for r in national for i in range(5) for j in range(5)]
    prefix = f'canonical_uncertain_pairs_{scope}_v1'
    products = {
        prefix + '_cells.csv': csv_bytes(rows, KEYS + PAIR + AREA + ERROR),
        prefix + '_conditional_cells.csv': csv_bytes(conditioned, list(conditioned[0])),
        prefix + '_summary.csv': csv_bytes(national, ['previous_year', 'event_year', 'cells', 'scope'] + PAIR + AREA + ERROR),
        prefix + '_conditional_summary.csv': csv_bytes(conditioned_national, list(conditioned_national[0])),
        prefix + '_cross_table.csv': csv_bytes(long, list(long[0]))}
    report = {'status': 'PASS', 'scope': scope, 'version': config['version'], 'cells': len(selected),
              'rows': len(rows), 'native_fixtures_passed': len(native),
              'scientific_full_domain_complete': scope == 'full',
              'checks': ['exact_inventory', 'runtime_constants', 'native_projections', 'native_fixtures',
                         'cell_partitions', 'zero_raster_mismatches', 'aggregate_partitions'] +
                        (['accepted_boundary_totals', 'accepted_pilot_identity'] if scope == 'full' else []),
              'boundary_controls': controls, 'input_sha256': inputs,
              'output_sha256': {name: hashlib.sha256(data).hexdigest() for name, data in products.items()},
              'execution_identity': {'supplied_script_sha256': inputs['supplied_script'],
                  'executed_script_sha256': None, 'operator_attestation': None,
                  'independently_verified_remote_execution': False},
              'limitations': ['Operator-provided native exports; not independently observed remote execution.',
                  'Pilot support is two cells only; no domain-wide PAS-overlap inference.' if scope == 'pilot'
                  else 'Endpoint PAS status only; no inference that a pixel was never PAS in other years.',
                  'Annual uncertain-pair area is distinct from unresolved pasture-origin area.']}
    products[prefix + '_validation.json'] = (json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()
    # Preflight every output before any write: immutable results may be reused byte-for-byte.
    for name, data in products.items():
        path = output_dir / name
        require(not path.exists() or path.read_bytes() == data, f'refusing to overwrite different output: {path}')
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, data in products.items():
        path = output_dir / name
        if not path.exists():
            path.write_bytes(data)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--scope', required=True, choices=['pilot', 'full'])
    parser.add_argument('--export-dir', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--pilot-validation', type=Path)
    args = parser.parse_args()
    try:
        report = validate(args.root, args.scope, args.export_dir, args.output_dir, args.pilot_validation)
    except (ValueError, KeyError, OSError, TypeError) as error:
        parser.exit(1, f'FAIL: {error}\n')
    print(json.dumps({k: report[k] for k in ['status', 'scope', 'cells', 'rows', 'native_fixtures_passed',
                                          'scientific_full_domain_complete']}, indent=2))


if __name__ == '__main__':
    main()
