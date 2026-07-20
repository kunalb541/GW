# Gate B — REGENERATED from the E92 artifact (2026-07-21)

**Status: reproducible.** All numbers below are read from `results/e92_curve_uncertainty_results.json`,
produced by `src/e92_curve_uncertainty.py` from the E94 posterior cache (no HDF5 access, seed 92,
200 bootstrap resamples/event, 266 events, 81 elongated).
The earlier hand-run values in this file were provisional and differed; where they differ, the
artifact wins. Gate A/C/D are likewise reproducible via E94/E95; **Gate E is NOT passed** — see
`results/e93_precision_law_results.json`.

## B1. Monte Carlo resolution (NOT coverage)

| quantity (elongated, axr ≥ 3, n=81) | value |
|---|---|
| median \|Δψ\| | 1.03° |
| median bootstrap σ on Δψ | **0.187°** |
| median \|Δψ\|/σ | **6.29** |
| fraction \|z\|<1 | 0.09 |
| fraction \|z\|<2 | 0.12 |

**Language correction.** These fractions are NOT coverage against nominal 68%/95% levels — an earlier
version of this file said they were, and that was wrong. A bootstrap over posterior samples measures the
Monte Carlo resolution of the released sample set; its σ shrinks as more samples are released and it
encodes no detector-noise, calibration, waveform or population uncertainty. The supported statement is
only that the ~1° discrepancy greatly exceeds finite-sample Monte Carlo error.

## B1b. Signed residual, per catalog (sdiff, not the absolute `adiff`)

| set | n | median signed Δψ | fraction positive | sign-test p |
|---|---|---|---|---|
| ALL | 81 | **-0.779°** | 0.22 | 0.000 |
| GWTC-3 | 30 | **-0.796°** | 0.03 | 0.000 |
| O4a | 19 | **-1.288°** | 0.21 | 0.019 |
| O4b | 32 | **-0.412°** | 0.41 | 0.377 |

**The signed offset is weaker than first reported and is NOT catalog-universal.** It is strong in the
training catalog, present in O4a, and **not significant in O4b (p = 0.377)** — the
provisional run gave 0.110 there; the artifact gives 0.377. Pooling all events into one
sign test overstates it. Spearman(signed, axr) = +0.276.

The `adiff` trap is retained as a lesson: the repo's `adiff` returns an ABSOLUTE value, and using it for
a sign test yielded a tautological "100% positive, p = 3e-24". `sdiff` is now guarded by a contract test.

## B2. Threshold sensitivity — axr ≥ 3 is not tuned

| axr threshold | n | curve | tangent |
|---|---|---|---|
| 1.5 | 170 | 2.32 | 6.04 |
| 2.0 | 117 | 1.39 | 5.89 |
| 2.5 | 88 | 1.09 | 5.16 |
| 3.0 | 81 | 1.03 | 5.02 |
| 4.0 | 50 | 0.71 | 3.36 |
| 5.0 | 37 | 0.60 | 2.40 |
| 6.0 | 26 | 0.57 | 1.84 |
| 8.0 | 13 | 0.34 | 0.81 |
| 10.0 | 9 | 0.34 | 0.79 |

Monotone and smooth; nothing distinguishes 3.

## Still provisional in this file

The arc-varying **thickness mechanism** (addendum below) has NO committed artifact and remains an
in-sample explanatory fit. It is not part of the reproducible package and must not be cited as a
quantified explanation of the residual.

---

## Addendum — the thickness mechanism, measured on real data (PARTIAL)

B1c proposed arc-varying posterior thickness as the residual's cause and showed it produces rotations of the
right magnitude synthetically. Measured on the 79 elongated events, by extracting each posterior's
perpendicular offset from the curve at its own $q$, binning to get $w(q)$, and rebuilding the model as
curve + measured per-$q$ thickness:

| model | median signed | median $|\Delta\psi|$ |
|---|---|---|
| pure curve (zero thickness) | −0.725° | 1.038° |
| **curve + measured thickness** | **−0.532°** | **0.803°** |

Improved on **71%** of events; Wilcoxon $p=3.4\times10^{-4}$.

Two structural facts: the perpendicular width is **~35% of the total spread** (these are not thin curves),
and thickness **grows along the arc in every single event** (median Spearman $w$ vs $q$ = **+1.000**).

**This is a partial explanation, not a solution.** It removes roughly a quarter of the residual, and the
per-event residual does not track the per-event taper ($\rho=+0.069$), so the remaining ~0.8° is still
unexplained. Note also that measured thickness is genuinely two-dimensional information, so this is a
MECHANISM test — it does not extend the "two 1-D summaries" compression claim, and must not be presented
as an improved reconstruction.
