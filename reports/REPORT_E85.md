# E85 lab notebook - Bayesian ringdown of GW250114: Kerr-consistent, honestly wide, and three defeated artifacts

> **RETRACTED - SUPERSEDED BY E87 (`reports/REPORT_E87.md`). Do not cite the numbers below.**
>
> The posterior reported here was **prior-dominated**: the entire 160-340 Hz grid sat within 4 lnL, so the
> "90% CI" [167, 333] was the grid, not a measurement, and it was statistically indistinguishable from no
> signal at all. Two defects in the noise covariance (a destructive ACF taper and a broadband-scaled ridge)
> destroyed ~33x of matched-filter SNR. Every "wide but Kerr-consistent" reading below is therefore
> vacuous: the IMR remnant fell inside the interval because *everything* did, and the apparent start-time
> stability was a flat surface, not a stable peak. The tell was that adding L1 to H1 failed to tighten the
> posterior. E87 fixes the covariance and passes the validation gate against LVK's own pyRing posteriors
> (median offset 2.0 Hz over 2M-18M). The machinery described below - analytic amplitude/phase
> marginalization, the Kerr inversion, and the truncation that defeats acausal whitening leakage - is
> sound and is reused unchanged in E87.

**CHARACTERIZATION (no prereg; a measurement with credible intervals).** The Bayesian layer over the E83
strain pipeline, built from scratch and applied to GW250114's ringdown: posterior on (f, tau) for the 220
mode -> mapped through the Berti-Cardoso-Will fits to a ringdown-ONLY (Mf, af) posterior -> compared to
the inspiral-derived IMR remnant. The final likelihood is the TRUNCATED time-domain form (pyRing-style):
the analysis window is compared to the model under the empirical noise autocovariance (Toeplitz C from the
off-source ACF, Cholesky solves), with amplitude+phase marginalized ANALYTICALLY (they are linear
parameters) and the (f, tau) posterior computed EXACTLY on a grid - deterministic, ~1 s per fit.

## Result (H1-only, 220-only, 40 ms window)
| start time | f220 [Hz, 90%] | tau [ms, 90%] | ringdown-only Mf_det [Msun] | af | IMR inside 90%? |
|---|---|---|---|---|---|
| peak+3 ms | 253.9 [167, 333] | 2.3 [0.9, 11.8] | 78.8 [45, 122] | 0.87 [0.19, 0.98] | **YES** |
| peak+5 ms | 256.1 [169, 333] | 2.5 [0.9, 11.9] | 78.6 [46, 122] | 0.87 [0.18, 0.98] | **YES** |

- **Start-time STABLE** (254 vs 256 Hz) and the median sits right at the IMR-Kerr prediction (248.6 Hz).
- The **IMR remnant (68.4 Msun, 0.679) lies inside the ringdown-only 90% credible region** - the no-hair
  consistency check, closed with our own machinery, at the precision a single-detector single-mode
  truncated segment actually supports (ringdown SNR ~ 6 at peak+3 ms; hence the wide intervals).
- Kerr-valid fraction of the posterior 44-47% (the rest is the low-Q noise region of the prior - reported,
  not hidden).

## The build story: three artifacts found, diagnosed, and regression-guarded
1. **Amplitude prior excluded the truth.** First MCMC run produced zero Kerr-valid samples; a raw-strain
   amplitude check showed the ringdown peak is ~2e-21 while the prior floor was 1.1e-20. (Guard: priors
   now bracket the measured amplitude scale.)
2. **Sampler missed a narrow 4-D mode.** After the prior fix, chains settled 9 lnL below the E83 point -
   a convergence failure diagnosed by direct likelihood comparison. Fix: amplitude+phase are LINEAR, so
   they are marginalized analytically and (f, tau) is gridded exactly - no sampler in the headline path.
   (The Goodman-Weare ensemble sampler stays in the module, contract-tested on a known Gaussian.)
3. **Whiten-then-window acausal leakage (the important one).** With the exact grid, the fit became
   PRECISELY wrong: narrow modes at 192 Hz (start+3 ms) vs 273 Hz (start+5 ms) - start-time UNSTABLE and
   excluding Kerr. Mechanism: whitening is an acausal filter; the 388-sigma merger 3 ms before the window
   rings FORWARD through the PSD structure into the analysis window, manufacturing narrow fake features.
   This is exactly why real ringdown pipelines use truncated time-domain likelihoods. Fix: the
   autocovariance likelihood above. (Regression test: a 500x-noise burst ending 1 ms BEFORE the window
   must produce a flat likelihood surface - it now does; a genuine in-window ringdown does not.)

## Verification
- 6 contract tests (tests/test_e85_bayes.py): ensemble sampler recovers a known 2D Gaussian; BCW Kerr
  inversion roundtrips (Mf, af) <-> (f, tau) to 1e-6 and rejects unphysical Q; end-to-end grid injection
  recovery (f to <5 Hz, tau to <35%); the marginal-lnL surface peaks at the injection; and the
  pre-window-burst leakage regression. Full suite 56/56.
- Start-time robustness on the real event (3 vs 5 ms: medians shift ~2 Hz).
- The truncated likelihood reproduces the expected ringdown SNR (~6) given the E83 point estimate.

## Honesty / limits
- H1 only (no L1 coherent combination), 220 only (no overtone - the published 99.9% overtone claim uses
  orthonormal multi-mode fits on multi-detector data), fixed start times (no start-time marginalization),
  flat amplitude prior. The +-80 Hz width is the honest cost of those simplifications.
- "IMR inside 90%" at this precision is a weak consistency statement, not a competitive no-hair bound; the
  value is that the ENTIRE chain (strain -> conditioning -> truncated likelihood -> Kerr inversion) is
  ours, verified, and artifact-hardened.
- The empirical-ACF taper and diagonal jitter are pragmatic positive-definiteness devices; a Welch-PSD
  circulant embedding would be the polished alternative.

## Successor
(1) Add L1 + coherent network likelihood; (2) add the 221 overtone basis (4 linear amplitudes - same
analytic marginalization); (3) start-time marginalization; then the overtone-significance and area-theorem
questions become addressable with our own pipeline - and only then the exotic-echo class, with this
truncated likelihood as the artifact-safe foundation.

Code: src/e85_bayesian_ringdown.py. Numbers: results/e85_bayesian_ringdown_results.json.
Tests: tests/test_e85_bayes.py. Data: data/strain/ (gitignored). Builds on E83/E74.
