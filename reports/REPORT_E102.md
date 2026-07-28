# REPORT — E102: does the orientation correction change a downstream quantity?

Prereg: `preregs/E102_downstream_demonstration_prereg.md`. Artifact:
`results/e102_downstream_demonstration_results.json`. Seed 102. Cache-backed, no HDF5.

Built to answer the review's fairest objection — the paper called the reconstruction a "cheap correction"
without ever showing an orientation error of this size costs anything downstream. The battery tests it and
reports both a null and a positive result honestly.

## Setup

For each elongated event, a 2-D Gaussian is built with the **true** sample mean and **true** covariance
eigenvalues, orientation set three ways: oracle (measured axis), curve (reconstruction), tangent (local
Gaussian approximation). Holding mean and eigenvalues fixed isolates orientation.

## Result — metric-dependent, and reported as such

**Primary metric (coverage of the 90% region): NULL.** The fraction of the true posterior inside the
Gaussian's 90% Mahalanobis ellipse is ~0.920 for the true axis and ~0.915 for the tangent — a gap of half
a percentage point that does not grow with axis ratio. Total-region coverage is set by the ellipse *area*
and is nearly insensitive to its *tilt*. The orientation correction does not help it, and we do not
pretend otherwise. This was the pre-registered primary metric, and it is a null.

**Secondary metric (component-mass marginal width): a clear effect.** The projected 90% credible width on
the secondary mass is orientation-sensitive. A tangent-oriented Gaussian misstates it by a median ~19%
across the three catalogs; the curve reduces this to ~5%, close to the ~2% of the oracle. A synthetic
check confirms the mechanism: for a realistic 5° mis-orientation of a 3:1 ellipse, the marginal-width
error changes by an order of magnitude more than the coverage.

## What this licenses in the manuscript

A specific, honestly-scoped downstream statement, now in the Discussion and Conclusions: the correction
improves the component-mass credible intervals of a Gaussian single-event approximation (secondary-mass
90% width error from ~19% to ~5%), while leaving total-region coverage unchanged. So a catalog-level
analysis that reads component-mass intervals from a Gaussian approximation benefits; a template-placement
or volume estimate that uses only the metric area does not. The earlier unqualified "cheap correction for
applications relying on orientation" is replaced by this.

The prereg's NULL branch (soften the language if coverage showed nothing) and its DEMONSTRATED intent
(show a real downstream effect) are both honoured: the language is softened where the metric was null, and
the genuine effect is stated where it is real.
