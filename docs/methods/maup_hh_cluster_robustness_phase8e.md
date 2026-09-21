# Phase 8E method — broad HH-cluster robustness

## Analytical sequence

Phase 8E follows the accepted alternative-grid Global Moran analysis. It uses
the same five focal metrics, three alternative grids, fixed support threshold
and eight five-year intervals. It does not rerun Earth Engine or recompute the
Phase 8B process metrics.

## Inputs

The script authenticates:

- canonical Phase 6 cell-level Local Moran results;
- canonical Phase 1 spatial geometries;
- the Phase 8B alternative metric panel;
- the three Phase 8A alternative-grid geometry files.

The canonical LISA classes remain the accepted Phase 6 raw-area results. On
the complete, nearly equal-area canonical lattice, positive density rescaling
does not change the intended high-versus-low interpretation. Alternative
area-valued metrics use density per 10,000 ha of raster-domain support so that
partial boundary support is not interpreted as low intensity.

## Alternative Local Moran

Shared-edge neighbors are reconstructed from axial coordinates. Conditional
C-R balance support induces a subgraph before row standardization. Each map is
computed with `esda.Moran_Local`, 9,999 conditional permutations, a stable
seed, zero island weight and GeoDa-disabled quadrant coding matching the Phase
6 convention.

BH and BY q-values are calculated only over tested, non-island cells within
each grid × metric × interval family. Complete checkpoint Parquets preserve
the statistics, p-values, q-values, quadrants and classifications.

## Spatial crosswalk

For each alternative grid, the supported polygons are intersected with the
canonical polygons in the project Albers equal-area CRS. Each crosswalk row
records canonical cell, alternative cell and overlap area. Crosswalk closure
is checked against the Phase 8A domain-intersection area and cached for reuse.

Comparisons use shared support within each canonical–alternative pair. This
prevents excluded low-support boundary cells from being counted as genuine
absence of an HH cluster.

## Location and persistence statistics

For each interval, intersection and union of the canonical and alternative HH
footprints are accumulated from crosswalk areas. Jaccard, overlap coefficient,
canonical capture and alternative precision follow directly.

For temporal comparison, HH occurrence counts and maximum runs are calculated
for the seven-interval primary and eight-interval full-observed windows.
Alternative frequencies are projected to canonical cells using overlap-area
weights. Weighted Spearman correlation measures agreement in recurrence;
persistent-HH footprints use the same area-overlap metrics as interval maps.

## Pilot and production

The pilot executes the complete production logic for:

```text
grid: hex20k_shift
metric: nat_tmp_density_per_10kha
interval: 2005–2010
permutations: 9,999
```

It also constructs and validates the shifted-grid crosswalk. The full run
reuses that statistical checkpoint and crosswalk, then completes the remaining
119 maps. A failed or interrupted full run can be resumed without recomputing
valid checkpoints.

## Outputs

The full stage produces:

- three alternative-grid cell-result Parquets;
- 240 interval footprint comparisons: BH and BY;
- 60 temporal persistence comparisons: BH and BY;
- 30 primary metric-grid-window robustness assessments;
- class-count summaries;
- three comparison figures;
- validation JSON and inventory.

The large cell-result Parquets and checkpoints may remain outside GitHub.
Compact comparison tables, figures, decision, method and validation records
are repository products after execution review.

