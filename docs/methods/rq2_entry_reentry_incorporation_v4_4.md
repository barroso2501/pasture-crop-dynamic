# RQ2 v4.4: incorporation of observed entry/re-entry chronology

2026-10-23. Scope: accepted canonical coverage-derived b1985 accounting, 24,889 cells, eight five-year intervals; 2020–2025 diagnostic. No new native export or change to canonical classes, raster alignment, origin reconstruction or flow estimand.

## Class definitions

The accepted origin of current observed PAS at t0 remains initial, confirmed post-1985 entry or unresolved. Initial means continuous PAS observations since 1985, with unknown earlier establishment date. The new auxiliary label subdivides only the confirmed-entry class. At a confident nonPAS→PAS entry, use observations strictly before the entry:

1. **Observed re-entry:** any earlier observed PAS exists, including a spell whose earlier origin was unresolved. Intervening gaps do not invalidate evidence of earlier PAS.
2. **First observed entry:** no earlier observed PAS and all earlier observations since 1985 valid.
3. **Prior-history uncertain:** no earlier observed PAS, but at least one earlier coverage gap. A confident nonPAS reset followed by observed entry establishes the current spell despite uncertainty in earlier history.

The auxiliary label is frozen at entry and carried during that confirmed spell. A missing observation is not a demonstrated exit, is never bridged and cannot itself establish a new confirmed entry. Baseline PAS is not a dated entry. First observed entry does not establish first-ever pasture implantation. The auxiliary integer age resets to 201 at confirmed entry/re-entry and advances on confirmed continuation; its native assurance concerns this coverage-derived engine, not every numeric value of the public pasture-age asset.

## Endpoint-flow and stock denominators

For interval [t0,t1], C denotes accepted endpoint PAS(t0)→TMP(t1) conversion and S denotes PAS stock at t0. Origin and subclass are assigned at t0. The classes do not reconstruct the annual path between the two endpoints.

The original identities are C = C_initial + C_entry + C_unresolved and S = S_initial + S_entry + S_unresolved. The auxiliary identities are C_entry = C_first + C_reentry + C_prior_uncertain, and the corresponding partition of S_entry. The update retains three distinct compositions:

- contribution to all conversion: C_kind / C;
- conditional composition of entry conversion: C_kind / C_entry;
- conditional composition of entry stock: S_kind / S_entry.

All domain fractions divide sums of cell areas. They are not averages of cell ratios. The flow and stock fractions have different denominators and do not by themselves estimate a hazard, preference or causal effect. First-interval entry conversion and stock are zero by construction, so conditional fractions are blank/undefined, without epsilon denominators or imputing a percentage of zero.

## Pooling and temporal comparison

Primary pooling sums the seven interval-conversion areas from 1985–1990 through 2015–2020 before computing class shares. Diagnostic 2020–2025 and full-observed 1985–2025 pools remain separate. The same pixel may contribute in more than one interval; pooled hectares are not a unique spatial union. No pooled stock/exposure ratio is created. Stock at t0 is not time-integrated exposure.

Re-entry histories have more opportunity to be observed farther from the 1985 boundary. Cohort/stock composition, calendar period and annual classification instability can also affect their shares. The primary conditional re-entry-flow sequence is not monotonic. No significance test, annual hazard, physical renewal process or causal trend is inferred.

## Authentication and evidence editions

The unchanged accepted full JSON authenticates 73 native CSVs, 199,112 cell/interval rows, 24,889 historical audits and the preserved native pilot (31 fixtures / 302 steps). This integration independently reaggregates all native interval records, authenticates the original critical-source snapshot and derived products (including the exact CSV restored from gzip), and reconciles unchanged canonical origin anchors within 0.001 ha. The 10 actual-history invariant counters per cell and one accepted-origin mismatch per cell/interval remain zero.

Matrix v4.4 preserves the schema and 35 finding IDs. Only P9A035/P9A036 receive substantive additions; 33 other findings, including P9A037, remain unchanged except edition. Canonical source paths/hashes, authentication flags, qualified statuses and causal flags are retained. The v4.4 source inventory retains all 13 v4.3 entries and adds eight traceable source/derivative entries. Events-v6 preserves all 12 events-v5 rows byte-for-byte and appends two supplementary events; this is not a suspension, rescission or status promotion.

The historical frozen protocol JSON remains unchanged. The new dated component-status JSON records accepted full coverage-derived chronology, auxiliary-age checks and uncertain-pair cross-tabs. It does not retrospectively claim that the original seeded annual-pixel sampling proposal was executed. Public-age complete numeric validation, remote executed-text attestation and public release readiness retain separate scopes.
