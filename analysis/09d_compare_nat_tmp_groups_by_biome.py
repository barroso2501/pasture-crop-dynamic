"""Descriptive comparison of four fixed primary NAT–TMP groups across the entire domain.

python 09d_compare_nat_tmp_groups_by_biome.py --gis-zip GIS.zip --output-dir OUTPUT
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

VERSION='phase4a-nat-tmp-biome-comparison-v1'

def run(args):
    p,inputs=load_panel(args);out=args.output_dir
    rank={'zero':0,'positive_low':1,'positive_moderate':2,'positive_high':3}
    check(set(p['nat_tmp_endpoint_ha__class'])<=set(rank),'Unknown NAT classes')
    p['rank']=p['nat_tmp_endpoint_ha__class'].map(rank)
    maximum=p[p.t0.lt(2020)].groupby('cell_id')['rank'].max()
    p['nat_primary_group']=p.cell_id.map(maximum).map(dict(enumerate(GROUPS)))
    # A positive intersection with both biomes defines cross-biome support.
    p['transbiome_flag']=(p.amazon_fraction_cell.gt(0)&p.cerrado_fraction_cell.gt(0)).astype(int)
    cells=p[p.t0.eq(1985)][['cell_id','primary_biome','nat_primary_group','transbiome_flag','amazon_fraction_cell','cerrado_fraction_cell']].copy()
    check(len(cells)==24889 and cells.cell_id.is_unique,'Cell assignment fails')
    rows=[];states=[];counts=[]
    for scope in ['all_cells','single_biome_cells']:
        panel=p if scope=='all_cells' else p[p.transbiome_flag.eq(0)]
        for biome,b in panel.groupby('primary_biome'):
            for group in GROUPS:
                counts.append({'scope':scope,'primary_biome':biome,'nat_primary_group':group,'cells':b[b.t0.eq(1985)&b.nat_primary_group.eq(group)].shape[0]})
            for (t0,t1),domain in b.groupby(['t0','t1']):
                total=domain.nat_tmp_endpoint_ha.sum()
                for group in GROUPS:
                    f=domain[domain.nat_primary_group.eq(group)];a=f.nat_tmp_endpoint_ha.sum();c=f.consolidation_ha.sum();r=f.replenishment_ha.sum();valid=f.stock0_nat.gt(1e-9)
                    rows.append({'scope':scope,'primary_biome':biome,'nat_primary_group':group,'t0':t0,'t1':t1,'diagnostic_interval':int(t0==2020),'cells':len(f),'nat_endpoint_ha':a,'biome_label_total_nat_ha':total,'share_biome_label_nat':ratio(a,total),'nat_ha_per_cell':ratio(a,len(f)),'supported_initial_native_intensity':ratio(f.loc[valid,'nat_tmp_endpoint_ha'].sum(),f.loc[valid,'stock0_nat'].sum()),'native_denominator_valid_cells':int(valid.sum()),'consolidation_ha':c,'replenishment_ha':r,'aggregate_cr_index':ratio(c-r,c+r),'any_pasture_share':ratio(f.nat_tmp_pas_any_ha.sum(),a),'consecutive2_pasture_share':ratio(f.nat_tmp_pas_consecutive2_ha.sum(),a)})
                    for state in CR_STAGES:
                        sub=f[f['cr_balance_index__class'].eq(state)]
                        states.append({'scope':scope,'primary_biome':biome,'nat_primary_group':group,'t0':t0,'t1':t1,'diagnostic_interval':int(t0==2020),'cr_state':state,'cells':len(sub),'nat_endpoint_ha':sub.nat_tmp_endpoint_ha.sum()})
    summary=pd.DataFrame(rows);state=pd.DataFrame(states);counts=pd.DataFrame(counts)
    base=summary[summary.scope.eq('all_cells')]
    check(base.groupby('t0').cells.sum().eq(24889).all(),'Biome/group population fails')
    check(np.allclose(base.groupby('t0').nat_endpoint_ha.sum(),p.groupby('t0').nat_tmp_endpoint_ha.sum(),rtol=1e-10,atol=1e-6),'Biome area partition fails')
    idx=['scope','primary_biome','nat_primary_group','t0']
    check(np.allclose(state.groupby(idx).nat_endpoint_ha.sum(),summary.set_index(idx).nat_endpoint_ha.sort_index(),rtol=1e-10,atol=1e-6),'CR state partition fails')
    check(np.array_equal(state.groupby(idx).cells.sum(),summary.set_index(idx).cells.sort_index()),'CR cell partition fails')
    check(cells.groupby('nat_primary_group').size().to_dict()=={'no_occurrence':11213,'maximum_low':4887,'maximum_moderate':6191,'maximum_high':2598},'Primary groups changed')
    pivot=summary.pivot(index=['primary_biome','nat_primary_group','t0','t1','diagnostic_interval'],columns='scope',values=['nat_endpoint_ha','share_biome_label_nat','aggregate_cr_index']).reset_index()
    pivot.columns=['_'.join(str(x) for x in col if x!='') for col in pivot.columns]
    pivot['transbiome_associated_nat_ha']=pivot.nat_endpoint_ha_all_cells-pivot.nat_endpoint_ha_single_biome_cells
    pivot['transbiome_associated_nat_fraction']=pivot.transbiome_associated_nat_ha.div(pivot.nat_endpoint_ha_all_cells.replace(0,np.nan))
    pivot['single_minus_all_group_share_percentage_points']=100*(pivot.share_biome_label_nat_single_biome_cells-pivot.share_biome_label_nat_all_cells)
    sequences=[]
    for cell,f in p.sort_values(['cell_id','t0']).groupby('cell_id',sort=False):
        for window,n in [('primary7',7),('full8',8)]:
            for metric in ['nat_tmp_endpoint_ha__class','cr_balance_index__class']:
                seq=f[metric].tolist()[:n];runs=episodes(seq)
                sequences.append({'primary_biome':f.primary_biome.iloc[0],'nat_primary_group':f.nat_primary_group.iloc[0],'transbiome_flag':int(f.transbiome_flag.iloc[0]),'window':window,'metric':metric,'changes':len(runs)-1,'constant':int(len(runs)==1),'max_episode_intervals':max(length for state,length in runs)})
    seq=pd.DataFrame(sequences);ts=[]
    for scope in ['all_cells','single_biome_cells']:
        f=seq if scope=='all_cells' else seq[seq.transbiome_flag.eq(0)]
        t=f.groupby(['primary_biome','nat_primary_group','window','metric']).agg(cells=('changes','size'),mean_changes=('changes','mean'),constant_cells=('constant','sum'),mean_max_episode_intervals=('max_episode_intervals','mean')).reset_index();t['scope']=scope;ts.append(t)
    for name,f in [('nat_biome_group_cells_v1.csv',cells),('nat_biome_group_counts_v1.csv',counts),('nat_biome_group_period_summary_v1.csv',summary),('nat_biome_group_cr_states_v1.csv',state),('nat_biome_transbiome_sensitivity_v1.csv',pivot),('nat_biome_group_trajectory_summary_v1.csv',pd.concat(ts))]:f.to_csv(out/name,index=False,encoding='utf-8-sig',float_format='%.15g')
    biomes=sorted(p.primary_biome.unique());fig,axes=plt.subplots(3,2,figsize=(14,12));x=np.arange(8);labels=[f'{y}–{y+5}'+('*' if y==2020 else '') for y in range(1985,2025,5)]
    for col,biome in enumerate(biomes):
        b=base[base.primary_biome.eq(biome)];bottom=np.zeros(8)
        for group,label,color in zip(GROUPS,LABELS,COLORS):
            f=b[b.nat_primary_group.eq(group)].sort_values('t0');a=f.nat_endpoint_ha.to_numpy()/1e6
            axes[0,col].bar(x,a,bottom=bottom,label=label,color=color);bottom+=a
            axes[1,col].plot(x,f.share_biome_label_nat*100,marker='o',color=color)
            axes[2,col].plot(x,f.aggregate_cr_index,marker='o',color=color)
        for row,ylabel in enumerate(['NAT→TMP (milhões ha)','Participação na área (%)','Índice agregado C–R']):
            ax=axes[row,col];ax.set_title(str(biome));ax.set_ylabel(ylabel);ax.set_xticks(x,labels,rotation=35,ha='right');ax.grid(axis='y',alpha=.2);ax.axvspan(6.5,7.5,color='gray',alpha=.1)
        axes[2,col].set_ylim(-1,1);axes[2,col].axhline(1/3,color='gray',ls='--');axes[2,col].axhline(-1/3,color='gray',ls='--')
    ceiling=max(ax.get_ylim()[1] for ax in axes[0]);[ax.set_ylim(0,ceiling) for ax in axes[0]]
    [ax.set_ylim(0,100) for ax in axes[1]]
    fig.legend(*axes[0,0].get_legend_handles_labels(),loc='upper center',ncol=4,bbox_to_anchor=(.5,.995))
    fig.text(.5,.01,'Áreas associadas ao bioma principal da célula. Grupos primários fixos. *2020–2025 diagnóstico.',ha='center')
    fig.tight_layout(rect=[0,.035,1,.96]);fig.savefig(out/'figures/nat_biome_group_comparison_v1.png',dpi=170);plt.close(fig)
    checks={'authenticated_balanced_inputs':True,'fixed_groups_preserved':True,'biome_group_cell_and_area_partition':True,'cr_state_cell_and_area_partition':True,'diagnostic_interval_included':True,'transbiome_removed_without_reassigning_groups':True,'two_core_axes_two_windows':len(seq)==99556}
    outputs={str(f.relative_to(out)):{'sha256':digest(f.read_bytes())} for f in out.rglob('*') if f.is_file() and f.name!='nat_biome_group_validation_v1.json'}
    dump(out/'nat_biome_group_validation_v1.json',{'validation_status':'PASS','script_version':VERSION,'execution_utc':datetime.now(timezone.utc).isoformat(),'script_sha256':digest(Path(__file__).read_bytes()),'inputs':inputs,'checks':checks,'transbiome_cells':int(cells.transbiome_flag.sum()),'transbiome_high_cells':int(cells.loc[cells.nat_primary_group.eq('maximum_high'),'transbiome_flag'].sum()),'outputs':outputs})
    print('BIOME COMPARISON PASS');print(counts.to_string(index=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--gis-zip',type=Path,required=True);parser.add_argument('--output-dir',type=Path,required=True);run(parser.parse_args())
