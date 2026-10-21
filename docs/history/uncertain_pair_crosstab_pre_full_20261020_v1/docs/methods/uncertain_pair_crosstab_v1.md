# PAS-conditioned annual uncertain-pair cross-tab, v1

**Current status, 2026-10-15: native pilot PASS; full PENDING.** See the [pilot acceptance](../validation/uncertain_pair_crosstab_pilot_acceptance_v1.md). The initial implementation-stage status below is retained as history.

Implementation prepared 2026-10-15. Native pilot and full execution are **pending**. This method implements the uncertain-pair component of Plan 009; it does not complete the entry/re-entry chronology, numerical-age 201 assurance, or a fresh boundary-raster asset comparison. Current scientific matrix v4.3 and cumulative events-v5 remain unchanged.

## Support and observation states

Use the canonical Collection 11 coverage and grid, the synchronized `lib/constants` module, and the pinned CRS/transform. Pairs are 2023→2024 and 2024→2025, both in the diagnostic extension. The source is annual coverage, not the auxiliary pasture-age image. In particular **coverage code 1 is valid observed non-PAS**; pasture-age code semantics must not be imported here.

| State ID | Name | Definition at the endpoint |
|---|---|---|
| 0 | observed_PAS | Unmasked source code 15 |
| 1 | observed_nonPAS | Unmasked expected source code other than 15 or 27 |
| 2 | NODATA | Unmasked source code 27 |
| 3 | masked | Raw endpoint mask is zero, regardless of stored value |
| 4 | unexpected | Unmasked code outside the expected list, including 0 or −9999 |

These five IDs describe observation quality and PAS presence; they are **not** pasture-origin IDs. Masking takes precedence over numeric codes. `unmask(value, true)` fills masked pixels within the original endpoint footprint. The pair support is the intersection of endpoint footprints. Areas outside that support are not counted as masked pixels. All 25 pairs are exported, including zero cells, using the common support and the canonical reduction grid. A positive domain area is required for every cell/pair.

This convention is explicit rather than inferred from an unavailable legacy script. Before accepting the full result, the new domain-wide uncertain, entry and termination totals must reproduce the accepted boundary summary within **0.001 ha**. Any disagreement fails validation; investigate support/classification rather than silently changing the reference. The package contains exact, SHA-pinned copies of the accepted summary and its validation. This is an aggregate reproduction check, not a per-cell comparison to the old boundary exports or to a raster asset.

## Accounting and conditional interpretation

`pij_ha` is the area with previous state i and current state j. A valid pair has both endpoints in {0,1}. A pair is uncertain if **at least one endpoint is NODATA, masked or unexpected**. Thus `uncertain_pair_ha` is a quality descriptor of all coverage in the domain, not a PAS loss or pasture-origin uncertainty measure. The same pair area appears under entry and termination in the historical summary; **do not sum those duplicate values**.

The uncertain set has three disjoint parts:

1. `uncertain_previous_PAS_ha`: p02+p03+p04; previous endpoint observed PAS, current endpoint invalid.
2. `uncertain_current_PAS_ha`: p20+p30+p40; previous endpoint invalid, current endpoint observed PAS.
3. `uncertain_no_observed_PAS_ha`: remaining uncertain pairs; neither endpoint is observed PAS.

The third label says nothing about PAS in any other year or at an invalid endpoint. It cannot establish that these pixels were never pasture. The long cross-table distinguishes every invalid destination/origin, including NODATA→masked and unexpected→PAS. Confirmed entry is p10; confirmed termination is p01.

Conditional previous-PAS uncertainty divides its uncertain area by the sum of the entire previous-PAS row, including valid and invalid destinations. Current-PAS uncertainty analogously divides by the current-PAS column. A separate fraction divides the third part by all uncertain area. Fractions are 0–1, and zero denominators yield an empty field, not zero or one. National fractions use summed areas, never averages of cell fractions. Pilot summaries cover two cells only.

The ~4.69 Mha historical all-class uncertainty and 62.568807 ha unresolved pasture-origin conversion have different populations and time definitions. Their numerical contrast is not evidence that uncertain coverage almost never concerns PAS. The full cross-tab will quantify observed endpoint overlap; no such result is claimed before validation.

## Native and local assurance

Both scripts share the same classification engine. Native pilot exports include 34 synthetic cases: all 25 state combinations; valid source codes 1, 39, 26, 84 and 91; unexpected 0/−9999; and masked stored PAS/unexpected values. All are reduced together once on the canonical projection in a small test rectangle. Every case must have positive pixel support and zero state, cross-classification and partition errors. Counts are reduction-weighted **pixel equivalents**, not necessarily integers.

Every actual cell/pair also exports three independent counters: failure of the 25-way partition, disagreement with the Boolean legacy valid-pair definition, and failure of the three-way conditional partition. The second counter uses a separately expressed valid/invalid Boolean rule on raw filled codes; it is not an independent implementation of the unavailable old script. Every counter must equal zero exactly. Native projection metadata for all three years is checked against the fixed transform, along with the full annual band inventory and runtime constants.

Local checks exercise the exact extracted engine through a scalar adapter over 7,396 value/mask combinations, check pilot/full engine identity and fixture definitions, and test the file validator using synthetic temporary exports. They do not execute Earth Engine, spatial footprints, reprojection or reducers. Synthetic integration results are not included as scientific/native output. Native exports are supplied by the operator; validation does not independently witness their remote origin.

## Acceptance, provenance and immutability

Pilot: exactly 2 cells × 2 pairs = 4 rows, one manifest and one 34-row native fixture CSV. Full: 24,889 cells × 2 pairs = 49,778 rows split across eight canonical batches, one full manifest, and the exact accepted pilot native CSV. Full validation also requires the accepted pilot validation JSON, with matching config and fixture hashes. Extra CSVs, duplicate retries, missing cells, changed batch assignments, non-finite/negative metrics, malformed rows and changed metadata fail validation.

Per-cell area identities tolerate 0.01 ha; aggregate identities and accepted boundary-total comparisons tolerate 0.001 ha. Tolerances are absolute, not rounding promises. Full acceptance requires both native counters/fixtures and all historical aggregate controls. Pilot PASS is technical acceptance on two cells, not scientific closure of the domain-wide question.

The package pins supplied script bytes and hashes every input. A supplied code snapshot is not an executed-text hash. Until an explicit operator attestation is recorded separately, `executed_script_sha256` and operator attestation remain null. Existing v3 or other historical validations are not edited. Output files are additive and write-once; identical reruns are reusable, differing files are rejected before writing.

## Primary API references

- [Image.unmask](https://developers.google.com/earth-engine/apidocs/ee-image-unmask): explicit footprint behavior.
- [Image.mask](https://developers.google.com/earth-engine/apidocs/ee-image-mask): raw endpoint observation mask.
- [Image.reduceRegions](https://developers.google.com/earth-engine/apidocs/ee-image-reduceregions): fixed CRS/transform and reduction parameters.

See `RUN_UNCERTAIN_PAIRS_PT.md` for operator steps. No full-domain results or scientific conclusion are generated by preparing this implementation.
