# PREREG — E103: is the exponent offset 1PN, finite-width, or both?

**Locked:** 2026-07-21, before the final battery run. **Seed:** 103.

## Motivation

A referee report identified an internal inconsistency: Section IV D attributes the exponent offset
($p^\star\approx0.63$ vs GR's $3/5$) categorically to 1PN phasing, while Appendix A attributes the same
offset to a finite-width effect, citing the elongation trend (the most-elongated half fits nearer $3/5$).
These are distinct mechanisms. The decisive test, in the referee's words: "correlate the per-event fitted
exponent against the per-event Fisher prediction, and each against elongation with the other partialled
out."

## Disclosure of prior exploration

This test was run once in scratch while verifying the referee's claim (not committed). It showed,
qualitatively: the population medians match exactly (fitted $0.630$ vs predicted $0.630$); the per-event
correlation is weak-positive; the 1PN prediction is flat in elongation while the fitted exponent declines
with it. **This battery is therefore confirmatory of a direction already seen**, run with locked
statistics and a committed artifact. The expected conclusion, stated before the run: **both mechanisms are
real — 1PN sets the population-level offset, and a distinct elongation-dependent (finite-width) effect
pulls the most-elongated events back toward $3/5$.** If the locked run contradicts this, the contradiction
is reported.

## Decision rules

Per elongated event ($\mathrm{axr}\ge3$, all catalogs): fitted exponent $p^\star_i$ = argmin over the E101
grid of the arc angular error on the event's own marginal; predicted $p^{\rm 1PN}_i$ from the 1PN Fisher
long axis; elongation $\mathrm{axr}_i$. Spearman correlations and rank-based partial correlations both
ways. Bootstrap (over events, 2000 draws) for CIs.

- **D1:** does the population median of $p^\star$ match the median 1PN prediction to within the bootstrap
  CI? (Expected: yes — the 1PN attribution of the *median* offset stands.)
- **D2:** does $p^\star$ depend on elongation after partialling out the 1PN prediction? (Expected: yes,
  negative — the elongation trend is NOT carried by 1PN, so a second, finite-width mechanism is required.)
- **D3:** does the 1PN prediction itself depend on elongation? (Expected: no — confirming it cannot carry
  the trend.)

## Consequence for the manuscript

Whatever the outcome, the categorical sentence in IV D ("the offset is therefore the imprint of 1PN
phasing") and the finite-width sentence in Appendix A are replaced by a conditioned, two-mechanism
statement quoting this battery. No number enters the paper except through `src/build_paper_numbers.py`.
