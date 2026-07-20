# E89 lab notebook - black-hole spin magnitude rises with mass across 265 events: a hierarchical-assembly signature

**CHARACTERIZATION (no prereg).** The trend was already visible in an earlier capability audit, so this is
NOT a blind test and is not scored as one. What is new here is that it survives a remnant-spin artifact
test, repeats in three independent observing runs, and is calibrated against two independent nulls after
two analysis traps were found and removed.

## The physics
A comparable-mass BBH merger leaves a remnant with **a_f ~ 0.69 almost independently of what went in** -
one of GR's cleanest predictions, and visible directly in this catalog (below, the `final_spin` column sits
at 0.690-0.707 in EVERY mass bin). So black holes that are themselves merger remnants - second-generation,
built by hierarchical assembly - should carry a ~ 0.7, and should sit preferentially at high mass. The
signature is a rising spin MAGNITUDE with mass.

**Why E42-E44 saw nothing.** Those batteries hunted the hierarchical channel in **chi_eff** and found no
requirement for it. That is exactly what should happen: dynamically assembled binaries have ISOTROPIC spin
orientations, so large spin magnitudes average to chi_eff ~ 0. chi_eff is structurally blind to this
population. E89 is E44's question asked in the observable that can see it, on 265 events instead of 75.

## Result
p(a_1 | m_1) = Beta with mean sigmoid(b0 + b1 ln(m1/30)), fitted hierarchically over all 265 events. The
a_1 prior is uniform(0,1) - verified against the `priors` group in the release files - so each event's
marginal posterior is proportional to its marginal likelihood and needs no reweighting.

| | value |
|---|---|
| slope **b1** | **+1.193** (raw fit; no bias correction is applied, because both nulls sit at zero) |
| dlnL vs slope = 0 | 10.94 |
| population mean a_1 at m1 = 8 / 30 / 60 / 100 Msun | **0.083 / 0.304 / 0.499 / 0.647** |
| remnant-spin reference a_f | 0.69 |

Descriptive: Spearman(m1, median a_1) = **+0.554**, p = 9e-23, n = 265.

**Repeats in three independent observing runs** - the coherence lens used positively:

| catalog | n | Spearman | p |
|---|---|---|---|
| GWTC-3 | 75 | +0.683 | 1.5e-11 |
| O4a | 86 | +0.490 | 1.7e-06 |
| O4b | 104 | +0.475 | 3.5e-07 |

## Significance: against nulls, not chi^2
The confound is real and large: heavier events are genuinely less informative
(Spearman(ln m1, posterior concentration) = **-0.517**). Two independent nulls, 150 trials each:

| null | what it destroys | b1 | dlnL | p(b1 >= obs) |
|---|---|---|---|---|
| **A** forward simulation, mass-INDEPENDENT truth, real per-event informativeness | any true correlation | -0.046 +/- 0.138 (max +0.432) | -1.28 +/- 9.64 (max 4.75) | **0/150** |
| **B** permute masses WITHIN concentration strata, real posteriors kept | any true correlation, holds measurement quality fixed | -0.002 +/- 0.173 (max +0.641) | 0.31 +/- 0.49 (max 3.39) | **0/150** |

Both nulls sit at zero: **the estimator is not biased by the confound.** The observed +1.193 exceeds the
maximum of all 300 null trials (9.0 sigma in units of null A's scatter, 6.9 sigma against null B;
empirical p < 1/150 in each).

## The remnant-spin artifact test (the obvious way this could have been fake)
For heavy events a_1 is inferred largely from merger-ringdown, where the REMNANT spin (~0.7) lives. If
remnant spin were leaking into the component-spin estimate it would manufacture exactly this trend. A leak
would show heavy a_1 ~ final_spin (gap ~ 0) and a per-event sample correlation ~ +1. It does not:

