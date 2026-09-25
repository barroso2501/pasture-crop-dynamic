# Pixel-level diagnosis of pasture-age code `1`

**Version:** 2  
**Status:** validated diagnostic; source meaning still requires MapBiomas confirmation  
**Supersedes:** `canonical_unresolved_pasture_age_pixel_diagnostic_v1.md` for interpretation and future citation  
**Analytical treatment:** Decision 003 remains in force  
**Recommended repository path:** `docs/validation/canonical_unresolved_pasture_age_pixel_diagnostic_v2.md`

## 1. Purpose

This record resolves the project's internal diagnostic question about whether
pasture-age code `1` is a transient numerical age, a persistent unresolved
state, or another source-product behavior. It combines the complete annual
cell census with a native-pixel history for every pixel carrying code `1` at
least once from 1985 through 2025.

Version 2 adds two analyses that were incomplete in version 1:

- the duration, recurrence, and right-censoring of code-`1` episodes; and
- the broader boundary context of affected cells, distinguishing the
  Amazon-Cerrado boundary from boundaries between the target domain and other
  Brazilian biomes.

It does not assign an official semantic meaning to code `1`. Only MapBiomas can
confirm the production cause and intended legend.

## 2. Authenticated inputs

| File | Records | SHA-256 |
|---|---:|---|
| `canonical_unresolved_pasture_age_cell_year_v3.csv` | 9,510 cell-year rows | `19ee1ebc853cabd0f973da4147597b613c56ddb5a808dd12b59287c4e142a5e0` |
| `canonical_unresolved_pasture_age_pixel_history_v4.csv` | 24,692 pixels | `0172889cdd7e649c21e1a79ae8d44b16b7133854b578661ba1c199bc13153163` |

The pixel-history table contains 41 annual pasture-age states and 41 annual
coverage states for every sampled pixel, together with native-grid coordinates
and canonical cell identifiers.

The spatial contextualization additionally uses the accepted canonical spatial
support attributes and the canonical neighbor graph. The graph reconstructed
from the accepted cell centroids and 17-km threshold reproduces the stored
neighbor count for all 24,889 cells.

## 3. Validation

- 24,692 rows and 24,692 unique native-grid coordinates;
- no duplicated pixel coordinates;
- no missing annual age or coverage fields;
- every exported pixel carries code `1` in at least one year;
- one script version and one authenticated source-census hash;
- annual history counts equal the rounded area-weighted pixel equivalents in
  the cell-year census in all 41 years;
- the largest difference between an integer pixel count and the corresponding
  area-weighted cell total is 0.165 pixel equivalent.

The cell-year census identified 350 cells with a positive area-weighted
contribution. Pixel-center sampling assigned the affected pixels to 348 cells.
The two cells without a sampled pixel center (`14330`, `14339`) contain only
fractional boundary overlaps. Their accumulated contribution is 0.874 ha-year,
with a maximum annual contribution of 0.0505 ha. This is a geometric assignment
difference, not missing source pixels.

## 4. Decisive result

Across all 1,012,372 pixel-year states in the exported population:

| Pasture-age state | Coverage state | Pixel-years |
|---|---|---:|
| `1` | pasture class `15` | 531,062 |
| `1` | any state other than `15` | 0 |
| not `1` | pasture class `15` | 0 |
| not `1` | any state other than `15` | 481,310 |

Therefore:

```text
pasture_age == 1  ⇔  coverage == 15
```

This equivalence holds for every year and every one of the 24,692 affected
pixels. Within this population, the pasture-age asset contains only two values:

- `1` while the coverage product identifies pasture; and
- masked/absent (`-9999` after export filling) while the coverage product does
  not identify pasture.

No affected pixel contains code `100`, `201`, `202`, any other value above
`200`, or any other positive age code in any year.

## 5. Temporal behavior

The pixel histories contain 29,335 distinct code-`1` episodes:

- every episode begins with `masked → 1` in the age asset;
- every episode begins in the same year that coverage equals pasture class
  `15`;
- every completed episode ends with `1 → masked` when coverage leaves class
  `15`; and
- episodes continuing through 2025 are right-censored by the series endpoint.

There are no transitions from `1` to `202`, `100`, or any other numerical age
code. The hypothesis that `1` is a one-year pasture incorrectly stored in place
of `201` is therefore rejected for this population.

### 5.1 Persistence and recurrence

