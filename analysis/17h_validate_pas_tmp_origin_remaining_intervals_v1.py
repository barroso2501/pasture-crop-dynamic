"""Validate eight batch CSVs for ONE remaining interval against its accepted v1 CSV."""
import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

OLD = ('censored', 'new', 'unresolved', 'unattributed')
NEW = ('initial', 'new', 'unresolved')
BASE = dict(zip(OLD, ('pas_tmp_censored', 'pas_tmp_new',
                      'pas_tmp_unresolved_age', 'pas_tmp_unattributed_age')))
TOL = 0.01


def value(row, key):
    v = float(row[key])
    if not math.isfinite(v):
        raise ValueError(f'Nonfinite {key} at {row["cell_id"]}')
    return v


def integer(row, key):
    v = value(row, key)
    if not v.is_integer():
        raise ValueError(f'Noninteger {key} at {row["cell_id"]}')
    return int(v)


def equal(x, y, label):
    if abs(x-y) > TOL:
        raise ValueError(f'{label}: {x} versus {y} ha')


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def empty():
    return {'cells':0, 'changed_cells':0, 'flow_pas_tmp_ha':0.,
            'flow_nat_pas_ha':0., 'old_ha':{x:0. for x in OLD},
            'reconstructed_ha':{y:0. for y in NEW},
            'transfers_ha':{x:{y:0. for y in NEW} for x in OLD}}


