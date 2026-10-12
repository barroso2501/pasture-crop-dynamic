"""Descriptive endpoint conversion fractions, using class stock at interval start.

National ratios divide sums of areas, not means of cell-level ratios. No
annual exposure, hazard, causal effect or inferential model is estimated.
"""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
import pandas as pd

SOURCE='outputs/validation/window_origin_sensitivity_v1/full/canonical_window_origin_interval_summary_v1.csv'
DEST='outputs/summary/rq2_relative_conversion_v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def derive(d):
    keys=['baseline_year','t0','t1','interval','diagnostic_interval','baseline_interval_by_construction']
    q=d[keys].copy()
    for origin in ['initial','entry','unresolved']:
        q[origin+'_conversion_ha']=d[origin+'_ha']
        q[origin+'_stock_t0_ha']=d[origin+'_pas_stock_ha']
        s=q[origin+'_stock_t0_ha'];c=q[origin+'_conversion_ha']
        q[origin+'_endpoint_conversion_fraction_5y']=c.div(s.where(s.gt(0)))
        q[origin+'_endpoint_conversion_pct_5y']=100*q[origin+'_endpoint_conversion_fraction_5y']
        q[origin+'_stock_share_pct']=100*s/d.stock0_pas_ha
        q[origin+'_conversion_share_pct']=100*c/d.flow_pas_tmp_ha
    q['all_pas_stock_t0_ha']=d.stock0_pas_ha
    q['all_pas_tmp_conversion_ha']=d.flow_pas_tmp_ha
    q['initial_entry_stock_ratio']=q.initial_stock_t0_ha.div(q.entry_stock_t0_ha.where(q.entry_stock_t0_ha.gt(0)))
    q['initial_entry_conversion_ratio']=q.initial_conversion_ha.div(q.entry_conversion_ha.where(q.entry_conversion_ha.gt(0)))
    si=q.initial_stock_t0_ha;se=q.entry_stock_t0_ha;ce=q.entry_conversion_ha
    ok=si.gt(0)&se.gt(0)&ce.gt(0)
    ratio=q.initial_endpoint_conversion_fraction_5y.div(q.entry_endpoint_conversion_fraction_5y.where(ok))
    q['relative_fraction_ratio_initial_entry']=ratio.where(ok)
    q['relative_ratio_status']=np.select([si.le(0),se.le(0),ce.le(0)],
      ['undefined_zero_initial_stock','undefined_zero_entry_stock','not_finite_zero_entry_conversion'],default='estimable')
    q['ratio_identity_residual']=q.initial_entry_conversion_ratio-q.initial_entry_stock_ratio*q.relative_fraction_ratio_initial_entry
    q['initial_share_minus_stock_share_pp']=q.initial_conversion_share_pct-q.initial_stock_share_pct
    return q

def run(root):
    source=root/SOURCE
    pins=json.loads((root/'config/rq2_relative_conversion_v1_source_pins.json').read_text())
    if sha(source)!=pins['interval_summary_sha256']:raise ValueError('Accepted source bytes changed')
    d=pd.read_csv(source,float_precision='round_trip')
    needed=['initial_ha','entry_ha','unresolved_ha','initial_pas_stock_ha','entry_pas_stock_ha',
            'unresolved_pas_stock_ha','stock0_pas_ha','flow_pas_tmp_ha']
    if len(d)!=19 or not np.isfinite(d[needed].to_numpy(float)).all() or d[needed].lt(0).any().any():
        raise ValueError('Source population or numeric fields differ')
    if d.duplicated(['baseline_year','t0','t1']).any():raise ValueError('Duplicate interval key')
    q=derive(d)
    identity=float(q.ratio_identity_residual.abs().max())
    if identity>1e-12:raise ValueError('Ratio factorization failed')
    qsort=q.sort_values(['baseline_year','t0']).reset_index(drop=True)
    if qsort.relative_ratio_status.eq('estimable').sum()!=16:raise ValueError('Expected 16 estimable interval ratios')
    first=qsort.loc[qsort.baseline_interval_by_construction.eq(1)]
    if len(first)!=3 or not first.relative_ratio_status.eq('undefined_zero_entry_stock').all() or first.relative_fraction_ratio_initial_entry.notna().any():
        raise ValueError('First interval ratio must be missing, not one')
    summaries=[]
    for b,group in qsort.groupby('baseline_year'):
        primary=group.loc[group.diagnostic_interval.eq(0)&group.relative_ratio_status.eq('estimable')]
        diag=group.loc[group.diagnostic_interval.eq(1)].iloc[0]
        summaries.append({'baseline_year':int(b),'estimable_primary_intervals':len(primary),
                          'primary_ratio_min':float(primary.relative_fraction_ratio_initial_entry.min()),
                          'primary_ratio_max':float(primary.relative_fraction_ratio_initial_entry.max()),
                          'diagnostic_2020_2025_ratio':float(diag.relative_fraction_ratio_initial_entry),
                          'primary_ratio_monotonic_increasing':bool(primary.relative_fraction_ratio_initial_entry.is_monotonic_increasing),
                          'primary_ratio_monotonic_decreasing':bool(primary.relative_fraction_ratio_initial_entry.is_monotonic_decreasing)})
    output=root/DEST;output.mkdir(parents=True,exist_ok=True)
    files={'canonical_relative_endpoint_conversion_fractions_v1.csv':qsort,
           'canonical_relative_endpoint_conversion_summary_v1.csv':pd.DataFrame(summaries)}
    identities={}
    for name,frame in files.items():
        payload=frame.to_csv(index=False,float_format='%.17g',na_rep='').encode()
        p=output/name
        if p.exists() and p.read_bytes()!=payload:raise ValueError('Different versioned output: '+name)
        if not p.exists():p.write_bytes(payload)
        identities[name]={'sha256':hashlib.sha256(payload).hexdigest(),'rows':len(frame),'bytes':len(payload)}
    record={'status':'PASS','scope':'national_descriptive_ratios_from_accepted_area_sums',
            'source_relative_path':SOURCE,'source_sha256':sha(source),'interval_rows':19,
            'estimable_ratios':16,'undefined_first_interval_ratios':3,
            'denominator':'observed_origin_class_PAS_stock_at_t0_not_time_integrated_exposure',
            'aggregation':'ratio_of_national_sums_not_mean_of_cell_ratios',
            'maximum_factorization_residual':identity,'outputs':identities,
            'new_native_execution':False,'annualized_hazard_or_rate':False,'causal_or_inferential_model':False,
            'unresolved_origin_retained_separately':True,'ratio_excludes_unresolved_class':True}
    p=output/'canonical_relative_endpoint_conversion_validation_v1.json'
    payload=(json.dumps(record,indent=2)+'\n').encode()
    if p.exists() and p.read_bytes()!=payload:raise ValueError('Different versioned validation output')
    if not p.exists():p.write_bytes(payload)
    return qsort,pd.DataFrame(summaries),record

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    rows,summaries,record=run(parser.parse_args().root)
    print('RELATIVE ENDPOINT CONVERSION FRACTIONS — PASS')
    print(summaries.to_string(index=False))
