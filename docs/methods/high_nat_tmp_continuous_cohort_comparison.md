# Continuous-area comparison of the fixed high NAT–TMP cohort

- **Date:** 2026-09-15.
- **Script:** `analysis/09b_compare_high_nat_tmp_continuous_areas.py`.
- **Version:** `phase4a-high-nat-tmp-continuous-v1`.
- **Status:** Executed descriptive extension of accepted Phase 4A products.

## Selection and input identities

Read the eight accepted GIS 08c tables with text identifiers and round-trip
floating-point parsing. Authenticate each table, manifest and field dictionary
against the received validation JSON. Match the upstream metrics and class
hashes to those accepted in Phase 4A. The source CSVs have 15 significant-digit
serialization, so metric identities use relative tolerance 1e-10 and absolute
area tolerance 1e-6 ha. Preserve the frozen class labels rather than
reclassifying rounded continuous values at ties.

Select the union of cell IDs with `nat_tmp_endpoint_ha__class = positive_high`
in any of the seven primary intervals: exactly 2,598 cells. Keep membership
fixed in all eight intervals, including flagged 2020–2025. All-domain totals
use the full 24,889-cell population for each interval. No limits, stages,
historical phases or clusters are fitted.

## Areas, denominators and composition

Sum cell-level endpoint, consolidation and replenishment areas by interval.
The cohort share of domain endpoint area is the ratio of corresponding sums.
The aggregate C–R balance is `(sum(C)-sum(R))/(sum(C)+sum(R))`; it is not the
mean cell index or an endpoint-area-weighted index. Positive values indicate
C exceeds R; the 2:1 dominance boundaries remain ±1/3.

Group endpoint area by existing cell C–R class as a separate measure. It
quantifies where endpoint area is associated with each balance state and does
not assign endpoint area to the constituent C or R flows.

Intermediate-pasture shares are sums of detected trajectory areas divided by
summed endpoint area, for any pasture and for two consecutive pasture years.
They include all valid absolute flows, retaining low endpoint supports. The
Phase 3 support filter is for interpreting individual share classes and does
not remove areas from this pooled accounting. Verify the nested inequalities
consecutive-two-year pasture <= any pasture <= endpoint.

For initial-native exposure, retain only cells with stock greater than the
accepted 1e-9-ha tolerance and divide supported endpoint area by their summed
initial stock. This is a ratio of sums, not a mean of rates or an annual hazard.

Time-pooled areas sum interval-level transitions without deduplicating pixels;
repeated process occurrence may count again. Lack of detected pasture is not
proof of a direct conversion pathway.

## Spatial proxy

Use the accepted geographic cell-centroid coordinates, transform them to the
predefined project Albers CRS and average projected X/Y with endpoint-hectare
weights. The CRS is:

```text
+proj=aea +lat_0=-32 +lon_0=-60 +lat_1=-5 +lat_2=-42
+x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs
```

Inverse-transform the weighted center to geographic coordinates for display.
Successive distances use geodesics on GRS 1980. Weighted RMS distance from the
projected center is an additional descriptive spread measure in kilometers.
The result approximates an area center by allocating weights to cell centroids;
it is not the exact centroid of converted pixels. The path is a change in
weights within a fixed set, not tracking parcels or demonstrating front motion.

Biomes use existing primary-cell labels. Areas associated with mixed cells are
not split by where the conversion occurred inside the polygon; do not report
these proxy groupings as exact within-biome pixel totals. No administrative
boundaries or formal spatial-significance tests are used.

## Visualization, outputs and reproduction

Maps use the same geographic extent and logarithmic area color scale across
all eight intervals. Red diamonds show the weighted cell-centroid proxy.
2020–2025 is marked in every period output and graph.

The script writes the selected cell-interval table, eight unique-cell GIS
CSVs, a compatible field schema without the unsupported CharacterSet option,
period sums, primary-biome sums, C–R-state endpoint areas, center GeoJSON,
three scientific PNGs and a JSON provenance/validation record.

```bash
python analysis/09b_compare_high_nat_tmp_continuous_areas.py --gis-zip GIS.zip --output-dir OUTPUT
```

Python dependencies: numpy, pandas, matplotlib, pyproj. This comparison runs
locally from the received tables and does not require a canonical Colab or GEE
rerun. The interpretation is recorded separately in
`docs/analysis/high_nat_tmp_continuous_comparison_v1.md`.
