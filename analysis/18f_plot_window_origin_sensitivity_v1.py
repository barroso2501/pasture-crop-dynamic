"""Plot accepted window-sensitivity summaries; no raster or panel recomputation."""
from pathlib import Path
import argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

def main(root):
    inputs = root / 'outputs/validation/window_origin_sensitivity_v1/full'
    d = pd.read_csv(inputs / 'canonical_window_origin_interval_summary_v1.csv')
    assert len(d) == 19 and set(d.baseline_year) == {1985, 1995, 2000}
    colors = {1985:'#1768AC',1995:'#B75A16',2000:'#21815B'}
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                         'svg.fonttype':'none','pdf.fonttype':42})
    fig, axes = plt.subplots(1,3,figsize=(15.0,5.4))
    a,b,c=axes
    a.axvspan(2017.5,2022.5,color='#eeeef1',zorder=0)
    for baseline,color in colors.items():
        q=d.loc[d.baseline_year.eq(baseline)].sort_values('t0')
        cal=q.loc[q.t0.ge(2000)]
        primary=cal.loc[cal.diagnostic_interval.eq(0)]
        a.plot(primary.t0,primary.initial_pct,'o-',color=color,lw=2,ms=5)
        last=cal.loc[cal.t0.ge(2015)]
        a.plot(last.t0,last.initial_pct,'o--',color=color,lw=1.7,ms=5)
        lag=q.loc[q.elapsed_intervals.lt(4)]
        b.plot(lag.elapsed_intervals*5,lag.initial_pct,'o-',color=color,lw=2,ms=5)
        c.plot(lag.elapsed_intervals*5,lag.continuous_baseline_stock_retained_pct,
               'o-',color=color,lw=2,ms=5,label=f'Janela {baseline}')
    a.set(title='A  Mesmo calendário',xlabel='Intervalo de conversão',ylabel='Origem initial em PAS→TMP (%)')
    a.set_xticks([2000,2005,2010,2015,2020],['2000–05','2005–10','2010–15','2015–20','2020–25'],rotation=35)
    a.text(2020,100,'Diagnóstico',ha='center',va='center',fontsize=8,color='#55555b')
    b.set(title='B  Mesmo tempo de acompanhamento',xlabel='Anos da janela até o início do intervalo',ylabel='Origem initial em PAS→TMP (%)')
    b.set_xticks([0,5,10,15])
    b.annotate('100% por construção',xy=(0,100),xytext=(2,93),fontsize=9,
               arrowprops={'arrowstyle':'->','color':'#55555b'},color='#44444a')
    c.set(title='C  Continuidade do estoque da janela',xlabel='Anos da janela até o início do intervalo',ylabel='Estoque PAS inicial ainda contínuo (%)')
    c.set_xticks([0,5,10,15])
    for ax in axes:
        ax.set_ylim(0,105)
        ax.set_yticks([0,25,50,75,100])
        ax.grid(axis='y',color='#dddddf',lw=.6,zorder=0)
    handles,labels=c.get_legend_handles_labels()
    fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.915),ncol=3,frameon=False)
    fig.suptitle('Sensibilidade à origem da janela de observação',fontsize=15,fontweight='bold',y=.992)
    fig.subplots_adjust(top=.79,bottom=.26,left=.065,right=.98,wspace=.38)
    fig.text(.065,.09,'24.889 células • Origem do episódio contínuo observado • Primeiras conversões: 100% initial por definição.',fontsize=10)
    fig.text(.065,.047,'B e C mudam calendário e coorte. Curvas não identificam uma fração de artefato nem demonstram estacionariedade.',fontsize=9.5,color='#44444a')
    output=root/'figures/window_origin_sensitivity_v1'
    output.mkdir(parents=True,exist_ok=True)
    for suffix in ['png','svg','pdf']:
        fig.savefig(output/f'fig01_window_origin_sensitivity_v1.{suffix}',dpi=180,facecolor='white')
    plt.close(fig)
    print('Scientific figure written from accepted interval summary.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    main(p.parse_args().root)
