# Corrected origin of PAS→temporary-crop conversion

**Research question 2:** among endpoint conversions from pasture (PAS) at the
start of a five-year interval to temporary crops at its end, how much came
from a pasture episode continuous since 1985, an episode with observed entry
after 1985, or an episode whose origin cannot be attributed?

The annual coverage sequence corrects the source-age asset's reuse of `100`
after an observed departure from pasture. Area totals for the PAS→temporary-
crop endpoint flow remain the same; the corrected result reallocates origin.

| Observed window | Old `100`/censored share | Reconstructed continuous-1985 share | Reconstructed post-1985 entry share | Unresolved share | Change in initial share |
|---|---:|---:|---:|---:|---:|
| Primary 1985–2020 | 51.73% | **46.91%** | **53.09%** | 0.00031% | −4.82 percentage points |
| Full observed 1985–2025 | 49.71% | **44.39%** | **55.61%** | 0.00032% | −5.32 percentage points |

The primary-window PAS→temporary-crop area is **20,119,468.10 ha**. The
crosswalk directly moves **969,747.77 ha** from the old censored category to
observed post-1985 entry. The full observed window totals **22,205,794.85
ha**, with **1,181,114.17 ha** in the same direct transfer. Other small
cross-category changes exist, so the direct transfer is not by itself the
complete net change of every category. Values are area-weighted sums of
endpoint transitions over intervals; they do not represent unique hectares
converted only once across the entire series.

The primary interpretation changes: post-1985 observed pasture episodes
account for a modest majority of PAS→temporary-crop endpoint conversion.
The 2020–2025 interval supports the same direction but is explicitly marked
as diagnostic; it is included in the full-observed window and does not set
the primary-window conclusion. The first interval, 1985–1990, necessarily
assigns all attributable PAS at t0 to the initial episode.

These are **episodes of PAS at t0**, not memberships in the fixed set of pixels
that were PAS in 1985. A pixel may remain a member of that fixed RQ1 cohort
while its later PAS episode is classified as a post-1985 entry. The endpoint
flow also does not establish the exact year of transition within a quinquennium.

The exact values, interval breakdown and old-to-new matrices are in
`outputs/validation/pasture_age_remediation_v1/canonical_pas_tmp_origin_series_reassessment_validation_v1.json`
and the companion CSV. Manuscript evidence identifiers P9A035–P9A037
remain suspended pending their separately recorded review and replacement.
