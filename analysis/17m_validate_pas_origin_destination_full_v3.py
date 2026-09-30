"""Decision 024 criterion 7: validate one full interval and export cell CSV.

Does not close Decision 024 criteria 9-12 or revalidate the RQ1 fixed cohort.
Requires an accepted RQ2 interval validation JSON authenticating eight batches.
--closure-export-style pilot accepts batch files created by 17j in any
interval, with their original _pilot_v1 names and provenance preserved.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

INTERVALS = ((1985,1990),(1990,1995),(1995,2000),(2000,2005),
             (2005,2010),(2010,2015),(2015,2020),(2020,2025))
ORIGINS = ('initial','new','unresolved')
DESTS = ('pas','tmp','nat','oag','out','water','nodata','unexpected','masked')
OBSERVED = ('tmp','nat','oag','out','water')
LOSS = ('nodata','unexpected','masked')
AREA_FIELDS = (('stock0_pas',) + tuple('origin_'+o for o in ORIGINS) +
               tuple(field for d in DESTS for field in
                     (('flow_pas_'+d,) + tuple('pas_'+o+'_to_'+d
                                                  for o in ORIGINS))))
OUTPUT_FIELDS = ['cell_id','GRID_ID','source_batch_id','t0','t1',
                 'diagnostic_interval'] + list(AREA_FIELDS) + [
                 'pas_observed_outflow_ha','pas_observation_loss_ha',
                 'accounting_version']
TOL = 0.01


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def value(row,key,cid):
    try:
        v=float(row[key])
    except (KeyError,ValueError,TypeError) as e:
        raise ValueError(f'{cid}: invalid or missing {key}') from e
    require(math.isfinite(v) and v >= -1e-7,
            f'{cid}: nonfinite or negative {key}: {v}')
    return v


def integer(row,key,cid):
    v=value(row,key,cid)
    require(v.is_integer(),f'{cid}: noninteger {key}')
    return int(v)


def equal(a,b,label):
    require(abs(a-b)<=TOL, f'{label}: {a:.9f} vs {b:.9f} ha')


def rows(path):
    require(path.is_file(),f'Missing file: {path}')
    with path.open(newline='',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        require(reader.fieldnames and 'cell_id' in reader.fieldnames,
                f'Missing cell_id column in {path}')
        for row in reader:
            yield row


def check_keys(row,cid,t0,t1,batch,diagnostic):
    require((integer(row,'t0',cid),integer(row,'t1',cid),
             integer(row,'source_batch_id',cid))==(t0,t1,batch),
            f'{cid}: interval/batch mismatch')
    if 'diagnostic_interval' in row:
        require(integer(row,'diagnostic_interval',cid)==diagnostic,
                f'{cid}: diagnostic flag mismatch')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--t0',required=True,type=int)
    p.add_argument('--baseline',required=True,type=Path)
    p.add_argument('--closure-dir',required=True,type=Path)
    p.add_argument('--closure-export-style',choices=('full','pilot'),
                   default='full',help='Use pilot when all non-reused batches '
                   'were exported by 17j with _pilot_v1 names')
    p.add_argument('--rq2-dir',required=True,type=Path)
    p.add_argument('--rq2-validation',required=True,type=Path)
    p.add_argument('--pilot-b00',type=Path,
                   help='Required for 2015–2020: already accepted pilot CSV')
    p.add_argument('--pilot-validation',type=Path,
                   help='Required for 2015–2020: pilot PASS JSON')
    p.add_argument('--output-dir',required=True,type=Path)
    a=p.parse_args()
    pair=next(((x,y) for x,y in INTERVALS if x==a.t0),None)
    require(pair is not None,f'Invalid t0: {a.t0}')
    t0,t1=pair
    interval=f'{t0}_{t1}'
    diagnostic=int(t0==2020)
    pilot=(t0==2015)
    require(bool(a.pilot_b00)==pilot and bool(a.pilot_validation)==pilot,
            '2015–2020 requires both pilot files; other intervals use neither')
    base={}
    expected={i:set() for i in range(8)}
    for row in rows(a.baseline):
        cid=row['cell_id'].strip()
        require(cid and cid not in base,f'Duplicate/empty baseline ID {cid}')
        batch=integer(row,'source_batch_id',cid)
        require(batch in range(8),f'{cid}: invalid baseline batch')
        check_keys(row,cid,t0,t1,batch,diagnostic)
        base[cid]=row
        expected[batch].add(cid)
    require(len(base)==24889,f'Expected 24,889 baseline cells: {len(base)}')
    accepted=json.loads(a.rq2_validation.read_text(encoding='utf-8'))
    require(accepted['status']=='PASS' and
            accepted['full_domain']['cells']==24889 and
            len(accepted['inventory'])==8,
            'RQ2 interval validation is not a full-domain PASS')
    if pilot:
        require(accepted['scope']=='canonical_full_domain_2015_2020_only',
                'Wrong accepted RQ2 scope for 2015–2020')
        pilot_record=json.loads(a.pilot_validation.read_text(encoding='utf-8'))
        require(pilot_record['status']=='PASS' and
                pilot_record['scope']=='2015_2020_batch_00_pilot_only' and
                pilot_record['cells']==len(expected[0]),
                'Invalid pilot validation')
        require(pilot_record['inputs']['baseline']['sha256']==sha(a.baseline),
                'Pilot baseline hash differs')
        require(pilot_record['inputs']['export']['sha256']==sha(a.pilot_b00),
                'Pilot export hash differs')
    else:
        require((accepted['scope'],accepted['interval'],accepted['t0'],
                 accepted['t1'],accepted['diagnostic_interval'])==
                ('canonical_full_domain_one_interval',interval,t0,t1,
                 diagnostic),'Wrong RQ2 interval/scope')
    require(accepted['baseline_sha256']==sha(a.baseline),
            'Accepted RQ2 baseline hash differs')
    rq2_inventory={r['batch']:r for r in accepted['inventory']}
    require(set(rq2_inventory)==set(range(8)),
            'Accepted RQ2 inventory lacks a batch')
    a.output_dir.mkdir(parents=True,exist_ok=True)
    out=a.output_dir/f'canonical_pas_origin_destination_{interval}_full_v3.csv'
    validation=a.output_dir/f'canonical_pas_origin_destination_{interval}_validation_v3.json'
    inventory=[]
    seen=set()
    totals={k:[] for k in ('stock0_pas','pas_persistence_ha',
                           'pas_observed_outflow_ha','pas_observation_loss_ha',
                           'flow_pas_tmp_ha')}
    # A temporary file prevents a partial CSV from appearing as a complete one.
    temp=out.with_suffix('.csv.partial')
    try:
        with temp.open('w',newline='',encoding='utf-8') as dest:
            writer=csv.DictWriter(dest,fieldnames=OUTPUT_FIELDS)
            writer.writeheader()
            for batch in range(8):
                suffix='v3' if pilot else 'v4'
                rq2path=a.rq2_dir/f'canonical_pas_tmp_origin_{interval}_b{batch:02d}_{suffix}.csv'
                require(rq2path.name==rq2_inventory[batch]['file'],
                        f'RQ2 inventory filename differs for batch {batch}')
                require(sha(rq2path)==rq2_inventory[batch]['sha256'],
                        f'RQ2 batch {batch} differs from accepted hash')
                rq2={}
                for r in rows(rq2path):
                    cid=r['cell_id'].strip()
                    require(cid and cid not in rq2,f'Duplicate RQ2 ID {cid}')
                    check_keys(r,cid,t0,t1,batch,diagnostic)
                    rq2[cid]=r
                suffix=('_pilot_v1' if a.closure_export_style=='pilot'
                        else '_v1')
                closure=(a.pilot_b00 if pilot and batch==0 else
                         a.closure_dir/f'canonical_pas_origin_destination_{interval}_b{batch:02d}{suffix}.csv')
                if pilot and batch==0:
                    require(pilot_record['inputs']['rq2_batch']['sha256']==sha(rq2path),
                            'Pilot RQ2 batch hash differs')
                observed=set()
                for row in rows(closure):
                    cid=row['cell_id'].strip()
                    require(cid and cid not in observed and cid not in seen and
                            cid in expected[batch] and cid in rq2,
                            f'Unknown, wrong-batch or duplicate cell {cid}')
                    check_keys(row,cid,t0,t1,batch,diagnostic)
                    expected_version=('pas-origin-destination-closure-pilot-v1'
                                      if (pilot and batch==0) or
                                      a.closure_export_style=='pilot' else
                                      'pas-origin-destination-closure-v1')
                    require(row.get('output_version')==expected_version,
                            f'{cid}: closure source version differs')
                    b=base[cid]
                    require(row['GRID_ID']==b['GRID_ID'],f'{cid}: GRID_ID differs')
                    stock=value(row,'stock0_pas',cid)
                    equal(stock,value(b,'stock0_pas',cid),f'{cid} stock')
                    equal(stock,math.fsum(value(row,'origin_'+o,cid)
                                          for o in ORIGINS),f'{cid} origin stock')
                    flows={}
                    for d in DESTS:
                        flows[d]=value(row,'flow_pas_'+d,cid)
                        equal(flows[d],value(b,'flow_pas_'+d,cid),
                              f'{cid} canonical PAS->{d}')
                        equal(flows[d],math.fsum(value(row,'pas_'+o+'_to_'+d,cid)
                                                   for o in ORIGINS),
                              f'{cid} origins for PAS->{d}')
                    for o in ORIGINS:
                        equal(value(row,'origin_'+o,cid),
                              math.fsum(value(row,'pas_'+o+'_to_'+d,cid)
                                        for d in DESTS),f'{cid} destinations of {o}')
                        equal(value(row,'pas_'+o+'_to_tmp',cid),
                              value(rq2[cid],'new_'+o,cid),
                              f'{cid} accepted RQ2 {o}')
                    observed_out=math.fsum(flows[d] for d in OBSERVED)
                    observation_loss=math.fsum(flows[d] for d in LOSS)
                    equal(stock,flows['pas']+observed_out+observation_loss,
                          f'{cid} full PAS stock closure')
                    for key,v in [('stock0_pas',stock),
                                  ('pas_persistence_ha',flows['pas']),
                                  ('pas_observed_outflow_ha',observed_out),
                                  ('pas_observation_loss_ha',observation_loss),
                                  ('flow_pas_tmp_ha',flows['tmp'])]:
                        totals[key].append(v)
                    output={k:row[k] for k in AREA_FIELDS}
                    output.update(cell_id=cid,GRID_ID=row['GRID_ID'],
                                  source_batch_id=batch,t0=t0,t1=t1,
                                  diagnostic_interval=diagnostic,
                                  pas_observed_outflow_ha=observed_out,
                                  pas_observation_loss_ha=observation_loss,
                                  accounting_version='pas-origin-destination-full-v3')
                    writer.writerow(output)
                    observed.add(cid)
                    seen.add(cid)
                require(observed==expected[batch] and observed==set(rq2),
                        f'Batch {batch} cell populations differ')
                inventory.append({'batch':batch,'closure_file':closure.name,
                                  'closure_sha256':sha(closure),
                                  'rq2_file':rq2path.name,
                                  'rq2_sha256':sha(rq2path),
                                  'cells':len(observed)})
        require(seen==set(base) and len(seen)==24889,
                'Full-domain population differs from canonical baseline')
        sums={k:math.fsum(v) for k,v in totals.items()}
        require(abs(sums['stock0_pas']-
                    (sums['pas_persistence_ha']+
                     sums['pas_observed_outflow_ha']+
                     sums['pas_observation_loss_ha'])) <= TOL*len(seen),
                'Full-domain PAS stock identity differs')
        require(abs(sums['flow_pas_tmp_ha']-
                    accepted['full_domain']['flow_pas_tmp_ha']) <= TOL*len(seen),
                'Accepted RQ2 full-domain PAS->TMP differs')
        temp.replace(out)
        result={'status':'PASS','scope':'one_interval_full_domain',
                'interval':interval,'t0':t0,'t1':t1,
                'diagnostic_interval':diagnostic,'cells':len(seen),
                'batches':len(inventory),'tolerance_ha_per_cell':TOL,
                'totals_ha':sums,'baseline_sha256':sha(a.baseline),
                'rq2_validation_sha256':sha(a.rq2_validation),
                'inventory':inventory,'output_csv':out.name,
                'output_sha256':sha(out),
                'closure_export_style':a.closure_export_style,
                'source_pilot_batch_00_reused':pilot,
                'decision_024_fully_implemented':False}
        validation.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',
                              encoding='utf-8')
    finally:
        if temp.exists():
            temp.unlink()
    print(f'PAS ORIGIN × DESTINATION {t0}–{t1} FULL VALIDATION PASS')
    print('Cells:',len(seen),'| batches:',len(inventory))
    print('CSV:',out)
    print('Validation:',validation)


if __name__=='__main__':
    main()
