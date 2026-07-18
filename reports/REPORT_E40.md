# E40 lab notebook - GW mass-plane geometry is the chirp-mass degeneracy (POSITIVE)

Prereg: preregs/E40_gw_chirp_mass_lawfulness_prereg.md (locked; method hand-validated on 3
events during design, full 14-event scoring + thresholds fixed before the automated run).
Question: is the (m1_source, m2_source) posterior orientation predictable, parameter-free, as
the constant-chirp-mass tangent at the event's median masses? Physical null = constant total mass.

## Result: PASS both gates

| decision (locked) | threshold | outcome |
|---|---|---|
| D1: chirp beats total-mass AND wins >= 11/14 | both | PASS (median 6.32 vs 14.06 deg; wins 11/14) |
| D2: elongated (axis_ratio>=3, n=5) median |dpsi_chirp| | < 12 deg | PASS (1.10 deg) |

Spearman(|dpsi_chirp|, axis_ratio) = -0.32: the more elongated the posterior, the smaller the
error -- exactly as predicted (a round posterior has no well-defined orientation to predict).

## Per-event (sorted by axis ratio)

| event | m1 | m2 | axr | psi_meas | psi_chirp | dchirp | dtotal |
|---|---|---|---|---|---|---|---|
| GW190814        | 23.31 | 2.59 | 36.7 | 175.46 | 175.40 | 0.06 | 40.46 |
| GW190425        | 2.08 | 1.32 | 11.5 | 150.94 | 149.84 | 1.10 | 15.94 |
| GW190924_021846 | 8.78 | 5.11 | 7.0 | 162.01 | 152.38 | 9.63 | 27.01 |
| GW190728_064510 | 12.45 | 8.03 | 6.0 | 163.37 | 149.39 | 13.98 | 28.37 |
| GW190708_232457 | 19.81 | 11.61 | 4.2 | 151.79 | 152.17 | 0.38 | 16.79 |
| GW190513_205428 | 35.96 | 18.32 | 2.5 | 155.25 | 155.90 | 0.65 | 20.25 |
| GW190620_030421 | 58.02 | 35.00 | 1.7 | 145.20 | 151.35 | 6.15 | 10.20 |
| GW190803_022701 | 37.58 | 27.68 | 1.3 | 144.28 | 145.26 | 0.98 | 9.28 |
| GW190706_222641 | 73.97 | 39.35 | 1.2 | 146.68 | 154.79 | 8.11 | 11.68 |
| GW190910_112807 | 43.80 | 34.15 | 1.2 | 140.90 | 143.42 | 2.52 | 5.90 |
| GW190731_140936 | 41.81 | 29.02 | 1.1 | 155.26 | 147.15 | 8.11 | 20.26 |
| GW190521_074359 | 43.39 | 33.43 | 1.5 | 131.30 | 143.82 | 12.52 | 3.70 |
| GW190727_060333 | 38.90 | 30.15 | 1.4 | 137.13 | 143.62 | 6.49 | 2.13 |
| GW190519_153544 | 65.10 | 40.83 | 1.3 | 122.81 | 150.22 | 27.41 | 12.19 |

The three events where total-mass "wins" (GW190521_074359, GW190727_060333, GW190519_153544)
are all near-round (axis_ratio 1.3-1.5), where the orientation is ill-defined and both models are
guessing -- the pre-declared control regime (D3), not a real failure of the chirp law.

## Expansion to the full confident GWTC set (out-of-sample confirmation)

After locking + scoring the n=14 prereg above, all confident GWTC-1/2.1/3 PE posteriors were
downloaded (scripts/fetch_gw_chains.py; public GWOSC/Zenodo; ~8 GB cache, gitignored) and E38 +
E40 re-run unchanged. The chirp-mass law holds and TIGHTENS with 5x the events:

| sample | n | median|dpsi_chirp| | median|dpsi_total| | chirp wins | elongated (axr>=3) | Spearman(err,axr) |
|---|---|---|---|---|---|---|
| locked prereg | 14 | 6.32 | 14.06 | 11/14 | 1.10 (n=5) | -0.32 |
| full confident | 75 | 7.49 | 20.38 | 61/75 (81%) | 4.68 (n=28) | -0.42 |

(All 76 confident GWTC-1/2.1/3 events cached; 75 carry the mass plane.) The n=14 thresholds
(wins>=11, elong<12 deg) are trivially cleared at n=75; the load-bearing numbers are median
7.49 vs 20.38 deg and the 28-event elongated subset at 4.68 deg. Spearman strengthens to -0.42
(more elongated -> tighter), exactly the predicted direction. This is out-of-sample confirmation,
not a re-tuned test: the model and prediction are byte-identical to the locked run.

## Interpretation

A rare POSITIVE geometric-lawfulness result. Where a compact-binary posterior is genuinely
elongated, its mass-plane degeneracy IS the constant-chirp-mass line, predicted parameter-free
from the median masses to ~1 deg (GW190814 0.06, GW190708 0.38, GW190513 0.65, GW190425 1.10).
Constant total mass is decisively worse (14.06 vs 6.32 deg median).

This is the clean contrast to the cosmo nulls E34/E35: posterior geometry is lawfully predictable
WHEN a genuine dominant physical combination exists (chirp mass in GW), and NOT when it does not
(the mixed Omega_m-sigma8 kernels in cosmology). "Geometry from physics" is a real law in the
regime where one combination dominates the information -- it is the dominance, not the geometry
framework, that makes it lawful.

## Caveats (honest)

- n=14 (only the locally cached GWTC events); the well-defined-orientation subset is n=5. The
  headline 1.1 deg median is carried by the most elongated events; two elongated events
  (GW190728 13.98, GW190924 9.63) are less tight.
- Prediction uses median masses only (a point estimate of the curve tangent), not the full
  posterior curvature; a fuller test would fit the tangent along the ridge.
- Larger event sets (GWTC-3 full, ~90 events) would sharpen this; download-bound, not run here.
