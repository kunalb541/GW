# Gate B — REGENERATED from the E92 artifact (2026-07-21)

> **BANNER 2026-07-21 — superseded numbers, and the same reversal as Gates A and C.** This note is kept
> unedited as a record. Its values came from a posterior cache that bootstrapped 4000 samples per row
> *with replacement*; the cache now stores every sample exactly. Regenerated:
> median |Δψ| **1.07°**, bootstrap σ **0.072°**, ratio **17.2×** (not 6.29×), and O4b signed
> **p = 0.110** — which is what this note calls "the provisional run" value before concluding the
> artifact's 0.377 superseded it. The provisional run was right. The measurements of record are
> `results/e92_curve_uncertainty_results.json`; the reader-facing summaries in
> [REFEREE_READINESS.md](REFEREE_READINESS.md) are generated from it and cannot drift again.


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

## Addendum — the thickness mechanism, REGENERATED from the E96 artifact

**Status: reproducible.** Read from `results/e96_curve_thickness_mechanism_results.json`
(`src/e96_curve_thickness_mechanism.py`, E94 cache, no HDF5, seed 96).
**Verdict: finite thickness SUPPORTED OUT-OF-SAMPLE; arc variation NOT ESTABLISHED.**

### The estimator, declared
curve point at the event's median Mc; unit normal from a finite difference dq=0.0001;
per-sample perpendicular offset; **6 equal-count q bins**, minimum **20** samples/bin and
**4** good bins required; width = std of the offset in each bin; **none; linear interpolation between bin centres, clamped**.

### Estimator control — the +1.000 is NOT imposed by binning
Constant true thickness → Spearman(w,q) = -0.31, -0.71, -0.37, +0.77 (random signs, flat profiles).
Genuinely growing thickness → +1.00, +1.00. So the real-data monotonicity is
genuine. On real events the median is **0.943**, with only 35% exactly +1 — the earlier
prose figure of "+1.000 in every event" came from an unfiltered binning and is corrected here.

### In-sample (weak by construction)
| model | median signed | median \|Δψ\| |
|---|---|---|
| pure curve (zero thickness) | -0.779° | 1.028° |
| curve + measured thickness | -0.609° | 0.884° |

n=81, improved on 63%, Wilcoxon p=1.8e-03; median relative thickness
0.327 of the total spread. *IN-SAMPLE: w(q) is learned from the same posterior it then helps reconstruct, and adds flexibility. Improvement here is not evidence of mechanism.*

### Out-of-sample — learn w(q) on one waveform family, predict the other's axis
| direction | n | pure curve | measured | constant | linear | quadratic |
|---|---|---|---|---|---|---|
| AtoB | 64 | 1.14° | **0.96°** (p=0.005) | 0.97° | 0.90° | 0.86° |
| BtoA | 64 | 1.00° | **0.74°** (p=0.028) | 0.87° | 0.72° | 0.81° |

**Finite thickness genuinely helps out of sample**: the measured profile beats the zero-thickness curve in
both directions (1.14→0.96, p=0.005; 1.00→0.74, p=0.028), using only the
source family's widths. So the zero-thickness idealization IS part of the residual.

**But the arc-VARYING part is not established.** A *constant* thickness does essentially as well as the
measured profile in A→B (0.97° vs 0.96°), and simple linear/quadratic tapers match or beat it in
both directions. So what matters is *having* thickness, not the specific measured taper.

> FINITE thickness improves cross-family prediction in both directions, so the zero-thickness idealization is genuinely part of the residual. But the ARC-VARYING part is NOT established: a constant or simple linear taper does as well as or better than the measured profile. Do not claim the measured taper is the mechanism, and do not quote a fraction of the residual explained.

**Withdrawn:** the earlier claim that arc-varying thickness "explains roughly a quarter of the residual."
E96 does not support attributing any fraction of the residual to the measured taper. Thickness is also
two-dimensional information and is NOT part of the two-summary compression claim.
