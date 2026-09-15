"""Descriptive continuous-area comparison of the fixed primary high NAT–TMP cohort.

python 09b_compare_high_nat_tmp_continuous_areas.py --gis-zip GIS.zip --output-dir OUTPUT
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


def run(args):
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
    ids=sorted(p.loc[p.t0.lt(2020)&p['nat_tmp_endpoint_ha__class'].eq('positive_high'),'cell_id'].unique())
    check(len(ids)==2598,'Primary fixed cohort differs from accepted exploration')
    cohort=p[p.cell_id.isin(ids)].copy().sort_values(KEYS).reset_index(drop=True)
    check(len(cohort)==20784 and cohort.groupby('cell_id').size().eq(8).all(),'Cohort selection loses records')
    checks.update(archive_crc=True,received_output_hashes_match=True,upstream_provenance_matches=True,
                  unique_balanced_panel=True,constant_spatial_context=True,area_and_flow_identities=True,
                  trajectory_areas_nested=True,fixed_primary_cohort_2598=True,diagnostic_flag_preserved=True)
    forward=Transformer.from_crs('EPSG:4326',AEA,always_xy=True)
    reverse=Transformer.from_crs(AEA,'EPSG:4326',always_xy=True)
    cohort['centroid_x_aea_m'],cohort['centroid_y_aea_m']=forward.transform(cohort.centroid_lon_aea.to_numpy(),cohort.centroid_lat_aea.to_numpy())
    # Projected weighted average of cell centroids is a proxy, not a burned/converted-pixel centroid.
    summaries=[];biome_rows=[];state_rows=[]
    for t0,t1 in INTERVALS:
        f=cohort[cohort.t0.eq(t0)]
        domain=p[p.t0.eq(t0)];w=f.nat_tmp_endpoint_ha.to_numpy();a=float(w.sum())
        check(a>0,'No weight for centroid')
        cx=float(np.average(f.centroid_x_aea_m,weights=w));cy=float(np.average(f.centroid_y_aea_m,weights=w))
        lon,lat=reverse.transform(cx,cy)
        c,r=float(f.consolidation_ha.sum()),float(f.replenishment_ha.sum())
        anypas=float(f.nat_tmp_pas_any_ha.sum());con2=float(f.nat_tmp_pas_consecutive2_ha.sum())
        defined=f.stock0_nat.gt(1e-9)
        supported=float(f.loc[defined,'nat_tmp_endpoint_ha'].sum());den=float(f.loc[defined,'stock0_nat'].sum())
        row={'t0':t0,'t1':t1,'diagnostic_interval':int(t0==2020),'cohort_cells':2598,
             'nat_endpoint_ha':a,'domain_nat_endpoint_ha':float(domain.nat_tmp_endpoint_ha.sum()),
             'cohort_share_domain_nat':a/float(domain.nat_tmp_endpoint_ha.sum()),
             'cohort_nat_high_cells':int(f['nat_tmp_endpoint_ha__class'].eq('positive_high').sum()),
             'consolidation_ha':c,'replenishment_ha':r,'net_cr_balance_ha':c-r,
             'aggregate_cr_index':(c-r)/(c+r),
             'any_pasture_detected_ha':anypas,'consecutive2_pasture_detected_ha':con2,
             'any_pasture_share_pooled_endpoint':anypas/a,'consecutive2_pasture_share_pooled_endpoint':con2/a,
             'no_pasture_detected_endpoint_ha':a-anypas,
             'initial_native_stock_ha':float(f.stock0_nat.sum()),'initial_pasture_stock_ha':float(f.stock0_pas.sum()),
             'pooled_nat_intensity_supported_initial_native':supported/den,
             'nat_intensity_supported_cells':int(defined.sum()),
             'centroid_x_aea_m':cx,'centroid_y_aea_m':cy,'weighted_centroid_lon':float(lon),'weighted_centroid_lat':float(lat),
             'weighted_rms_distance_to_centroid_km':float(np.sqrt(np.average((f.centroid_x_aea_m-cx)**2+(f.centroid_y_aea_m-cy)**2,weights=w))/1000)}
        for biome,b in f.groupby('primary_biome'):
            ba=float(b.nat_tmp_endpoint_ha.sum())
            biome_rows.append({'t0':t0,'t1':t1,'diagnostic_interval':int(t0==2020),'primary_biome':biome,
                               'cells':len(b),'nat_endpoint_ha':ba,'share_cohort_nat':ba/a,
                               'any_pasture_share_pooled_endpoint':float(b.nat_tmp_pas_any_ha.sum())/ba})
        for stage in CR_STAGES:
            sub=f[f['cr_balance_index__class'].eq(stage)];sa=float(sub.nat_tmp_endpoint_ha.sum())
            state_rows.append({'t0':t0,'t1':t1,'diagnostic_interval':int(t0==2020),'cr_stage':stage,
                               'cells':len(sub),'nat_endpoint_ha':sa,'share_cohort_nat':sa/a})
            row['nat_area_in_cr_'+stage]=sa
        check(np.isclose(sum(x['nat_endpoint_ha'] for x in biome_rows if x['t0']==t0),a,rtol=1e-10,atol=1e-6),'Biome sum differs')
        check(np.isclose(sum(x['nat_endpoint_ha'] for x in state_rows if x['t0']==t0),a,rtol=1e-10,atol=1e-6),'State sum differs')
        summaries.append(row)
    summary=pd.DataFrame(summaries)
    geod=Geod(ellps='GRS80')
    shift=[None]
    for i in range(1,8):
        _,_,d=geod.inv(summary.weighted_centroid_lon.iloc[i-1],summary.weighted_centroid_lat.iloc[i-1],
                      summary.weighted_centroid_lon.iloc[i],summary.weighted_centroid_lat.iloc[i])
        shift.append(float(d/1000))
    summary['weighted_centroid_shift_from_previous_km']=shift
    check(np.isfinite(summary[['weighted_centroid_lon','weighted_centroid_lat']]).all().all(),'Nonfinite centroid')
    check(np.isclose(summary.loc[summary.t0.lt(2020),'nat_endpoint_ha'].sum(),8010398.701347958,rtol=1e-10,atol=1e-6),'Primary area does not reproduce prior exploration')
    checks.update(biome_associated_area_partitions_close=True,cr_state_area_partitions_close=True,
                  projected_weighted_centroids_finite=True,primary_area_reproduces_previous_exploration=True)
    # Retain native denominator for interpretability, but do not treat summed stocks across intervals as unique areas.
    kept=list(dict.fromkeys(KEYS+['GRID_ID','diagnostic_interval']+spatial+required_areas+
                           ['gross_cr_activity_ha','net_cr_balance_ha','cr_balance_index','nat_tmp_endpoint_ha__class',
                            'cr_balance_index__class','nat_tmp_intensity_initial_native','nat_tmp_intensity_defined',
                            'nat_tmp_endpoint_share_defined','nat_tmp_pas_any_share_endpoint','nat_tmp_pas_consecutive2_share_endpoint']))
    cohort[kept].to_csv(out/'high_nat_tmp_continuous_cell_interval_v1.csv',index=False,encoding='utf-8-sig',float_format='%.17g')
    gis=out/'gis';gis.mkdir(exist_ok=True)
    schema=[]
    for t0,t1 in INTERVALS:
        frame=cohort.loc[cohort.t0.eq(t0),kept].copy()
        name=f'high_nat_tmp_continuous_{t0}_{t1}_v1.csv'
        check(frame.cell_id.is_unique and len(frame)==2598,'GIS cohort cardinality differs')
        frame.to_csv(gis/name,index=False,encoding='utf-8-sig',float_format='%.17g')
        schema += [f'[{name}]','Format=CSVDelimited','ColNameHeader=True','MaxScanRows=0']
        for i,col in enumerate(frame.columns,1):
            kind=('Long' if pd.api.types.is_integer_dtype(frame[col]) else 'Double'
                  if pd.api.types.is_numeric_dtype(frame[col]) else 'Text Width 256')
            schema.append(f'Col{i}={col} {kind}')
        schema.append('')
    (gis/'schema.ini').write_text('\n'.join(schema),encoding='ascii')
    checks.update(eight_gis_cohort_tables_unique=True,schema_has_no_invalid_charset_option=True)
    summary.to_csv(out/'high_nat_tmp_continuous_period_summary_v1.csv',index=False,encoding='utf-8-sig',float_format='%.17g')
    pd.DataFrame(biome_rows).to_csv(out/'high_nat_tmp_continuous_primary_biome_v1.csv',index=False,encoding='utf-8-sig',float_format='%.17g')
    pd.DataFrame(state_rows).to_csv(out/'high_nat_tmp_continuous_cr_state_v1.csv',index=False,encoding='utf-8-sig',float_format='%.17g')
    # Static scientific plots with the same numeric scales and diagnostic marker across periods.
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    labels=[f'{y}–{y+5}'+('*' if y==2020 else '') for y in range(1985,2025,5)]
    x=np.arange(8)
    fig,axs=plt.subplots(2,2,figsize=(13,9))
    ax=axs[0,0];ax.plot(x,summary.domain_nat_endpoint_ha/1e6,'o-',color='#a8a8a8',label='Domínio completo')
    ax.plot(x,summary.nat_endpoint_ha/1e6,'o-',color='#246b8e',label='Coorte fixa');ax.set_title('Área NAT→TMP por intervalo');ax.set_ylabel('Milhões de hectares');ax.legend(frameon=False)
    ax=axs[0,1];ax.plot(x,summary.replenishment_ha/1e6,'o-',color='#238b45',label='Reposição NAT→PAS')
    ax.plot(x,summary.consolidation_ha/1e6,'o-',color='#8856a7',label='Consolidação PAS→TMP');ax.set_title('Fluxos C–R da coorte');ax.set_ylabel('Milhões de hectares');ax.legend(frameon=False)
    ax=axs[1,0];ax.plot(x,summary.aggregate_cr_index,'o-',color='#36566d');ax.axhline(0,color='#555',lw=.8)
    ax.axhline(-1/3,color='#238b45',lw=.8,ls=':');ax.axhline(1/3,color='#8856a7',lw=.8,ls=':')
    ax.set_ylim(-1,1);ax.set_title('Índice C–R calculado pelas somas dos fluxos');ax.set_ylabel('(ΣC − ΣR) / (ΣC + ΣR)')
    ax=axs[1,1];ax.plot(x,100*summary.any_pasture_share_pooled_endpoint,'o-',color='#8e6b36',label='Alguma pastagem detectada')
    ax.plot(x,100*summary.consecutive2_pasture_share_pooled_endpoint,'o-',color='#244d68',label='Dois anos consecutivos');ax.set_ylim(0,10)
    ax.set_title('Pastagem intermediária: participação na área NAT→TMP');ax.set_ylabel('% da soma da área endpoint');ax.legend(frameon=False,fontsize=9)
    for ax in axs.ravel():
        ax.set_xticks(x,labels,rotation=40,ha='right');ax.axvspan(6.5,7.5,color='#999',alpha=.12);ax.grid(axis='y',alpha=.2)
    fig.suptitle('Áreas contínuas na coorte fixa de 2.598 células',fontsize=15)
    fig.text(.5,.025,'*2020–2025: diagnóstico. Participações de trajetória = razão entre somas, sem excluir os endpoints pequenos.',ha='center',fontsize=9)
    fig.subplots_adjust(top=.91,bottom=.13,hspace=.6,wspace=.28)
    fig.savefig(figures/'high_nat_tmp_area_flows_composition_v1.png',dpi=200);plt.close(fig)
    # Projected proxy centroid and geographic maps of the continuous measure.
    domain=support=frames[0]
    fig,axs=plt.subplots(2,4,figsize=(15,10))
    maxvalue=float(cohort.nat_tmp_endpoint_ha.max());norm=LogNorm(vmin=.1,vmax=maxvalue)
    for i,ax in enumerate(axs.ravel()):
        f=cohort[cohort.t0.eq(INTERVALS[i][0])];pos=f.nat_tmp_endpoint_ha.gt(1e-9)
        ax.scatter(domain.centroid_lon_aea,domain.centroid_lat_aea,s=2,color='#e3e5e7',linewidths=0,rasterized=True)
        dots=ax.scatter(f.loc[pos,'centroid_lon_aea'],f.loc[pos,'centroid_lat_aea'],s=9,c=f.loc[pos,'nat_tmp_endpoint_ha'],
                        cmap='viridis',norm=norm,linewidths=0,rasterized=True)
        ax.scatter(summary.weighted_centroid_lon.iloc[i],summary.weighted_centroid_lat.iloc[i],s=95,marker='D',
                   facecolors='#ff574f',edgecolors='#fff',linewidths=.8,zorder=4)
        ax.set_xlim(-75,-40);ax.set_ylim(-26,6);ax.set_aspect('equal');ax.set_xticks([-70,-60,-50,-40]);ax.set_yticks([-25,-15,-5,5]);ax.grid(alpha=.15)
        t0,t1=INTERVALS[i];ax.set_title(f'{t0}–{t1}'+(' · diagnóstico' if i==7 else '')+f'\nNAT→TMP: {summary.nat_endpoint_ha.iloc[i]/1e6:.3f} Mha',fontsize=10)
        ax.set_xlabel('Longitude (°)',fontsize=8);ax.set_ylabel('Latitude (°)',fontsize=8);ax.tick_params(labelsize=8)
    fig.suptitle('Magnitude NAT→TMP e centro ponderado da distribuição na coorte',fontsize=14)
    cax=fig.add_axes([.35,.105,.4,.017]);fig.colorbar(dots,cax=cax,orientation='horizontal',label='Área NAT→TMP por célula (ha) · escala logarítmica fixa')
    fig.text(.5,.018,'Losango vermelho = centro ponderado pelos hectares. Pontos = centroides das células; não são centroides dos pixels convertidos.',ha='center',fontsize=9)
    fig.subplots_adjust(top=.9,bottom=.18,hspace=.32,wspace=.32)
    fig.savefig(figures/'high_nat_tmp_continuous_spatial_panels_v1.png',dpi=200);plt.close(fig)
    # Geographic trajectory over cell-centroid backdrop; numbers give chronological order.
    fig,ax=plt.subplots(figsize=(8,7))
    firstframe=cohort[cohort.t0.eq(1985)]
    ax.scatter(firstframe.centroid_lon_aea,firstframe.centroid_lat_aea,s=4,color='#d4d7da',linewidths=0)
    ax.plot(summary.weighted_centroid_lon.iloc[:7],summary.weighted_centroid_lat.iloc[:7],'-',color='#236b8e',lw=1.5)
    ax.plot(summary.weighted_centroid_lon.iloc[6:],summary.weighted_centroid_lat.iloc[6:],'--',color='#b54d3c',lw=1.5)
    ax.scatter(summary.weighted_centroid_lon.iloc[:7],summary.weighted_centroid_lat.iloc[:7],s=70,color='#236b8e',edgecolors='white',zorder=3)
    ax.scatter(summary.weighted_centroid_lon.iloc[7],summary.weighted_centroid_lat.iloc[7],s=100,color='#b54d3c',marker='D',edgecolors='white',zorder=3)
    for i,row in summary.iterrows():ax.annotate(str(i+1),(row.weighted_centroid_lon,row.weighted_centroid_lat),xytext=(5,5),textcoords='offset points',fontsize=10)
    ax.set_xlim(-62,-43);ax.set_ylim(-21,-5);ax.set_aspect('equal');ax.grid(alpha=.2);ax.set_xlabel('Longitude (°)');ax.set_ylabel('Latitude (°)')
    ax.set_title('Centro ponderado da área NAT→TMP\nCoorte fixa; projeção Albers no cálculo',fontsize=13)
    fig.text(.02,.015,'1: 1985–90   2: 1990–95   3: 1995–2000   4: 2000–05\n5: 2005–10   6: 2010–15   7: 2015–20   8: 2020–25 (diagnóstico)\nA linha representa redistribuição dos pesos, não deslocamento de parcelas.',fontsize=9)
    fig.subplots_adjust(bottom=.17)
    fig.savefig(figures/'high_nat_tmp_weighted_centroid_trajectory_v1.png',dpi=200);plt.close(fig)
    features=[]
    for row in summary.itertuples():
        features.append({'type':'Feature','geometry':{'type':'Point','coordinates':[row.weighted_centroid_lon,row.weighted_centroid_lat]},
                         'properties':{'t0':row.t0,'t1':row.t1,'diag':row.diagnostic_interval,'nat_ha':row.nat_endpoint_ha}})
    dump(out/'high_nat_tmp_weighted_centroids_v1.geojson',{'type':'FeatureCollection','features':features})
    checks.update(all_outputs_written=True)
    output_records={str(f.relative_to(out)):{'sha256':digest(f.read_bytes()),'bytes':f.stat().st_size}
                    for f in sorted(out.rglob('*')) if f.is_file() and f.name!='high_nat_tmp_continuous_validation_v1.json'}
    validation={'validation_status':'PASS','script_version':VERSION,'execution_utc':datetime.now(timezone.utc).isoformat(),
                'script_sha256':digest(Path(__file__).read_bytes()),'inputs':inputs,'checks':checks,
                'scope':{'domain_cells':24889,'fixed_primary_cohort_cells':2598,'cell_interval_rows':20784,
                         'primary_intervals':7,'full_intervals':8,'high_threshold_reference_ha':FROZEN_HIGH,
                         'cohort_selected_from_frozen_class_labels':True,'thresholds_refitted':False,'gee_used':False,
                         'formal_spatial_inference':False,'per_biome_areas_assigned_by_primary_cell_label':True,
                         'centroid_is_cell_center_proxy':True,'share_aggregation':'ratio_of_sums_without_share_class_support_exclusion',
                         'csv_source_precision':'15 significant digits','identity_rtol':1e-10,'identity_atol_ha':1e-6},
                'projection':AEA,'software':{'pandas':pd.__version__,'numpy':np.__version__,'matplotlib':matplotlib.__version__,'pyproj':PYPROJ_VERSION},
                'outputs':output_records}
    dump(out/'high_nat_tmp_continuous_validation_v1.json',validation)
    print(summary[['t0','nat_endpoint_ha','cohort_share_domain_nat','aggregate_cr_index','any_pasture_share_pooled_endpoint','weighted_centroid_lon','weighted_centroid_lat','weighted_centroid_shift_from_previous_km']].to_string(index=False))
    print('Continuous-area cohort comparison: PASS')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--gis-zip',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True)
    run(p.parse_args())
