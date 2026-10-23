"""Plot eight accepted canonical intervals; diagnostic extension separate; no smoothing."""
from pathlib import Path
import argparse,csv,hashlib,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

def plot(root):
 root=Path(root);source=root/'outputs/summary/rq2_entry_reentry_v4_4/canonical_entry_reentry_interval_composition_v4_4.csv'
 with source.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
 claims=json.loads((root/'outputs/summary/rq2_entry_reentry_v4_4/canonical_rq2_entry_reentry_claims_v4_4.json').read_text())
 native=root/'outputs/validation/entry_reentry_v1/full/canonical_entry_reentry_full_v1_summary.csv'
 if hashlib.sha256(native.read_bytes()).hexdigest()!=claims['source_summary_sha256']:raise ValueError('Accepted source changed')
 assert len(rows)==8 and [int(r['t0']) for r in rows]==list(range(1985,2025,5))
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42})
 fig,(a,b)=plt.subplots(2,1,figsize=(12,9),gridspec_kw={'height_ratios':[1.15,1]},sharex=True)
 xs=list(range(8));bottom=[0.]*8
 cats=[('initial_ha','Episódio contínuo desde 1985','#73899B'),('first_observed_entry_ha','Primeira entrada observada','#218C74'),('observed_reentry_ha','Reentrada observada','#D78532'),('prior_history_uncertain_ha','Entrada: histórico anterior incerto','#9971B5'),('unresolved_ha','Origem do episódio não resolvida','#BE5260')]
 for field,label,color in cats:
  vals=[float(r[field])/1e6 for r in rows]
  a.bar(xs,vals,bottom=bottom,width=.64,color=color,label=label,linewidth=0)
  bottom=[u+v for u,v in zip(bottom,vals)]
 for x,total in zip(xs,bottom):a.text(x,total+.065,f'{total:.2f}'.replace('.',','),ha='center',va='bottom',fontsize=9,color='#344352')
 a.set_ylim(0,5.65);a.set_ylabel('Fluxo PAS → TMP (milhões de ha)')
 a.set_title('A  Origem do fluxo no início de cada intervalo',loc='left',fontsize=12,fontweight='bold',pad=12)
 a.legend(loc='upper left',bbox_to_anchor=(0,1.02),ncol=2,frameon=False,fontsize=9,columnspacing=1.8)
 a.tick_params(axis='x',labelbottom=False)
 for field,label,color in [('observed_reentry_fraction_of_entry_flow','Reentrada / fluxo de entrada pós-1985','#BD671F'),('observed_reentry_fraction_of_entry_stock','Reentrada / estoque de entrada em t0','#216B9A')]:
  vals=[100*float(r[field]) if r[field] else float('nan') for r in rows]
  b.plot(xs[1:7],vals[1:7],color=color,marker='o',lw=2.1,ms=5,label=label)
  b.plot(xs[6:8],vals[6:8],color=color,marker='o',lw=1.9,ms=5,ls='--')
  b.annotate(f'{vals[6]:.2f}%'.replace('.',','),(6,vals[6]),xytext=(-8,8 if color=='#BD671F' else -16),textcoords='offset points',ha='right',color=color,fontsize=9)
  b.annotate(f'{vals[7]:.2f}%'.replace('.',','),(7,vals[7]),xytext=(-8,8 if color=='#BD671F' else -16),textcoords='offset points',ha='right',color=color,fontsize=9)
 b.set_ylim(0,37);b.set_ylabel('Participação condicional da reentrada')
 b.yaxis.set_major_formatter(PercentFormatter(100,decimals=0));b.set_title('B  Reentrada dentro do componente de entrada pós-1985',loc='left',fontsize=12,fontweight='bold',pad=12)
 b.text(0,10,'Indefinida:\nentrada = 0',ha='center',va='center',fontsize=9,color='#677484')
 b.legend(loc='upper left',frameon=False,fontsize=9)
 b.set_xticks(xs,[r['t0']+'–'+r['t1'] for r in rows]);b.set_xlabel('Intervalo de cinco anos',labelpad=12)
 for ax in [a,b]:
  ax.axvspan(6.5,7.5,color='#E9EDF2',zorder=-1)
  ax.grid(axis='y',color='#DCE1E7',lw=.65);ax.set_axisbelow(True);ax.set_xlim(-.6,7.6)
  if ax is a:ax.text(7,.97,'Diagnóstico',ha='center',va='top',transform=ax.get_xaxis_transform(),fontsize=9,color='#485465')
 fig.suptitle('Primeira entrada e reentrada observadas na conversão de pastagem',fontsize=15,fontweight='bold',x=.08,ha='left',y=.975)
 fig.text(.08,.938,'Janela desde 1985 • 24.889 células • cobertura anual 1985–2025',fontsize=10.5,color='#526174')
 fig.subplots_adjust(left=.09,right=.98,top=.88,bottom=.17,hspace=.36)
 fig.text(.09,.102,'A: todos os componentes do fluxo. B: percentuais com denominadores próprios de fluxo e estoque em t0.',fontsize=9)
 fig.text(.09,.075,'Primeira entrada observada não significa primeira implantação histórica. Frações iniciais indefinidas ficam sem ponto.',fontsize=9)
 fig.text(.09,.048,'Classes residuais pequenas são preservadas nas tabelas. Áreas somadas entre intervalos não são áreas únicas.',fontsize=9)
 out=root/'figures/rq2_entry_reentry_v4_4';out.mkdir(parents=True,exist_ok=True)
 for ext in ['png','svg','pdf']:
  options={'metadata':{'Creator':'Pasture-crop-dynamic; RQ2 v4.4','Date':None}} if ext=='svg' else {'metadata':{'CreationDate':None,'ModDate':None}} if ext=='pdf' else {}
  with matplotlib.rc_context({'svg.hashsalt':'rq2-entry-reentry-v4.4'}):fig.savefig(out/f'fig01_entry_reentry_composition_v4_4.{ext}',dpi=180,facecolor='white',**options)
 plt.close(fig)
 print('Eight-interval entry/re-entry figure written (PNG/SVG/PDF).')

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);plot(ap.parse_args().root)