| Measure | Result |
|---|---:|
| Pixels carrying code `1` at least once | 24,692 |
| Code-`1` episodes | 29,335 |
| Code-`1` pixel-years | 531,062 |
| Pixels with an episode lasting at least 2 consecutive years | 24,457 (99.05%) |
| Pixels with an episode lasting at least 5 consecutive years | 22,379 (90.63%) |
| Pixels with an episode lasting at least 10 consecutive years | 19,193 (77.73%) |
| Pixels with an episode lasting at least 20 consecutive years | 13,983 (56.63%) |
| Mean longest episode | 20.62 years |
| Median total observed years with code `1` | 23 years |
| Maximum consecutive duration | 40 years |
| Pixels with the maximum 40-year episode | 319 |
| Pixels still carrying `1` in 2025 | 19,975 (80.90%) |
| Pixels continuously carrying `1` from first appearance through 2025 | 16,796 (68.02%) |
| Pixels with one uninterrupted episode | 20,717 (83.90%) |
| Pixels with two or more episodes | 3,975 (16.10%) |
| Maximum episodes observed for one pixel | 7 |

The same native-grid pixel can therefore remain at code `1` across several
five-year intervals and, in some cases, for almost the entire observable
series. This is incompatible with a correctly incrementing one-year age.

The multiple episodes are not changes among age codes. They mirror pasture
exit and re-entry in the coverage series: when a pixel leaves class `15`, the
age value becomes masked; when pasture returns, code `1` reappears without a
resolved numerical age.

## 6. Spatial behavior

### 6.1 Amazon-Cerrado boundary and other biome boundaries

Version 1 used `crosses_amazon_cerrado_boundary = false` as if it meant that a
cell was not transboundary. That interpretation was too broad. The field tests
only whether a cell overlaps both the Amazon and Cerrado target biomes; it does
not identify contact with Pantanal, Caatinga, Atlantic Forest, or other areas
outside the two-biome target domain.

The corrected cell classification is:

| Assignment basis | Amazon-Cerrado boundary | Other target-domain boundary | Interior to target domain | Total affected cells |
|---|---:|---:|---:|---:|
| Pixel-center assignment | 310 | 38 | 0 | 348 |
| Area-weighted cell census | 312 | 38 | 0 | 350 |

All 38 cells previously described as non-boundary have a positive fraction
outside the combined Amazon+Cerrado target domain. Of these cells, 37 have
Amazon as the primary biome and one has Cerrado as the primary biome. Their
outside-domain area fraction ranges from 0.0083 to 0.9780, with mean 0.4593 and
median 0.4743.

The earlier pixel-level stratum counts remain numerically correct but require
corrected labels:

| Primary biome and boundary stratum | Unique affected pixels | Code-`1` pixel-years | Pixels carrying `1` in 2025 |
|---|---:|---:|---:|
| Amazon, other target-domain boundary | 13,700 | 314,909 | 12,284 |
| Amazon, Amazon-Cerrado boundary | 5,312 | 111,600 | 3,859 |
| Cerrado, other target-domain boundary | 172 | 4,306 | 110 |
| Cerrado, Amazon-Cerrado boundary | 5,508 | 100,247 | 3,722 |

Therefore, every affected cell is associated with either the Amazon-Cerrado
boundary or another boundary of the target domain. No affected cell is a true
interior cell under the broader boundary definition.

The 37 primary-Amazon cells form one connected spatial component near
approximately 58°W and 16°S. Their location is consistent with the
Amazon-Pantanal contact, but confirmation requires overlay with the complete
official biome layer. The one primary-Cerrado cell forms a separate component;
its external biome also cannot be assigned from the two-biome layer alone.

### 6.2 Neighborhood structure of the 38 other-boundary cells

| Canonical neighbors per affected cell | Number of cells |
|---:|---:|
| 2 | 1 |
| 3 | 3 |
| 4 | 9 |
| 5 | 8 |
| 6 | 17 |

The 38 cells have a mean of 4.97 and a median of 5 canonical neighbors. Their
neighborhood structure contains:

- 189 neighbor incidences;
- 70 distinct neighboring cells when within-set neighbors are included;
- 33 distinct neighboring cells outside the set of 38;
- 64 internal undirected edges among the 38 cells; and
- two components: one connected block of 37 cells and one isolated affected
  cell.

This configuration demonstrates that the large concentration is not a set of
spatially independent anomalies. It is a compact, connected block associated
with a boundary of the target domain.

## 7. Interpretation

