# Phase 4 temporal synthesis validation

Date: 2026-09-15. Status: executed PASS; independent output review PASS.
Version: `phase4-temporal-synthesis-v1`. Executed UTC: `2026-09-15T17:49:46.591852+00:00`.
Script SHA-256: `904359581e5a334127592d31df5bb6124ad27ccd7578e8a86f4a122e4008ef7b`.

## Inputs and numerical acceptance

The eight 08c metric/class CSVs are authenticated against accepted source
validation/manifest and upstream panel hashes. Four accepted core trajectory
GIS tables have unique complete cell populations, retained component hashes
and sequences verified against every frozen cell-interval state. Episode
counts/maxima and constant code/flag equivalence passed. Accepted activity and
reversal descriptors are reused rather than redefined.

All 9 recorded synthesis checks pass: 99,556 cell/axis/window
sequences, 647,114 consecutive transition records across overlapping windows,
746,670 observed interval records partitioned into 227231 episodes,
all fixed groups and primary biomes, primary/full windows, and 2,598 unique
high-group late-state flags. These counts include overlap between windows and
are not independent unique transition/interval samples.

## Independent review

Every recorded execution output hash matches delivered bytes. Reread episode
records partition seven/eight intervals per sequence, observed years equal
five times interval count, persistent flags exactly indicate ≥2 intervals,
and every sequence has one episode flagged at each observation boundary.
Dated transition counts sum to the expected population; pooled row fractions
sum to one for each observed origin. GIS late flags have unique text cell IDs.
Diagnostic follow-up of late-persistent cells was reconstructed from complete
terminal episodes and recorded in `temporal_synthesis_independent_review_v1.json`.

The final transition-matrix figure was inspected. No live ArcGIS opening test,
repository synchronization, statistical significance, survival or causal claim
is asserted. Source CSV serialization tolerance remains rtol 1e-10/atol 1e-6 ha.

## Scope and interpretation

Same-state duration includes substantive zero/inactive states; active-persistent
flags exclude those states. Boundary-censored observed durations do not estimate
uncensored lifetimes. Pooled matrices repeat cells across dates; primary/full
windows overlap. Direct/mediated reversal cell counts may overlap; any-reversal
counts use their union. Retrospective fixed groups and whole-cell primary-biome
attribution retain qualifications from preceding analyses. Removing top-flow
cells is a descriptive altered-population sensitivity, not confidence or causal
analysis. Existing decisions, 12-axis Phase 4A products and typology are preserved.

The core temporal analysis is completed and ready for registration; this record
does not itself update the investigation plan or certify downstream spatial
inference. No upstream rerun is required.
