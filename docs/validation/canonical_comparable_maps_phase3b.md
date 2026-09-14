# Canonical comparable maps: Phase 3B validation

- **Status:** PASS; computational map production accepted
- **Map product version:** `canonical-comparable-interval-maps-v1`
- **Class version:** `canonical-comparable-map-classes-v2`
- **Final script version:** `phase3b-comparable-interval-maps-script-v3`
- **Final script:** `analysis/08b_build_comparable_interval_maps_v3.py`
- **Script SHA-256:** `ceacb43641ab18183812cc462db8b8fccf740b0e75d7988b968ce4bc0260fb5c`
- **Validation record:** `canonical_comparable_maps_validation_v1.json`
- **Validation-record SHA-256:** `c7e8a3d4df68615d058b1e1935fe1bd57a8a22884920b61853bf1acca9d769cc`

## Scope

Phase 3B reproduced the 12 frozen Phase 3A classifications for all eight
intervals and rendered one comparable multi-panel map per metric in PNG and
SVG. The output contains 199,112 cell-interval classifications for 24,889
cells. The diagnostic interval 2020-2025 was mapped with the frozen limits but
did not influence their estimation.

## Corrective revisions

Two failed attempts were informative and are retained as implementation
provenance:

1. The first script expected the stored support geometry to already use the
   projected Albers CRS. The input was actually stored in WGS 84, so the run
   stopped before acceptance.
2. The second revision explicitly reprojected WGS 84 geometry to the project
   Albers CRS, but attempted to reproduce accepted class counts using rounded
   break values from the display CSV. Values close to class boundaries caused
   a count mismatch, and the validation stopped.
3. The accepted third revision preserved the reprojection fix and used the
   full-precision break values authenticated in the Phase 3A validation JSON.
   Reproduced class counts then matched Phase 3A exactly.

No accepted class boundary was changed by these revisions. They corrected the
cartographic CRS handling and the numerical source used to reproduce already
accepted classes.

## Acceptance evidence

The machine-readable validation record reports PASS for all required checks,
including:

- authenticated Phase 2 and Phase 3A inputs;
- balanced and unique panel keys;
- exact spatial-to-panel cell-population agreement;
- valid geometry after projection to the project Albers CRS;
- area reconciliation within the prescribed tolerance;
- one frozen limit record for each of 12 metrics;
- exclusion of 2020-2025 from limit fitting;
- no recalculation of class limits;
- exact reproduction of all Phase 3A class counts;
- complete class populations for every metric and interval;
- fixed colors for every class label;
- creation and readability of all 12 PNG maps;
- creation and parseability of all 12 SVG maps; and
- a complete map inventory.

The subsequent GIS-table exporter independently required this Phase 3B
validation record to have `PASS` status, all checks equal to true, the expected
map product and class versions, and a matching classified-panel hash before it
would create any interval table. That downstream gate also passed.

## Acceptance decision

Phase 3B is accepted as a reproducible computational and classification
product. Small later cartographic refinements may improve publication layout,
but they must not alter class membership, fixed colors, interval comparability,
or the diagnostic label for 2020-2025.

Spatial interpretation is not declared complete by this validation. The maps
now provide the fixed descriptive basis for Phase 4 cell-trajectory analysis
and the later spatial-autocorrelation phases.

