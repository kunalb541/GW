# E65 preregistration — deriving the E40 law from PN Fisher geometry: the mass-plane ROTATION law (LOCKED 2026-07-16)

**Question.** E40 established empirically that the (m1,m2) posterior orientation follows the
constant-chirp-mass tangent (median |Δψ| 7.5° on 75 events). But its own residual table shows
structure: the events where the law fails and constant-TOTAL-mass wins are the *heavy* systems
(GW190519, GW190521_074359, GW190727). E65 tests whether the whole pattern — law + failures — is
derivable from the Fisher geometry of the waveform: chirp-mass information accumulates over inspiral
cycles in band; heavy (merger-dominated) systems instead measure the total mass (which sets the
merger/ringdown frequency scale). Prediction: the posterior long axis **rotates from the constant-Mc
tangent toward the constant-Mtot tangent as detector-frame total mass grows**, at a rate set by the
inspiral-vs-merger information ratio computed from the detector PSD.

## Model (locked)
Two-direction Fisher mixture at each event's median masses (detector frame for the weights,
angles evaluated in the source-frame (m1,m2) plane — angles are invariant under the common (1+z)
rescaling):
- u_c = unit normal to the constant-Mc curve at (m1,m2); u_t = unit normal to constant-Mtot.
- C⁻¹ ∝ W_c·u_c u_cᵀ + κ·W_t·u_t u_tᵀ ; ψ_pred = long axis of C.
- W_c = 0PN phase Fisher on ln Mc integrated over the inspiral band:
  W_c = ∫_{20Hz}^{f_ISCO} [ (5/3)·(3/128)(π Mc_det f)^(-5/3) ]² · f^(-7/3) / S_n(f) df,
  f_ISCO = 4397 Hz / (Mtot_det/M☉).
- W_t = merger-band SNR²: W_t = ∫_{f_ISCO}^{min(4·f_ISCO, 1024Hz)} f^(-7/3)/S_n(f) df
  (crude but locked; the merger measures a frequency scale ∝ 1/Mtot).
- S_n(f): analytic aLIGO fit (Ajith 2011): S = 1e-49·[x^(-4.14) − 5x^(-2) + 111(1−x²+x⁴/2)/(1+x²/2)],
  x = f/215 Hz — an approximation to the real O3 PSD, adequate for a *ratio* of weights; recorded.
- κ: ONE global dimensionless calibration constant (the crude W_t normalization), fit by minimizing
  median |ψ_pred − ψ_meas| on the **14 locked E40-prereg events ONLY**, then frozen.

## Data
results/e40_gw_chirp_mass_lawfulness_results.json (per-event ψ_meas, ψ_chirp, ψ_total, source
masses, axis ratio — unchanged) + local PE files for median detector-frame masses and Mc_det.
The 75-event set splits: 14 calibration (E40 prereg events) / 61 test (never touched by the fit).

## Decision rules (LOCKED)
- **D1 (out-of-sample).** On the 61 test events: median |ψ_pred − ψ_meas| of the mixture model is
  SMALLER than median |ψ_chirp − ψ_meas| (the E40 baseline). PASS/FAIL.
- **D2 (heavy regime).** On test events with Mtot_source > 60 M☉: mixture reduces the median error
  vs pure-chirp by >30%. PASS/FAIL.
- **D3 (parameter-free sign test — needs no κ).** Among ALL 75 events with axis_ratio ≥ 1.5 and
  |ψ_chirp − ψ_total| > 10°: the measured ψ lies BETWEEN ψ_chirp and ψ_total (shortest arc, mod 180°)
  in ≥ 70% of events, and the rotation fraction toward ψ_total increases with Mtot_det
  (Spearman > 0.3). PASS/FAIL.
- Interpretation (locked): D1∧D3 pass → the E40 law + its failures are Fisher geometry (measurement
  optics, not astrophysics) — E40 upgraded to "derived". D3 pass but D1 fail → rotation is real but
  the two-band weight model is too crude. All fail → the deviations are NOT mass-organized Fisher
  structure (waveform/prior systematics remain the candidate; E40 stands as empirical).

## Honesty
- The W_t band and the single κ are crude; that is exactly why D3 (parameter-free) is included.
- ψ_meas sampling noise is negligible (thousands of PE samples), but ψ is ill-defined for round
  posteriors — hence the axr ≥ 1.5 gate in D3 (same control logic as E40's D3).
- Angles mod 180° with shortest-arc conventions throughout; betweenness defined on the shortest arc
  from ψ_chirp to ψ_total. Seed 65 (no RNG expected).
