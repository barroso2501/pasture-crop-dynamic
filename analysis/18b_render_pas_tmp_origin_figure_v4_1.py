"""Render the window-qualified PAS->TMP origin figure from unchanged interval v2."""
import argparse
import hashlib
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = p.parse_args()
    source = args.root / 'outputs/summary/pasture_spell_panel_v2/canonical_pas_tmp_origin_interval_summary_v2.csv'
    if hashlib.sha256(source.read_bytes()).hexdigest() != '8b24c1c3475f1f19bca6abc09c425df43400f573e04d41df7afd0473b088c897':
        raise ValueError('Accepted interval source hash differs')
    interval = pd.read_csv(source)
    fig, ax = plt.subplots(figsize=(11.5, 6.5))
    bottom = [0.] * 8
    for key, label, color in [('initial_pct', 'Continuous baseline-1985 spell', '#3075A5'), ('new_pct', 'Observed post-1985 entry (includes re-entry)', '#E99A35'), ('unresolved_pct', 'Unresolved', '#777777')]:
        vals = interval[key].to_numpy()
        bars = ax.bar(range(8), vals, bottom=bottom, label=label, color=color, width=.7)
        bars[-1].set_hatch('///')
        bottom = [a+b for a, b in zip(bottom, vals)]
    for n, row in interval.iterrows():
        if n:
            ax.text(n, row.initial_pct/2, f'{row.initial_pct:.2f}%', ha='center', va='center', color='white', fontsize=10)
            ax.text(n, row.initial_pct+row.new_pct/2, f'{row.new_pct:.2f}%', ha='center', va='center', fontsize=10)
    ax.text(0, 50, '100%\nby\nconstruction', ha='center', va='center', color='white', fontsize=8, fontweight='bold')
    ax.set_xticks(list(range(8)), [x.replace('_', '–')+('\nDiagnostic' if n==7 else '') for n, x in enumerate(interval.interval)], rotation=22, ha='right')
    ax.set_ylim(0, 100)
    ax.set_ylabel('Share of PAS→TMP endpoint conversion area (%)')
    ax.set_title('Observed pasture-spell origin within the 1985 observation window', pad=16)
    ax.spines[['top', 'right']].set_visible(False)
    ax.legend(loc='upper center', bbox_to_anchor=(.5, -.21), ncol=1, frameon=False, fontsize=10)
    fig.text(.065, .045, '1985 is an observation boundary. Shares are window-dependent; the 50% crossing is not a process threshold.\nUnresolved <0.001% in every interval; it is retained in the denominator. Final interval has limited boundary support.', fontsize=10)
    fig.subplots_adjust(left=.09, right=.98, top=.89, bottom=.37)
    out = args.root / 'figures/decision024_review_v1'
    out.mkdir(parents=True, exist_ok=True)
    with matplotlib.rc_context({'svg.hashsalt': 'decision024-origin-v4.1'}):
        fig.savefig(out / 'fig02_pas_tmp_origin_composition_v4_1.png', dpi=180)
        fig.savefig(out / 'fig02_pas_tmp_origin_composition_v4_1.svg', metadata={'Date': '2026-10-09'})
    plt.close(fig)
    print('Rendered figure v4.1 from authenticated interval v2.')


if __name__ == '__main__':
    main()
