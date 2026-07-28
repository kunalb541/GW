# PREREG — E102: does the orientation correction change a downstream quantity?

**Locked:** 2026-07-21, before running. **Seed:** 102. **Blind:** the coverage numbers below have not
been computed.

## Motivation

An external review's fairest objection: the paper asserts the reconstruction is "a cheap correction for
applications relying on orientation" but never demonstrates that an orientation error of this size costs
anything. This battery tests it honestly, and will report a null result plainly if that is what it finds.

## The test

Many downstream uses (hierarchical population inference with Gaussian single-event likelihood
approximations, low-latency proposals, metric-based estimates) approximate a single-event $(m_1,m_2)$
posterior as a 2-D Gaussian. The orientation of that Gaussian is exactly what this paper reconstructs.

For each elongated event ($\mathrm{axr}\ge3$) build a 2-D Gaussian with the **true** sample mean and the
**true** covariance eigenvalues, but with the principal-axis orientation set three ways:
- **oracle** — the measured axis (best possible);
- **curve** — the constant-$\mathcal{M}_c$ reconstruction;
- **tangent** — the local Gaussian/metric approximation.

Because the mean and eigenvalues are held fixed, any difference isolates the effect of orientation alone.

**Metric (primary):** the fraction of the true posterior samples falling inside the Gaussian's 90%
Mahalanobis ellipse. A well-oriented approximation covers close to its nominal 90%; a mis-oriented ellipse
of the same area covers less. Report per catalog and per axis-ratio band.

**Metric (secondary, astrophysical):** the fractional error in the Gaussian-approximated 90% credible
width on the secondary mass $m_2$, relative to the true posterior. Orientation error biases marginal
widths even when the mean is exact.

## Decision rule

- **DEMONSTRATED** if the curve orientation recovers more than half of the oracle$-$tangent coverage gap,
  i.e. the correction closes most of the distance between the crude and the best-possible approximation,
  and the effect grows with axis ratio as it must.
- **NULL** if curve coverage $\approx$ tangent coverage (gap closed $<$ 25%). In that case the orientation
  correction does not materially improve a Gaussian approximation, the paper's "cheap correction"
  language must be softened to "a more accurate orientation, of limited demonstrated downstream value,"
  and this null is reported.

## Output
`results/e102_downstream_demonstration_results.json`; report in `reports/`; data-free contract tests.
No number enters the manuscript until regenerated through `src/build_paper_numbers.py`.
