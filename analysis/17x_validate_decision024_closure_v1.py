"""Verify the compact Decision 024 closure package; optionally recheck full cell CSVs.

Usage: python analysis/17x_validate_decision024_closure_v1.py --root .
Optional: --closure-dir /content/drive/MyDrive/Trabalho/Contabilidade/spatial/phase9/pasture_spell_closure_full_v1
This validates existing artifacts; it does not run GEE or rewrite upstream records.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def table(path):
    with path.open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument('--closure-dir', type=Path)
    args = p.parse_args()
    root = args.root.resolve()
    base = root / 'outputs/validation/decision024_closure_v1'
    review = json.loads((base / 'canonical_decision024_closure_validation_v1.json').read_text())
    require(review['status'] == 'PASS' and review['criterion_12'] == 'PASS', 'Review status differs')
    require(review['decision_024_fully_implemented'] is True, 'Closure flag differs')
    require(all(v is True for v in review['checks'].values()), 'A review check is not PASS')
    require([x['criterion'] for x in review['acceptance_criteria']] == list(range(1, 13)), 'Criteria population differs')
    for rel, identity in review['outputs'].items():
        path = root / rel
        require(path.is_file() and path.stat().st_size == identity['bytes'] and sha(path) == identity['sha256'], 'Artifact hash differs: ' + rel)
    old_path = root / 'outputs/summary/phase9a2_terminology_harmonization_v1/canonical_integrated_evidence_matrix_v3.csv'
    old = table(old_path)
    new = table(root / 'outputs/summary/decision024_closure_v1/canonical_integrated_evidence_matrix_v4.csv')
    term = json.loads((root / 'outputs/validation/phase9a2_terminology_harmonization_v1/canonical_phase9a2_terminology_validation_v1.json').read_text())
    require(sha(old_path) == term['outputs'][old_path.name]['sha256'], 'Historical matrix authentication fails')
    require(len(new) == len(old) == 35, 'Matrix population differs')
    require(len({x['finding_id'] for x in new}) == 35, 'Duplicate finding')
    changed = []
    for a, b in zip(old, new):
        require(a['finding_id'] == b['finding_id'], 'Finding order or identity differs')
        a = {k: v for k, v in a.items() if k != 'evidence_matrix_version'}
        bb = {k: v for k, v in b.items() if k != 'evidence_matrix_version'}
        if a != bb:
            changed.append(b['finding_id'])
            require(sha(root / b['source_relative_path']) == b['source_sha256'], 'Corrected finding source hash differs')
        require(b['causal_claim_flag'] == '0', 'Causal claim introduced')
    require(changed == ['P9A035', 'P9A036', 'P9A037'], 'Substantive change scope differs')
    v1 = root / 'outputs/validation/pasture_age_remediation_v1/canonical_evidence_status_events_v1.csv'
    v2 = base / 'canonical_evidence_status_events_v2.csv'
    require(v2.read_bytes().startswith(v1.read_bytes()), 'Historical event bytes differ')
    events = table(v2)
    require(len(events) == 6 and len({x['event_id'] for x in events}) == 6, 'Status-event population differs')
    for fid in changed:
        history = [x for x in events if x['finding_id'] == fid]
        require([x['event_status'] for x in history] == ['suspended', 'rescinded'], 'Invalid event sequence: ' + fid)
        require(history[-1]['source_version'] == 'canonical_integrated_evidence_matrix_v4', 'Rescission targets wrong edition')
    intervals = table(root / 'outputs/summary/pasture_spell_panel_v2/canonical_pas_tmp_origin_interval_summary_v2.csv')
    pooled = table(root / 'outputs/summary/pasture_spell_panel_v2/canonical_pas_tmp_origin_pooled_summary_v2.csv')
    require(len(intervals) == 8 and [int(x['diagnostic_interval']) for x in intervals] == [0]*7+[1], 'Interval roles differ')
    for x in intervals:
        total = float(x['flow_pas_tmp_ha'])
        require(abs(sum(float(x[o + '_ha']) for o in ('initial', 'new', 'unresolved')) - total) <= .001, 'Interval partition fails')
        for o in ('initial', 'new', 'unresolved'):
            require(abs(float(x[o+'_ha']) / total*100 - float(x[o+'_pct'])) <= 1e-9, 'Interval share differs')
    for x in pooled:
        sub = intervals if int(x['includes_diagnostic_interval']) else intervals[:-1]
        for field in ('flow_pas_tmp_ha', 'initial_ha', 'new_ha', 'unresolved_ha'):
            require(abs(sum(float(z[field]) for z in sub) - float(x[field])) <= .001, 'Pooled total differs: ' + field)
    # Exact original JS functions/update are embedded in scalar runners and tied to their source hashes.
    synth = json.loads((base / 'canonical_pasture_spell_synthetic_review_v1.json').read_text())
    pilot = root / 'gee/17a_reconstruct_observed_pasture_spell_age_pilot_v1.js'
    prod = root / 'gee/17g_compare_pas_tmp_origin_interval_batches_v1.js'
    require(sha(pilot) == synth['pilot_js_sha256'] and sha(prod) == synth['production_js_sha256'], 'Source logic hashes differ')
    for runner, required_fragment in [('closure_synthetic_exact.js', pilot.read_text().split('var S =', 1)[1].split('var source = ee.Image', 1)[0]), ('closure_production_engine.js', prod.read_text().split('var previous=', 1)[1].split('\nvar c0=', 1)[0])]:
        require(required_fragment in (root / 'analysis' / runner).read_text(), 'Runner does not contain the exact source segment')
    # Runners can be executed if Node is available; prior recorded runs remain part of provenance.
    import shutil
    if shutil.which('node'):
        for runner in ('closure_synthetic_exact.js', 'closure_production_engine.js'):
            done = subprocess.run(['node', str(root / 'analysis' / runner)], check=True, capture_output=True, text=True)
            require(json.loads(done.stdout)['status'] == 'PASS', 'Synthetic runner fails')
    if args.closure_dir:
        import numpy as np
        import pandas as pd
        ids = None
        for rec in review['independent_review']['closure_records']:
            path = args.closure_dir / Path(rec['project_relative_path']).name
            require(sha(path) == rec['raw_csv_sha256'], 'External cell CSV hash differs')
            f = pd.read_csv(path, dtype={'cell_id': 'string'}, float_precision='round_trip')
            require(len(f) == 24889 and f.cell_id.is_unique and f.cell_id.notna().all(), 'External cell population differs')
            keys = set(f.cell_id)
            if ids is None:
                ids = keys
            require(keys == ids, 'External cell sets differ')
            states = ('pas', 'tmp', 'nat', 'oag', 'out', 'water', 'nodata', 'unexpected', 'masked')
            cols = [c for c in f if c.startswith(('flow_pas_', 'pas_initial_to_', 'pas_new_to_', 'pas_unresolved_to_')) or c in ('stock0_pas', 'origin_initial', 'origin_new', 'origin_unresolved', 'pas_observed_outflow_ha', 'pas_observation_loss_ha')]
            require(np.isfinite(f[cols].to_numpy()).all() and f[cols].min().min() >= -1e-9, 'Invalid area value')
            residuals = [f.stock0_pas-f[['origin_initial', 'origin_new', 'origin_unresolved']].sum(axis=1)]
            for state in states:
                residuals.append(f['flow_pas_'+state]-f[[f'pas_{o}_to_{state}' for o in ('initial','new','unresolved')]].sum(axis=1))
            for o in ('initial','new','unresolved'):
                residuals.append(f['origin_'+o]-f[[f'pas_{o}_to_{state}' for state in states]].sum(axis=1))
            residuals.append(f.stock0_pas-f.flow_pas_pas-f.pas_observed_outflow_ha-f.pas_observation_loss_ha)
            require(max(float(r.abs().max()) for r in residuals) <= .01, 'External cell closure fails')
    print('DECISION 024 CLOSURE PACKAGE — PASS')
    print('35 findings; exactly 3 corrected; 32 preserved; 6 cumulative events; 12 criteria recorded PASS.')
    print('Full external cell CSVs checked:', bool(args.closure_dir))
    print('Historical source-age statements remain superseded; current authority is matrix v4.')


if __name__ == '__main__':
    main()
