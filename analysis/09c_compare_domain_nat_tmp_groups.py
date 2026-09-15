"""Descriptive comparison of four fixed primary NAT–TMP groups across the entire domain.

python 09c_compare_domain_nat_tmp_groups.py --gis-zip GIS.zip --output-dir OUTPUT
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

def run(args):
    p,inputs=load_panel(args);out=args.output_dir
    rank={'zero':0,'positive_low':1,'positive_moderate':2,'positive_high':3}
    check(set(p['nat_tmp_endpoint_ha__class'])<=set(rank),'Unknown NAT magnitude states')
    p['nat_rank']=p['nat_tmp_endpoint_ha__class'].map(rank)
    maximum=p[p.t0.lt(2020)].groupby('cell_id').nat_rank.max()
    cells=p[p.t0.eq(1985)][['cell_id','primary_biome','centroid_lon_aea','centroid_lat_aea']].copy()
    cells['primary_maximum_rank']=cells.cell_id.map(maximum)
    cells['nat_primary_group']=cells.primary_maximum_rank.map(dict(enumerate(GROUPS)))
    diag=set(p.loc[p.t0.eq(2020)&p.nat_rank.eq(3),'cell_id'])
    cells['diagnostic_only_high_flag']=(cells.cell_id.isin(diag)&cells.primary_maximum_rank.lt(3)).astype(int)
    check(cells.cell_id.is_unique and len(cells)==24889,'Incomplete group assignment')
    check(cells.nat_primary_group.eq('maximum_high').sum()==2598,'High cohort mismatch')
    check(cells.diagnostic_only_high_flag.sum()==106,'Diagnostic-only high mismatch')
    p=p.merge(cells[['cell_id','nat_primary_group','diagnostic_only_high_flag']],on='cell_id',validate='many_to_one')
    forward=Transformer.from_crs('EPSG:4326',AEA,always_xy=True)
    reverse=Transformer.from_crs(AEA,'EPSG:4326',always_xy=True)
    p['x'],p['y']=forward.transform(p.centroid_lon_aea.to_numpy(),p.centroid_lat_aea.to_numpy())
    rows=[];state_rows=[];biomes=[]
    for t0,t1 in INTERVALS:
        domain=p[p.t0.eq(t0)];total=domain.nat_tmp_endpoint_ha.sum()
        for group in GROUPS:
            f=domain[domain.nat_primary_group.eq(group)];a=f.nat_tmp_endpoint_ha.sum()
            c=f.consolidation_ha.sum();r=f.replenishment_ha.sum();valid=f.stock0_nat.gt(1e-9)
            row={'t0':t0,'t1':t1,'diagnostic_interval':int(t0==2020),'nat_primary_group':group,'cells':len(f),
                 'active_nat_cells':int(f.nat_tmp_endpoint_ha.gt(1e-9).sum()),'current_high_cells':int(f.nat_rank.eq(3).sum()),
                 'nat_endpoint_ha':a,'domain_nat_share':ratio(a,total),'nat_ha_per_group_cell':ratio(a,len(f)),
                 'initial_native_stock_ha':f.stock0_nat.sum(),'native_denominator_valid_cells':int(valid.sum()),
                 'nat_intensity_supported_initial_native':ratio(f.loc[valid,'nat_tmp_endpoint_ha'].sum(),f.loc[valid,'stock0_nat'].sum()),
                 'nat_ha_excluded_invalid_native_denominator':f.loc[~valid,'nat_tmp_endpoint_ha'].sum(),
                 'consolidation_ha':c,'replenishment_ha':r,'aggregate_cr_index':ratio(c-r,c+r),
                 'any_pasture_share':ratio(f.nat_tmp_pas_any_ha.sum(),a),'consecutive2_pasture_share':ratio(f.nat_tmp_pas_consecutive2_ha.sum(),a)}
            if a>0:
                x=np.average(f.x,weights=f.nat_tmp_endpoint_ha);y=np.average(f.y,weights=f.nat_tmp_endpoint_ha)
                lon,lat=reverse.transform(x,y)
                row.update(weighted_centroid_lon=lon,weighted_centroid_lat=lat,weighted_rms_radius_km=np.sqrt(np.average((f.x-x)**2+(f.y-y)**2,weights=f.nat_tmp_endpoint_ha))/1000)
            else:row.update(weighted_centroid_lon=np.nan,weighted_centroid_lat=np.nan,weighted_rms_radius_km=np.nan)
            rows.append(row)
            for state in CR_STAGES:
                b=f[f['cr_balance_index__class'].eq(state)]
                state_rows.append({'t0':t0,'t1':t1,'diagnostic_interval':int(t0==2020),'nat_primary_group':group,'cr_state':state,'cells':len(b),'cell_share_group':ratio(len(b),len(f)),'nat_endpoint_ha':b.nat_tmp_endpoint_ha.sum(),'nat_area_share_group':ratio(b.nat_tmp_endpoint_ha.sum(),a)})
            for biome,b in f.groupby('primary_biome'):
                biomes.append({'t0':t0,'t1':t1,'diagnostic_interval':int(t0==2020),'nat_primary_group':group,'primary_biome':biome,'cells':len(b),'nat_endpoint_ha':b.nat_tmp_endpoint_ha.sum()})
    summary=pd.DataFrame(rows);states=pd.DataFrame(state_rows)
    check(summary.groupby('t0').cells.sum().eq(24889).all(),'Groups do not partition domain cells')
    check(np.allclose(summary.groupby('t0').nat_endpoint_ha.sum(),p.groupby('t0').nat_tmp_endpoint_ha.sum(),rtol=1e-10,atol=1e-6),'Groups do not partition domain areas')
    check(summary[summary.nat_primary_group.eq('no_occurrence')&summary.t0.lt(2020)].nat_endpoint_ha.eq(0).all(),'No-occurrence group has primary activity')
    check(np.allclose(states.groupby(['t0','nat_primary_group']).nat_endpoint_ha.sum(),summary.set_index(['t0','nat_primary_group']).nat_endpoint_ha.sort_index(),rtol=1e-10,atol=1e-6),'CR area partition fails')
    trajectory=[]
    for cell,f in p.sort_values(['cell_id','t0']).groupby('cell_id',sort=False):
        for window,n in [('primary7',7),('full8',8)]:
            for metric in ['nat_tmp_endpoint_ha__class','cr_balance_index__class']:
                seq=f[metric].tolist()[:n];runs=episodes(seq)
                trajectory.append({'cell_id':cell,'nat_primary_group':f.nat_primary_group.iloc[0],'window':window,'metric':metric,'sequence_json':json.dumps(seq),'state_change_count':len(runs)-1,'distinct_states':len(set(seq)),'maximum_episode_intervals':max(length for state,length in runs),'maximum_episode_observed_years':5*max(length for state,length in runs),'persistent_episode_count':sum(length>=2 for state,length in runs),'active_nat_intervals':sum(state!='zero' for state in seq) if metric.startswith('nat_') else np.nan,'high_nat_intervals':seq.count('positive_high') if metric.startswith('nat_') else np.nan})
    tr=pd.DataFrame(trajectory)
    ts=tr.groupby(['nat_primary_group','window','metric'],sort=False).agg(cells=('cell_id','size'),mean_state_changes=('state_change_count','mean'),constant_cells=('state_change_count',lambda s:int(s.eq(0).sum())),mean_maximum_episode_intervals=('maximum_episode_intervals','mean'),mean_active_nat_intervals=('active_nat_intervals','mean'),mean_high_nat_intervals=('high_nat_intervals','mean')).reset_index()
    check(len(tr)==24889*4,'Trajectory population mismatch')
    for name,frame in [('domain_nat_group_cells_v1.csv',cells),('domain_nat_group_period_summary_v1.csv',summary),('domain_nat_group_cr_states_v1.csv',states),('domain_nat_group_primary_biome_v1.csv',pd.DataFrame(biomes)),('domain_nat_group_trajectory_summary_v1.csv',ts),('domain_nat_group_cell_trajectories_v1.csv',tr)]:frame.to_csv(out/name,index=False,encoding='utf-8-sig',float_format='%.15g')
    schema=['[domain_nat_group_cells_v1.csv]','Format=CSVDelimited','ColNameHeader=True','MaxScanRows=0']
    for i,col in enumerate(cells.columns,1):
        typ='Text Width 64' if col in ['cell_id','primary_biome','nat_primary_group'] else ('Long' if col.endswith('rank') or col.endswith('flag') else 'Double')
        schema.append(f'Col{i}={col} {typ}')
    (out/'schema.ini').write_text('\n'.join(schema)+'\n',encoding='ascii')
    fig,axes=plt.subplots(2,2,figsize=(14,9));x=np.arange(8);labels=[f'{y}–{y+5}'+('*' if y==2020 else '') for y in range(1985,2025,5)]
    bottom=np.zeros(8)
    for group,label,color in zip(GROUPS,LABELS,COLORS):
        f=summary[summary.nat_primary_group.eq(group)].sort_values('t0');a=f.nat_endpoint_ha.to_numpy()/1e6
        axes[0,0].bar(x,a,bottom=bottom,label=label,color=color);bottom+=a
        axes[0,1].plot(x,f.domain_nat_share*100,marker='o',color=color,label=label)
        axes[1,0].plot(x,f.nat_intensity_supported_initial_native*100,marker='o',color=color,label=label)
        axes[1,1].plot(x,f.aggregate_cr_index,marker='o',color=color,label=label)
    for ax,title,ylabel in zip(axes.flat,['Área NAT→TMP por grupo','Participação na área NAT→TMP do domínio','Intensidade relativa ao estoque natural inicial','Balanço agregado consolidação–reposição'],['Milhões de hectares','%','%','(ΣC−ΣR)/(ΣC+ΣR)']):
        ax.set_title(title);ax.set_ylabel(ylabel);ax.set_xticks(x,labels,rotation=35,ha='right');ax.grid(axis='y',alpha=.2);ax.axvspan(6.5,7.5,color='#d9d9d9',alpha=.3)
    axes[1,1].axhline(1/3,color='gray',ls='--');axes[1,1].axhline(-1/3,color='gray',ls='--');axes[1,1].set_ylim(-1,1)
    fig.legend(*axes[0,0].get_legend_handles_labels(),loc='upper center',ncol=4,bbox_to_anchor=(.5,.995))
    fig.text(.5,.01,'Grupos fixos definidos em 1985–2020. *2020–2025: diagnóstico incluído. Razões calculadas entre somas.',ha='center')
    fig.tight_layout(rect=[0,.04,1,.95]);fig.savefig(out/'figures/domain_nat_group_comparison_v1.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,9))
    for group,label,color in zip(GROUPS,LABELS,COLORS):
        f=cells[cells.nat_primary_group.eq(group)];ax.scatter(f.centroid_lon_aea,f.centroid_lat_aea,s=3,color=color,label=f'{label}: {len(f):,}'.replace(',','.'))
    ax.set_xlabel('Longitude');ax.set_ylabel('Latitude');ax.set_title('Distribuição dos quatro grupos NAT→TMP — centroides das células');ax.legend(markerscale=4);ax.set_aspect(1);ax.grid(alpha=.2);fig.tight_layout();fig.savefig(out/'figures/domain_nat_group_spatial_v1.png',dpi=180);plt.close(fig)
    check(episodes(['R','R','I','R'])==[['R',2],['I',1],['R',1]],'Episode engine verification failure')
    check(episodes(['zero']*7)==[['zero',7]],'Constant sequence verification failure')
    checks={'episode_engine_examples_verified':True,'authenticated_inputs':True,'balanced_domain_199112':True,'exclusive_exhaustive_groups_24889':True,'high_cohort_2598':True,'diagnostic_only_high_106':True,'group_area_partition_exact_within_tolerance':True,'cr_state_area_partition':True,'primary_zero_group_verified':True,'trajectory_population_99556':True,'corrected_schema_without_charset':True}
    outputs={str(f.relative_to(out)):{'sha256':digest(f.read_bytes()),'bytes':f.stat().st_size} for f in sorted(out.rglob('*')) if f.is_file() and f.name!='domain_nat_group_validation_v1.json'}
    dump(out/'domain_nat_group_validation_v1.json',{'validation_status':'PASS','script_version':VERSION,'execution_utc':datetime.now(timezone.utc).isoformat(),'script_sha256':digest(Path(__file__).read_bytes()),'inputs':inputs,'checks':checks,'group_counts':cells.nat_primary_group.value_counts().to_dict(),'diagnostic_only_high_by_primary_group':cells[cells.diagnostic_only_high_flag.eq(1)].nat_primary_group.value_counts().to_dict(),'outputs':outputs})
    print('DOMAIN GROUP COMPARISON: PASS');print(cells.nat_primary_group.value_counts().to_string())

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Compare four fixed primary NAT–TMP magnitude groups across the full domain.')
    parser.add_argument('--gis-zip',type=Path,required=True);parser.add_argument('--output-dir',type=Path,required=True)
    run(parser.parse_args())
