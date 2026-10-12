# Observation-window sensitivity — executed method v2

**Date:** 2026-10-12. **Status:** native pilot and full-domain exports validated PASS. This version updates execution status after completion of section 1 of plan 009. The estimator, baselines, tolerances and comparison design are unchanged from method v1, retained as provenance. Results are in [the findings](../results/window_origin_sensitivity_full_findings_v1.md).

## Estimand and comparisons

Reconstruct current observed pasture-spell origin at interval start t0, with the same categorical rule and coverage source as the accepted motor, replacing its first year by b∈{1985,1995,2000}. PAS observed continuously from b receives baseline-continuous origin; PAS after a confirmed non-PAS reset receives observed-entry origin, including re-entry; gaps yield unresolved origin until a confirmed non-PAS reset. A gap at b remains uncertain. No bridging or pasture-age source decoding is used. RQ1's fixed-1985 cohort is unchanged.

The endpoint conversion population is PAS(t0)→TMP(t1), on the accepted native raster lattice and fixed 24,889-cell domain. All active baseline origins are reduced in the same native computation for each interval and batch, keeping the denominator identical. Export the conversion partition, the current-PAS-stock origin partition and baseline PAS stock, plus zero-expected categorical invariant counters. Pixel-year counters can contain fractional pixel equivalents from weighted boundary reductions; they are not hectares and are not unique-pixel counts. Their required value is zero.

| Comparison | Period | What is held constant | What changes |
|---|---|---|---|
| Calendar-matched primary | 2000–2005 through 2015–2020 | Endpoint conversions and calendar intervals | Baseline-defined origin categories and cohort selection |
| Calendar-matched diagnostic | 2020–2025, separate | Endpoint conversions | Same redefinition, plus source boundary limitations |
| Follow-up matched | First four intervals after each b (20 years) | Elapsed time since the baseline | Calendar period and baseline population |
| Own-window pooled | b–2020 and b–2025 | Each window's reporting rule | Unequal horizons; marked noncomparable across baselines |

The first interval of each baseline has 100% baseline-continuous origin **by construction** where its conversion area is positive. In a cell or interval with zero conversions, origin shares are undefined, not 100%. Continuous baseline stock can only lose membership, but its share of selected conversions need not decline. At a fixed calendar interval, later baselines can only expand the initial category and reduce the observed-entry/unresolved categories; the validator checks that set-nesting implication per cell.

Rebased trajectories can demonstrate sensitivity to the observation boundary. They cannot isolate a causal window artifact, estimate an artifact fraction, prove stationarity, or identify a process threshold at a 50% crossing. Follow-up matching changes calendar time and the baseline populations. A null renewal/hazard model would be a separate identification exercise. Observed entry is not first-ever establishment. Pooled areas sum interval conversions and may count pixels repeatedly. PAS classification accuracy is not validated by accounting closure.

## Export design

Use the provided pilot and full scripts without editing their parameters. The pilot selects `GRID_ID` IK-77 and GH-123, corresponding to cell IDs 32173 and 18081, for 2015–2020. Its cell table contains six rows (two cells × three baselines), accompanied by one run manifest and 30 native synthetic cases (10 sequences × three baselines). Native tests use the same reconstruction function as the coverage export and require positive tested pixel support and zero mismatches at every synthetic step. They test categorical origin states, not auxiliary numerical age 201 or the separate 2024/2025 event raster.

The full script creates 48 cell-table tasks (six intervals × eight canonical batches) plus one six-row run manifest. It computes 1995–2000 through 2020–2025, with 1985 as a repeated control. The eight accepted full-v3 cell CSVs are authenticated by their pinned hashes. The first two b=1985 intervals are reused from those accepted tables; they are labeled as reference reuse and never receive invented native audit counts. The final normalized panel has 19 baseline/interval populations and 472,891 rows, including 423,113 freshly exported rows and 49,778 reused rows.

Both scripts import the existing constants module. The supplied `constants_window_sensitivity_reference_v1.js` is an offline reference snapshot, not an instruction to overwrite the current module. The run manifest records actual runtime asset identifiers, class groups, code vectors, all 41 coverage band names/order, area convention, native CRS and transform. The validator rejects any mismatch with the prespecified configuration.

The scripts use explicit native `crs` and `crsTransform`, with `tileScale=16`, and preserve the accepted `unmask` convention. These API choices were checked against the official [reduceRegions](https://developers.google.com/earth-engine/apidocs/ee-image-reduceregions), [unmask](https://developers.google.com/earth-engine/apidocs/ee-image-unmask) and [table export](https://developers.google.com/earth-engine/apidocs/export-table-todrive) references. The two-cell pilot passed on 2026-10-09 and all six-interval/eight-batch full exports passed validation on 2026-10-12. No measured runtime or memory benchmark is claimed.

## Acceptance and outputs

Pilot acceptance requires complete three-file exports, exact two-cell/reference crosswalks, all three baselines, native synthetic PASS, positive test support, zero field-invariant counters, closure, unchanged flow/stock totals, and reproduced b=1985 origins. Pilot PASS is mandatory before full validation. Full validation additionally requires all 48 cell files, exact batch/domain populations, all 19 populations after labeled reference reuse, per-cell and aggregate control agreement, baseline-stock constancy and non-increasing continuous-cohort area.

Per-cell area tolerance is 0.01 ha; aggregate b=1985 flow/component tolerance is 0.001 ha; zero counter tolerance is 10⁻⁹. These tolerances test arithmetic consistency, not source uncertainty. Full validation produces the cell panel, 19 interval summaries, 15 calendar comparison rows (including diagnostic rows separately flagged), 12 elapsed-time comparison rows, 15 pooled rows and three window-specific crossing descriptors. Weighted cell quantiles exclude zero-flow cells, use conversion area as weight, and use the inverse empirical weighted cumulative distribution.

Snapshots of both supplied scripts have SHA-256 identities in the package. The validator always records that snapshot identity and the observed export/run-manifest hashes. `--attest-unmodified-supplied-script` additionally records the supplied-script hash as operator-attested executed text. This is an operator statement, not independent authentication by the GEE service. Omit the flag if the text was edited; preserve the actually executed text and arrange validation of a new version rather than claiming the unchanged template was executed. Remote constants bytes and mutable asset contents are not cryptographically authenticated by their names alone.

Accepted inputs and versioned outputs are not silently overwritten. Local scalar and synthetic-tabular self-tests verify software behavior only; none of their fabricated tables is distributed as a scientific result. The real native pilot and full-domain window-sensitivity exports have passed validation. This completes the specified descriptive sensitivity; it does not add a renewal/hazard model, first-entry/re-entry decomposition, auxiliary-age 201 test or uncertain-pair cross-tabulation.

## Projection metadata correction

The corrected scripts obtain `projection().getInfo()` once before task creation and validate a CRS plus six finite affine coefficients. `Projection.transform()` returns WKT and is not used as a coefficient list. Both submitted manifests pass the native projection check. Supplied source snapshot hashes are retained; executed remote-text identity is not independently authenticated.