The observed behavior is incompatible with a numerical consecutive-age value.
For the affected pixels, code `1` is behaviorally identical to a binary
pasture-presence mask. The strongest working interpretation is therefore:

> In a small, spatially structured subset of the public pasture-age asset, the
> value `1` appears to preserve pasture membership but not pasture age.

The temporal evidence shows that this is not an isolated annual mismatch. The
same pixel can remain unresolved for decades, and the code can disappear and
return in exact agreement with pasture exit and re-entry. The spatial evidence
shows that all affected cells are boundary-associated under the broader domain
definition.

Together, these results support a spatial production artifact involving a
mask, mosaic, seam, regional module, tile, or biome-domain boundary. They do not
identify which operation generated the value. The phrase **binary
pasture-presence leakage** is therefore an appropriate diagnostic hypothesis,
but it must not be presented as an official source definition until MapBiomas
confirms it.

## 8. Consequence for the project

The accepted treatment is confirmed rather than changed:

- coverage class `15` remains authoritative for pasture membership;
- code `1` remains **pasture with unresolved age**;
- its area remains included in pasture stocks and land-cover flows;
- it remains excluded from age-attributable cohorts;
- it must not be recoded to `201` or any other numerical age; and
- accounting closure continues through the explicit unresolved-age component.

The anomaly remains negligible for aggregate conclusions: it represents less
than 0.001% of PAS-to-temporary-crop conversion in the accepted origin
partition. Its resolution matters for source provenance and exact cohort
attribution, not for the direction of the study's substantive findings.

## 9. Questions for MapBiomas

1. Is code `1` an intended sentinel for pasture without attributable age, or
   is it an unintended value in `pasture_age_v1`?
2. Can the production chain insert or preserve a binary pasture mask in the age
   mosaic for particular pixels, tiles, biome modules, overlaps, or seams?
3. Why do affected pixels remain `1` for as long as 40 consecutive years while
   coverage equals class `15`, without incrementing to `202`, `203`, and later
   values?
4. Why does code `1` disappear when a pixel leaves class `15` and reappear when
   pasture returns, still without an attributable age?
5. Are the affected blocks associated with boundaries between regional or
   biome production modules, including Amazon-Pantanal and other contacts?
6. Is there a corrected asset or an authoritative recoding rule planned for
   these pixels?
7. Can MapBiomas provide the complete official meaning and mask behavior for
   codes `0`, `1`, `100`, `101–200`, and values above `200`?

## 10. Suggested message to MapBiomas

> Fizemos uma auditoria anual, pixel a pixel, do valor `1` no asset público
> `mapbiomas_brazil_collection11_pasture_age_v1`. Foram identificados 24.692
> pixels com valor `1` ao menos uma vez entre 1985 e 2025. Nos 1.012.372 estados
> pixel-ano examinados, ocorreu uma equivalência perfeita: o produto de idade
> assume valor `1` exatamente quando o produto de cobertura assume classe `15`,
> e fica mascarado quando a cobertura deixa de ser pastagem. Não foi observada
> nenhuma transição `1→202`, `1→100` ou para qualquer outro código de idade. O
> mesmo pixel pode permanecer em `1` por até 40 anos consecutivos; 90,6% dos
> pixels afetados tiveram episódios de pelo menos cinco anos e 77,7%, de pelo
> menos dez anos. Quando a pastagem sai e posteriormente retorna, o valor `1`
> também pode reaparecer. Assim, nesses pixels, o valor `1` se comporta como uma
> máscara binária de presença de pastagem, e não como idade consecutiva. O
> padrão é integralmente associado a limites espaciais: 310 das 348 células com
> pixels atribuídos atravessam a fronteira Amazônia-Cerrado, enquanto as 38
> restantes ultrapassam o domínio combinado Amazônia+Cerrado e incluem um bloco
> conectado de 37 células próximo ao provável contato Amazônia-Pantanal.
> Poderiam confirmar o significado oficial do código `1` e verificar se esse
> comportamento pode resultar de mosaico, transferência de máscara, módulos
> regionais, limites de biomas ou tiles específicos?

## 11. Documentation action

This version supersedes version 1 for interpretation and future citation. The
version-1 file should remain in repository history and must not be silently
overwritten.

This record should be added as a validation supplement to Decision 003.
Decision 003 itself should not be rewritten as a resolved source definition.
If MapBiomas later provides an authoritative explanation or corrected asset, a
new decision should record the source response, required reprocessing, and
sensitivity comparison with the accepted unresolved-age treatment.

