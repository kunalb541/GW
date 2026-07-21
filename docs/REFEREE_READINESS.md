# REFEREE READINESS — frozen snapshot

Analysis state frozen at commit `a29cc84` (this document adds no analysis) · 136 contract tests passing · manuscript 10 pp, zero LaTeX warnings, zero uncited
bibliography entries. This file is the honest summary a referee should read first.

## The thesis, in three sentences

The orientation of a compact-binary $(m_1,m_2)$ posterior can be **reconstructed** from two
one-dimensional marginal of that same posterior — its mass-ratio marginal —
using the constant-chirp-mass curve, with no coefficient calibrated on the validation catalogs, to a
median 1.0°–1.3° on elongated events across two later, disjoint
event catalogs. This is not the trivial statement that a curve beats a line: substituting any other
event's mass-ratio marginal degrades it several-fold and the achieved error lies below the minimum of
300 permutations, while the reconstruction transfers between separately inferred waveform-family
posteriors of the same event. The residual ~1° is a real systematic, about 6×
the Monte Carlo resolution of the released samples, whose size is predicted by the curve's failure of
Hastie–Stuetzle self-consistency.

## What is artifact-backed

Every number below regenerates from committed code. No figure or analysis module reads raw PE files.

<!-- BEGIN GENERATED: key-numbers -->
| claim | value | artifact |
|---|---|---|
| out-of-sample reconstruction (elongated) | 0.88° / 1.26° / 1.19° | `e95_gate_regeneration_results.json` |
| median-point tangent, same events | 4.83° / 6.67° / 4.20° | same |
| pooled-$q$ baseline, same events | 9.94° / 4.03° / 3.77° | same |
| permutation null (300 draws), own-$q$ below **minimum** | min 4.55° / 3.19° / 2.23° | same |
| cross-waveform transfer A→B, B→A | 2.08°, 2.78° (reference scale 1.99°) | same |
| residual vs Monte Carlo resolution | 1.07° vs 0.072° (17.2×) | `e92_curve_uncertainty_results.json` |
| signed residual, per catalog | GWTC-3 $p<0.001$, O4a $p=0.019$, O4b $p=0.110$ | same |
| self-consistency violation predicts residual | ρ = +0.677, p = 7.4e-12 | `e97_principal_curve_selfconsistency_results.json` |
| Gaussian (BvM) orientation error | 4.92° vs 1.07° (4.6×) | `e98_framework_audit_results.json` |
| posterior cache | no subsampling; 972/972 rows in full, 23.1 M samples | `e94_posterior_cache_manifest.json` |
<!-- END GENERATED: key-numbers -->

## What is explicitly NOT claimed

- **Not a test of general relativity.** The posteriors were generated with GR waveform models; their
  internal geometry cannot bound deviations from GR. The exponent fit is a diagnostic only.
- **Not a prediction from source medians.** The $q$ marginal comes from the posterior being
  reconstructed. This is posterior *compression*, not external prediction.
- **Not coordinate-invariant.** The same angle is 1.03°, 0.31° and 0.77° in
  source-frame, detector-frame and log-mass coordinates. No invariance theorem is invoked.
- **Not coverage.** The bootstrap measures Monte Carlo resolution of the released samples only.
- **The precision law is NOT established** — pooled fit rejects the 5/3 exponent
  (b_mass = +1.475 ± 0.055, z = -3.48); the
  light-band agreement (+1.591 ± 0.101) rests on a split chosen *after*
  seeing that rejection. Exploratory.
- **Arc-varying thickness is not established** — a constant taper does as well in one transfer
  direction (0.97° vs 0.96°).
- **No hyperribbon claim** — our 2-D eigenvalue ratio has median 3.3,
  not the many decades sloppiness requires.

## Known weak points (where a referee should push)

1. **O4a's preregistration is not publicly timestamped.** Its prereg and results entered the public
   repository in the same commit; only O4b's lock (17 h gap) is verifiable from the public record. The
   two out-of-sample scores are **not equivalent evidence**.
2. **O4a and O4b are disjoint *event* catalogs, not independent experiments** — shared detectors,
   calibration, waveform families, priors and analysis conventions.
<!-- BEGIN GENERATED: signed-rr -->
3. **The signed residual is not catalog-universal**: significant in GWTC-3 (p < 0.001) and O4a
   (p = 0.019), **not significant in O4b (p = 0.110)** — the newest and largest catalog.
<!-- END GENERATED: signed-rr -->
<!-- BEGIN GENERATED: weakest-rr -->
4. **O4b is the weakest panel of Figure 2**: its pooled-q (3.77°) and
   tangent (4.20°) are closest together, and its null minimum
   (2.23°) is nearest own-q (1.19°).
<!-- END GENERATED: weakest-rr -->
<!-- BEGIN GENERATED: arc-rr -->
5. **Arc length correlates negatively with the tangent error** (ρ = -0.51, -0.57, -0.49 across catalogs), where
   an earlier draft reported it weakly positive and claimed residuals *grow* with elongation. Both
   were wrong; the manuscript does not rest on either.
<!-- END GENERATED: arc-rr -->

## Exact reproduction

```
# 1. fetch the public PE releases into data/  (see docs/DATA_AVAILABILITY.md; ~68 GB, not distributed)
# 2. build the one-time cache (~5 min, the only HDF5 pass in the project)
python3 src/e94_build_posterior_cache.py

# 3. regenerate every analysis artifact
python3 src/e95_gate_regeneration.py            # Gates A / C / D
python3 src/e92_curve_uncertainty.py            # Gate B  (Monte Carlo resolution, threshold curve)
python3 src/e93_precision_law.py                # Gate E  (exploratory; writes NOT PASSED)
python3 src/e96_curve_thickness_mechanism.py    # thickness mechanism
python3 src/e97_principal_curve_selfconsistency.py
python3 src/e98_framework_audit.py

# 4. figures and their artifact-derived captions
python3 src/fig1b_tangent_vs_curve_residual.py
python3 src/fig1c_nontriviality_q_baselines.py
python3 src/fig2a_posterior_geometry_examples.py
python3 src/build_manuscript_figures.py

# 5. manuscript
cd paper && pdflatex manuscript.tex && pdflatex manuscript.tex

# 6. tests (data-free; run anywhere)
python3 -m pytest tests/ -q
```

`results/e94_posterior_cache.npz` (572 MB — it stores every posterior sample, no subsampling) is
gitignored and regenerable; its manifest is committed.

## Provenance discipline

Gate measurements were first written as prose and were **not** reproducible; that was corrected by
building E92–E98 so every number regenerates from committed code, and the gate documents were
regenerated *from* those artifacts. Figure captions are emitted from the figure sidecars so text and
figure cannot drift. Citations were verified at full text — see
[CITATION_VERIFICATION.md](CITATION_VERIFICATION.md), which records two narrowings and two removals.
