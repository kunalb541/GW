# E16 — Complete H0-axis map: every independent H0 instrument (incl. real GW posterior)

**Locked:** before `src/e16_h0_axis.py` is run. **Builds on:** E10 (JWST), E13.

## Data (all H0 instruments; GW as a REAL combined posterior we compute)
CMB Planck 67.36+/-0.54; DESI+CMB chain ~67.0; cosmic chronometers (repo fit) ~67.8+/-3;
GW dark-siren GWTC-3 combined 69.3+/-12.9 (computed from the LVK gwcosmo per-event H0
posteriors, fiducial population, 46 events); JWST-CCHP TRGB 68.81+/-2.22, JAGB 67.80+/-2.72,
combined 69.96+/-1.53; TDCOSMO 2025 71.6+/-3.6; SH0ES 73.04+/-1.04.

## Method
Place every anchor on the H0 value axis; tension (sigma) vs the CMB/early value; tag each
rd-free/ladder-free vs standard-ruler. Classify the tension structure.

## Locked outcome rule
| Outcome | Trigger | Reading |
|---|---|---|
| **(SH0ES-outlier)** | all non-SH0ES anchors within 2.5 sigma of CMB AND SH0ES > 2.5 sigma | the H0 tension is SH0ES-specific; the independent instruments (GW, JWST, chronometers, TDCOSMO) cluster near the early value. |
| **(broad-tension)** | multiple anchors > 2.5 sigma from CMB | a broad late-vs-early excess. |
| **(concordant)** | all within 2.5 sigma | no significant tension. |

## Controls
GW posterior recomputed from the public per-event data (not a literature quote). Report
each anchor's tension + rd-free tag. Descriptive.

## Date
Locked 2026-06-24, before src/e16_h0_axis.py is run.
