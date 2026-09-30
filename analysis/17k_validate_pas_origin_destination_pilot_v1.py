"""Validate one Decision 024 PAS-origin-by-destination pilot batch.

Example in Colab after mounting Drive:
python 17k_validate_pas_origin_destination_pilot_v1.py \
  --export /content/drive/MyDrive/pasture_spell_closure_pilot_v1/canonical_pas_origin_destination_2015_2020_b00_pilot_v1.csv \
  --baseline /content/drive/MyDrive/pasture_crop_dynamic_canonical/canonical_stock_flow_2015_2020_full_v1.csv \
  --rq2-batch /content/drive/MyDrive/pasture_spell_remediation_v3/canonical_pas_tmp_origin_2015_2020_b00_v3.csv \
  --output /content/drive/MyDrive/Trabalho/Contabilidade/spatial/phase9/pasture_spell_closure_pilot_v1/canonical_pas_origin_destination_2015_2020_b00_validation_v1.json

Confirm the actual RQ2 batch path; --rq2-batch is always explicit.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

ORIGINS = ('initial', 'new', 'unresolved')
DESTS = ('pas', 'tmp', 'nat', 'oag', 'out', 'water', 'nodata',
         'unexpected', 'masked')
OBSERVED = ('tmp', 'nat', 'oag', 'out', 'water')
LOSS = ('nodata', 'unexpected', 'masked')
TOL = 0.01  # hectares per cell; same order as accepted interval validator


def require(ok, message):
    if not ok:
        raise ValueError(message)


def number(row, field, cid):
    try:
        x = float(row[field])
    except (KeyError, TypeError, ValueError) as e:
        raise ValueError(f'{cid}: missing or invalid {field}') from e
    require(math.isfinite(x), f'{cid}: nonfinite {field}')
    require(x >= -1e-7, f'{cid}: negative {field}')
    return x


def same(actual, expected, label):
    require(abs(actual-expected) <= TOL,
            f'{label}: {actual:.9f} versus {expected:.9f} ha')


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def load(path, label):
    require(path.is_file(), f'Missing {label}: {path}')
    rows = {}
    with path.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        require(reader.fieldnames and 'cell_id' in reader.fieldnames,
                f'{label}: missing cell_id')
        for row in reader:
            cid = row['cell_id'].strip()
            require(cid and cid not in rows, f'{label}: duplicate/empty {cid}')
            rows[cid] = row
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--export', required=True, type=Path)
    p.add_argument('--baseline', required=True, type=Path)
    p.add_argument('--rq2-batch', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args()
    actual = load(a.export, 'closure export')
    baseline = load(a.baseline, 'canonical stock-flow baseline')
    rq2 = load(a.rq2_batch, 'accepted RQ2 batch')
    require(set(actual) == set(rq2),
            'Closure export and RQ2 batch cell populations differ')
    require(set(actual) <= set(baseline),
            'Closure export includes a cell outside canonical baseline')
    require(len(baseline) == 24889,
            f'Expected 24,889 baseline cells, got {len(baseline)}')
    require(len(actual) > 0, 'Empty closure batch')
    totals = {'stock0_pas':0.0, 'observed_outflow':0.0,
              'observation_loss':0.0, 'persistence':0.0}
    for cid, row in actual.items():
        base, source = baseline[cid], rq2[cid]
        t0, t1 = int(float(row['t0'])), int(float(row['t1']))
        batch = int(float(row['source_batch_id']))
        require((t0,t1,batch) == (2015,2020,0),
                f'{cid}: pilot only accepts 2015-2020 batch 0')
        for other, label in ((base,'baseline'),(source,'RQ2')):
            require((int(float(other['t0'])),int(float(other['t1'])),
                     int(float(other['source_batch_id']))) ==
                    (t0,t1,batch), f'{cid}: {label} key mismatch')
        stock = number(row,'stock0_pas',cid)
        same(stock,number(base,'stock0_pas',cid),f'{cid} initial PAS stock')
        same(stock,math.fsum(number(row,'origin_'+o,cid) for o in ORIGINS),
             f'{cid} origin partition of initial PAS stock')
        flows = {}
        for d in DESTS:
            flow = number(row,'flow_pas_'+d,cid)
            flows[d] = flow
            same(flow,number(base,'flow_pas_'+d,cid),
                 f'{cid} canonical PAS->{d}')
            same(flow,math.fsum(number(row,'pas_'+o+'_to_'+d,cid)
                                for o in ORIGINS),
                 f'{cid} origin partition of PAS->{d}')
        for o in ORIGINS:
            same(number(row,'origin_'+o,cid),
                 math.fsum(number(row,'pas_'+o+'_to_'+d,cid) for d in DESTS),
                 f'{cid} destinations of {o} PAS stock')
            same(number(row,'pas_'+o+'_to_tmp',cid),
                 number(source,'new_'+o,cid),
                 f'{cid} previously validated RQ2 {o} origin')
        observed = math.fsum(flows[d] for d in OBSERVED)
        loss = math.fsum(flows[d] for d in LOSS)
        same(stock,flows['pas']+observed+loss,
             f'{cid} PAS stock = persistence + outflow + observation loss')
        for k,v in [('stock0_pas',stock),('observed_outflow',observed),
                    ('observation_loss',loss),('persistence',flows['pas'])]:
            totals[k] += v
    same(totals['stock0_pas'],
         totals['persistence']+totals['observed_outflow']+
         totals['observation_loss'],'pilot aggregate closure')
    record = {'status':'PASS', 'scope':'2015_2020_batch_00_pilot_only',
              'cells':len(actual), 'baseline_cells':len(baseline),
              'tolerance_ha_per_cell':TOL,'totals_ha':totals,
              'inputs':{label:{'filename':str(path),'sha256':digest(path)}
                        for label,path in [('export',a.export),
                          ('baseline',a.baseline),('rq2_batch',a.rq2_batch)]},
              'decision_024_full_domain_complete':False}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(record,indent=2,allow_nan=False)+'\n',
                        encoding='utf-8')
    print('PAS ORIGIN x DESTINATION PILOT — VALIDATION PASS')
    print('Cells:',len(actual),'| initial PAS ha:',totals['stock0_pas'])
    print('Validation:',a.output)


if __name__ == '__main__':
    main()
