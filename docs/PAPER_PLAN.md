# PAPER PLAN - *The Curved Chirp-Mass Geometry of Compact-Binary Mass Posteriors* (2026-07-21)

This revision follows a hostile-referee audit of [PAPER_DIRECTION.md](PAPER_DIRECTION.md). It supersedes
the broader "lawful and diagnostic" plan. The previous version had a strong central result but diluted it
with a five-case methods taxonomy, an unrelated ringdown appendix, and an overclaimed test of GR.

## Review verdict: major revision, promising after narrowing

The defensible paper is the curved chirp-mass result. Its precise claim is:

> In the fixed source- or detector-frame $(m_1,m_2)$ coordinates used by LVK posterior releases, the
> principal-axis orientation of an elongated component-mass posterior can be reconstructed accurately from
> its median chirp mass and mass-ratio marginal. The reconstruction has no coefficients calibrated on the
> validation catalogs, and a mapping fixed on GWTC-3 scores at median errors of $1.26^\circ$ on O4a and
> $1.22^\circ$ on O4b.

Use **zero calibrated parameters**, not "zero-parameter prediction." The event's own $q$ marginal is an
input derived from the posterior being reconstructed. The result is therefore a strong posterior-compression
and out-of-sample reconstruction law, not a prediction from source medians alone.

## Claims that must be removed or demoted

1. **Not an independent test of GR.** The posterior samples were inferred with GR waveform models. Fitting
   an effective chirp-mass exponent to their geometry tests the internal geometry of those inferences; it is
   not waveform-independent evidence for or against GR. E78/E79 can appear only as an exploratory
   sensitivity diagnostic, preferably in an appendix, and must not be in the title or abstract.
2. **Not coordinate-invariant information geometry.** A PCA angle changes under reparameterization and
   rescaling. State the coordinate convention explicitly and demonstrate robustness under the physically
   relevant common mass rescalings. Do not invoke Fisher-Rao or Cencov invariance to imply that the measured
   Euclidean angle is invariant.
3. **No generic rule that coherence means systematic.** Real physics can also be coherent. The valid test is
   whether an anomaly follows a nuisance coordinate more strongly than a declared physical scaling, survives
   independent waveform families, and vanishes under a controlled limit.
4. **No five-failure-mode taxonomy in this paper.** E47, E85/E87, E88, and E89 use different likelihoods,
   scientific questions, and maturity levels. Together they read as a research diary rather than evidence
   for the component-mass result.
5. **No ringdown validation appendix.** E87 validates a ringdown pipeline that the narrowed paper does not
   use. It invites a second referee community without supporting the main result.
6. **Do not say the tangent residual grows with axis ratio.** The reported Spearman correlations of absolute
   tangent error with axis ratio are negative ($-0.42,-0.40,-0.69$): orientation becomes better defined as
   elongation increases. The curvature correction is clearest among elongated events, but that is not the
   same statement as a positive error-vs-axis-ratio trend.

## Required analyses before drafting

These are submission gates, not optional upgrades.

### A. Establish that the reconstruction is non-trivial

- Compare the curved reconstruction with at least four declared baselines: median-point tangent,
  constant-total-mass curve, pooled-catalog $q$ marginal, and a shuffled-event $q$ marginal.
- Quantify how much accuracy comes from the event's own $q$ marginal. Report the degradation when it is
  replaced by a pooled or shuffled marginal.
- Perform a cross-waveform test where possible: use waveform family A's median $\mathcal M_c$ and $q$
  marginal to predict waveform family B's measured axis, then reverse A/B. This is the strongest available
  answer to the same-posterior circularity objection.
- State the compression honestly: the full two-dimensional posterior is reduced to one scalar plus one
  one-dimensional marginal, not to source medians alone.

### B. Put uncertainty on every angle

- Bootstrap posterior samples to obtain an uncertainty for $\psi_{\rm meas}$ and $\psi_{\rm curve}$.
- Score both raw angular error and uncertainty-normalized residual.
- Show coverage or a posterior-predictive calibration: how often does the reconstructed angle lie within the
  bootstrap 68% and 95% intervals?
- Replace the hard $\mathrm{axr}\ge3$ presentation with a threshold-sensitivity curve over a declared range.
  Keep $\mathrm{axr}\ge3$ as the locked primary score, but show that the conclusion is not threshold-tuned.

### C. Audit the coordinate and frame dependence

- Repeat the primary result in detector-frame masses. Source-frame masses introduce redshift uncertainty
  that can correlate with the mass samples.
- Report what happens in $(\log m_1,\log m_2)$ and $(\mathcal M_c,q)$ coordinates. The angle need not be
  invariant; the point is to identify exactly which statement is stable.
- Define the modulo-$180^\circ$ convention and the behavior near a round covariance explicitly.
- Do not use the phrase "unique information metric" unless an actual Fisher-Rao quantity is computed.

### D. Separate event independence from pipeline independence

- O4a and O4b contain disjoint events, but share detector calibration, waveform families, priors, and LVK
  analysis conventions. Call them **disjoint event catalogs**, not fully independent experiments.
- Document the preregistration timestamps and immutable decision rules for the two out-of-sample scores.
- Report results by waveform family and release pipeline, not only by the preferred/largest posterior group.

### E. Re-test the precision law before including it

