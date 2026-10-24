"""Render three descriptive manuscript figures from authenticated accepted summaries."""
from pathlib import Path
import argparse,csv,hashlib,json,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.ticker import PercentFormatter

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def save(fig,folder,name):
 for ext in ['png','svg','pdf']:
  opts={'metadata':{'Date':None}} if ext=='svg' else {'metadata':{'CreationDate':None,'ModDate':None}} if ext=='pdf' else {}
  with matplotlib.rc_context({'svg.hashsalt':'integrated-manuscript-v1'}):fig.savefig(folder/(name+'.'+ext),dpi=180,facecolor='white',**opts)
 plt.close(fig)
def main(root):
 root=Path(root);pins=json.loads((root/'config/manuscript_integrated_v1/baseline_pins_v1.json').read_text())['sha256']
 sources=['outputs/validation/phase9_gap_resolution_v1/canonical_fixed_1985_pasture_cohort_summary_v1.csv','outputs/summary/phase7_biome_comparison_v1/canonical_phase7_biome_process_summary_v1.csv','outputs/validation/phase8e_maup_hh_cluster_v1/canonical_maup_hh_robustness_assessment_v1.csv']
 for n in sources:
  if sha(root/n)!=pins[n]:raise ValueError('Accepted plotting source changed: '+n)
 folder=root/'figures/manuscript_integrated_v1';folder.mkdir(parents=True,exist_ok=True)
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42})
 data=read(root/sources[0]);combined=sorted([x for x in data if x['boundary_scope']=='combined_domain'],key=lambda x:int(x['year']))
 cats=[('pas_share','Pastagem','#2A896F'),('tmp_share','Culturas temporárias','#D69834'),('nat_share','Vegetação natural','#547EAB'),('oag_share','Outros usos agropecuários','#A17EB3'),('other','Demais estados / sem observação','#B4BEC8')]
 def values(x,k):
  if k=='other':return 100*math.fsum(float(x[v+'_share']) for v in ['out','water','nodata','unexpected','masked'])
  return 100*float(x[k])
 fig,(a,b)=plt.subplots(1,2,figsize=(13,6),gridspec_kw={'width_ratios':[2.1,1]})
 bottom=[0.]*len(combined)
 for k,label,color in cats:
  vals=[values(x,k) for x in combined];a.bar(range(9),vals,bottom=bottom,width=.66,color=color,label=label);bottom=[u+v for u,v in zip(bottom,vals)]
 assert all(abs(x-100)<1e-8 for x in bottom)
 a.axvspan(7.5,8.5,color='#EDF0F4',zorder=-1);a.set_xticks(range(9),[x['year'] for x in combined]);a.set_ylim(0,102);a.yaxis.set_major_formatter(PercentFormatter());a.set_ylabel('Participação da área fixa da coorte');a.set_title('A  Composição nos anos de referência',loc='left',fontweight='bold');a.set_xlabel('Ano observado (2025 diagnóstico)');a.legend(loc='upper center',bbox_to_anchor=(.63,-.18),ncol=3,frameon=False,fontsize=9)
 by=[next(x for x in data if x['boundary_scope']=='primary_assignment' and x['year']=='2020' and x['primary_biome']==v) for v in ['Amazon','Cerrado']];bottom=[0.,0.]
 for k,label,color in cats:
  vals=[values(x,k) for x in by];b.bar(range(2),vals,bottom=bottom,width=.58,color=color);bottom=[u+v for u,v in zip(bottom,vals)]
 b.set_xticks([0,1],['Amazônia\n7,747 Mha','Cerrado\n41,289 Mha']);b.set_ylim(0,102);b.yaxis.set_major_formatter(PercentFormatter());b.set_title('B  Coortes atribuídas, 2020',loc='left',fontweight='bold')
 for ax in [a,b]:ax.grid(axis='y',color='#E0E5EA',lw=.6);ax.set_axisbelow(True)
 fig.suptitle('Destino observado da coorte de pastagem de 1985',x=.075,ha='left',fontsize=15,fontweight='bold',y=.975)
 fig.text(.075,.925,'49,036 milhões de hectares fixos • a permanência em PAS não é uma curva de sobrevivência',fontsize=10,color='#536174')
 fig.subplots_adjust(left=.07,right=.98,top=.81,bottom=.29,wspace=.27)
 fig.text(.075,.055,'Bioma principal atribui células inteiras. Estados em datas sucessivas não revelam todos os caminhos entre elas.',fontsize=9)
 save(fig,folder,'fig02_fixed_1985_cohort_endpoints_v1')
 process=read(root/sources[1]);fig,axes=plt.subplots(1,3,figsize=(12,5.2))
 for ax,metric,title in zip(axes,['consolidation_ha','replenishment_ha','nat_tmp_endpoint_ha'],['Consolidação: PAS → TMP','Reposição: NAT → PAS','Endpoint NAT → TMP']):
  vals=[math.fsum(float(x['value_sum']) for x in process if x['boundary_scope']=='primary_assignment' and x['primary_biome']==b and x['metric']==metric and x['diagnostic_interval']=='0')/1e6 for b in ['Amazon','Cerrado']]
  ax.bar([0,1],vals,color=['#327D9A','#CA872E'],width=.6);ax.set_xticks([0,1],['Amazônia','Cerrado']);ax.set_title(title,fontsize=11,fontweight='bold');ax.set_ylabel('Soma dos fluxos de intervalo (Mha)');ax.set_ylim(0,max(vals)*1.25)
  for i,v in enumerate(vals):ax.text(i,v+max(vals)*.035,f'{v:.2f}'.replace('.',','),ha='center',fontsize=11)
  ax.grid(axis='y',color='#E0E5EA',lw=.6);ax.set_axisbelow(True)
 fig.suptitle('Contrastes entre biomas no período principal, 1985–2020',x=.07,ha='left',fontweight='bold',fontsize=15,y=.98)
 fig.text(.07,.90,'População completa • atribuição pelo bioma principal de cada célula',color='#536174',fontsize=10)
 fig.subplots_adjust(left=.07,right=.98,top=.77,bottom=.22,wspace=.45)
 fig.text(.07,.09,'Eixos verticais próprios por painel. As somas não são áreas únicas nem mudanças líquidas de estoque.',fontsize=9)
 fig.text(.07,.045,'A atribuição de células inteiras não representa uma partição exata dos pixels convertidos por limite de bioma.',fontsize=9)
 save(fig,folder,'fig05_primary_biome_process_totals_v1')
 hh=read(root/sources[2]);metrics=['consolidation_density_per_10kha','replenishment_density_per_10kha','nat_tmp_density_per_10kha','net_cr_density_per_10kha','cr_balance_index'];actual=set(x['metric'] for x in hh)
 # Use the accepted metric names; fail if the expected five-part comparison changes.
 if set(metrics)!=actual:
  for old,new in [('net_cr_density_per_10kha','net_cr_balance_density_per_10kha')]:
   if old not in actual and new in actual:metrics[metrics.index(old)]=new
 assert set(metrics)==actual,(metrics,actual)
 grids=['hex10k_base','hex20k_shift','hex40k_base'];windows=['primary_1985_2020','full_observed_1985_2025'];columns=[(w,g) for w in windows for g in grids]
 index={(x['metric'],x['window'],x['grid_code']):x for x in hh};arr=[[int(index[(m,w,g)]['overall_prespecified_robustness_pass']=='True') for w,g in columns] for m in metrics]
 assert sum(sum(row) for row in arr)==21
 fig,ax=plt.subplots(figsize=(12,5.5));ax.imshow(arr,cmap=ListedColormap(['#B5A5BC','#4A967D']),vmin=0,vmax=1,aspect='auto')
 for i,row in enumerate(arr):
  for k,v in enumerate(row):ax.text(k,i,'Passa' if v else 'Sensível',ha='center',va='center',color='white' if v else '#302C33',fontsize=10,fontweight='bold')
 ax.set_yticks(range(5),['Consolidação','Reposição','NAT → TMP','Balanço líquido C−R','Índice C−R']);ax.set_xticks(range(6),['10 mil ha','20 mil: deslocada','40 mil ha']*2);ax.axvline(2.5,color='white',lw=3)
 ax.set_xticks([x-.5 for x in range(7)],minor=True);ax.set_yticks([x-.5 for x in range(6)],minor=True);ax.grid(which='minor',color='white',lw=1.5);ax.tick_params(which='minor',length=0)
 ax.text(1,-.85,'Principal: 1985–2020',ha='center',fontweight='bold');ax.text(4,-.85,'Inclui diagnóstico: 1985–2025',ha='center',fontweight='bold')
 fig.suptitle('A robustez dos hotspots depende da métrica',x=.06,ha='left',fontsize=15,fontweight='bold',y=.97)
 fig.subplots_adjust(left=.19,right=.98,top=.76,bottom=.22)
 fig.text(.06,.10,'Critério composto de localização, recorrência e persistência HH: 21 de 30 avaliações passam.',fontsize=10)
 fig.text(.06,.05,'Sensibilidade a escala ou zoneamento é um resultado científico, não uma falha contábil.',fontsize=10)
 save(fig,folder,'fig06_hh_maup_robustness_v1')
 manifest={'date':'2026-10-24','sources':{n:sha(root/n) for n in sources},'new_analytical_fit':False,'description':'Descriptive rendering and arithmetic regrouping of accepted summaries; no new spatial model, native export or significance test.','outputs':{str(p.relative_to(root)):sha(p) for p in sorted(folder.glob('*')) if p.suffix in ['.png','.svg','.pdf']}}
 (folder/'figure_source_manifest_v1.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('Three integrated figures written: cohort endpoints, biome totals, HH robustness (PNG/SVG/PDF).')

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);main(ap.parse_args().root)
