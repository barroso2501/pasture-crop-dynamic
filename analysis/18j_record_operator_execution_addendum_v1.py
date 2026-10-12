"""Append an operator attestation without editing the accepted execution JSON.

Requires the exact saved text used and an explicit operator declaration. It
does not execute GEE or independently establish the historical remote text.
"""
from pathlib import Path
import argparse,hashlib,json,re
from datetime import datetime,timezone

def build(script,validation,operator,gee_path,execution_date=None,commit=None):
    accepted=json.loads(validation.read_text())
    if accepted.get('status')!='PASS' or accepted.get('scope')!='full':raise ValueError('Requires the accepted full validation JSON')
    if not operator.strip() or not gee_path.strip():raise ValueError('Operator and GEE script path required')
    digest=hashlib.sha256(script.read_bytes()).hexdigest()
    expected=accepted['source_script_snapshot']['sha256']
    return {'record_type':'operator_execution_text_attestation_addendum_v1',
            'recorded_at_utc':datetime.now(timezone.utc).isoformat(),'operator_name':operator,
            'operator_attests_exact_text_used':True,'gee_script_path_operator_supplied':gee_path,
            'execution_date_operator_supplied':execution_date,'repository_commit_operator_supplied':commit,
            'accepted_validation_filename':validation.name,
            'accepted_validation_sha256':hashlib.sha256(validation.read_bytes()).hexdigest(),
            'executed_script_sha256_operator_attested':digest,
            'supplied_snapshot_sha256_in_original_record':expected,
            'matches_supplied_snapshot_bytes':digest==expected,
            'remote_execution_identity_independently_verified':False,
            'status':'operator_attestation_recorded' if digest==expected else 'operator_attestation_recorded_snapshot_differs_revalidation_required',
            'historical_validation_json_modified':False,
            'limits':['This records an operator declaration, not independent service evidence.',
                      'A current file without the exact-text-used declaration cannot fill this gap.',
                      'Different source bytes require review/revalidation; no silent reassociation.']}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--executed-script',type=Path,required=True)
    p.add_argument('--accepted-validation',type=Path,required=True)
    p.add_argument('--operator-name',required=True)
    p.add_argument('--gee-script-path',required=True)
    p.add_argument('--operator-attests-exact-text-used',action='store_true',required=True)
    p.add_argument('--execution-date')
    p.add_argument('--repository-commit')
    p.add_argument('--addendum-id',required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+',a.addendum_id):p.error('Invalid addendum-id')
    record=build(a.executed_script,a.accepted_validation,a.operator_name,a.gee_script_path,a.execution_date,a.repository_commit)
    out=a.output_dir/(a.addendum_id+'.json')
    if out.exists():raise ValueError('Addendum already exists; choose a new ID')
    snapshot=a.output_dir/(record['executed_script_sha256_operator_attested']+'_'+a.executed_script.name)
    if snapshot.exists() and snapshot.read_bytes()!=a.executed_script.read_bytes():raise ValueError('Conflicting snapshot')
    a.output_dir.mkdir(parents=True,exist_ok=True)
    if not snapshot.exists():snapshot.write_bytes(a.executed_script.read_bytes())
    record['script_snapshot_file']=snapshot.name
    out.write_text(json.dumps(record,indent=2)+'\n')
    print(record['status']);print(out)
