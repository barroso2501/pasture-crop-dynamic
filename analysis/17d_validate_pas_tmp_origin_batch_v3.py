"""Validate a small RQ2 pasture-origin batch against canonical v1 CSV.

python 17d_validate_pas_tmp_origin_batch_v3.py --pilot PILOT.csv \
  --baseline canonical_stock_flow_2015_2020_full_v1.csv --output-dir OUT
"""
import argparse
import csv
import json
import math
from pathlib import Path

OLD=('censored','new','unresolved','unattributed')
NEW=('initial','new','unresolved')
SOURCE={'censored':'pas_tmp_censored','new':'pas_tmp_new',
        'unresolved':'pas_tmp_unresolved_age',
        'unattributed':'pas_tmp_unattributed_age'}
TOL=0.01

def value(row,name):
    x=float(row[name])
    if not math.isfinite(x): raise ValueError(f'Nonfinite {name}: {row["cell_id"]}')
    return x

def near(a,b,label):
    if abs(a-b)>TOL:
        raise ValueError(f'{label}: {a} versus {b} (difference {a-b} ha)')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pilot',type=Path,required=True)
    p.add_argument('--baseline',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args()
    with a.baseline.open(newline='',encoding='utf-8-sig') as f:
        baseline={}
        for r in csv.DictReader(f):
            if r['cell_id'] in baseline: raise ValueError('Duplicate baseline cell')
            baseline[r['cell_id']]=r
    if len(baseline)!=24889: raise ValueError('Baseline must contain 24,889 cells')
    totals={'flow_pas_tmp_ha':0.,'flow_nat_pas_ha':0.,
            'old':{x:0. for x in OLD},'reconstructed':{x:0. for x in NEW},
            'transfers':{x:{y:0. for y in NEW} for x in OLD}}
    seen=set()
    with a.pilot.open(newline='',encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            cid=r['cell_id']
            if cid in seen or cid not in baseline:
                raise ValueError(f'Duplicate or unknown pilot cell: {cid}')
            seen.add(cid)
            old=baseline[cid]
            if int(float(r['source_batch_id'])) != 0 or \
               int(float(old['source_batch_id'])) != 0:
                raise ValueError('Pilot must be batch 0 only')
            if (int(float(r['t0'])),int(float(r['t1'])))!=(2015,2020):
                raise ValueError('Wrong interval')
            for field in ('flow_pas_tmp','flow_nat_pas','stock0_pas'):
                near(value(r,field),value(old,field),cid+' '+field)
            area=value(r,'flow_pas_tmp')
            oldparts={x:value(r,'old_'+x) for x in OLD}
            newparts={x:value(r,'new_'+x) for x in NEW}
            near(sum(oldparts.values()),area,cid+' old partition')
            near(sum(newparts.values()),area,cid+' reconstructed partition')
            for x in OLD:
                near(oldparts[x],value(old,SOURCE[x]),cid+' source '+x)
                transfers={y:value(r,'move_'+x+'_to_'+y) for y in NEW}
                near(sum(transfers.values()),oldparts[x],cid+' row '+x)
                totals['old'][x]+=oldparts[x]
                for y in NEW: totals['transfers'][x][y]+=transfers[y]
            for y in NEW:
                near(sum(value(r,'move_'+x+'_to_'+y) for x in OLD),
                     newparts[y],cid+' column '+y)
                totals['reconstructed'][y]+=newparts[y]
            if min([area,*oldparts.values(),*newparts.values(),
                    *(value(r,'move_'+x+'_to_'+y)
                      for x in OLD for y in NEW)]) < -1e-7:
                raise ValueError('Negative area in cell '+cid)
            totals['flow_pas_tmp_ha']+=area
            totals['flow_nat_pas_ha']+=value(r,'flow_nat_pas')
    expected={cid for cid,r in baseline.items()
              if int(float(r['source_batch_id']))==0}
    if len(expected)!=3168 or seen!=expected:
        raise ValueError(f'Batch population mismatch: expected {len(expected)}, observed {len(seen)}')
    den=totals['flow_pas_tmp_ha']
    if den<=0: raise ValueError('PAS→TMP denominator is zero')
    totals['old_pct']={k:100*v/den for k,v in totals['old'].items()}
    totals['reconstructed_pct']={k:100*v/den
                                 for k,v in totals['reconstructed'].items()}
    totals['initial_minus_old_censored_pp']=(
        totals['reconstructed_pct']['initial']-totals['old_pct']['censored'])
    result={'status':'PASS','scope':'batch_0_only_not_domain_estimate',
            'interval':'2015–2020','cells':len(seen),
            'max_allowed_per_cell_difference_ha':TOL,'totals':totals}
    a.output_dir.mkdir(parents=True,exist_ok=True)
    path=a.output_dir/'pas_tmp_origin_impact_batch00_v3.json'
    path.write_text(json.dumps(result,indent=2,ensure_ascii=False,
                               allow_nan=False)+'\n',encoding='utf-8')
    print('RQ2 BATCH 00 VALIDATION PASS | cells:',len(seen))
    print('Old shares (%):',totals['old_pct'])
    print('Reconstructed shares (%):',totals['reconstructed_pct'])
    print('This is a batch diagnostic; do not report as national RQ2 shares.')
    print('Validation:',path)

if __name__=='__main__': main()
