# Relative endpoint conversion fractions v1

Date: 2026-10-12. Descriptive calculation on accepted full-domain interval sums; no new native execution or inference.

For origin o and interval [t0,t1], f_o=C_o/S_o, where C_o is endpoint PAS(t0)→TMP(t1) area attributed to o at t0 and S_o is the PAS stock of o at t0. R=f_initial/f_entry. All values are ratios of national sums, not averages of cell fractions or ratios. Unresolved origin remains separately reported; R compares the two resolved classes. The original origin shares retain the complete endpoint-flow denominator.

The identity C_initial/C_entry=(S_initial/S_entry)R separates stock composition and endpoint conversion fractions algebraically. It is not a causal decomposition or attribution of a mechanical artifact fraction. Stock at t0 is not time-integrated exposure, and endpoint conversion is not a first-event hazard. Geographic/cohort composition, competing transitions, source classification and censoring remain unadjusted. Do not annualize or label R as an adjusted causal preference.

If either class stock is zero, its fraction and the corresponding R are missing. If entry conversion is zero with positive stock, no finite R is recorded; the reason is explicit. The three first intervals have zero entry stock and undefined R, not R=1. C_initial=0 with positive stocks and positive entry fraction gives estimable R=0. No epsilon denominator or arbitrary replacement is used. Pools over unequal histories are not reported as exposure-normalized ratios.

19 interval rows are derived directly from the hash-pinned accepted interval-summary CSV. There are 16 estimable ratios and three first-interval missing values. The derivative CSV retains stocks, conversion areas, fractions, percentages, stock and conversion shares, R, status and the ratio-factorization residual. Source and outputs are hashed; canonical CSVs remain byte-identical. Six focused tests cover denominators, zero conversion and the distinction between ratio of sums and mean cell ratios.

Reproduce: `python analysis/18h_derive_relative_conversion_fractions_v1.py`. Software checks: `python analysis/test_relative_endpoint_conversion_fractions_v1.py`.
