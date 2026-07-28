# REPORT — the reproducible spine (E92–E100)

The batteries that regenerate the manuscript's numbers from a committed cache. The older `reports/`
entries (E16–E89) documented the exploratory program; this one documents the reproducible core the paper
actually rests on, which previously had no written record. **Numbers are not transcribed here** — each
battery's authoritative output is its `results/eXX_*_results.json`; this report states purpose, method and
verdict, and quotes only headline values that are independently guarded by the test suite.

## E94 — posterior cache (`src/e94_build_posterior_cache.py`)

One-time extract of the released posteriors so every downstream battery runs in seconds with no HDF5
access. **Stores every usable sample, no subsampling** (23.1 M samples across 972 waveform-group rows,
972/972 held in full). Manifest: `results/e94_posterior_cache_manifest.json`; the cache `.npz` itself is
gitignored (~572 MB). Locked by `test_cache_stores_every_sample_and_never_bootstraps`.

*History:* an earlier version drew 4000 samples per row with replacement, which never used the full
sample at any cap and left up to 0.54° of seed scatter in every downstream number. That defect was found
by E99 and corrected; three paper numbers had been "corrected" to wrong values while it stood.

## E95 — gate regeneration (`src/e95_gate_regeneration.py`)

Gates A/C/D from the cache: the out-of-sample reconstruction (own-q vs pooled/permuted baselines), the
cross-waveform transfer (both directions), and the per-waveform-family scores. Uses a 300-draw
catalog-stratified permutation null; stores the raw draws so "below all 300" is auditable. Own-q
reconstruction ≈ 1.26° (O4a) / 1.19° (O4b); cross-family transfer ≈ 2.08° A→B. Verdict: **reconstruction
reproducible, non-trivial, and transfers across families.**

## E92 — residual uncertainty (`src/e92_curve_uncertainty.py`)

Joint bootstrap that isolates the Monte Carlo resolution of the released samples from the reconstruction
residual, plus the signed-residual sign test per catalog and the axis-ratio threshold sensitivity.
Residual ≈ 1.07°, about 17× the Monte Carlo resolution (median of per-event ratios). Verdict: **the ~1°
residual is a property of the model, not sampling noise.**

## E96 — thickness mechanism (`src/e96_curve_thickness_mechanism.py`)

Tests whether finite posterior thickness perpendicular to the curve contributes to the residual, learning
the width profile on one waveform family and predicting another's axis. Verdict: **finite thickness
SUPPORTED out-of-sample; arc-variation NOT established** (a constant or simple taper does as well).

## E97 — principal-curve self-consistency (`src/e97_principal_curve_selfconsistency.py`)

Implements the Hastie–Stuetzle self-consistency definition and tests it on the constant-Mc curve across a
grid sweep. Verdict: **the violation predicts the per-event residual (SUPPORTED, grid-robust); the
one-iteration correction does NOT survive out-of-sample.**

## E98 — framework audit (`src/e98_framework_audit.py`)

Checks which mathematical frameworks the measurement actually earns. Verdict: Bernstein–von Mises /
Gaussian-limit comparison **EARNED**; sloppy-model concept supported but the **hyperribbon geometry NOT**
(2-D eigenvalue ratio median ≈ 3, not the many decades a hyperribbon needs); Čencov and Backus–Gilbert
not applicable / not earned.

## E100 — frames, coordinates, elongation bands (`src/e100_frames_and_bands.py`)

The coordinate-dependence of the measured angle (source vs detector vs log-mass), the matched-axis-ratio
control behind the detector-frame claim, the elongation-band degradation, the threshold sweep, the
chirp-vs-total win fractions, and the arc-length correlation. These previously lived only as prose in a
gate note and had drifted. Verdict: **angle is coordinate-dependent (reported, not assumed); the
elongation gate is a smooth physical effect, threshold monotone.**

## E99 — cache stability audit (`src/e99_cache_stability_audit.py`)

The one battery that re-reads the HDF5 files directly, bypassing the cache, to verify the cache is
representative. Verdict: **the current no-subsampling cache is fit for purpose** and reproduces the
independent full-sample pass exactly for O4a and O4b. Its `by_seed`/`summary` blocks describe the
*retired* 4000-sample scheme and are labelled as such; `full_sample_reference` is the cache-independent
check. Verified by `test_cache_reproduces_the_independent_full_sample_pass`.
