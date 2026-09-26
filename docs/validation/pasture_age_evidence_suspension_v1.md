# Pasture-age evidence suspension — pre-implementation status

## Status

**Accepted governance record; not a computational validation report.**

This document records the immediate consequence of Decision 024 while the
observed pasture-spell reconstruction and corrected PAS→temporary-crop origin
partition are pending implementation.

## Suspended findings

| Finding | Status | Reason |
|---|---|---|
| `P9A035` | Suspended | Depends on PAS→TMP origin attribution derived directly from the public pasture-age asset |
| `P9A036` | Suspended | Depends on the temporal comparison of that source-based origin partition |
| `P9A037` | Suspended | Depends on the source-based unresolved/unattributed origin component |

These findings must not be used in manuscripts, abstracts, presentations,
releases, or public claims as accepted results while suspension is active.

## What is not suspended

The source anomaly does not by itself invalidate:

- annual coverage classifications;
- total class stocks;
- total PAS→TMP or PAS→NAT endpoint area;
- NAT→PAS replenishment;
- NAT→TMP endpoint transitions and within-interval pathways;
- consolidation–replenishment balance; or
- spatial analyses based only on non-origin fields.

Those products remain subject to a formal invariance check during remediation.
If that gate fails, the affected downstream scope will be expanded explicitly.

## Rescission rule

Suspension may be rescinded only after:

1. the temporal state engine passes all synthetic tests;
2. the 2015–2020 pilot passes origin, destination, and observation-loss closure;
3. the full eight-interval run passes the Decision 024 acceptance criteria;
4. non-origin fields pass the downstream invariance gate or affected phases are
   reprocessed;
5. corrected RQ2 evidence rows and figures are regenerated; and
6. the validating artifacts and hashes are registered.

Rescission must be recorded in a new version of the structured event file and
must cite the relevant validation record. The present event file is immutable.

## Pending validation records

The following documents do not yet exist because no corrected execution has
been accepted:

```text
docs/validation/canonical_pasture_spell_age_validation_v1.md
docs/validation/pasture_age_source_asset_impact_audit_v1.md
```

They must not be created as placeholders claiming `PASS`.
