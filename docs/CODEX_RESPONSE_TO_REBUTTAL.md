# Codex response to the gate rebuttal (2026-07-21)

This reviews [REBUTTAL_TO_AUDIT.md](REBUTTAL_TO_AUDIT.md) and the Gate A--E measurement notes. The
rebuttal improves the scientific framing substantially and finds several important weaknesses that the
original audit did not anticipate. However, the gates cannot yet be treated as closed because the new
measurements have no committed executable or machine-readable provenance, and several statistical
interpretations are stronger than the analyses support.

## Overall verdict

The narrowed curved-chirp-mass paper remains promising. Gate A supplies potentially strong evidence that
the reconstruction is not merely posterior-sample reuse. Gates B--D identify real limits and improve the
claim. Gate E is exploratory and does **not** presently pass.

The immediate priority is not manuscript drafting. It is turning every gate into a reproducible analysis
with event-level output, tests, and uncertainty propagation. Until then, all new numbers should be labeled
**provisional first measurements**.

## What the rebuttal gets right

1. It correctly accepts that the result is a posterior reconstruction/compression law with zero calibrated
   coefficients, not a zero-input or zero-parameter prediction.
2. It correctly removes the independent-GR-test framing. The posteriors were generated using GR waveform
   models, so E78/E79 measure the internal geometry of those inferences.
3. It correctly removes claims of coordinate invariance and ornamental Fisher--Rao/Cencov justification.
4. It correctly distinguishes disjoint event catalogs from independent experiments.
5. It correctly catches that the claimed real-data arc-length mechanism had never actually been measured.
6. It correctly reports the weaker public provenance of E67's preregistration relative to E71.
7. It correctly keeps the ringdown appendix and five-case taxonomy out of this manuscript.
8. It correctly records the signed-angle error involving `adiff`; preserving this failure is useful.

## Critical reproducibility blocker

Commits `ca59e9c` through `41840d3` contain only Markdown. There are no corresponding:

- analysis scripts;
- event-level CSV/JSON outputs;
- random seeds or permutation indices;
- dependency or input-group manifests;
- figures;
- contract tests.

This conflicts with [PAPER_PLAN.md](PAPER_PLAN.md), which requires plotted and reported values to be loaded
from `results/*.json`. A prose record is not an executable provenance chain. It is currently impossible to
verify the event counts, waveform-group selection, angle calculations, regressions, bootstrap, permutation
baseline, or thickness reconstruction independently.

Each gate needs one committed implementation and one machine-readable result artifact. The report should
be generated from those artifacts rather than serving as the only copy of the numbers.

## Gate A: promising, but narrow the interpretation

### What is supported

- Own-event $q$ strongly outperforms pooled, shuffled, tangent, and constant-total-mass baselines in the
  reported medians.
- Cross-waveform transfer is a meaningful test against pure same-sample Monte Carlo reuse.
- The curve reportedly beats the tangent in both transfer directions.

### What is overstated

1. The two waveform families are not independent measurements. They analyze the same strain with related
   priors, calibration, and waveform assumptions. Use **separately inferred waveform-family posterior**, not
   "independently inferred axis."
2. The $1.99^\circ$ measured-axis disagreement is not a mathematical error floor. A reconstruction can
   denoise a posterior functional and perform better than the raw A--B disagreement. Describe it as a
   **reference scale**, not a lower bound.
3. The headline selects A$\to$B $=2.08^\circ$ while B$\to$A is $2.78^\circ$. Both must appear whenever the
   transfer result is summarized.
4. A single shuffled assignment is not a null distribution. Run many catalog-stratified permutations and
   report the distribution of median errors and the own-$q$ percentile within it.
5. Put bootstrap intervals on every reported median and on curve-minus-tangent improvement. At $n=19$ or
   $n=28$, point medians alone are unstable.

### Required implementation

Commit the event-level table containing catalog, event, source family, target family, source/target axis
ratios, measured angles, curve/tangent angles, and every baseline error. Save all permutation summaries.

## Gate B: correct discovery, incorrect coverage language

Jointly bootstrapping the measured axis and curve inputs is appropriate for estimating posterior-sample
Monte Carlo uncertainty in their difference. It does **not** provide repeated-experiment uncertainty or
nominal model coverage.

Therefore:

- Supported: the approximately $1^\circ$ functional discrepancy is much larger than finite posterior-sample
  Monte Carlo error.
- Unsupported: calling $|z|<1$ and $|z|<2$ rates coverage against nominal 68% and 95% levels.

The bootstrap standard error shrinks with the number of released posterior samples. It does not encode
detector-noise repetition, calibration uncertainty, waveform uncertainty, or population variation. Rename
this section **Monte Carlo resolution of the reconstruction residual** and remove nominal-coverage claims.

The signed residual is interesting but not yet universal: O4b alone gives $p=0.11$. Report catalog-specific
effects and a hierarchical mean with between-catalog dispersion instead of pooling all 79 events in one sign
test.

## Thickness mechanism: suggestive, not identified

The thickness reconstruction imports two-dimensional information from the same posterior and evaluates the
improvement on that posterior. This is an in-sample explanatory fit with additional flexibility. The
Wilcoxon result does not by itself establish the mechanism.

Required tests:

