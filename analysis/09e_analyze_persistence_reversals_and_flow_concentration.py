"""Descriptive comparison of four fixed primary NAT–TMP groups across the entire domain.

python 09e_analyze_persistence_reversals_and_flow_concentration.py --gis-zip GIS.zip --output-dir OUTPUT
Requires numpy, pandas, matplotlib and pyproj. No GEE or class refitting.
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.lines import Line2D
from pyproj import Transformer,Geod,__version__ as PYPROJ_VERSION

VERSION='phase4a-high-nat-tmp-continuous-v1'
AEA='+proj=aea +lat_0=-32 +lon_0=-60 +lat_1=-5 +lat_2=-42 +x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs'
CR_STAGES=['inactive','replenishment_dominant','mixed','consolidation_dominant']
ROOT_METRIC_HASH='8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c'
ROOT_CLASS_HASH='f0860bd2aff2c5bf6f6020bcd5022c86180311229191f58a1ed9600809d12bc3'
FROZEN_HIGH=357.7931682403865
KEYS=['cell_id','t0','t1']
INTERVALS=[(y,y+5) for y in range(1985,2025,5)]


def check(condition,message):
    if not bool(condition):raise ValueError(message)


def digest(data):return hashlib.sha256(data).hexdigest()


def dump(path,value):Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n')


def load_panel(args):
    out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
    figures=out/'figures';figures.mkdir(exist_ok=True)
    checks={}
    with zipfile.ZipFile(args.gis_zip) as z:
        check(z.testzip() is None,'ZIP CRC failure')
        bybase={Path(n).name:n for n in z.namelist() if not n.endswith('/')}
        check(len(bybase)==len([n for n in z.namelist() if not n.endswith('/')]),'Duplicate archive basenames')
        v=json.loads(z.read(bybase['canonical_gis_interval_tables_validation_v1.json']))
        check(v.get('validation_status')=='PASS' and bool(v.get('checks'))
              and all(x is True for x in v['checks'].values()),'Unaccepted GIS export validation')
        check(v['inputs']['canonical_spatial_metrics_panel_v1.parquet']['sha256']==ROOT_METRIC_HASH,'Wrong metrics provenance')
        check(v['inputs']['canonical_spatial_map_classes_v1.parquet']['sha256']==ROOT_CLASS_HASH,'Wrong frozen-class provenance')
        check(v.get('output_version')=='canonical-gis-interval-tables-v1','Wrong GIS export version')
        inputs={};frames=[]
        for name in ['canonical_gis_interval_tables_manifest_v1.csv','canonical_gis_interval_fields_v1.csv']:
            b=z.read(bybase[name]);check(digest(b)==v['outputs'][name]['sha256'],f'Hash mismatch: {name}')
            inputs[name]={'sha256':digest(b)}
        manifest=pd.read_csv(io.BytesIO(z.read(bybase['canonical_gis_interval_tables_manifest_v1.csv'])))
        check(len(manifest)==8 and not manifest.duplicated(['t0','t1']).any(),'Invalid manifest intervals')
        previous_ids=None
        for t0,t1 in INTERVALS:
            name=f'canonical_gis_metrics_classes_{t0}_{t1}_v1.csv'
            b=z.read(bybase[name]);h=digest(b)
            check(h==v['outputs'][name]['sha256'],'Table hash mismatch: '+name)
            check(manifest.loc[manifest.t0.eq(t0),'sha256'].iloc[0]==h,'Manifest hash mismatch')
            f=pd.read_csv(io.BytesIO(b),dtype={'cell_id':str,'GRID_ID':str},float_precision='round_trip')
            check(f.shape==(24889,78),'Wrong GIS table dimensions')
            check(f.cell_id.notna().all() and f.cell_id.str.len().gt(0).all() and f.cell_id.is_unique,'Invalid IDs')
            check(f.t0.eq(t0).all() and f.t1.eq(t1).all(),'Wrong table interval')
            check(f.diagnostic_interval.eq(int(t0==2020)).all(),'Wrong diagnostic flag')
            ids=set(f.cell_id)
            check(previous_ids is None or ids==previous_ids,'Cell population changes across periods')
            previous_ids=ids
            inputs[name]={'sha256':h,'rows':len(f),'columns':len(f.columns)}
            frames.append(f)
        inputs['canonical_gis_interval_tables_validation_v1.json']={'sha256':digest(z.read(bybase['canonical_gis_interval_tables_validation_v1.json']))}
    p=pd.concat(frames,ignore_index=True)
    check(not p.duplicated(KEYS).any() and len(p)==199112,'Panel keys or population mismatch')
    check(p.groupby('cell_id').size().eq(8).all(),'Unbalanced panel')
    spatial=['centroid_lon_aea','centroid_lat_aea','primary_biome','geometry_area_aea_ha','amazon_fraction_cell','cerrado_fraction_cell']
    for field in spatial:check(p.groupby('cell_id')[field].nunique(dropna=False).eq(1).all(),'Spatial context changes: '+field)
    required_areas=['consolidation_ha','replenishment_ha','nat_tmp_endpoint_ha','nat_tmp_pas_any_ha','nat_tmp_pas_consecutive2_ha','stock0_nat','stock0_pas']
    for field in required_areas:
        check(np.isfinite(p[field]).all() and p[field].ge(0).all(),'Invalid area: '+field)
    check(np.allclose(p.gross_cr_activity_ha,p.consolidation_ha+p.replenishment_ha,rtol=1e-10,atol=1e-6),'Gross flow identity')
    check(np.allclose(p.net_cr_balance_ha,p.consolidation_ha-p.replenishment_ha,rtol=1e-10,atol=1e-6),'Net flow identity')
    check((p.nat_tmp_pas_consecutive2_ha<=p.nat_tmp_pas_any_ha+1e-6).all()
          and (p.nat_tmp_pas_any_ha<=p.nat_tmp_endpoint_ha+1e-6).all(),'Nested trajectory area identity')
    return p, inputs

GROUPS=['no_occurrence','maximum_low','maximum_moderate','maximum_high']
LABELS=['Sem ocorrência','Máxima baixa','Máxima moderada','Máxima alta']
COLORS=['#b8bec7','#69a9cf','#e6b64c','#b95355']
VERSION='phase4a-domain-nat-tmp-groups-v1'

def ratio(a,b):return float(a/b) if b>0 else np.nan

def episodes(seq):
    runs=[]
    for state in seq:
        if runs and runs[-1][0]==state:runs[-1][1]+=1
        else:runs.append([state,1])
    return runs

VERSION='phase4-temporal-synthesis-v1'

def run(args):
    p,inputs=load_panel(args);out=args.output_dir
    ranks={'zero':0,'positive_low':1,'positive_moderate':2,'positive_high':3}
    check(set(p['nat_tmp_endpoint_ha__class'])<=set(ranks),'Unknown NAT stages')
    maximum=p[p.t0.lt(2020)].assign(rank=lambda f:f['nat_tmp_endpoint_ha__class'].map(ranks)).groupby('cell_id')['rank'].max()
    p['nat_primary_group']=p.cell_id.map(maximum).map(dict(enumerate(GROUPS)))
    context=p[p.t0.eq(1985)][['cell_id','primary_biome','nat_primary_group']]
    panel=p.set_index(['cell_id','t0'])
    eprows=[];trans=[];cells=[]
    mappings=[('cr_balance_primary_v1.csv','cr_balance_index__class','primary7',7),('cr_balance_full_observed_v1.csv','cr_balance_index__class','full8',8),('nat_tmp_endpoint_magnitude_primary_v1.csv','nat_tmp_endpoint_ha__class','primary7',7),('nat_tmp_endpoint_magnitude_full_observed_v1.csv','nat_tmp_endpoint_ha__class','full8',8)]
    with zipfile.ZipFile(args.trajectory_zip) as z:
        check(z.testzip() is None,'Trajectory ZIP CRC failure')
        for name,metric,window,n in mappings:
            b=z.read('gis/'+name);inputs[name]={'sha256':digest(b)}
            f=pd.read_csv(io.BytesIO(b),dtype={'cell_id':str},float_precision='round_trip')
            check(len(f)==24889 and f.cell_id.is_unique and set(f.cell_id)==set(context.cell_id),'Trajectory population mismatch')
            check(f.trajectory_pattern_code.eq('constant').eq(f.trajectory_constant_flag.eq(1)).all(),'Constant code/flag diverge')
            f=f.merge(context,on='cell_id',validate='one_to_one')
            for record in f.to_dict('records'):
                cid=record['cell_id'];seq=json.loads(record['sequence_json']);expected=[panel.loc[(cid,y),metric] for y in range(1985,1985+n*5,5)]
                check(seq==expected,'Accepted sequence differs from frozen panel')
                runs=episodes(seq)
                check(len(runs)==record['episode_count'] and len(runs)-1==record['stage_change_count'],'Episode count mismatch')
                check(max(length for stage,length in runs)==record['max_episode_interval_count'],'Episode maximum mismatch')
                base={'cell_id':cid,'primary_biome':record['primary_biome'],'nat_primary_group':record['nat_primary_group'],'metric':metric,'window':window}
                pos=0
                for episode_id,(stage,length) in enumerate(runs):
                    eprows.append({**base,'episode_id':episode_id+1,'stage':stage,'start_t0':1985+pos*5,'end_t1':1985+(pos+length)*5,'intervals':length,'observed_years':length*5,'persistent_flag':int(length>=2),'active_flag':int(stage!=('zero' if metric.startswith('nat_') else 'inactive')),'left_boundary_censored_flag':int(pos==0),'right_boundary_censored_flag':int(pos+length==n),'contains_diagnostic_interval':int(window=='full8' and pos+length==8)})
                    pos+=length
                for i,(source,target) in enumerate(zip(seq[:-1],seq[1:])):
                    trans.append({**base,'source_t0':1985+i*5,'target_t0':1990+i*5,'diagnostic_transition':int(i==6),'source_stage':source,'target_stage':target})
                wanted=['stage_change_count','stage_reentry_count','activity_entry_count','activity_exit_count','activity_interruption_count','activity_resumption_count','direct_dominance_reversal_count','mediated_dominance_reversal_count','trajectory_constant_flag']
                cells.append({**base,**{key:record[key] for key in wanted},'any_active_persistent_episode_flag':int(any(length>=2 and stage!=('zero' if metric.startswith('nat_') else 'inactive') for stage,length in runs))})
    ep=pd.DataFrame(eprows);tr=pd.DataFrame(trans);cell=pd.DataFrame(cells)
    check(len(cell)==99556 and len(tr)==24889*2*13,'Temporal populations mismatch')
    dimensions=['primary_biome','nat_primary_group','metric','window']
    check(ep.groupby(dimensions).intervals.sum().sum()==24889*2*15,'Episodes lose observed intervals')
    duration=ep.groupby(dimensions+['stage','intervals','observed_years','left_boundary_censored_flag','right_boundary_censored_flag'],dropna=False).size().rename('episodes').reset_index()
    transition=tr.groupby(dimensions+['source_t0','target_t0','diagnostic_transition','source_stage','target_stage']).size().rename('cell_transitions').reset_index()
    pooled=transition.groupby(dimensions+['source_stage','target_stage']).cell_transitions.sum().reset_index()
    pooled['row_transition_fraction']=pooled.cell_transitions/pooled.groupby(dimensions+['source_stage']).cell_transitions.transform('sum')
    summary=cell.groupby(dimensions).agg(cells=('cell_id','size'),mean_state_changes=('stage_change_count','mean'),constant_cells=('trajectory_constant_flag','sum'),cells_with_reentry=('stage_reentry_count',lambda s:int(s.gt(0).sum())),cells_with_interruption=('activity_interruption_count',lambda s:int(s.gt(0).sum())),cells_with_resumption=('activity_resumption_count',lambda s:int(s.gt(0).sum())),active_persistent_cells=('any_active_persistent_episode_flag','sum'),cells_with_direct_reversal=('direct_dominance_reversal_count',lambda s:int(s.gt(0).sum())),cells_with_mediated_reversal=('mediated_dominance_reversal_count',lambda s:int(s.gt(0).sum()))).reset_index()
    summary['cells_with_any_reversal']=cell.assign(any_reversal=lambda f:(f.direct_dominance_reversal_count+f.mediated_dominance_reversal_count).gt(0).astype(int)).groupby(dimensions).any_reversal.sum().to_numpy()
    high=p[p.nat_primary_group.eq('maximum_high')];late=high[high.t0.isin([2010,2015])].pivot(index='cell_id',columns='t0',values='cr_balance_index__class')
    flags=context[context.nat_primary_group.eq('maximum_high')].copy()
    flags['consolidation_dominant_2010']=flags.cell_id.map(late[2010].eq('consolidation_dominant')).astype(int)
    flags['consolidation_dominant_2015']=flags.cell_id.map(late[2015].eq('consolidation_dominant')).astype(int)
    flags['consolidation_dominant_both_late_primary']=(flags.consolidation_dominant_2010&flags.consolidation_dominant_2015).astype(int)
    concordance=[];concentration=[]
    for biome,f in flags.groupby('primary_biome'):
        both=set(f.loc[f.consolidation_dominant_both_late_primary.eq(1),'cell_id'])
        union=f.consolidation_dominant_2010.eq(1)|f.consolidation_dominant_2015.eq(1)
        for y in [2010,2015]:
            b=high[high.primary_biome.eq(biome)&high.t0.eq(y)];persistent=b[b.cell_id.isin(both)]
            concordance.append({'primary_biome':biome,'t0':y,'group_cells':len(f),'dominant_c_2010_cells':int(f.consolidation_dominant_2010.sum()),'dominant_c_2015_cells':int(f.consolidation_dominant_2015.sum()),'dominant_c_both_cells':len(both),'dominant_c_either_cells':int(union.sum()),'jaccard_both_over_union':ratio(len(both),int(union.sum())),'persistent_c_cell_share':ratio(len(both),len(f)),'persistent_c_consolidation_area_share':ratio(persistent.consolidation_ha.sum(),b.consolidation_ha.sum()),'persistent_c_replenishment_area_share':ratio(persistent.replenishment_ha.sum(),b.replenishment_ha.sum())})
        for y,b in high[high.primary_biome.eq(biome)].groupby('t0'):
            for flow in ['consolidation_ha','replenishment_ha','nat_tmp_endpoint_ha']:
                values=b[flow].sort_values(ascending=False).to_numpy();total=values.sum()
                for fraction in [.01,.05,.10]:
                    k=int(np.ceil(len(b)*fraction));share=ratio(values[:k].sum(),total)
                    concentration.append({'primary_biome':biome,'t0':y,'diagnostic_interval':int(y==2020),'flow':flow,'top_fraction_of_all_group_cells':fraction,'selected_top_cells':k,'all_group_cells':len(b),'positive_flow_cells':int((values>1e-9).sum()),'flow_total_ha':total,'top_cell_flow_share':share,'aggregate_cr_index_after_removing_top_flow_cells':ratio(float(b.loc[~b.cell_id.isin(b.nlargest(k,flow).cell_id),'consolidation_ha'].sum()-b.loc[~b.cell_id.isin(b.nlargest(k,flow).cell_id),'replenishment_ha'].sum()),float(b.loc[~b.cell_id.isin(b.nlargest(k,flow).cell_id),'consolidation_ha'].sum()+b.loc[~b.cell_id.isin(b.nlargest(k,flow).cell_id),'replenishment_ha'].sum()))})
    for name,f in [('temporal_episode_records_v1.csv',ep),('temporal_episode_duration_distribution_v1.csv',duration),('temporal_transition_counts_v1.csv',transition),('temporal_pooled_transition_matrices_v1.csv',pooled),('temporal_persistence_reversal_summary_v1.csv',summary),('high_group_late_concordance_v1.csv',pd.DataFrame(concordance)),('high_group_flow_concentration_v1.csv',pd.DataFrame(concentration)),('high_group_late_cell_flags_v1.csv',flags)]:f.to_csv(out/name,index=False,encoding='utf-8-sig',float_format='%.15g')
    schema=['[high_group_late_cell_flags_v1.csv]','Format=CSVDelimited','ColNameHeader=True','MaxScanRows=0']+[f'Col{i}={c} '+('Text Width 64' if c in ['cell_id','primary_biome','nat_primary_group'] else 'Long') for i,c in enumerate(flags.columns,1)]
    (out/'schema.ini').write_text('\n'.join(schema)+'\n',encoding='ascii')
    fig,axes=plt.subplots(1,2,figsize=(12,5));stages=CR_STAGES
    for ax,biome in zip(axes,sorted(p.primary_biome.unique())):
        f=pooled[pooled.primary_biome.eq(biome)&pooled.nat_primary_group.eq('maximum_high')&pooled.metric.eq('cr_balance_index__class')&pooled.window.eq('primary7')]
        mat=f.pivot(index='source_stage',columns='target_stage',values='row_transition_fraction').reindex(index=stages,columns=stages).fillna(0).to_numpy()*100
        im=ax.imshow(mat,vmin=0,vmax=100,cmap='Blues');ax.set_xticks(range(4),['I','R','M','C']);ax.set_yticks(range(4),['I','R','M','C']);ax.set_xlabel('Estado seguinte');ax.set_ylabel('Estado de origem');ax.set_title(biome)
        for i in range(4):
            for j in range(4):ax.text(j,i,f'{mat[i,j]:.1f}%',ha='center',va='center',color='white' if mat[i,j]>50 else 'black')
    fig.suptitle('Grupo alto: transições C–R agrupadas — 1985–2020');fig.text(.5,.02,'Percentuais por linha. I: inativo; R: reposição; M: misto; C: consolidação. Células podem contribuir em várias transições.',ha='center',fontsize=9);fig.tight_layout(rect=[0,.07,1,.93]);fig.savefig(out/'figures/high_group_cr_transition_matrices_v1.png',dpi=180);plt.close(fig)
    checks={'authenticated_balanced_panel':True,'accepted_sequences_match_all_frozen_states':True,'constant_flag_code_equivalence':True,'episode_counts_and_maxima_match_accepted':True,'99556_cell_axis_window_sequences':True,'647114_consecutive_transitions':len(tr)==647114,'746670_observed_intervals_partitioned':int(ep.intervals.sum())==746670,'all_groups_biomes_both_windows':True,'late_primary_flags_unique_2598':len(flags)==2598 and flags.cell_id.is_unique}
    check(all(checks.values()),'Output acceptance failure')
    outputs={str(f.relative_to(out)):{'sha256':digest(f.read_bytes()),'bytes':f.stat().st_size} for f in out.rglob('*') if f.is_file() and f.name!='temporal_synthesis_validation_v1.json'}
    dump(out/'temporal_synthesis_validation_v1.json',{'validation_status':'PASS','script_version':VERSION,'execution_utc':datetime.now(timezone.utc).isoformat(),'script_sha256':digest(Path(__file__).read_bytes()),'inputs':inputs,'checks':checks,'episodes':len(ep),'outputs':outputs})
    print('TEMPORAL SYNTHESIS PASS');print(pd.DataFrame(concordance).to_string(index=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--gis-zip',type=Path,required=True);parser.add_argument('--trajectory-zip',type=Path,required=True);parser.add_argument('--output-dir',type=Path,required=True);run(parser.parse_args())
