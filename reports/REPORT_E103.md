# REPORT — E103: is the exponent offset 1PN, finite-width, or both?

Prereg: `preregs/E103_exponent_attribution_prereg.md` (prior scratch run disclosed; this is the
confirmatory locked run). Artifact: `results/e103_exponent_attribution_results.json`. Seed 103.

Built to resolve a referee-identified inconsistency: Section IV D attributed the exponent offset
(p* ≈ 0.63 vs GR's 3/5) categorically to 1PN phasing, while Appendix A attributed it to a finite-width
effect via the elongation trend. The referee's decisive test: per-event fitted exponent vs the per-event
1PN Fisher prediction, each vs elongation with the other partialled out.

## Result — both, with a clean division of labour

On the 80 elongated events:

- **D1 (medians):** fitted p* = 0.630, predicted 0.630 — the difference is consistent with zero under a
  2000-draw bootstrap. The 1PN attribution of the *population-level* offset stands, exactly.
- **D3 (prediction vs elongation):** ρ = +0.05, p = 0.68 — the 1PN prediction is flat in axis ratio and
  cannot carry any elongation trend.
- **D2 (fitted exponent vs elongation, prediction partialled out):** partial ρ = −0.26, p = 0.021 — the
  elongation trend is real and survives. Per-event, fitted vs predicted correlate only weakly (+0.24),
  largely because the prediction is nearly constant (IQR 0.628–0.639).

**Verdict: two mechanisms.** The 1PN η-dependent phasing sets the central displacement of the exponent
above 3/5; a distinct, elongation-dependent finite-width effect pulls the most-elongated events back
toward it (most-elongated half: p* = 0.620 vs predicted 0.630). Neither categorical attribution alone was
correct. The manuscript's IV D and Appendix A now state the conditioned, two-mechanism version, quoting
this artifact.
