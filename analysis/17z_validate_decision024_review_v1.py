"""Check the current review package and archived byte-exact closure dependencies.

python analysis/17z_validate_decision024_review_v1.py --root .
Optional --closure-dir <eight-full-v3-CSV-directory> rechecks supplementary sums.
--write-report creates the versioned review report; it never edits upstream JSONs.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import tempfile


REV = 'outputs/validation/decision024_review_v1'
SUM = 'outputs/summary/decision024_review_v1'
REPORT = REV + '/canonical_decision024_review_validation_v1.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        result = list(reader)
        if any(None in x or any(v is None for v in x.values()) for x in result):
            raise ValueError('CSV column mismatch: ' + path.name)
        return result


def require(value, message):
    if not value:
        raise ValueError(message)


def validate(root, closure_dir=None):
    checks = {}
    mapping = rows(root / REV / 'canonical_historical_document_snapshot_map_v1.csv')
    require(len({x['updated_path'] for x in mapping}) == len(mapping), 'Repeated historical path')
    mapped = {x['updated_path']: x for x in mapping}
    for x in mapping:
        require(sha(root / x['original_snapshot_path']) == x['original_sha256'], 'Historical snapshot hash differs')
        text = (root / x['updated_path']).read_text()
        if text.startswith('> **Status notice'):
            require(text.split('\n\n', 1)[1] == (root / x['original_snapshot_path']).read_text(), 'Historical body changed beyond notice')
    checks['historical_snapshots_and_banner_bodies_preserved'] = True
    original = json.loads((root / 'outputs/validation/decision024_closure_v1/canonical_decision024_closure_validation_v1.json').read_text())
    require(original['status'] == 'PASS', 'Original review differs')
    for rel, value in original['outputs'].items():
        path = root / (mapped[rel]['original_snapshot_path'] if rel in mapped else rel)
        require(path.stat().st_size == value['bytes'] and sha(path) == value['sha256'], 'Historical closure artifact differs: ' + rel)
    checks['original_closure_output_hashes_resolve_current_or_archived_bytes'] = True
    v4path = root / 'outputs/summary/decision024_closure_v1/canonical_integrated_evidence_matrix_v4.csv'
    v4 = rows(v4path)
    newpath = root / SUM / 'canonical_integrated_evidence_matrix_v4_1.csv'
    new = rows(newpath)
    require(newpath.read_bytes().startswith(b'\xef\xbb\xbf'), 'v4.1 BOM is missing')
    require(len(v4) == len(new) == 35 and len({x['finding_id'] for x in new}) == 35, 'Matrix population differs')
    changed = []
    for old, now in zip(v4, new):
        require(old['finding_id'] == now['finding_id'], 'Matrix identity/order differs')
        a = {k: v for k, v in old.items() if k != 'evidence_matrix_version'}
        b = {k: v for k, v in now.items() if k != 'evidence_matrix_version'}
        if a != b:
            changed.append(now['finding_id'])
            require(now['evidence_status'] == 'qualified' and 'by construction' in now['interpretation_boundary'], 'Window qualification missing')
        for key in ('source_relative_path', 'source_sha256', 'source_authenticated', 'causal_claim_flag'):
            require(now[key] == old[key], 'Source or causal flag changed')
        require(now['causal_claim_flag'] == '0', 'Causal claim introduced')
    require(changed == ['P9A035', 'P9A036'], 'Erratum changed unintended findings')
    checks['only_two_interpretations_changed_33_substantive_rows_preserved'] = True
    checks['v4_unchanged_v4_1_bom_and_source_hashes_preserved'] = True
    v2 = rows(root / 'outputs/validation/decision024_closure_v1/canonical_evidence_status_events_v2.csv')
    v3path = root / REV / 'canonical_evidence_status_events_v3.csv'
    v3 = rows(v3path)
    require(len(v2) == 6 and len(v3) == 8, 'Event population differs')
    require(len({x['event_id'] for x in v3}) == 8, 'Duplicate event')
    for old, now in zip(v2, v3[:6]):
        require(all(now[k] == v for k, v in old.items()), 'Historical event field changed')
    require([x['finding_id'] for x in v3[6:]] == changed, 'Erratum event scope differs')
    require(all(line.startswith('"') for line in v3path.read_text().splitlines()), 'Event CSV is not explicitly quoted')
    checks['historical_event_fields_preserved_v3_has_two_interpretation_events'] = True
    summary = json.loads((root / SUM / 'canonical_pas_nat_origin_summary_validation_v1.json').read_text())
    require(summary['status'] == 'PASS' and summary['eight_input_csvs_authenticated'], 'NAT aggregation not accepted')
    require(summary['primary_direction_agreements'] == summary['primary_comparisons'] == 6 and summary['diagnostic_direction_agrees'] is False, 'NAT/TMP direction scope differs')
    for name, info in summary['outputs'].items():
        require(sha(root / SUM / name) == info['sha256'], 'NAT output hash differs')
    interval = rows(root / SUM / 'canonical_pas_nat_origin_interval_summary_v1.csv')
    pooled = rows(root / SUM / 'canonical_pas_nat_origin_pooled_summary_v1.csv')
    require(len(interval) == 8 and len(pooled) == 2, 'NAT summary population differs')
    for x in interval:
        total = float(x['flow_pas_nat_ha'])
        require(abs(sum(float(x[o + '_ha']) for o in ('initial', 'new', 'unresolved')) - total) <= .001, 'NAT partition differs')
        for o in ('initial', 'new', 'unresolved'):
            require(abs(100 * float(x[o + '_ha']) / total - float(x[o + '_pct'])) < 1e-9, 'NAT share differs')
    for x in pooled:
        sub = interval if int(x['includes_diagnostic_interval']) else interval[:-1]
        for field in ('flow_pas_nat_ha', 'initial_ha', 'new_ha', 'unresolved_ha'):
            require(abs(sum(float(z[field]) for z in sub) - float(x[field])) <= .001, 'NAT pooled total differs')
    checks['nat_summaries_hashes_partitions_pools_and_direction_verified'] = True
    release = rows(root / 'config/public_release_decision024_required_files_v1.csv')
    raw = {Path(x['project_relative_path']).name: x for x in original['independent_review']['closure_records']}
    require(len(release) == 11, 'Release dependencies incomplete')
    require(all(x['required_for'] == 'v1.0.0' and x['doi_status'] == 'pending_not_minted' for x in release), 'Unjustified DOI/release status')
    for x in release[:8]:
        require(x['sha256'] == raw[Path(x['source_relative_path']).name]['raw_csv_sha256'], 'Release raw hash differs')
    panel = json.loads((root / 'outputs/validation/pasture_spell_panel_v2/canonical_pasture_spell_panel_v2_validation.json').read_text())
    require({x['sha256'] for x in release[8:]} == {x['sha256'] for x in panel['outputs'].values()}, 'Release Parquet hash differs')
    checks['eight_csv_and_three_parquet_doi_dependencies_recorded_without_claiming_deposit'] = True
    methods = (root / 'docs/methods/data_sources_and_classification.md').read_text()
    require('The affected findings P9A035–P9A037 remain suspended' not in methods, 'Normative suspension still stale')
    require('uncertain_pair_ha' in methods and 'have not been quantified' not in methods, 'Boundary definition missing')
    require('has not been quantified' in methods and 'not exactly identical between years' in methods, 'Boundary population or equality overclaimed')
    readme = (root / 'README.md').read_text()
    require('Phases 2–8 were not re-executed' in readme and '100% initial by construction' in readme, 'README scope warning missing')
    # Current clickable documentation links must resolve; historic plain-text paths are not treated as bundled data.
    for rel in ['README.md', 'docs/decisions/024_implementation_closure_v2.md'] + list(mapped):
        if not rel.endswith('.md'):
            continue
        path = root / rel
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if target.startswith(('https:', 'http:', '#', 'mailto:')):
                continue
            require((path.parent / target.split('#')[0]).is_file(), 'Broken current link: ' + rel + ' -> ' + target)
    checks['current_methods_readme_and_navigation_links_consistent'] = True
    if closure_dir:
        import importlib.util
        module_path = root / 'analysis/17y_summarize_pas_nat_origins_v1.py'
        spec = importlib.util.spec_from_file_location('pas_nat', module_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as work:
            mod.aggregate(root, closure_dir, Path(work))
            for name in summary['outputs']:
                require(sha(Path(work) / name) == summary['outputs'][name]['sha256'], 'Reproduced raw aggregate differs')
        checks['optional_full_cell_nat_reproduction'] = True
    return checks


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument('--closure-dir', type=Path)
    p.add_argument('--write-report', action='store_true')
    args = p.parse_args()
    root = args.root.resolve()
    checks = validate(root, args.closure_dir)
    report_path = root / REPORT
    if args.write_report:
        outputs = {}
        for path in sorted(root.rglob('*')):
            rel = path.relative_to(root).as_posix()
            if path.is_file() and rel not in (REPORT, 'GITHUB_PACKAGE_MANIFEST.csv') and '__pycache__' not in rel:
                outputs[rel] = {'sha256': sha(path), 'bytes': path.stat().st_size}
        report = {'status': 'PASS', 'review_date': '2026-10-09', 'scope': 'interpretation_documentation_supplementary_aggregation_and_release_dependencies',
                  'checks': checks, 'outputs': outputs, 'findings': 35, 'substantive_interpretations_amended': ['P9A035', 'P9A036'],
                  'scientific_window_sensitivity_executed': False, 'entry_reentry_decomposition_executed': False,
                  'new_native_gee_execution': False, 'independent_all_pixel_invariant_verification': False,
                  'unqualified_empirical_completion_certified': False, 'phases_2_to_8_reexecuted': False,
                  'doi_release_deposited': False, 'parquet_bytes_rehashed_in_this_review': False,
                  'native_classification_accuracy_validated': False,
                  'previous_closure_json_unchanged': True, 'previous_matrix_v4_and_events_v2_unchanged': True,
                  'original_17x_reproduction_scope': 'original_closure_zip_not_current_banner_updated_tree'}
        report_path.write_text(json.dumps(report, indent=2) + '\n')
    else:
        report = json.loads(report_path.read_text())
        require(report['status'] == 'PASS', 'Review report status differs')
        for rel, meta in report['outputs'].items():
            path = root / rel
            require(path.stat().st_size == meta['bytes'] and sha(path) == meta['sha256'], 'Current artifact differs: ' + rel)
    print('REVIEW PACKAGE — PASS: 35 findings; only 2 interpretations amended; historical source data preserved.')
    print('PAS->NAT supplementary summaries verified. Window sensitivity, native assurance and DOI deposit remain pending.')


if __name__ == '__main__':
    main()
