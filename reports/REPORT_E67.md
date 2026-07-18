# E67 lab notebook - GWTC-4 out-of-sample: the curved chirp-mass law PASSES (1.26 deg)

Prereg: preregs/E67_gwtc4_curved_law_prereg.md - locked and pushed BEFORE any GWTC-4 file was
opened. The prediction under test was placed on record in REPORT_E65 (commit 8d09cbf), derived
exclusively from GWTC-1/2.1/3 events: *median |psi_curve - psi_meas| < 2 deg for elongated O4a
events*. GWTC-4.0 (Zenodo 16053484): 86 O4a events, one combined_PEDataRelease.hdf5 each (14.6 GB;
7 throttle-dropped files re-fetched; all 86 h5py-validated, zero corrupt, zero dropped from
analysis). Dataset per event: the catalog's Mixed samples (largest if several variants), per the
locked preference; recorded per event in the results JSON.

## Locked outcomes

| decision (locked) | threshold | outcome |
|---|---|---|
| **D1 - the on-record E65 prediction** (elongated, axr>=3, n=19) | median < 2 deg | **PASS - 1.26 deg** |
| D2 - curved beats tangent, all 86 events | median smaller | PASS (7.53 vs 9.36 deg) |
| D3 - E40 tangent-law replication (descriptive) | - | replicates: 9.36 deg (GWTC-3: 7.49); wins 86% (81%); Spearman(err,axr) -0.40 (-0.42) |

## What the elongated table shows

The curved law lands at 0.2-3.3 deg on 18 of 19 elongated events (one outlier: GW231118_005626 at
6.2 deg, axr=3.1, borderline-round), while the tangent law carries systematic 4-11 deg errors that
the curvature term removes almost exactly - e.g. GW231118_090602: tangent 10.73 -> curve 0.54;
GW231020_142947: 7.97 -> 0.20; GW230529 (the mass-gap merger): 2.94 -> 0.29. The pattern from E65
(tangent error grows with arc length; curve absorbs it) reproduces without any tuning - the law has
no free parameters at all (each prediction uses only the event's own median source chirp mass and
its q marginal).

## Status of the law after E67

- E40 (GWTC-3, empirical): posterior lies along the constant-Mc TANGENT, ~7.5 deg.
- E65 (post-hoc diagnosis): the residuals are curvature; the posterior IS the constant-Mc CURVE.
- E67 (out-of-sample, locked): the curved form CONFIRMED on a disjoint catalog at 1.26 deg.

The E65 finding is hereby promoted from "post-hoc" to "out-of-sample confirmed": the (m1, m2)
posterior geometry of GW events is the constant-chirp-mass curve at the event's measured Mc, with
extent set by the q marginal - measurement optics, now validated predictively across catalogs.
The E40 tangent law also replicates independently (86% wins, same elongation scaling), closing the
loop on the whole mass-plane geometry program.

## Verification

Headline numbers re-derived from the results JSON through an independent aggregation path (D1
1.26, D2 7.525/9.355 - exact match) and one event (GW231020_142947) recomputed end-to-end by hand
from the raw HDF5 (psi_meas 159.57, psi_curve 159.77 - exact match). Machinery contract tests are
E65's 5 (angle conventions, kappa limits, chord-arc mechanism) - unchanged and green.

Code: src/e67_gwtc4_curved_law.py. Numbers: results/e67_gwtc4_curved_law_results.json.
Data: data/chains/gwtc4/ (gitignored; Zenodo 16053484).