E42 measured the SNR slope and a partial correlation with chirp mass; it did not directly establish
$\sigma_{\mathcal M}/\mathcal M\propto\mathcal M^{5/3}/\mathrm{SNR}$. Inclusion requires the multivariate fit

$$
\log\frac{\sigma_{\mathcal M}}{\mathcal M}
=b_0+b_\rho\log\rho+b_M\log\mathcal M+\epsilon,
$$

with uncertainties and tests of $b_\rho=-1$ and $b_M=5/3$, plus an out-of-sample catalog check. Control for
$f_{\rm low}$ or waveform duration if they differ across releases. If this is not completed, remove the
precision law from the paper rather than presenting a correlation as an exponent measurement.

## Manuscript structure

| Section | Content | Evidence | Status |
|---|---|---|---|
| 1 | Introduction: can a 2D mass posterior's orientation be reconstructed from its dominant measured combination? | literature audit | verify full text |
| 2 | Operational definitions, coordinate convention, curved reconstruction, and baselines | E40/E65 methods | rewrite |
| 3 | Training-catalog diagnosis: tangent failure and curved reconstruction | E40/E65 | results exist |
| 4 | Locked validation on disjoint O4a and O4b event catalogs | E67/E71 | results exist |
| 5 | Non-triviality: pooled/shuffled marginals and cross-waveform prediction | new required battery | not run |
| 6 | Uncertainty, threshold, frame, and parameterization robustness | new required battery | not run |
| 7 | Discussion: posterior compression, rapid diagnostics, and strict limits | synthesis | to write |
| A | Optional effective-exponent diagnostic, explicitly not a GR test | E78/E79 | demote |
| B | Optional precision law only after direct coefficient fit and validation | E42 successor | gated |

## Figures

1. **Mechanism:** representative elongated posteriors with measured PCA axis, median-point tangent, and
   curved reconstruction. Include one failure/borderline case; do not show only successes.
2. **Out-of-sample result:** event-level angular errors for GWTC-3, O4a, and O4b, with raw and
   uncertainty-normalized summaries.
3. **Non-triviality:** event-$q$ reconstruction against pooled-$q$, shuffled-$q$, tangent, and total-mass
   baselines.
4. **Robustness:** threshold curve plus cross-waveform and detector/source-frame comparisons.

Every plotted number must be loaded from `results/*.json`; no hand-transcribed result tables.

## Literature and novelty checks

- Verify Hannam et al. 2013, Ohme et al. 2013, `simple-pe`, and related rapid-PE papers at full-text level.
- Search specifically for posterior reconstruction from one-dimensional marginals, not only plots of
  constant-$\mathcal M_c$ contours.
- Maintain VERIFIED / UNVERIFIED labels in [NOVELTY.md](NOVELTY.md).
- Replace ornamental references to principal curves, sloppy models, Backus-Gilbert theory, Bernstein-von
  Mises, and Cencov with only the mathematics actually used in the derivation.

## Explicitly outside this paper

- E47's catalog-level no-hair combination.
- E68 PTA degeneracy sliding.
- E78/E79 as a claimed test of GR.
- E85/E87 ringdown prior-domination and validation.
- E88 overtone evidence and its injection study. The injection result currently uses one off-source stretch
  and one reference phase for the absorption table; it needs a larger phase/noise ensemble and a complete
  detector-response model before a standalone methods claim. Coleman & Finch leave the narrow Bayesian
  pinned-remnant versus marginalized-remnant evidence comparison open, but they do vary the remnant in
  their least-squares studies. Dey et al. (arXiv:2605.18595) already sample remnant mass, spin, amplitudes,
  phases, and extrinsic parameters jointly on GW250114; they find same-$(\ell,m)$ amplitude ratios relatively
  robust to sky treatment. Therefore the verified gap is the isolated *size* of remnant--overtone evidence
  absorption, not full joint inference, and sky position is not yet established as the cause of E88's flat
  real-data systematic.
- E89 mass-spin population trends and selection-bias demonstrations.
- Black-hole matter, echoes, quantum-gravity, or other speculative physics not measured by this analysis.

## Submission criterion

Draft the manuscript only after gates A-D pass. The paper succeeds if it demonstrates a useful,
out-of-sample posterior reconstruction that beats honest baselines and survives cross-waveform transfer. It
does not need to be a new test of GR. A narrower true claim will be substantially harder for a referee to
dismiss than a broad claim assembled from several unrelated analyses.


---

## Reproducibility status (2026-07-21, appended)

| gate | artifact | status |
|---|---|---|
| A | `results/e95_gate_regeneration_results.json` (via `src/e94`,`src/e95`) | **reproducible** |
| B | `results/e92_curve_uncertainty_results.json` (`src/e92`) | **reproducible**; coverage language removed; signed residual NOT significant in O4b |
| C | `results/e95_gate_regeneration_results.json` | **reproducible**; mediation only *consistent with*, not established |
| D | `results/e95_gate_regeneration_results.json` | **reproducible** (per-family sweep); E67 prereg lock not publicly timestamped |
| E | `results/e93_precision_law_results.json` (`src/e93`) | **NOT PASSED — exploratory**; post-hoc mass split unresolved |

`results/e94_posterior_cache.npz` (100 MB) is gitignored and regenerable via `python3 src/e94_build_posterior_cache.py`
(~284 s, one HDF5 pass). Its manifest IS committed. No other module touches HDF5.

Still without any committed artifact: the arc-varying **thickness mechanism** (in-sample explanatory fit only).
