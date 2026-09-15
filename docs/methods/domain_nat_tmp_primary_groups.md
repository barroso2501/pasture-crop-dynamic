# Fixed primary NAT–TMP magnitude groups

## Scope and inputs

Descriptive extension of Phase 4A across all 24,889 cells and eight five-year
intervals. Use authenticated GIS 08c CSVs and frozen class labels. Primary window:
1985–2020; observed complete window: 1985–2025. Include and flag 2020–2025, without
using it to define or expand primary groups. No thresholds are refitted.

## Assignment

Map zero/positive_low/positive_moderate/positive_high to 0/1/2/3. Compute each
cell's maximum rank over the seven primary intervals; assign no_occurrence,
maximum_low, maximum_moderate or maximum_high accordingly. These are fixed,
mutually exclusive, exhaustive retrospective groups, not each interval's states.
The maximum_high group equals the previously accepted 2,598-cell cohort.
Unknown or missing states must stop execution rather than imply zero.

Diagnostic-only high = full observed last interval high AND primary maximum <3.
This flag does not change the primary group. New positive diagnostic occurrence
is a separate condition and includes ranks 1–3.

## Aggregations

For each group and interval sum NAT endpoint, C=PAS→TMP, R=NAT→PAS and initial
stocks. Area share = group NAT area / domain NAT area. Mean endpoint hectares per
group cell includes zero-area cells. Supported native intensity = sum NAT area /
sum initial native stock over cells with stock >1e-9; report valid cell count and
excluded numerator area. This is a pooled ratio, not a mean of cell rates or an
annual probability. Aggregate C–R index = (sum C−sum R)/(sum C+sum R), undefined
at zero gross activity. Mixed boundaries are inclusive −1/3 and +1/3.

Report cell counts and NAT areas associated with each frozen C–R state. These
are distinct denominators. Pasture-trajectory shares use ratios of summed
trajectory areas to endpoint areas; no cell-level low-support exclusion is
applied to aggregate accounting. Zero denominators produce missing values.
Primary-biome grouping assigns whole-cell area by its label, not exact within-
biome converted-pixel area. Pooled interval areas are not unique-pixel totals.

## Temporal descriptors

For the two core classified axes and each primary7/full8 window, retain sequence,
state changes, distinct states, consecutive same-state episodes, maximum episode
length and its observed duration (5 × intervals), and persistent episodes (≥2).
Count positive and high intervals for NAT magnitude. Zero/inactive episodes are
valid episodes; maximum episode length is not necessarily active duration.
Compare reconstructed descriptors with accepted Phase 4A GIS products. Preserve
the existing typology and censoring rules; do not generate a new pattern code.

## Spatial descriptors

Project cell geographic centroids to the project's custom Albers equal-area CRS
(central longitude −60, origin latitude −32, standard parallels −5/−42, GRS80).
For each positive-area group/interval calculate endpoint-weighted mean x/y and
weighted RMS distance to that mean. Transform means to EPSG:4326. Zero endpoint
area means undefined weighted center. These are cell-center proxies, not exact
converted-pixel centers. The categorical overview uses geographic coordinates,
not polygon support or a formal cluster test.

## Provenance, GIS and reproduction

Authenticate archive CRC, per-component hashes against the export validation and
manifest, upstream metric/class hashes, keys, population and stable spatial context.
Do not reclassify rounded CSV numbers at frozen ties. Numeric identities allow
rtol 1e-10 and atol 1e-6 ha. Run the self-contained 09c script with --gis-zip and
--output-dir; dependencies: pandas, NumPy, matplotlib and pyproj. No GEE rerun.

The cell assignment table supports 1:1 joins by text cell_id. Keep its schema.ini
beside it, preserve filename/column order, and omit the unsupported CharacterSet
option. Do not claim live ArcGIS interoperability until actually retested.
