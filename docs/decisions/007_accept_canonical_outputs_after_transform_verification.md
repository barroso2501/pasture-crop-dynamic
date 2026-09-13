# Acceptance of canonical outputs after native-transform verification

- **Status:** Accepted and implemented
- **Decision date:** 2026-09-12
- **Applies to:** Canonical Earth Engine stock-flow and trajectory outputs
- **Related plan:** `docs/planning/006_spatiotemporal_investigation_plan.md`
- **Validation record:**
  `docs/validation/runtime_configuration_and_native_transform.md`

## Context

An external repository audit identified a possible provenance ambiguity. The
`CRS_TRANSFORM` value in `config/constants.js` had been changed from a global
origin to the native origin of the MapBiomas Collection 11 `coverage_v3`
asset. The repository alone could not establish whether the accepted Earth
Engine outputs had been produced with the native transform or with the
superseded value.

Internal accounting closure could not resolve this question because a
spatially shifted computation can still close algebraically. The issue was
therefore treated as a provenance gate before spatial analysis.

## Decision

The existing canonical outputs remain accepted. The eight stock-flow
intervals and eight within-interval trajectory outputs will not be
reprocessed solely because of the `CRS_TRANSFORM` question.

This decision is based on two independent checks:

1. a runtime audit of the hosted Earth Engine constants module against the
   repository configuration and the native source projections; and
2. an explicit-native-transform replication of the accepted 2005-2010 `b00`
   stock-flow pilot, compared cell by cell with the original export.

## Evidence

The runtime audit confirmed:

- the final public Collection 11 coverage and pasture-age assets;
- the canonical 24,889-cell analytical grid;
- 24,889 distinct `cell_id` values;
- `EPSG:4326` as the runtime and source CRS;
- equality among the repository transform, hosted-module transform, and
  native coverage transform;
- 41 bands in each source product; and
- integer coverage-to-pasture-age lattice offsets of 76 pixels in X and 2,205
  pixels in Y.

All 20 runtime checks passed. The controlled `b00` replication produced
3,168 rows and 90 columns. All identifiers, seven metadata fields, and 82
numeric fields matched the accepted pilot exactly. The maximum numerical
difference was `0.0` ha, and the two CSV files had the same SHA-256:

```text
bad0505b70a8ed1c408edc8290d5e9c5dfca22913edd8d0447db1c12112b1636
```

## Consequences

- The configuration-provenance gate in Phase 0 is closed.
- The canonical integrated panel remains the accepted input for spatial
  analysis.
- No upstream result is changed by this decision.
- Phase 1 of the approved spatiotemporal investigation may begin.
- Future Earth Engine production runs must record the hosted configuration
  before execution and must use an explicit CRS and affine transform or a
  verified version-controlled constants module.

## Scope

This decision establishes computational provenance and spatial-lattice
consistency. It does not validate the thematic accuracy of MapBiomas classes,
resolve pasture-age code `1`, or change the diagnostic status of the
2020-2025 interval.
