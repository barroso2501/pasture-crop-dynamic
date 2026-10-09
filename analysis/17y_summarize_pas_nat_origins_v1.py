"""Aggregate supplementary PAS->NAT origins from the eight authenticated cell CSVs.

python analysis/17y_summarize_pas_nat_origins_v1.py --closure-dir /path/to/csvs
Requires pandas and numpy. Does not run Earth Engine or modify accepted inputs.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(test, message):
    if not test:
        raise ValueError(message)


def aggregate(root, source, output):
    accepted = json.loads((root / 'outputs/validation/decision024_closure_v1/canonical_decision024_closure_validation_v1.json').read_text())
    tmp = pd.read_csv(root / 'outputs/summary/pasture_spell_panel_v2/canonical_pas_tmp_origin_interval_summary_v2.csv', float_precision='round_trip')
    records, rows, ids, max_residual = [], [], None, 0.0
    for rec in accepted['independent_review']['closure_records']:
        tag = rec['interval']
        t0, t1 = map(int, tag.split('_'))
        path = source / Path(rec['project_relative_path']).name
        require(sha(path) == rec['raw_csv_sha256'], 'Input hash differs: ' + path.name)
        frame = pd.read_csv(path, dtype={'cell_id': 'string'}, float_precision='round_trip')
        require(len(frame) == 24889 and frame.cell_id.notna().all() and frame.cell_id.is_unique, 'Cell population differs')
        keys = set(frame.cell_id)
        if ids is None:
            ids = keys
        require(keys == ids, 'Cell identities differ')
        require(frame.t0.eq(t0).all() and frame.t1.eq(t1).all(), 'Interval differs')
        require(frame.diagnostic_interval.eq(int(t0 == 2020)).all(), 'Diagnostic flag differs')
        cols = ['flow_pas_nat', 'flow_pas_tmp'] + ['pas_' + o + '_to_' + d for d in ('nat', 'tmp') for o in ('initial', 'new', 'unresolved')]
        require(np.isfinite(frame[cols].to_numpy()).all() and frame[cols].min().min() >= 0, 'Invalid area')
        ref = tmp.loc[tmp.interval.eq(tag)].iloc[0]
        for dest in ('nat', 'tmp'):
            residual = frame['flow_pas_' + dest] - frame[['pas_' + o + '_to_' + dest for o in ('initial', 'new', 'unresolved')]].sum(axis=1)
            max_residual = max(max_residual, float(residual.abs().max()))
            require(float(residual.abs().max()) <= .01, 'Per-cell destination partition fails')
            total = float(frame['flow_pas_' + dest].sum())
            components = {o + '_ha': float(frame['pas_' + o + '_to_' + dest].sum()) for o in ('initial', 'new', 'unresolved')}
            require(abs(sum(components.values()) - total) <= .001, 'Aggregated destination partition fails')
            if dest == 'tmp':
                require(abs(total - ref.flow_pas_tmp_ha) <= .001, 'Accepted TMP total differs')
                for key, value in components.items():
                    require(abs(value - float(ref[key])) <= .001, 'Accepted TMP origin differs')
            else:
                rows.append({'interval': tag, 'diagnostic_interval': int(t0 == 2020), 'flow_pas_nat_ha': total, **components,
                             **{o + '_pct': 100 * components[o + '_ha'] / total for o in ('initial', 'new', 'unresolved')}})
        records.append({'interval': tag, 'filename': path.name, 'sha256': sha(path), 'rows': len(frame)})
    require(len(rows) == 8, 'Expected eight intervals')
    nat = pd.DataFrame(rows).sort_values('interval')
    pooled_rows = []
    for name, include in [('primary_1985_2020', 0), ('full_observed_1985_2025', 1)]:
        sub = nat if include else nat.loc[nat.diagnostic_interval.eq(0)]
        sums = {col: float(sub[col].sum()) for col in ('flow_pas_nat_ha', 'initial_ha', 'new_ha', 'unresolved_ha')}
        pooled_rows.append({'window': name, 'includes_diagnostic_interval': include, 'intervals': len(sub), **sums,
                            **{o + '_pct': 100 * sums[o + '_ha'] / sums['flow_pas_nat_ha'] for o in ('initial', 'new', 'unresolved')}})
    pooled = pd.DataFrame(pooled_rows)
    comp = nat[['interval', 'diagnostic_interval', 'initial_pct', 'new_pct']].merge(tmp[['interval', 'initial_pct', 'new_pct']], on='interval', validate='one_to_one', suffixes=('_nat', '_tmp'))
    for dest in ('nat', 'tmp'):
        comp['initial_change_pp_' + dest] = comp['initial_pct_' + dest].diff()
    comp['direction_agrees_with_tmp'] = (np.sign(comp.initial_change_pp_nat) == np.sign(comp.initial_change_pp_tmp)).astype('boolean')
    comp.loc[0, 'direction_agrees_with_tmp'] = pd.NA
    output.mkdir(parents=True, exist_ok=True)
    files = []
    for frame, name in [(nat, 'canonical_pas_nat_origin_interval_summary_v1.csv'), (pooled, 'canonical_pas_nat_origin_pooled_summary_v1.csv'), (comp, 'canonical_pas_nat_tmp_origin_direction_comparison_v1.csv')]:
        path = output / name
        frame.to_csv(path, index=False)
        files.append(path)
    report = {'status': 'PASS', 'scope': 'supplementary_pas_nat_origin_aggregation_only', 'native_pixel_reprocessing': False,
              'eight_input_csvs_authenticated': True, 'input_records': records, 'cells_per_interval': 24889,
              'maximum_destination_identity_residual_ha_per_cell': max_residual,
              'accepted_pas_tmp_summaries_reproduced': True,
              'primary_direction_agreements': int(comp.iloc[1:7].direction_agrees_with_tmp.sum()), 'primary_comparisons': 6,
              'diagnostic_direction_agrees': bool(comp.iloc[7].direction_agrees_with_tmp),
              'limits': ['First interval is 100% initial by construction.', 'Shares are window-dependent, not process thresholds.',
                         'Pooled areas may count a pixel in several intervals.', 'PAS->NAT does not by itself identify ecological regeneration.',
                         'No spatial or causal inference; no uncertainty decomposition or window sensitivity executed.'],
              'outputs': {p.name: {'sha256': sha(p), 'bytes': p.stat().st_size} for p in files}}
    (output / 'canonical_pas_nat_origin_summary_validation_v1.json').write_text(json.dumps(report, indent=2) + '\n')
    return nat, pooled, comp, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--closure-dir', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    output = args.output_dir or args.root / 'outputs/summary/decision024_review_v1'
    nat, pooled, comp, report = aggregate(args.root, args.closure_dir, output)
    print('PAS->NAT supplementary summary: PASS; 8 authenticated inputs, 24,889 cells each.')
    print(pooled.to_string(index=False))


if __name__ == '__main__':
    main()