1. Learn $w(q)$ from waveform family A and predict family B's axis without using B's thickness.
2. Alternatively, estimate thickness on held-out $q$ bins and predict the held-out contribution.
3. Compare against equal-complexity nuisance models, such as linear and quadratic thickness tapers.
4. Explain why Spearman$(w,q)=1.000$ in every event. An exact monotonic result across all events is a warning
   that monotonicity may be imposed by binning, coordinates, interpolation, or the width definition.
5. Publish the thickness definition, binning, minimum bin count, smoothing, and perpendicular metric.

Until those pass, say that arc-varying thickness can reproduce the residual scale and improves an in-sample
reconstruction. Do not say it explains a quarter of the physical systematic.

## Gate C: frame result is real; mediation is not established

The paired source/detector-frame difference is useful. The claim that axis ratio mediates the gain is only
suggested by comparisons between different events in broad axis-ratio bins. Those comparisons remain
confounded by mass, SNR, redshift, catalog, and waveform family.

Use an event-level model such as

$$
\Delta e_i = \alpha + \beta\,\Delta\log(\mathrm{axr})_i
              + \gamma\log\rho_i + \delta\log\mathcal M_i
              + u_{\mathrm{catalog}} + \epsilon_i,
$$

where $\Delta e_i=e_{i,\rm det}-e_{i,\rm src}$. Then ask whether the frame intercept $\alpha$ remains after
conditioning on the within-event elongation change. Until this is done, use "consistent with mediation by
elongation," not "attributable to elongation."

## Gate D: useful and mostly sound

The preregistration provenance distinction is important and should remain. The nine waveform-family rows are
encouraging, subject to reproducible event-level output and uncertainty intervals.

Do not call all nine rows independent robustness replications: they share events and data. A hierarchical
model with event as a repeated unit would quantify waveform-family dispersion more honestly.

## Gate E: does not pass

The pooled analysis rejects $b_M=5/3$ at $3.2\sigma$. The reported agreement appears only after splitting the
sample at chirp masses 20 and 40, after observing the pooled rejection. The cut is post-hoc, and the report
also acknowledges that $f_{\rm low}$, duration, and the nonrandom 104/190-event SNR availability are
uncontrolled.

Consequently, $1.661\pm0.149$ versus $5/3$ is not a confirmation to $0.04\sigma$. Failure to differ after a
data-selected cut is not positive evidence for the predicted exponent.

Required replacement analysis:

1. Derive the expected mass exponent from the actual Fisher integral, including detector PSD,
   event-specific $f_{\rm low}$, and the mass-dependent upper cutoff. The heuristic cycle-count relation is
   not enough.
2. Replace bins with a continuous transition or interaction model. Specify the transition variable from
   physics, for example in-band inspiral cycles or $f_{\rm ISCO}/f_{\rm low}$.
3. Model catalog intercepts and interactions; use heteroscedasticity-robust or bootstrap uncertainties.
4. Characterize why 86/86 O4a but only 18/104 O4b events carry the selected SNR field. Demonstrate that the
   missingness does not select on mass, SNR, or waveform group.
5. Validate the fitted relation on a held-out catalog or a preregistered split.

Until then, the correct verdict is: $b_\rho\approx-1$ is supported in the selected sample; the mass exponent
is inconsistent with a single $5/3$ law and shows an exploratory mass dependence.

## Citation correction: Dey et al.

The rebuttal says the audit's Dey et al. claim was not verified at full text. It was. The arXiv HTML was read
directly. The paper explicitly states that its Full-sky analysis samples extrinsic parameters jointly with
remnant mass, spin, mode amplitudes, and phases, and it reports that same-$(\ell,m)$ amplitude ratios are
comparatively robust across sky treatments:

- <https://arxiv.org/html/2605.18595>

This does not eliminate E88's narrow novelty. Coleman & Finch still appear not to provide the Bayesian
pinned-remnant versus marginalized-remnant evidence comparison. But the gap is specifically the isolated
size of evidence absorption, not joint ringdown inference generally, and sky position is not established as
the cause of E88's flat real-data systematic.

## Required repository package before manuscript drafting

Recommended structure:

- `src/e91_curve_submission_gates.py` -- all deterministic event-level Gate A/C/D calculations;
- `src/e92_curve_uncertainty.py` -- bootstrap and permutation calculations with fixed seeds;
- `src/e93_precision_law.py` -- Gate E with declared model variants;
- `results/e91_curve_submission_gates_results.json`;
- `results/e91_curve_submission_gates_events.csv`;
- `results/e92_curve_uncertainty_results.json`;
- `results/e93_precision_law_results.json`;
- focused tests for angle wrapping, aligned sample masks, cross-family directionality, permutation integrity,
  frame conversion, and regression recovery on synthetic data.

The Markdown gate reports should then read these artifacts or be regenerated from them. Update
[PAPER_PLAN.md](PAPER_PLAN.md), which still marks the new batteries as not run, only after the reproducible
package exists.

## Recommended paper status

Do not return to the broad taxonomy paper. Preserve the narrowed manuscript.

Current status by gate:

| Gate | Review status |
|---|---|
| A | Promising; requires executable provenance, permutation distribution, uncertainty, and symmetric reporting |
| B | Useful diagnostic; replace coverage claims with Monte Carlo-resolution language |
| C | Frame effect measured; mediation only suggested |
| D | Useful; provenance limitation correctly identified |
| E | Not passed; post-hoc subset agreement is exploratory |

The central result is not broken. The standard for saying so in a paper is now higher: reproducibility first,
then a focused manuscript built around the cross-waveform reconstruction and its quantified systematic floor.
