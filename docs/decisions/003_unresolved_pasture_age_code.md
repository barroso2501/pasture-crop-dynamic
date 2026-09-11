# Decision 003 — Treat pasture-age code 1 as unresolved

- **Status:** Accepted
- **Date recorded:** 2026-09-09
- **Scope:** Pasture-age encoding and age-dependent analyses
- **Related validation:** `docs/validation/canonical_input_audit.md`
- **Related method:** `docs/methods/data_sources_and_classification.md`
- **Related configuration:** `config/constants.js`

## Context

The canonical input audit found a small area of pasture-age value `1` in the
public MapBiomas Collection 11 pasture-age asset. Code `1` is the only observed
value from 1 through 99 in the retained analytical domain. It is absent in
1985 and occurs in every audited quinquennial year from 1990 through 2025.

The observed area increases from 294.52 ha in 1990 to 1,732.52 ha in 2025. In
2025 it represents 0.00159% of mapped pasture in the retained domain. These
pixels coincide with pasture class `15` in the annual coverage product; the
audit found no pasture-presence disagreement between the two products.

The formal pasture-age encoding used by the project defines `100` as the
initial pasture stock present in 1985 and `2xx` as `200 + consecutive age` for
pasture established during the observed series. Code `1` is not defined by
that rule.

On 2026-09-09, the MapBiomas technician responsible for the pasture-age
product was consulted. The technician confirmed that code `1` was unexpected
and reported that the issue would be investigated. An official clarification
or corrected asset may not be available in the short term.

## Decision

The project assigns pasture-age code `1` the status **unresolved age**.

The following rules apply:

1. Code `1` must not be recoded as `201` or interpreted as a one-year-old
   pasture.
2. Annual coverage class `15` remains authoritative for pasture membership.
3. Pixels with code `1` remain in total pasture stock and land-cover transition
   accounting.
4. When a transition is decomposed by pasture age or origin, code `1` is
   exported as a separate `unresolved-age` component.
5. Code `1` is excluded from cohorts requiring an attributable numeric age.
6. Its area is reported, and age-dependent outputs include a sensitivity check
   showing whether exclusion affects the substantive result.
7. The rule is revisited only if MapBiomas publishes an official clarification,
   changes the public asset, or supplies a validated replacement rule.

The anomaly remains open at the source-product level but is operationally
resolved for the present workflow through explicit classification and
reporting. It does not block land-cover stock-and-flow reprocessing.

## Rationale

Reinterpreting an unexpected source value would introduce unsupported
information. Dropping the affected pixels entirely would instead undercount
pasture and break otherwise valid coverage-based accounting. Separating
pasture membership from attributable age preserves the land-cover evidence
while keeping the uncertainty visible in analyses that depend on age.

The affected proportion is very small, but magnitude alone is not used to
justify silent deletion or recoding. Explicit treatment makes the decision
reproducible and allows its influence to be measured.

## Consequences

### Land-cover accounting

Pasture stocks and transitions continue to be determined from coverage class
`15`. Code `1` does not create missing pasture area in these totals.

### Age-dependent accounting

Every decomposition by pasture origin must close with an explicit unresolved
component. For example:

```text
PAS→TMP total = initial-stock origin + attributable-age origin
                + unresolved-age origin + other unattributed-age origin
```

Age summaries must state the denominator used. If unresolved pixels are
excluded from the denominator, their excluded area and share must be reported.

### Reproducibility

`config/constants.js` records `[1]` in
`PASTURE_AGE_UNRESOLVED_CODES`. The decoding helper returns no numeric age for
this value. Downstream scripts must use this shared rule rather than create
local recodings.

### Future source resolution

If MapBiomas resolves the anomaly, the project will record the clarification,
update the shared configuration, rerun affected age-dependent outputs, and
compare them with the unresolved-code version. Existing results will not be
silently overwritten without a provenance record.

## Alternatives considered

### Recode `1` as `201`

Rejected because the product specialist confirmed that `1` was unexpected.
There is currently no validated basis for treating it as a one-year-old
pasture.

### Exclude the pixels from all analyses

Rejected because the annual coverage product classifies them as pasture and
the products agree on pasture presence. Exclusion would unnecessarily bias
coverage-based stock and transition totals.

### Suspend all reprocessing until MapBiomas resolves the issue

Rejected because the anomaly affects only age attribution for a very small
area and can be isolated transparently. It does not invalidate the canonical
coverage product or general land-cover accounting.

## Acceptance criteria

This decision is implemented when:

- code `1` is centralized as an unresolved value in `config/constants.js`;
- no canonical script decodes code `1` as a numeric age;
- pasture totals continue to use coverage class `15`;
- age-origin exports contain an explicit unresolved component;
- closure tests include that component;
- the affected area and sensitivity results are retained with analytical
  outputs; and
- any future MapBiomas resolution triggers a documented update and targeted
  reprocessing.
