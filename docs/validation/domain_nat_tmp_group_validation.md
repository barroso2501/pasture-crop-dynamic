# Domain NAT–TMP group comparison validation

- Date: 2026-09-15.
- Status: executed numerical comparison PASS; figures inspected.
- Script version: `phase4a-domain-nat-tmp-groups-v1`.
- Executed UTC: `2026-09-15T16:45:55.028503+00:00`.
- Script SHA-256: `45b4eb9ec678f9395d1e9ec1f08bd74c52b56c573c46bc9070ceaf1fe59487a0`.

## Input provenance and automated acceptance

Eight received 08c tables were authenticated against both the original export
validation and manifest; upstream metric and frozen-class hashes match accepted
Phase 4A provenance. Each table has 24,889 rows and 78 columns, unique text IDs,
and the expected interval and diagnostic flag. Archive CRC, stable spatial
context, finite nonnegative process areas, C+R/C−R identities and nested trajectory
areas passed. Transport ZIP bytes need not equal the earlier portable ZIP.

All 11 checks recorded in `domain_nat_group_validation_v1.json` passed:
exhaustive exclusive assignment of 24,889 cells; 199,112 balanced input records;
2,598 high-group cells; 106 diagnostic-only high cells; exact area partitions
within declared numeric tolerance; zero primary NAT activity in the no-occurrence
group; 99,556 sequence records; constant/interrupted episode engine examples;
and the corrected schema definition. Numeric identities allow relative 1e-10
and absolute 1e-6 ha tolerance for source CSV serialization.

Group counts: no_occurrence 11,213; maximum_low 4,887; maximum_moderate 6,191;
maximum_high 2,598. Diagnostic-only high counts: 4, 17 and 85 in the first three
groups respectively. The last interval does not change any primary assignment.

## Independent output review

All output hashes in the execution JSON were reproduced from delivered bytes.
The cell assignment table was reread with text IDs and has 24,889 unique records.
All schema column positions match headers and no CharacterSet option is present.
The 32 period rows partition both cells and domain area; shares sum to one.

All 99,556 reconstructed sequences were compared with the four accepted Phase 4A
GIS tables. Sequence values and five descriptors match exactly for every cell:
state changes, distinct states, maximum same-state episode length, its observed
years, and persistent episode count. No new typology code was generated.
Details and accepted component hashes are in the separate independent review JSON.
The original run validation was not changed to insert this later review.

The two final PNG figures were inspected for label readability and layout. No
live opening or join of the new table in ArcGIS is claimed. Numerical/schema
checks do not substitute for a future software interoperability check.

## Interpretation and status

Retrospective magnitude groups are not random samples, clusters or inferred
historical stages. Aggregate indexes differ from cell-state frequencies. Long
same-state episodes may be zero/inactive; observed durations do not estimate
uncensored episode lifetimes. Projected weighted cell centers approximate the
location of converted hectares; primary-biome associations do not allocate
pixels within mixed cells. No causal, spatial-significance or survival claim is
validated. 2020–2025 remains included and flagged.

This is a descriptive implementation following accepted Phase 4A. It does not
change decisions 009/010, refit classes or require GEE/upstream reruns. Results,
method and reusable script are ready for repository registration; no repository
synchronization has been performed here.
