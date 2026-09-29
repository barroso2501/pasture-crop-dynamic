"""Assemble eight independently validated interval JSONs into both RQ2 windows."""
import argparse
import csv
import json
import math
from pathlib import Path

INTERVALS=((1985,1990),(1990,1995),(1995,2000),(2000,2005),
           (2005,2010),(2010,2015),(2015,2020),(2020,2025))
OLD=('censored','new','unresolved','unattributed')
NEW=('initial','new','unresolved')
OLD_MAP={'censored':'pas_tmp_censored_ha','new':'pas_tmp_new_ha',
         'unresolved':'pas_tmp_unresolved_age_ha',
         'unattributed':'pas_tmp_unattributed_age_ha'}


def within(a,b,tag):
    if abs(a-b)>0.01:
        raise ValueError(f'{tag}: {a} != {b}')


def aggregate(intervals):
    d={'intervals':len(intervals),'cells_per_interval':24889,
       'flow_pas_tmp_ha':math.fsum(x['flow_pas_tmp_ha'] for x in intervals),
       'flow_nat_pas_ha':math.fsum(x['flow_nat_pas_ha'] for x in intervals),
       'old_ha':{k:math.fsum(x['old_ha'][k] for x in intervals) for k in OLD},
       'reconstructed_ha':{k:math.fsum(x['reconstructed_ha'][k]
                                    for x in intervals) for k in NEW},
       'transfers_ha':{k:{j:math.fsum(x['transfers_ha'][k][j]
                                          for x in intervals) for j in NEW}
                       for k in OLD}}
    total=d['flow_pas_tmp_ha']
    if total<=0:raise ValueError('Zero denominator')
    d['old_pct']={k:100*v/total for k,v in d['old_ha'].items()}
    d['reconstructed_pct']={k:100*v/total for k,v in
                            d['reconstructed_ha'].items()}
    d['initial_minus_old_censored_pp']=(
        d['reconstructed_pct']['initial']-d['old_pct']['censored'])
    within(sum(d['old_ha'].values()),total,'Old series closure')
    within(sum(d['reconstructed_ha'].values()),total,'New series closure')
    for k in OLD:
        within(sum(d['transfers_ha'][k].values()),d['old_ha'][k],
               'Transfer row '+k)
    for k in NEW:
        within(sum(d['transfers_ha'][j][k] for j in OLD),
               d['reconstructed_ha'][k],'Transfer column '+k)
    return d


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--validation-dir',type=Path,required=True,
                   help='Directory containing eight interval validation JSONs')
    p.add_argument('--old-pooled-summary',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args()
    rows=[]
    for index,(t0,t1) in enumerate(INTERVALS):
        label=f'{t0}_{t1}'
        path=a.validation_dir/f'canonical_pas_tmp_origin_impact_{label}_validation_v1.json'
        r=json.loads(path.read_text(encoding='utf-8'))
        if r['status']!='PASS' or r['full_domain']['cells']!=24889 or \
           len(r['inventory'])!=8:
            raise ValueError('Invalid or incomplete interval: '+label)
        if index==6:
            if r.get('scope')!='canonical_full_domain_2015_2020_only':
                raise ValueError('2015–2020 must be the accepted validation')
        elif (r.get('interval'),r.get('t0'),r.get('t1'),
              r.get('diagnostic_interval'))!=(label,t0,t1,int(index==7)):
            raise ValueError('Mismatched interval validation: '+label)
        all_batches=sum(r['batches'][f'b{k:02d}']['cells'] for k in range(8))
        if all_batches!=24889:
            raise ValueError('Incomplete batch population: '+label)
        rows.append({'interval':label,'t0':t0,'t1':t1,
                     'diagnostic_interval':int(index==7),
                     'full':r['full_domain']})
    with a.old_pooled_summary.open(newline='',encoding='utf-8-sig') as f:
        accepted={r['window']:r for r in csv.DictReader(f)}
    windows={}
    for name,subset in (('primary_1985_2020',rows[:7]),
                        ('full_observed_1985_2025',rows)):
        d=aggregate([r['full'] for r in subset])
        reference=accepted[name]
        within(d['flow_pas_tmp_ha'],float(reference['consolidation_ha']),
               name+' canonical flow')
        for key in OLD:
            within(d['old_ha'][key],float(reference[OLD_MAP[key]]),
                   name+' canonical old '+key)
        d['includes_diagnostic_interval']=int(name=='full_observed_1985_2025')
        windows[name]=d
    a.output_dir.mkdir(parents=True,exist_ok=True)
    dest=a.output_dir/'canonical_pas_tmp_origin_series_reassessment_validation_v1.json'
    dest.write_text(json.dumps({'status':'PASS','intervals':rows,
                                'windows':windows},indent=2,
                               ensure_ascii=False,allow_nan=False)+'\n',
                    encoding='utf-8')
    out=a.output_dir/'canonical_pas_tmp_origin_series_reassessment_v1.csv'
    with out.open('w',newline='',encoding='utf-8') as f:
        columns=['window','intervals','includes_diagnostic_interval',
                 'flow_pas_tmp_ha','old_censored_pct','old_new_pct',
                 'new_initial_pct','new_new_pct','new_unresolved_pct',
                 'initial_minus_old_censored_pp','old_censored_to_new_ha']
        w=csv.DictWriter(f,fieldnames=columns);w.writeheader()
        for name,d in windows.items():
            w.writerow({'window':name,'intervals':d['intervals'],
                        'includes_diagnostic_interval':d['includes_diagnostic_interval'],
                        'flow_pas_tmp_ha':d['flow_pas_tmp_ha'],
                        'old_censored_pct':d['old_pct']['censored'],
                        'old_new_pct':d['old_pct']['new'],
                        'new_initial_pct':d['reconstructed_pct']['initial'],
                        'new_new_pct':d['reconstructed_pct']['new'],
                        'new_unresolved_pct':d['reconstructed_pct']['unresolved'],
                        'initial_minus_old_censored_pp':
                        d['initial_minus_old_censored_pp'],
                        'old_censored_to_new_ha':
                        d['transfers_ha']['censored']['new']})
    print('RQ2 EIGHT-INTERVAL SERIES VALIDATION PASS')
    print('Primary:',windows['primary_1985_2020']['reconstructed_pct'])
    print('Full observed:',windows['full_observed_1985_2025']['reconstructed_pct'])
    print('Validation:',dest)
    print('Summary:',out)


if __name__=='__main__':main()
