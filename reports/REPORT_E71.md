# E71 lab notebook - GWTC-5 (O4b) out-of-sample: the curved chirp-mass law PASSES AGAIN (1.22 deg)

Prereg: preregs/E71_gwtc5_curved_law_prereg.md - locked and committed (d19a7a8) BEFORE any GWTC-5
file was opened. The prediction under test was placed on record in REPORT_E65 (GWTC-1/2.1/3 only)
and independently reconfirmed on GWTC-4/O4a in E67 (1.26 deg): *median |psi_curve - psi_meas| < 2 deg
for elongated events*. GWTC-5.0 O4b PE (Zenodo 20276106 Part 1 + 20348006 Part 2): 104 per-event
combined_PEDataRelease.hdf5 files, 52.84 GB; all 104 h5py-validated, zero corrupt, **zero dropped**
from analysis. This is the THIRD disjoint catalog (train GWTC-1/2.1/3 -> confirm O4a -> reconfirm O4b).

## Locked outcomes

| decision (locked, identical to E67) | threshold | outcome |
|---|---|---|
| **D1 - the on-record E65/E67 prediction** (elongated, axr>=3, n=32) | median < 2 deg | **PASS - 1.22 deg** |
| D2 - curve beats tangent, all 104 events | median smaller | PASS (5.41 vs 8.23 deg) |
| D3 - E40 tangent-law replication (descriptive) | - | replicates: 8.23 deg (GWTC-3 7.49; GWTC-4 9.36); wins 92/104 = 88% (81%; 86%); Spearman(err,axr) -0.69 (-0.42; -0.40) |

Disjointness (pre-committed check): O4b dates 240413-250119, all post-O4a (>240116); name-overlap with
the E67/O4a 86-event set = **0**; 12 events from the 2025 tail. Fully disjoint from every prior battery.

## Structural note (correcting an earlier overgeneralization)
GWTC-5 O4b PE is Bilby/RIFT via PESummary. The waveform group actually selected by the locked rule
("Mixed if present, else largest analysis") was: SEOBNRv5PHM x83, NRSur7dq4 x7, IMRPhenomXPHM-SpinTaylor
x5, IMRPhenomXPNR x4, **C00:Mixed x4, C01:Mixed x1**. So 5 of 104 events DO carry a combined "Mixed"
group (the rule correctly used it); the other 99 do not, and the rule fell back to the largest
single-waveform analysis. (An earlier note said GWTC-5 has "no Mixed group" - that was true of the
validation subset, not the full catalog; the locked rule handles both cases without modification.)

## What the elongated table shows
The curved law lands at 0.01-3.4 deg on the 32 elongated (axr>=3) events, while the tangent law carries
systematic 2-10 deg errors that the curvature term removes - e.g. GW250118_055802: tangent 9.72 -> curve
1.30; GW240530_012417: 6.89 -> 0.17; GW240622_004008: 6.75 -> 0.60; GW240601_231004: 6.35 -> 0.06;
GW240915_001357: 5.00 -> 0.01. Best single fits: GW240910_103535 (Mixed) 0.02, GW240915_001357 0.01,
GW240601_231004 0.06. The E65/E67 pattern (tangent error grows with arc length; curve absorbs it)
reproduces without any tuning - zero free parameters, each prediction using only the event's own median
source chirp mass and its q marginal. The err-vs-elongation Spearman (-0.69) is the strongest of the
three catalogs, i.e. O4b's more elongated events make the tangent's curvature deficit most visible.

## Waveform robustness (the one real difference from E67)
E67 used a homogeneous "Mixed" combination; here the largest-analysis pick varies per event. Checked on
GW241011_233834 (axr 17.3) and GW240910_103535 (axr 6.0): across all 3-4 waveform families the pick
shifts the ABSOLUTE orientation by ~3 deg, but psi_curve tracks psi_meas WITHIN each family (err_curve
stays 0.02-0.62 deg regardless of waveform). The curved law is therefore waveform-robust; the
heterogeneous picks do not threaten D1 (which measures the within-event curve-vs-meas agreement).

## Status of the law after E71
- E40 (GWTC-3, empirical): posterior lies along the constant-Mc TANGENT, ~7.5 deg.
- E65 (post-hoc diagnosis): the residuals are curvature; the posterior IS the constant-Mc CURVE.
- E67 (out-of-sample, locked, O4a): curved form CONFIRMED at 1.26 deg.
- **E71 (out-of-sample, locked, O4b): curved form RECONFIRMED at 1.22 deg on a third disjoint catalog.**

The (m1, m2) posterior geometry of GW events is the constant-chirp-mass curve at the event's measured
source Mc, extent set by the q marginal - now validated predictively across THREE independent catalogs
spanning the full GW catalog history. The E40 tangent law also replicates independently a third time
(88% wins, same elongation scaling). "Confirmed once" is now "reproducible law across catalogs."

## E72 seed (descriptive, post-hoc - NOT a decision)
The 10 largest curve residuals are ALL near-round events (axr 1.1-1.4, residuals up to 78 deg, masses
33-58 Msun, q~0.71-0.79) - the ill-defined-orientation regime the axr>=3 gate exists to exclude, not
law-breaking physics. Lesson for E72: a naive residual ranking merely re-finds round posteriors; the
outlier atlas must control for axr (rank within elongated events, or normalize by orientation
precision) before correlating residuals against precession/q/spin/waveform-disagreement.

## Verification (four legs, all pass)
- **Contract tests**: E65's 5 machinery tests (angle conventions, kappa limits, chord-arc mechanism)
  green; full suite 17/17.
- **Independent re-derivation**: D1 (1.22), D2 (5.410/8.230), n_elong=32, n=104 reproduced from the
  results JSON through a plain-numpy aggregation path - exact match.
- **Hand-recompute end-to-end**: GW241011_233834 recomputed from raw HDF5 via a DIFFERENT linear-algebra
  path (np.cov+np.linalg.eig for psi_meas; SVD for psi_curve, vs the scorer's eigh): psi_meas 164.11 and
  psi_curve 164.73 match the scorer to 0.004/0.002 deg.
- **Published-value / column-ID gate**: computed median masses reproduce the release's own
  PESummaryTable published medians for the matched analysis - exact for most events, <0.23 Msun (<0.6%)
  for 8 late-2024/2025 high-mass events (a within-analysis summary-vs-samples median nuance, matching
  the correct analysis in all cases). chirp_mass_source == Mc(m1,m2) per-sample on all 104 - column
  identity confirmed catalog-wide; mass_ratio<=1 (m2/m1) on all 104.

## Honesty / limits
- Heterogeneous waveform picks (no single "Mixed" for 99/104): shown waveform-robust above, but the
  absolute-orientation scatter (~3 deg across families) is larger than E67's homogeneous case; D1
  measures relative agreement and is unaffected.
- The largest curve residuals are round-posterior artifacts (axr~1), not physics; do not read them as
  law violations.
- Published summary medians differ from sample medians by <0.6% for a few late high-mass events (release
  versioning/reweighting); immaterial to the geometry, none in the elongated D1 set.
- Locked pick-then-check drops any event whose largest group lacks a mass column: 0/104 triggered.

Code: src/e71_gwtc5_curved_law.py. Numbers: results/e71_gwtc5_curved_law_results.json.
Data: data/chains/gwtc5/ (gitignored; Zenodo 20276106 + 20348006).
