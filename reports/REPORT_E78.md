# E78 lab notebook - a posterior-geometry test of GR: the inspiral mass-combination exponent = 0.616 +/- 0.011 (GR: 0.600)

**EXPLORATORY / POST-HOC** (developed and run on O4b in a single pass; labelled as such per WORKFLOW.md -
NOT a blind-locked out-of-sample test). It grew directly out of E71/E72: since the (m1,m2) posterior
orientation is a lawful, zero-parameter function of the constant-chirp-mass curve, we can INVERT that law
and ask which chirp-mass exponent the geometry actually prefers - a test of GR done through posterior
geometry rather than waveform-template fitting.

## The idea
The E71 curve m1(q) = Mc (1+q)^(1/5) q^(-3/5) has exponents fixed by the 0PN inspiral phase
(phase ~ Mc^(-5/3), Mc = (m1 m2)^(3/5) (m1+m2)^(-1/5)). Generalize to a one-parameter mass family
Mc_p = (m1 m2)^p (m1+m2)^(1-2p), with GR at p = 3/5 = 0.600, and MEASURE p from the posterior orientation.
Key property: orientation is SCALE-FREE - m1(q;p) ~ q^(-p) (1+q)^(2p-1), the Mc prefactor cancels - so the
fit isolates the exponent from the mass scale. A deviation from 0.600 would signal modified inspiral
phasing (dipole radiation, varying-G, anomalous PN mass-dependence).

## Result (32 elongated O4b events, axr>=3)
| quantity | value |
|---|---|
| **p_hat (geometry-fit exponent)** | **0.616 +/- 0.011 (stat, bootstrap) +/- 0.004 (waveform syst)** |
| GR value | 0.600 |
| consistency | **1.3 sigma - CONSISTENT with GR** |
| estimator bias (injection at GR) | +0.0002 (UNBIASED) |
| waveform-family means | SEOBNRv5PHM 0.619, IMRPhenomXPHM-SpinTaylor 0.613, IMRPhenomXPNR 0.610 |

A ~2%-precision confirmation of the GW inspiral's leading mass-combination exponent, from posterior
geometry alone, with no waveform-template fitting.

## Validation (why the +0.016 is not an artifact)
- **Injection recovery**: synthetic GR (p=0.6) posteriors built on the events' own q-marginals with
  perpendicular width tuned to each event's measured axr are recovered at p_hat=0.600 (bias +0.0002);
  p=0.55 -> 0.550 and p=0.65 -> 0.651. The estimator is unbiased.
- **Waveform systematic is negligible** (spread +/-0.004 across families): although per-event psi_meas
  moves ~3 deg across waveforms (E72), that scatter is INCOHERENT and averages out of the catalog mean.
- **5 contract tests** (tests/test_e78_exponent.py): p=0.6 reproduces the E71 curve exactly; scale-
  invariance; injection recovery over p in [0.50,0.70]; monotone, >3 deg sensitivity (the test has power:
  dpsi/dp ~ 30 deg/unit p); determinism. Full suite 32/32.

## Interpretation
The measured exponent 0.616 +/- 0.011 agrees with the quadrupole-formula value 3/5 at 1.3 sigma - no
evidence for modified inspiral phasing (dipole radiation etc.). This is a genuinely independent test of
GR: it uses the geometry of the mass posterior as the observable and shares NONE of the machinery of the
LVK parameterized-deviation pipeline (E46). Its value is that independence, not raw sensitivity.

## Honesty / limits
- **A cross-check, not a more-sensitive probe.** The direct LVK -1PN dipole bounds constrain modified
  inspiral phasing far more tightly; E78 is a methodologically independent, physics-blind confirmation,
  not a competitor. Frame it that way.
- **O4b-only.** The preregisterable successor (below) is cross-catalog reproducibility.
- **Prior dependence.** The q-marginal carries the release's mass prior; a different prior shifts the
  q-distribution and could bias p_hat. Not yet controlled - a residual systematic to quantify.
- **The E71 law-residual floor.** The curved law itself has a ~1.2 deg intrinsic residual (finite width /
  higher-order geometry), i.e. ~0.04 in p per event. The Gaussian injection validates against symmetric
  width but would NOT catch a COHERENT non-Gaussian residual; the small +0.016 offset is at the level of
  the law's own imperfection and is NOT claimed as physics.

## Successor prediction (preregisterable)
Locked estimator, to run when GWTC-3 and GWTC-4/O4a are re-scored: the geometry-fit exponent is
REPRODUCIBLE across GWTC-3 / O4a / O4b and equals 0.600 within errors. A coherent, catalog-consistent
departure would be the real signal; a per-catalog scatter consistent with 0.600 confirms GR and closes it.

Code: src/e78_geometric_gr_exponent.py. Numbers: results/e78_geometric_gr_exponent_results.json.
Tests: tests/test_e78_exponent.py. Data: data/chains/gwtc5/ (gitignored). Builds on locked E71 residuals.
