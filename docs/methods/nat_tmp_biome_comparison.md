# NAT–TMP groups by primary biome: method

## Regional support

Use existing primary_biome labels Amazon/Cerrado. These regions are defined
before the comparison, not selected from observed peaks. Keep four exhaustive
fixed groups from maximum frozen NAT magnitude class during 1985–2020. Process
all eight intervals and flag 2020–2025; never use it to reassign groups.

## Main and sensitivity populations

Main scope all_cells includes every cell attributed to its primary biome.
Cross-biome = amazon_fraction_cell >0 AND cerrado_fraction_cell >0, using source
fractions, not a newly optimized threshold. Sensitivity single_biome_cells
excludes these cells but retains original groups/labels and recalculates both
numerators and denominators on the restricted population. A single-biome cell
may still include support outside the analyzed biomes. This comparison does not
allocate converted pixels exactly to biomes or infer counterfactual outcomes.

## Indicators and temporal support

For each scope × primary biome × fixed group × interval report cell count,
endpoint hectares, share of endpoint area in that scope/biome, hectares per cell,
initial-native-stock supported intensity, consolidation PAS→TMP, replenishment
NAT→PAS, aggregate index (sum C−sum R)/(sum C+sum R), and intermediate pasture
trajectory shares. Ratios use sums and missing values for zero denominators.
Native support requires initial stock >1e-9. Mixed index boundaries are inclusive
±1/3. Preserve separate counts/endpoint areas by frozen C–R cell state.

Sensitivity table reports removed cell-associated endpoint area, its fraction
of the main numerator, index differences and percentage-point differences in
group share. Share changes reflect removal from both group and biome denominator.

Summarize the two core sequences for primary7/full8 by region/group/scope:
changes, constant sequences and maximum consecutive same-state episode. Preserve
zero/inactive, existing censored-episode interpretation and typology. Do not
interpret long inactive episodes as active persistence or observed length as
uncensored lifetime. No clustering, significance or causal attribution.

## Validation and reproducibility

Authenticate eight GIS table hashes against upstream validation/manifest,
check provenance, balanced keys and population, stable spatial context and
area identities. Reuse class labels to avoid rounded-boundary reclassification.
Ensure biome/group and C–R partitions reproduce areas/cell counts, and fixed
groups agree with the accepted comparison. Numeric tolerance rtol 1e-10,
atol 1e-6 ha. The self-contained 09d script accepts --gis-zip and --output-dir;
dependencies pandas/NumPy/matplotlib/pyproj. No GEE rerun. Output tables carry
scope and diagnostic flags. Figure uses common vertical scales across biomes.
