"""Plot the accepted derivative; no smoothing or inferential estimates."""
from pathlib import Path
import argparse,json,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

def main(root):
    folder=root/'outputs/summary/rq2_relative_conversion_v1'
    source=folder/'canonical_relative_endpoint_conversion_fractions_v1.csv'
    v=json.loads((folder/'canonical_relative_endpoint_conversion_validation_v1.json').read_text())
    if hashlib.sha256(source.read_bytes()).hexdigest()!=v['outputs'][source.name]['sha256']:raise ValueError('Derivative hash differs')
    d=pd.read_csv(source);colors={1985:'#1768AC',1995:'#B75A16',2000:'#21815B'}
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42})
    fig,(a,b)=plt.subplots(1,2,figsize=(12,5.4))
    a.axhline(1,color='#777777',lw=1,ls=':',label='Frações iguais (R=1)')
    for base,color in colors.items():
        q=d.loc[d.baseline_year.eq(base)].sort_values('t0')
        primary=q.loc[q.diagnostic_interval.eq(0)]
        a.plot(primary.t0,primary.relative_fraction_ratio_initial_entry,'o-',color=color,label=f'Janela {base}',lw=2,ms=5)
        last=q.loc[q.t0.ge(2015)]
        a.plot(last.t0,last.relative_fraction_ratio_initial_entry,'o--',color=color,lw=1.5,ms=5)
    a.set(title='A  Frações por estoque em t0',ylabel='Razão initial / observed entry',xlabel='Início do intervalo de cinco anos',ylim=(.55,1.55))
    a.set_xticks([1990,1995,2000,2005,2010,2015,2020])
    a.legend(loc='upper left',ncol=2,frameon=False,fontsize=9)
    q=d.loc[d.baseline_year.eq(1985)].sort_values('t0')
    for field,label,color in [('initial_conversion_share_pct','Initial na conversão PAS→TMP','#6B3A90'),('initial_stock_share_pct','Initial no estoque PAS em t0','#148078')]:
        b.plot(q.loc[q.diagnostic_interval.eq(0),'t0'],q.loc[q.diagnostic_interval.eq(0),field],'o-',lw=2,ms=5,label=label,color=color)
        last=q.loc[q.t0.ge(2015)]
        b.plot(last.t0,last[field],'o--',lw=1.5,ms=5,color=color)
    b.set(title='B  Composição, janela de 1985',ylabel='Participação initial (%)',xlabel='Início do intervalo de cinco anos',ylim=(0,105))
    b.set_xticks([1985,1995,2005,2015,2020])
    b.legend(loc='upper right',frameon=False,fontsize=9)
    for ax in [a,b]:
        ax.axvspan(2017.5,2022.5,color='#eeeef1',zorder=0)
        ax.grid(axis='y',lw=.6,color='#ddd')
    fig.suptitle('Conversão quinquenal: composição do estoque e frações por classe',fontweight='bold',fontsize=14,y=.985)
    fig.subplots_adjust(top=.83,bottom=.24,left=.07,right=.985,wspace=.25)
    fig.text(.07,.09,'R = (conversão initial / estoque initial) ÷ (conversão entry / estoque entry). Primeiros R: indefinidos.',fontsize=9.5)
    fig.text(.07,.045,'Sombreado/tracejado: diagnóstico 2020–2025. Estoque em t0 não é exposição temporal; R não é risco causal ajustado.',fontsize=9.2)
    out=root/'figures/rq2_relative_conversion_v1';out.mkdir(parents=True,exist_ok=True)
    for ext in ['png','svg','pdf']:fig.savefig(out/f'fig01_relative_endpoint_conversion_v1.{ext}',dpi=180,facecolor='white')
    plt.close(fig)
    print('Relative endpoint-conversion figure written.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    main(p.parse_args().root)
