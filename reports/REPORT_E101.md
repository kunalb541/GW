# REPORT — E101: alternative-curve null and the 1PN origin of the residual

Prereg: `preregs/E101_alternative_curves_and_1pn_prereg.md`. Artifact:
`results/e101_alternative_curves_and_1pn_results.json`. Seed 101. Cache-backed, no HDF5.

Built to answer an external review's strongest objection: that the non-triviality tests attack the wrong
alternative, and that the ~1° residual has an uncomputed 1PN origin. The review predicted this would
deflate the result. Run honestly, it does the opposite for the physics and confirms the review's
diagnosis of the offset.

## D1 — alternative-curve exponent null (own marginal)

Generalized curve $m_1(q;p)\propto q^{-p}(1+q)^{2p-1}$ evaluated on each event's own $q$ marginal. Median
angular error vs GR ($p=3/5$) and neighbours:

| catalog | p=0.50 | **p=0.60 (GR)** | p=0.70 | optimum $p^\star$ (boot 90%) |
|---|---|---|---|---|
| GWTC-3 | 4.14° | **0.88°** | 2.11° | 0.62 [0.62, 0.63] |
| O4a | 4.12° | **1.26°** | 1.49° | 0.63 [0.61, 0.66] |
| O4b | 3.43° | **1.19°** | 1.92° | 0.63 [0.60, 0.67] |

The exponents carry real content: $p=0.5$ is 2.9–4.7× worse than GR. The function is **asymmetric** —
the optimum sits just **above** GR at $p^\star\approx0.63$, which is the 1PN offset (D3), not a weakness.
This is the null the reviewer said should be primary; it supports non-triviality, it does not deflate it.

## D2 — chord baseline

A 5th–95th-percentile chord replaces the curve. Ordering **tangent > chord > curve** holds in all three
catalogs (e.g. O4a: 6.67° > 2.78° > 1.26°). So the tangent is indeed a weak baseline — but the full arc
beats a chord by roughly 2×, contrary to the review's claim that a chord "recovers most of it." The arc
curvature carries content beyond a chord.

## D3 — 1PN Fisher prediction of the residual direction (blind)

Stationary-phase inspiral Fisher in $(m_1,m_2)$ over $[20\,\mathrm{Hz}, f_{\rm ISCO}]$, long axis =
smallest-eigenvalue eigenvector, computed with no reference to the measured axis.

- **Verified sanity:** at 0PN the effective exponent is **exactly 0.600** and the 0PN long axis equals the
  constant-$\mathcal{M}_c$ tangent to $0.000°$. The derivation is self-consistent.
- **Blind result:** the 1PN $\eta$-dependent term shifts the effective exponent to
  $p_{\rm eff}=0.630$ (IQR [0.628, 0.639]).

This matches the empirical optimum from D1 ($p^\star\approx0.63$) and Appendix A's independent fit
($p=0.628\pm0.009$). **The exponent offset is 1PN phasing, predicted from first principles — not a false
alarm.** The reviewer's diagnosis was correct.

**Honest scope.** The 1PN Fisher direction is a *local* rotation of the median-point tangent: it moves the
error only from 4.92° (0PN) to 4.50° (1PN). The bulk of the reconstruction (down to ~1°) comes from the
global arc integration over the marginal (the curve), not the local Fisher direction. So the 1PN
calculation explains the **direction and size of the exponent offset**, and the local part of the
residual; it does **not** explain the global arc or finite thickness (E96). Reported as such.

## Consequence for the manuscript (not yet folded in)

This converts Appendix A from "a 3σ offset we demote as a false alarm" into "the offset is 1PN phasing,
predicted at $p_{\rm eff}=0.630$." It gives the paper the alternative-curve null as a genuine primary
non-triviality test, an honest chord baseline, and a first-principles account of the offset. Folding these
into the manuscript is a separate, larger revision (promote D1 to a figure, add the chord row, move the
1PN result into the residual section, cut the "false alarm" framing). No E101 number enters the paper
until it is wired through `src/build_paper_numbers.py`.