def accumulate(target, source):
    for k in ('cells','changed_cells','flow_pas_tmp_ha','flow_nat_pas_ha'):
        target[k] += source[k]
    for x in OLD:
        target['old_ha'][x] += source['old_ha'][x]
        for y in NEW:
            target['transfers_ha'][x][y] += source['transfers_ha'][x][y]
    for y in NEW:
        target['reconstructed_ha'][y] += source['reconstructed_ha'][y]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pilot-dir',type=Path,required=True)
    p.add_argument('--baseline',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--t0',type=int,required=True)
    p.add_argument('--t1',type=int,required=True)
    a=p.parse_args()
    expected_intervals={(1985,1990),(1990,1995),(1995,2000),
                        (2000,2005),(2005,2010),(2010,2015),(2020,2025)}
    if (a.t0,a.t1) not in expected_intervals:
        raise ValueError('Choose one of seven intervals; 2015–2020 is accepted')
    interval=f'{a.t0}_{a.t1}'
    diagnostic=int(a.t0==2020)
    baseline={}
    expected=defaultdict(set)
    with a.baseline.open(newline='',encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            cid=row['cell_id']
            if not cid or cid in baseline:
                raise ValueError(f'Duplicate/empty baseline cell_id {cid}')
            if (integer(row,'t0'),integer(row,'t1'))!=(a.t0,a.t1):
                raise ValueError(f'Wrong accepted baseline interval at {cid}')
            batch=integer(row,'source_batch_id')
            if batch not in range(8):
                raise ValueError(f'Unexpected source batch {batch}')
            baseline[cid]=row
            expected[batch].add(cid)
    if len(baseline)!=24889:
        raise ValueError(f'Expected 24,889 canonical cells; got {len(baseline)}')
    required={'cell_id','source_batch_id','t0','t1','diagnostic_interval','flow_pas_tmp',
              'flow_nat_pas','stock0_pas'} | {
              'old_'+x for x in OLD} | {'new_'+y for y in NEW} | {
              'move_'+x+'_to_'+y for x in OLD for y in NEW}
    batches={}
    inventory=[]
    seen=set()
    full=empty()
    for batch in range(8):
        filename=f'canonical_pas_tmp_origin_{interval}_b{batch:02d}_v4.csv'
        path=a.pilot_dir/filename
        if not path.is_file():
            raise FileNotFoundError(f'Missing batch {batch}: {path}')
        current=empty()
        observed=set()
        with path.open(newline='',encoding='utf-8-sig') as f:
            reader=csv.DictReader(f)
            if not reader.fieldnames or not required.issubset(reader.fieldnames):
                raise ValueError(f'{filename}: missing {required-set(reader.fieldnames or [])}')
            for r in reader:
                cid=r['cell_id']
                if not cid or cid in seen or cid not in expected[batch]:
                    raise ValueError(f'Unknown, wrong-batch or duplicate cell {cid}')
                if integer(r,'source_batch_id')!=batch or \
                   (integer(r,'t0'),integer(r,'t1'))!=(a.t0,a.t1) or \
                   integer(r,'diagnostic_interval')!=diagnostic:
                    raise ValueError(f'Wrong batch/interval for {cid}')
                seen.add(cid)
                observed.add(cid)
                base=baseline[cid]
                for k in ('flow_pas_tmp','flow_nat_pas','stock0_pas'):
                    equal(value(r,k),value(base,k),f'{cid} {k}')
                area=value(r,'flow_pas_tmp')
                old={x:value(r,'old_'+x) for x in OLD}
                new={y:value(r,'new_'+y) for y in NEW}
                cross={x:{y:value(r,'move_'+x+'_to_'+y) for y in NEW}
                       for x in OLD}
                if min([area,value(r,'flow_nat_pas'),value(r,'stock0_pas'),
                        *old.values(),*new.values(),
                        *(cross[x][y] for x in OLD for y in NEW)]) < -1e-7:
                    raise ValueError(f'Negative component at {cid}')
                equal(sum(old.values()),area,f'{cid} old closure')
                equal(sum(new.values()),area,f'{cid} reconstructed closure')
                for x in OLD:
                    equal(old[x],value(base,BASE[x]),f'{cid} old source {x}')
                    equal(sum(cross[x].values()),old[x],f'{cid} cross row {x}')
                    current['old_ha'][x]+=old[x]
                    for y in NEW:
                        current['transfers_ha'][x][y]+=cross[x][y]
                for y in NEW:
                    equal(sum(cross[x][y] for x in OLD),new[y],
                          f'{cid} cross column {y}')
                    current['reconstructed_ha'][y]+=new[y]
                current['cells']+=1
                current['changed_cells']+=(cross['censored']['new']>0)
                current['flow_pas_tmp_ha']+=area
                current['flow_nat_pas_ha']+=value(r,'flow_nat_pas')
        if observed!=expected[batch]:
            raise ValueError(f'Batch {batch} has {len(observed)} cells; '
                             f'expected {len(expected[batch])}')
        batches[f'b{batch:02d}']=current
        accumulate(full,current)
        inventory.append({'batch':batch,'file':filename,'cells':len(observed),
                          'bytes':path.stat().st_size,'sha256':sha(path)})
    if seen!=set(baseline):
        raise ValueError('Full-domain cell population differs from baseline')
    for key,output in (('flow_pas_tmp','flow_pas_tmp_ha'),
                       ('flow_nat_pas','flow_nat_pas_ha')):
        equal(full[output],math.fsum(value(row,key) for row in baseline.values()),
              'Full domain '+key)
    for x in OLD:
        equal(full['old_ha'][x],
              math.fsum(value(row,BASE[x]) for row in baseline.values()),
              'Full domain old '+x)
    for s in [full,*batches.values()]:
        den=s['flow_pas_tmp_ha']
        if den<=0:
            raise ValueError('Zero PAS→TMP denominator')
        s['old_pct']={x:100*s['old_ha'][x]/den for x in OLD}
        s['reconstructed_pct']={y:100*s['reconstructed_ha'][y]/den
                                 for y in NEW}
        s['initial_minus_old_censored_pp']=(
            s['reconstructed_pct']['initial']-s['old_pct']['censored'])
    result={'status':'PASS','scope':'canonical_full_domain_one_interval',
            'interval':interval,'t0':a.t0,'t1':a.t1,
            'diagnostic_interval':diagnostic,
            'tolerance_ha_per_cell':TOL,'baseline_sha256':sha(a.baseline),
            'inventory':inventory,'full_domain':full,'batches':batches}
    a.output_dir.mkdir(parents=True,exist_ok=True)
    out=a.output_dir/f'canonical_pas_tmp_origin_impact_{interval}_validation_v1.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2,
                              allow_nan=False)+'\n',encoding='utf-8')
    summary=a.output_dir/f'canonical_pas_tmp_origin_impact_{interval}_summary_v1.csv'
    fields=['group','cells','flow_pas_tmp_ha','flow_nat_pas_ha'] + [
        'old_'+x+'_pct' for x in OLD]+['new_'+y+'_pct' for y in NEW]+[
        'initial_minus_old_censored_pp','old_censored_to_new_ha']
    with summary.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        for label,s in [('full_domain',full),*batches.items()]:
            line={'group':label,'cells':s['cells'],
                  'flow_pas_tmp_ha':s['flow_pas_tmp_ha'],
                  'flow_nat_pas_ha':s['flow_nat_pas_ha'],
                  'initial_minus_old_censored_pp':s['initial_minus_old_censored_pp'],
                  'old_censored_to_new_ha':s['transfers_ha']['censored']['new']}
            line.update({'old_'+x+'_pct':s['old_pct'][x] for x in OLD})
            line.update({'new_'+y+'_pct':s['reconstructed_pct'][y] for y in NEW})
            writer.writerow(line)
    print(f'RQ2 {a.t0}–{a.t1} FULL-DOMAIN ORIGIN — VALIDATION PASS')
    print('Cells:',full['cells'],'| batches:',len(batches))
    print('Old shares (%):',full['old_pct'])
    print('Reconstructed shares (%):',full['reconstructed_pct'])
    print('Initial share change (pp):',full['initial_minus_old_censored_pp'])
    print('Validation:',out)
    print('Summary:',summary)


if __name__=='__main__':
    main()