| m1 bin | n | median a_1 | median final_spin | gap | per-event corr(a_1, final_spin) |
|---|---|---|---|---|---|
| 0-15 | 54 | 0.271 | 0.691 | -0.420 | +0.468 |
| 15-35 | 72 | 0.400 | 0.690 | -0.290 | +0.457 |
| 35-60 | 105 | 0.446 | 0.691 | -0.246 | +0.396 |
| >60 | 28 | 0.510 | 0.707 | -0.197 | +0.517 |

The gap stays large at high mass and the per-event correlation is ~0.4-0.5 for LIGHT events too, so it is
the generic physical contribution of component spin to remnant spin, not a high-mass leak.

## Two traps this battery fell into first (both now contract-tested)
**(1) An "informative events" cut is circular.** Splitting on how far each posterior sits from its prior
looks like the E85 lesson applied well, and gives a beautifully strengthened trend (+0.627, and heavy
median a_1 = 0.669 vs 0.499 uncut). It is circular: among heavy events spin is well measured precisely
WHEN IT IS LARGE. Measured: **Spearman(a_1, KS-from-prior) = +0.927 across the 10 heaviest events.** No
informativeness cut is used in the result above.

**(2) The first null generator was wrong, and it under-reported the result.** Simulating each posterior as
a Beta CENTRED on the truth with low concentration makes a small true spin pile against a_1 = 0, which
looks highly informative. Real uninformative posteriors do not do that - they relax to the flat prior
(real heavy events with concentration <= 4 have median a_1 = **0.474**, i.e. the prior median). The wrong
shape produced a spurious null slope of **+0.42 +/- 0.11**, which would have been subtracted from +1.19 as
if it were estimator bias. Corrected to a mixture of truth and the uniform prior, the null moved to
-0.046 +/- 0.138. Generator fidelity after the fix: Spearman(ln m1, KS) real -0.425 vs simulated -0.417;
heavy median-of-medians real 0.494 vs simulated 0.439.

A tempting analytic argument - that a flat posterior contributes ln(integral of a normalized density) = 0
to every population model and so cannot bias anything - is true only in the exact-flat limit. NEAR-flat
posteriors do not obey it, which is why the nulls had to be run rather than reasoned about.

## Honesty / limits
- **SELECTION EFFECTS ARE NOT MODELLED.** This is a statement about the DETECTED population, not the
  astrophysical one. Aligned spin raises SNR (orbital hang-up), so high-spin systems are detectable
  further away at fixed mass; without a VT/injection campaign the astrophysical amplitude of the trend is
  not established. This is the single largest caveat and it is not small.
- The effect is not novel: a mass/spin correlation and the hierarchical interpretation of high-mass
  high-spin events are both discussed in the literature. What is done here is an independent measurement
  across 265 events with the artifact and null calibration spelled out.
- Event masses are treated as fixed at their posterior medians; mass uncertainty is not propagated.
- The Beta population model is rigid (one concentration for all masses); a mixture model would be the
  natural successor and is the right way to test a genuine 2G SUBPOPULATION rather than a smooth trend.
- The individual high-mass, high-spin events (GW231123 a_1 = 0.899, GW190403 a_1 = 0.892, GW231028 0.787)
  carry much of the signal; n = 28 above 60 Msun.
- Spin tilts are not analysed here, so the isotropy prediction of dynamical assembly is untested.

## Verification
- 9 contract tests (`tests/test_e89_mass_spin.py`): concentration detects a flat posterior; the fit
  recovers a true slope; it is unbiased when measurement quality is mass-independent; **the null generator
  must relax to the flat prior** (trap 2, with the discarded shape shown failing); the confound alone does
  NOT manufacture a slope; a true slope survives the confound; the permutation null is centred at zero and
  only has power when informativeness and mass are not near-deterministically coupled; **the
  informativeness cut is circular** (trap 1); and flat posteriors contribute ~nothing to the comparison.
- Full suite 89/89.

Code: `src/e89_mass_spin_hierarchical.py`. Numbers: `results/e89_mass_spin_hierarchical_results.json`.
Tests: `tests/test_e89_mass_spin.py`. Data: `data/chains/` (gitignored).
Successor: a 2-component mixture (1G + 2G) with a selection function, and the tilt-isotropy test.
