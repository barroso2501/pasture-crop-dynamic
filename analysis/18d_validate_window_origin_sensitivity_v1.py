"""Validate native GEE window sensitivity exports; never invent execution results.

Pilot: --scope pilot --export-dir <GEE folder> --reference-dir <eight accepted CSVs>
Full: same arguments with --scope full and --pilot-validation <pilot PASS JSON>.
All outputs use a new namespace. This script never edits accepted canonical data.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

VERSION = 'window-origin-sensitivity-v1'
METRICS = ['flow_pas_tmp_ha', 'stock0_pas_ha', 'baseline_pas_stock_ha',
           'initial_ha', 'entry_ha', 'unresolved_ha', 'initial_pas_stock_ha',
           'entry_pas_stock_ha', 'unresolved_pas_stock_ha',
           'origin_partition_error_pixel_years', 'initial_continuity_error_pixel_years',
           'confirmed_entry_error_pixel_years']
KEYS = ['cell_id', 'GRID_ID', 'source_batch_id', 'baseline_year', 't0', 't1',
        'elapsed_intervals', 'diagnostic_interval', 'baseline_interval_by_construction',
        'scope', 'output_version', 'run_id']
ERRORS = METRICS[-3:]
NATIVE_ERRORS = ['state_mismatch_pixel_steps', 'partition_mismatch_pixel_steps',
                 'initial_mismatch_pixel_steps', 'entry_mismatch_pixel_steps']


def require(condition, message):
    if not bool(condition):
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def read(path, required):
    require(path.is_file(), 'Missing file: ' + str(path))
    with path.open(newline='', encoding='utf-8-sig') as f:
        head = next(csv.reader(f), [])
    require(len(head) == len(set(head)) and set(required) <= set(head), 'Missing/duplicate columns: ' + path.name)
    d = pd.read_csv(path, dtype={'cell_id': 'string', 'GRID_ID': 'string'}, encoding='utf-8-sig', float_precision='round_trip')
    for key in ('cell_id', 'GRID_ID'):
        if key in d:
            require(d[key].notna().all(), 'Missing identifiers: ' + path.name)
            d[key] = d[key].str.strip()
            require(d[key].ne('').all(), 'Empty identifiers: ' + path.name)
    return d


def numeric(d, fields):
    for field in fields:
        d[field] = pd.to_numeric(d[field], errors='coerce')
    require(np.isfinite(d[fields].to_numpy(float)).all(), 'Missing/nonfinite numeric data')


def integers(d, fields):
    numeric(d, fields)
    require((d[fields] == np.floor(d[fields])).all().all(), 'Noninteger key/flag')


def close(a, b, tolerance, label):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    delta = np.abs(a-b)
    maximum = float(delta.max()) if delta.size else 0.
    require(maximum <= tolerance, f'{label}: maximum difference {maximum:.12g} > {tolerance}')
    return maximum


def identity(path):
    return {'filename': path.name, 'sha256': sha(path), 'bytes': path.stat().st_size}


def references(cfg, directory):
    result, inventory, ids = {}, [], None
    fields = ['cell_id', 'GRID_ID', 'source_batch_id', 't0', 't1', 'diagnostic_interval',
              'stock0_pas', 'origin_initial', 'origin_new', 'origin_unresolved', 'flow_pas_tmp',
              'pas_initial_to_tmp', 'pas_new_to_tmp', 'pas_unresolved_to_tmp']
    for item in cfg['immutable_reference_files']:
        path = directory / item['filename']
        require(path.is_file() and sha(path) == item['sha256'], 'Accepted reference hash differs: ' + item['filename'])
        d = read(path, fields)[fields]
        integers(d, ['source_batch_id', 't0', 't1', 'diagnostic_interval'])
        numeric(d, fields[6:])
        t0, t1 = map(int, item['interval'].split('_'))
        require(len(d) == cfg['expected_cells'] and d.cell_id.is_unique, 'Reference cell population differs')
        require(d.t0.eq(t0).all() and d.t1.eq(t1).all() and d.diagnostic_interval.eq(int(t0 == 2020)).all(), 'Reference interval differs')
        if ids is None:
            ids = set(d.cell_id)
        require(set(d.cell_id) == ids, 'Reference cell sets differ')
        result[t0] = d.set_index('cell_id', drop=False).sort_index()
        inventory.append(identity(path))
    require(len(result) == 8, 'Eight reference files required')
    return result, inventory


def validate_manifest(root, cfg, export_dir, scope):
    path = export_dir / f'canonical_window_origin_run_manifest_{scope}_v1.csv'
    fields = ['run_id', 'scope', 'interval_index', 't0', 't1', 'baselines_json',
              'expected_cells', 'source_script', 'output_version', 'config_json', 'pilot_cells_json',
              'coverage_band_count', 'coverage_bands_csv', 'native_crs', 'native_transform_csv']
    d = read(path, fields)
    indices = [cfg['pilot_interval_index']] if scope == 'pilot' else cfg['fresh_interval_indices']
    integers(d, ['interval_index', 't0', 't1', 'expected_cells', 'coverage_band_count'])
    require(len(d) == len(indices) and set(d.interval_index) == set(indices), 'Run manifest population differs')
    source = json.loads((root / 'config/window_origin_sensitivity_source_snapshots_v1.json').read_text())['gee_scripts'][scope]
    require(sha(root / 'gee' / source['filename']) == source['sha256'], 'Supplied GEE script snapshot differs')
    for _, row in d.iterrows():
        index = int(row.interval_index)
        t0, t1 = cfg['all_intervals'][index]
        require((row.t0, row.t1, row.scope, row.output_version, row.source_script) == (t0, t1, scope, VERSION, source['filename']), 'Run manifest metadata differs')
        require(row.run_id == cfg['run_tag'] + f'_{scope}_i{index}', 'Run identifier differs')
        require(row.expected_cells == (2 if scope == 'pilot' else cfg['expected_cells']), 'Manifest cell population differs')
        require(json.loads(row.baselines_json) == [b for b in cfg['baselines'] if b <= t0], 'Manifest baselines differ')
        require(json.loads(row.pilot_cells_json) == cfg['pilot_cell_ids'], 'Pilot selection differs')
        actual = json.loads(row.config_json)
        for key in ('coverage_asset', 'grid_asset', 'crs', 'crs_transform', 'classes', 'constants_module', 'baselines', 'version'):
            require(actual[key] == cfg[key], 'Runtime configuration differs: ' + key)
        require(actual['valid_source_codes'] == cfg['valid_source_codes'] and actual['square_metres_per_hectare'] == 10000, 'Source-code/area configuration differs')
        require(row.coverage_band_count == 41 and row.coverage_bands_csv == '|'.join('classification_' + str(y) for y in range(1985, 2026)), 'Coverage bands/order differ')
        require(row.native_crs == cfg['crs'], 'Native coverage CRS differs')
        transform = [float(x) for x in row.native_transform_csv.split('|')]
        require(len(transform) == 6, 'Native transform length differs')
        close(transform, cfg['crs_transform'], 1e-13, 'Native coverage transform')
    return d.set_index('t0'), identity(path), source


def validate_native(root, cfg, export_dir):
    path = export_dir / 'canonical_window_origin_native_synthetic_v1.csv'
    fields = ['baseline_year', 'case_id', 'steps', 'scope', 'output_version', 'run_id', 'test_pixel_equivalents'] + NATIVE_ERRORS
    d = read(path, fields)
    integers(d, ['baseline_year', 'steps'])
    numeric(d, NATIVE_ERRORS + ['test_pixel_equivalents'])
    require(d.test_pixel_equivalents.gt(0).all(), 'Native synthetic region has no tested pixel support')
    cases = json.loads((root / 'config/window_origin_sensitivity_synthetic_cases_v1.json').read_text())
    expected = {(b, c['case_id']): len(c['values']) for b in cfg['baselines'] for c in cases}
    keys = list(zip(d.baseline_year, d.case_id))
    require(len(keys) == len(set(keys)) == len(expected) and set(keys) == set(expected), 'Native synthetic case population differs')
    for _, x in d.iterrows():
        require(x.steps == expected[x.baseline_year, x.case_id], 'Native case length differs')
    require(d.scope.eq('native_synthetic').all() and d.output_version.eq(VERSION).all(), 'Native synthetic scope/version differs')
    require(d.run_id.eq(cfg['run_tag'] + '_pilot_native_synthetic').all(), 'Native synthetic run differs')
    require(d[NATIVE_ERRORS].min().min() >= 0 and d[NATIVE_ERRORS].max().max() <= cfg['zero_invariant_tolerance'], 'Native synthetic mismatch is nonzero')
    return identity(path), len(d)


def validate_exports(root, cfg, scope, export_dir, refs, manifest):
    indices = [cfg['pilot_interval_index']] if scope == 'pilot' else cfg['fresh_interval_indices']
    expected_paths = []
    for i in indices:
        t0, t1 = cfg['all_intervals'][i]
        groups = ['pilot'] if scope == 'pilot' else [f'b{x:02d}' for x in cfg['expected_batches']]
        expected_paths.extend(export_dir / f'canonical_window_origin_{t0}_{t1}_{group}_v1.csv' for group in groups)
    pattern = 'canonical_window_origin_[0-9][0-9][0-9][0-9]_*_pilot_v1*.csv' if scope == 'pilot' else 'canonical_window_origin_[0-9][0-9][0-9][0-9]_*_b??_v1*.csv'
    # Drive retry duplicates such as _v1 (1).csv must not be silently selected.
    observed_paths = set(export_dir.glob(pattern))
    require(observed_paths == set(expected_paths), 'Missing or duplicate/unexpected sensitivity export files')
    frames, inputs, max_delta = [], [], 0.
    celltol, sumtol = cfg['per_cell_tolerance_ha'], cfg['summary_tolerance_ha']
    for path in expected_paths:
        d = read(path, KEYS + METRICS)
        integers(d, ['source_batch_id', 'baseline_year', 't0', 't1', 'elapsed_intervals', 'diagnostic_interval', 'baseline_interval_by_construction'])
        numeric(d, METRICS)
        require(d[METRICS].min().min() >= 0, 'Negative sensitivity area/count')
        require(d[ERRORS].max().max() <= cfg['zero_invariant_tolerance'], 'Nonzero native field invariant count')
        require(d.scope.eq(scope).all() and d.output_version.eq(VERSION).all(), 'Export scope/version differs')
        require(not d.duplicated(['cell_id', 'baseline_year', 't0', 't1']).any(), 'Duplicate cell-window-interval key')
        t0 = int(d.t0.iloc[0]) if len(d) else -1
        require(t0 in manifest.index and d.t0.eq(t0).all() and d.t1.eq(t0+5).all(), 'Export interval differs')
        require(d.run_id.eq(manifest.loc[t0, 'run_id']).all(), 'Export run differs')
        active = [b for b in cfg['baselines'] if b <= t0]
        require(set(d.baseline_year) == set(active), 'Export active baselines differ')
        require(d.diagnostic_interval.eq(int(t0 == 2020)).all(), 'Diagnostic flag differs')
        require(d.elapsed_intervals.eq((d.t0-d.baseline_year)/5).all() and d.baseline_interval_by_construction.eq((d.t0 == d.baseline_year).astype(int)).all(), 'Elapsed/baseline flags differ')
        if scope == 'pilot':
            wanted = refs[t0].loc[cfg['pilot_cell_ids']]
        else:
            batch = int(path.name.rsplit('_b', 1)[1][:2])
            wanted = refs[t0].loc[refs[t0].source_batch_id.eq(batch)]
        require(len(d) == len(wanted)*len(active), 'Batch/window row population differs')
        for b in active:
            sub = d.loc[d.baseline_year.eq(b)].set_index('cell_id', drop=False).sort_index()
            require(sub.index.is_unique and set(sub.index) == set(wanted.index), 'Cell identities differ')
            control = wanted.loc[sub.index]
            require(sub.GRID_ID.eq(control.GRID_ID).all() and sub.source_batch_id.eq(control.source_batch_id).all(), 'Cell GRID_ID/batch crosswalk differs')
            max_delta = max(max_delta, close(sub.flow_pas_tmp_ha, control.flow_pas_tmp, celltol, 'Total flow invariance'), close(sub.stock0_pas_ha, control.stock0_pas, celltol, 'PAS-stock invariance'))
            close(sub.baseline_pas_stock_ha, refs[b].loc[sub.index].stock0_pas, celltol, 'Baseline PAS stock')
            close(sub[['initial_ha', 'entry_ha', 'unresolved_ha']].sum(axis=1), sub.flow_pas_tmp_ha, celltol, 'Flow origin partition')
            close(sub[['initial_pas_stock_ha', 'entry_pas_stock_ha', 'unresolved_pas_stock_ha']].sum(axis=1), sub.stock0_pas_ha, celltol, 'Stock origin partition')
            for label in ('initial', 'entry', 'unresolved'):
                require((sub[label+'_ha'] <= sub[label+'_pas_stock_ha']+celltol).all(), 'Origin conversion exceeds its origin stock')
            require((sub.initial_pas_stock_ha <= sub.baseline_pas_stock_ha+celltol).all(), 'Continuous cohort exceeds baseline stock')
            if b == t0:
                close(sub.initial_ha, sub.flow_pas_tmp_ha, celltol, 'First interval 100% by construction')
                close(sub.initial_pas_stock_ha, sub.stock0_pas_ha, celltol, 'Initial baseline stock')
                require(sub[['entry_ha', 'unresolved_ha', 'entry_pas_stock_ha', 'unresolved_pas_stock_ha']].max().max() <= celltol, 'Noninitial area at baseline year')
            if b == 1985:
                for left, right in [('initial_ha', 'pas_initial_to_tmp'), ('entry_ha', 'pas_new_to_tmp'), ('unresolved_ha', 'pas_unresolved_to_tmp'), ('initial_pas_stock_ha', 'origin_initial'), ('entry_pas_stock_ha', 'origin_new'), ('unresolved_pas_stock_ha', 'origin_unresolved')]:
                    max_delta = max(max_delta, close(sub[left], control[right], celltol, '1985 accepted per-cell origin reproduction'))
        inputs.append(identity(path))
        d['data_source'] = 'fresh_native_gee_export'
        frames.append(d)
    fresh = pd.concat(frames, ignore_index=True)
    require(not fresh.duplicated(['cell_id', 'baseline_year', 't0', 't1']).any(), 'Duplicate across export files')
    for t0 in sorted(fresh.t0.unique()):
        here = fresh.loc[fresh.t0.eq(t0)]
        active = sorted(here.baseline_year.unique())
        previous = None
        expected_ids = set(cfg['pilot_cell_ids']) if scope == 'pilot' else set(refs[t0].index)
        for b in active:
            sub = here.loc[here.baseline_year.eq(b)].set_index('cell_id').sort_index()
            require(set(sub.index) == expected_ids, 'Full interval population differs')
            close([sub[['initial_ha', 'entry_ha', 'unresolved_ha']].to_numpy().sum()],
                  [sub.flow_pas_tmp_ha.sum()], sumtol, 'Aggregate flow-origin partition')
            close([sub[['initial_pas_stock_ha', 'entry_pas_stock_ha', 'unresolved_pas_stock_ha']].to_numpy().sum()],
                  [sub.stock0_pas_ha.sum()], sumtol, 'Aggregate stock-origin partition')
            if previous is not None:
                for field in ('flow_pas_tmp_ha', 'stock0_pas_ha'):
                    close(sub[field], previous[field], celltol, 'Calendar denominator changes across baselines')
                require((sub.initial_ha+celltol >= previous.initial_ha).all() and (sub.initial_pas_stock_ha+celltol >= previous.initial_pas_stock_ha).all(), 'Later baseline initial origin must contain earlier baseline origin')
                for field in ('entry_ha', 'unresolved_ha', 'entry_pas_stock_ha', 'unresolved_pas_stock_ha'):
                    require((sub[field] <= previous[field]+celltol).all(), 'Later-baseline entry/unresolved origin exceeds earlier one')
            previous = sub
        control = refs[t0] if scope == 'full' else refs[t0].loc[cfg['pilot_cell_ids']]
        selected = here.loc[here.baseline_year.eq(1985)]
        for left, right in [('flow_pas_tmp_ha', 'flow_pas_tmp'), ('initial_ha', 'pas_initial_to_tmp'), ('entry_ha', 'pas_new_to_tmp'), ('unresolved_ha', 'pas_unresolved_to_tmp')]:
            close([selected[left].sum()], [control[right].sum()], sumtol, '1985 interval-summary reproduction')
    if scope == 'full':
        ordered = fresh.sort_values(['baseline_year', 'cell_id', 't0'])
        require((ordered.groupby(['baseline_year', 'cell_id']).initial_pas_stock_ha.diff().dropna() <= celltol).all(), 'Continuous cohort gains membership through time')
        bounds = ordered.groupby(['baseline_year', 'cell_id']).baseline_pas_stock_ha.agg(['min', 'max'])
        require(((bounds['max']-bounds['min']) <= celltol).all(), 'Baseline stock varies over follow-up')
    return fresh, inputs, max_delta


def reuse_early_1985(refs):
    result = []
    for t0 in (1985, 1990):
        d = refs[t0].reset_index(drop=True).rename(columns={'stock0_pas': 'stock0_pas_ha', 'flow_pas_tmp': 'flow_pas_tmp_ha',
            'origin_initial': 'initial_pas_stock_ha', 'origin_new': 'entry_pas_stock_ha', 'origin_unresolved': 'unresolved_pas_stock_ha',
            'pas_initial_to_tmp': 'initial_ha', 'pas_new_to_tmp': 'entry_ha', 'pas_unresolved_to_tmp': 'unresolved_ha'})
        d['baseline_year'] = 1985
        d['elapsed_intervals'] = (t0-1985)//5
        d['baseline_interval_by_construction'] = int(t0 == 1985)
        d['baseline_pas_stock_ha'] = refs[1985].loc[d.cell_id].stock0_pas.to_numpy()
        d['scope'], d['output_version'] = 'full', VERSION
        d['run_id'] = 'accepted_reference_reuse'
        d['data_source'] = 'accepted_reused_1985_reference'
        for field in ERRORS:
            d[field] = np.nan  # Not falsely claimed as a fresh native invariant audit.
        result.append(d[KEYS+METRICS+['data_source']])
    return pd.concat(result, ignore_index=True)


def weighted_quantile(values, weights, q):
    order = np.argsort(values, kind='stable')
    values, weights = np.asarray(values)[order], np.asarray(weights)[order]
    index = min(int(np.searchsorted(np.cumsum(weights), weights.sum()*q, side='left')), len(values)-1)
    return float(values[index])


def summaries(frame):
    rows = []
    for (b, t0, t1), d in frame.groupby(['baseline_year', 't0', 't1'], sort=True):
        total = float(d.flow_pas_tmp_ha.sum())
        row = {'baseline_year': int(b), 't0': int(t0), 't1': int(t1), 'interval': f'{t0}_{t1}',
               'elapsed_intervals': int((t0-b)//5), 'diagnostic_interval': int(t0 == 2020),
               'baseline_interval_by_construction': int(t0 == b), 'cells': len(d),
               'cells_positive_flow': int(d.flow_pas_tmp_ha.gt(0).sum())}
        for field in METRICS[:9]:
            row[field] = float(d[field].sum())
        for label in ('initial', 'entry', 'unresolved'):
            row[label+'_pct'] = 100*row[label+'_ha']/total if total else np.nan
        row['continuous_baseline_stock_retained_pct'] = 100*row['initial_pas_stock_ha']/row['baseline_pas_stock_ha'] if row['baseline_pas_stock_ha'] else np.nan
        positive = d.loc[d.flow_pas_tmp_ha.gt(0)]
        for q in (.1, .5, .9):
            row[f'flow_weighted_cell_initial_share_q{int(q*100):02d}_pct'] = weighted_quantile(100*positive.initial_ha/positive.flow_pas_tmp_ha, positive.flow_pas_tmp_ha, q) if len(positive) else np.nan
        rows.append(row)
    interval = pd.DataFrame(rows)
    calendar = interval.loc[interval.t0.ge(2000)].copy()
    anchor = calendar.loc[calendar.baseline_year.eq(1985)].set_index('t0')
    for label in ('initial', 'entry', 'unresolved'):
        calendar[label+'_delta_vs_b1985_pp'] = calendar[label+'_pct']-calendar.t0.map(anchor[label+'_pct'])
    elapsed = interval.loc[interval.elapsed_intervals.lt(4)].copy()
    anchor = elapsed.loc[elapsed.baseline_year.eq(1985)].set_index('elapsed_intervals')
    for label in ('initial', 'entry', 'unresolved'):
        elapsed[label+'_delta_vs_b1985_same_lag_pp'] = elapsed[label+'_pct']-elapsed.elapsed_intervals.map(anchor[label+'_pct'])
    pools, crossings = [], []
    for b, d in interval.groupby('baseline_year'):
        for label, sub, comparable in [('own_primary_to_2020', d.loc[d.diagnostic_interval.eq(0)], False),
             ('own_full_to_2025', d, False), ('common_calendar_primary_2000_2020', d.loc[d.t0.between(2000, 2015)], True),
             ('common_calendar_diagnostic_2020_2025', d.loc[d.t0.eq(2020)], True),
             ('equal_followup_first_20_years', d.loc[d.elapsed_intervals.lt(4)], True)]:
            row = {'baseline_year': int(b), 'comparison_window': label, 'first_t0': int(sub.t0.min()), 'last_t1': int(sub.t1.max()),
                   'intervals': len(sub), 'window_years': int(sub.t1.max()-sub.t0.min()),
                   'horizon_comparable_across_baselines': comparable, 'includes_diagnostic_interval': bool(sub.diagnostic_interval.max())}
            for field in ('flow_pas_tmp_ha', 'initial_ha', 'entry_ha', 'unresolved_ha'):
                row[field] = float(sub[field].sum())
            for origin in ('initial', 'entry', 'unresolved'):
                row[origin+'_pct'] = 100*row[origin+'_ha']/row['flow_pas_tmp_ha'] if row['flow_pas_tmp_ha'] else np.nan
            pools.append(row)
        primary = d.loc[d.diagnostic_interval.eq(0)]
        crossing = primary.loc[primary.entry_pct.gt(50)].sort_values('t0')
        crossings.append({'baseline_year': int(b), 'first_primary_entry_share_gt50_interval': crossing.interval.iloc[0] if len(crossing) else '',
                          'elapsed_intervals_at_first_gt50': int(crossing.elapsed_intervals.iloc[0]) if len(crossing) else '',
                          'interpretation': 'window_specific_descriptive_statistic_not_process_threshold'})
    return {'canonical_window_origin_interval_summary_v1.csv': interval,
            'canonical_window_origin_calendar_comparison_v1.csv': calendar,
            'canonical_window_origin_elapsed_comparison_v1.csv': elapsed,
            'canonical_window_origin_pooled_summary_v1.csv': pd.DataFrame(pools),
            'canonical_window_origin_crossing_diagnostic_v1.csv': pd.DataFrame(crossings)}


def write_once(path, payload):
    require(not path.exists() or path.read_bytes() == payload, 'Versioned output already exists with different bytes: ' + str(path))
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix+'.partial')
        temporary.write_bytes(payload)
        temporary.replace(path)


def run(root, export_dir, reference_dir, output_dir, scope, pilot_validation=None, attests=False):
    config_path = root / 'config/window_origin_sensitivity_v1.json'
    cfg = json.loads(config_path.read_text())
    refs, reference_inventory = references(cfg, reference_dir)
    manifest, manifest_identity, source = validate_manifest(root, cfg, export_dir, scope)
    native_identity, native_cases = validate_native(root, cfg, export_dir)
    pilot_hash = None
    if scope == 'full':
        require(pilot_validation is not None and pilot_validation.is_file(), 'Full requires pilot PASS JSON')
        pilot = json.loads(pilot_validation.read_text())
        require(pilot['status'] == 'PASS' and pilot['scope'] == 'pilot' and pilot['version'] == VERSION and pilot['native_synthetic_cases'] == native_cases, 'Pilot acceptance differs')
        require(pilot['config_sha256'] == sha(config_path) and pilot['native_synthetic_input']['sha256'] == native_identity['sha256'], 'Pilot config/native input hash differs')
        pilot_hash = sha(pilot_validation)
    fresh, export_inputs, maximum = validate_exports(root, cfg, scope, export_dir, refs, manifest)
    if scope == 'full':
        frame = pd.concat([reuse_early_1985(refs), fresh], ignore_index=True)
        require(len(frame) == 19*cfg['expected_cells'], 'Expected 19 baseline-interval populations')
        products = summaries(frame)
        require(len(products['canonical_window_origin_interval_summary_v1.csv']) == 19 and len(products['canonical_window_origin_calendar_comparison_v1.csv']) == 15 and len(products['canonical_window_origin_elapsed_comparison_v1.csv']) == 12, 'Comparison-table populations differ')
    else:
        frame = fresh
        products = {}
    products['canonical_window_origin_cell_panel_v1.csv' if scope == 'full' else 'pilot_window_origin_native_cell_panel_v1.csv'] = frame
    output_inventory = {}
    for name, d in products.items():
        payload = d.to_csv(index=False, float_format='%.17g', na_rep='').encode('utf-8')
        path = output_dir / name
        output_inventory[name] = {'sha256': hashlib.sha256(payload).hexdigest(), 'rows': len(d), 'bytes': len(payload)}
    report = {'status': 'PASS', 'scope': scope, 'version': VERSION, 'config_sha256': sha(config_path),
              'source_script_snapshot': source, 'operator_attests_unmodified_supplied_script': bool(attests),
              'executed_script_sha256_operator_attested': source['sha256'] if attests else None,
              'independently_verified_remote_script_identity': False,
              'runtime_config_and_native_projection_verified': True, 'native_synthetic_cases': native_cases,
              'native_synthetic_input': native_identity, 'native_field_invariant_counts_zero': True,
              'reference_inputs': reference_inventory, 'run_manifest_input': manifest_identity,
              'fresh_export_inputs': export_inputs, 'maximum_control_or_1985_origin_difference_ha_per_cell': maximum,
              'fresh_rows': len(fresh), 'normalized_rows': len(frame), 'pilot_validation_sha256': pilot_hash,
              'whole_domain_sensitivity_complete': scope == 'full', 'baseline_years': cfg['baselines'],
              'early_1985_reference_rows_reused': 2*cfg['expected_cells'] if scope == 'full' else 0,
              'fresh_native_audit_for_reused_early_rows': False, 'outputs': output_inventory,
              'interpretation_limits': ['The first interval is 100% baseline-continuous by construction where conversion area is positive.',
               'Calendar matches hold endpoint conversions fixed but change origin definitions.',
               'Equal follow-up comparisons change calendar time and baseline cohort composition.',
               'Neither identifies an artifact fraction or proves stationarity/regime change.',
               'Observed entry includes re-entry and is not first-ever establishment.',
               'Pooled interval conversion area is not deduplicated pixel area.',
               '2020-2025 is diagnostic; source classification accuracy is not validated.']}
    # Serialize and check every target before writing any report or table.
    payloads = [(output_dir / name, d.to_csv(index=False, float_format='%.17g', na_rep='').encode('utf-8')) for name, d in products.items()]
    report_name = ('pilot' if scope == 'pilot' else 'canonical') + '_window_origin_sensitivity_validation_v1.json'
    payloads.append((output_dir / report_name, (json.dumps(report, indent=2)+'\n').encode()))
    for path, payload in payloads:
        require(not path.exists() or path.read_bytes() == payload, 'Existing versioned output differs: ' + str(path))
    for path, payload in payloads:
        write_once(path, payload)
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument('--scope', choices=['pilot', 'full'], required=True)
    p.add_argument('--export-dir', type=Path, required=True)
    p.add_argument('--reference-dir', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--pilot-validation', type=Path)
    p.add_argument('--attest-unmodified-supplied-script', action='store_true', help='Operator states the supplied script was copied without edits; this is not independent service attestation.')
    args = p.parse_args()
    report = run(args.root, args.export_dir, args.reference_dir, args.output_dir, args.scope, args.pilot_validation, args.attest_unmodified_supplied_script)
    print('WINDOW ORIGIN SENSITIVITY — ' + args.scope.upper() + ' VALIDATION PASS')
    print('Native synthetic cases:', report['native_synthetic_cases'], '| field mismatch counts: zero')
    print('Fresh rows:', report['fresh_rows'], '| normalized rows:', report['normalized_rows'])
    print('Whole-domain sensitivity complete:', report['whole_domain_sensitivity_complete'])
    print('Outputs:', args.output_dir)


if __name__ == '__main__':
    main()
