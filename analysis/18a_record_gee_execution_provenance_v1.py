"""Record exact local script/configuration snapshots and export hashes for a GEE run.

This records operator-supplied provenance; it does not execute or authenticate GEE.
Example:
python analysis/18a_record_gee_execution_provenance_v1.py \
  --script gee/17u_export_pasture_age_source_audit_v1.js \
  --run-id audit-20261009 --gee-path users/barroso2501/pasture-crop:17u \
  --constants-file config/constants.js --state prepared --output-dir execution_records
After execution, use --state completed --operator-attests-exact-script and
one or more --export-file arguments; keep the saved snapshot unchanged.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil


def identity(path):
    return {'filename': path.name, 'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--script', type=Path, required=True)
    p.add_argument('--constants-file', type=Path)
    p.add_argument('--run-id', required=True)
    p.add_argument('--gee-path', required=True)
    p.add_argument('--repository-commit')
    p.add_argument('--state', choices=['prepared', 'completed'], default='prepared')
    p.add_argument('--operator-attests-exact-script', action='store_true')
    p.add_argument('--export-file', type=Path, action='append', default=[])
    p.add_argument('--output-dir', type=Path, required=True)
    args = p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.run_id):
        p.error('run-id must contain only letters, digits, underscores or hyphens')
    if args.state == 'completed' and (not args.operator_attests_exact_script or not args.export_file):
        p.error('completed requires the operator attestation and at least one export-file')
    script_id = identity(args.script)
    constants_id = identity(args.constants_file) if args.constants_file else None
    exports = [identity(path) for path in args.export_file]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    # Content-addressed snapshots never silently replace a different executed script.
    for path, meta in [(args.script, script_id)] + ([(args.constants_file, constants_id)] if args.constants_file else []):
        target = args.output_dir / (meta['sha256'] + '_' + path.name)
        if target.exists() and target.read_bytes() != path.read_bytes():
            raise ValueError('Snapshot differs: ' + target.name)
        if not target.exists():
            shutil.copyfile(path, target)
        meta['snapshot_file'] = target.name
    record = {'run_id': args.run_id, 'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
              'execution_state': args.state, 'gee_repository_path': args.gee_path,
              'repository_commit': args.repository_commit, 'script': script_id,
              'executed_script_sha256': script_id['sha256'] if args.state == 'completed' else None,
              'script_snapshot_sha256': script_id['sha256'], 'constants': constants_id,
              'exports': exports, 'operator_attests_exact_script': args.operator_attests_exact_script,
              'independently_verified_remote_execution': False,
              'limits': ['Commit is operator-supplied and not independently checked.',
                         'Asset identifiers do not pin mutable remote raster bytes.',
                         'Historical null execution hashes are not retroactively filled from current source.']}
    record_path = args.output_dir / (args.run_id + '_' + args.state + '.json')
    if record_path.exists():
        raise ValueError('Record already exists; choose a new run-id rather than overwrite provenance')
    record_path.write_text(json.dumps(record, indent=2) + '\n')
    print(record_path)


if __name__ == '__main__':
    main()
