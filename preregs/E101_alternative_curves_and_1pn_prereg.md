# PREREG — E101: alternative-curve null and the 1PN origin of the residual

**Locked:** 2026-07-21, before the final battery run. **Seed:** 101.

## Motivation

An external review argued that the paper's non-triviality tests attack the wrong alternative, and that the
test that actually isolates whether the *chirp-mass exponents* do the work is a **different curve family
evaluated on the same event's own marginal**. It also argued that the ~1° residual has an obvious,
uncomputed origin — the constant-$\mathcal{M}_c$ direction corrected by the 1PN $\eta$-dependent phase —
and that this same physics would explain the exponent offset found in Appendix A ($p=0.628$ vs GR's
$3/5$).

Both points are correct in spirit. This battery does the work.

## Disclosure of prior exploration (honesty about what is confirmatory vs blind)

While assessing the review I ran a **scratch** computation (not committed) that showed, qualitatively:
(i) the constant-$\mathcal{M}_c$ exponents beat neighbouring exponents on the same marginal, with a
minimum near $p\approx0.63$; (ii) a 5th–95th-percentile chord is worse than the full curve but better than
the tangent. Therefore **D1 and D2 below are confirmatory measurements of a direction already seen**, run
here with a proper per-event error model and locked statistics. **D3 is genuinely blind:** the 1PN Fisher
long-axis angle has not been computed at prereg time, and its predictions are falsifiable.

## Decision rules

### D1 — alternative-curve exponent null (own marginal)
Generalize the curve to $m_1(q;p)\propto q^{-p}(1+q)^{2p-1}$ (GR: $p=3/5$). For each elongated event
($\mathrm{axr}\ge3$), evaluate the curve at a grid of $p$ over its **own** $q$ marginal and score
$|\psi_{\rm curve}(p)-\psi_{\rm meas}|$. Report the per-catalog median error vs $p$, with a bootstrap CI
over events, and the empirical minimizing $p^\star$ with its bootstrap uncertainty.
- **PASS** if $p=3/5$ is markedly better than distant exponents (median error at $p\in\{0.5,0.7\}$ at
  least $2\times$ the error at $p=0.6$), establishing the exponents carry real content.
- **Separately reported** (not a pass/fail): whether $p^\star$ is consistent with $3/5$ or displaced, with
  a bootstrap CI. If displaced, that is a limitation on the specificity of GR's exponents at this
  precision, to be stated as such — not demoted.

### D2 — chord baseline
Define the chord as the line through the curve points at the 5th and 95th percentiles of the event's $q$
marginal. Score its angular error. **Expected ordering, locked:** tangent $>$ chord $>$ curve (chord
between the strawman and the full construction). Report all three per catalog.

### D3 — 1PN Fisher prediction of the long axis (BLIND)
Build the inspiral-phase Fisher matrix $\Gamma_{ij}=\int f^{-7/3}S_n(f)^{-1}(\partial_i\Psi)(\partial_j\Psi)\,df$
over $[20\,\mathrm{Hz}, f_{\rm ISCO}]$ in $(m_1,m_2)$ coordinates, with $\Psi$ the stationary-phase
inspiral phase to **1PN**:
$$\Psi \propto (\pi\mathcal{M}_c f)^{-5/3}\left[1 + \tfrac{20}{9}\left(\tfrac{743}{336}+\tfrac{11}{4}\eta\right)(\pi M f)^{2/3}\right].$$
The posterior long axis is the smallest-eigenvalue eigenvector of $\Gamma$. Compute its position angle at
each event's median masses, using **no information from the measured axis**.
- **D3a (falsifiable):** the 1PN long axis rotates *away* from the 0PN constant-$\mathcal{M}_c$ direction
  *toward* the measured axis, i.e. median $|\psi_{\rm 1PN}-\psi_{\rm meas}| <
  |\psi_{\rm 0PN}-\psi_{\rm meas}|$. FAIL if it does not reduce the error, or rotates the wrong way.
- **D3b (falsifiable):** the effective exponent implied by the 1PN long axis is $>3/5$, in the same
  direction as the empirical $p^\star$ from D1. FAIL if it predicts $p<3/5$.
- **Honest scope, stated up front:** the 1PN Fisher direction is a *local* (median-point) rotation; it
  addresses the exponent offset and the local part of the residual, NOT the global arc curvature or finite
  thickness (E96). The battery will report how much of the residual it accounts for and will not claim the
  rest.

## What would make this battery a failure worth reporting
If D1 shows the exponents do **not** matter (flat in $p$), the paper's non-triviality claim collapses and
must be withdrawn — this is the reviewer's strongest hypothesis and it is tested here honestly. If D3
predicts a rotation in the wrong direction, the "1PN explains the residual" story is wrong and stays an
open problem, as the manuscript currently states.

## Outputs
`results/e101_alternative_curves_and_1pn_results.json`; report in `reports/`; data-free contract tests.
No number enters the manuscript until it is regenerated through `src/build_paper_numbers.py`.
