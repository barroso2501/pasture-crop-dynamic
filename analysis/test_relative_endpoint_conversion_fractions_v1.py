"""Meaningful denominator/aggregation checks; synthetic inputs are not results."""
import importlib.util
from pathlib import Path
import unittest
import pandas as pd

p=Path(__file__).with_name('18h_derive_relative_conversion_fractions_v1.py')
spec=importlib.util.spec_from_file_location('fractions',p)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

def row(si=100,se=100,ci=10,ce=5):
    return {'baseline_year':1985,'t0':1995,'t1':2000,'interval':'1995_2000',
            'diagnostic_interval':0,'baseline_interval_by_construction':0,
            'initial_ha':ci,'entry_ha':ce,'unresolved_ha':0,
            'initial_pas_stock_ha':si,'entry_pas_stock_ha':se,
            'unresolved_pas_stock_ha':0,'stock0_pas_ha':si+se,'flow_pas_tmp_ha':ci+ce}

class Fractions(unittest.TestCase):
    def test_equal_stocks_different_fractions(self):
        q=module.derive(pd.DataFrame([row()])).iloc[0]
        self.assertEqual(q.relative_fraction_ratio_initial_entry,2)
    def test_equal_fractions_different_composition(self):
        q=module.derive(pd.DataFrame([row(si=100,se=300,ci=10,ce=30)])).iloc[0]
        self.assertEqual(q.relative_fraction_ratio_initial_entry,1)
        self.assertEqual(q.initial_conversion_share_pct,25)
        self.assertEqual(q.initial_stock_share_pct,25)
    def test_missing_when_entry_stock_zero(self):
        q=module.derive(pd.DataFrame([row(se=0,ce=0)])).iloc[0]
        self.assertTrue(pd.isna(q.relative_fraction_ratio_initial_entry))
        self.assertEqual(q.relative_ratio_status,'undefined_zero_entry_stock')
    def test_no_finite_ratio_when_entry_conversion_zero(self):
        q=module.derive(pd.DataFrame([row(ce=0)])).iloc[0]
        self.assertTrue(pd.isna(q.relative_fraction_ratio_initial_entry))
        self.assertEqual(q.relative_ratio_status,'not_finite_zero_entry_conversion')
    def test_zero_initial_conversion_is_estimable(self):
        q=module.derive(pd.DataFrame([row(ci=0)])).iloc[0]
        self.assertEqual(q.relative_fraction_ratio_initial_entry,0)
        self.assertEqual(q.relative_ratio_status,'estimable')
    def test_ratio_of_sums_is_not_mean_of_ratios(self):
        cells=pd.DataFrame([row(100,10,20,1),row(10,100,1,20)])
        ratios=module.derive(cells).relative_fraction_ratio_initial_entry
        total=row(110,110,21,21)
        aggregate=module.derive(pd.DataFrame([total])).iloc[0]
        self.assertEqual(aggregate.relative_fraction_ratio_initial_entry,1)
        self.assertEqual(ratios.mean(),1.25)

if __name__=='__main__':unittest.main()
