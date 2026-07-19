# E82 lab notebook - the GW inference manifold: the whole catalog as one geometric object

**CHARACTERIZATION / exploratory (post-hoc analysis of the existing O4a+O4b catalog; no blind test, no
prereg).** Radical idea #1 made concrete: treat all 190 events' (m1,m2) posteriors as ONE geometric
object -- each a Gaussian N(mu, Sigma), the catalog the cloud of them, with the 2-Wasserstein distance
(location term |dmu|^2 + Bures shape term) as the posterior-to-posterior metric -- and ask whether the
measurement law (E71) removes a dimension of it, leaving the population as the residual.

## Result
1. **Location vs shape.** 95% of the total posterior-to-posterior distance is LOCATION (where events sit
   = the population mass function), 5% is SHAPE (the measurement ellipses).
2. **Orientation is slaved to location by the law.** The curved law predicts each ellipse's orientation
   from its location to median 1.26 deg (E71), and that residual is physics-blind (E72). So orientation
   carries ~0 information independent of location -- it is NOT an independent axis of the manifold.
3. **Effective dimensionality collapses.** Classical MDS of the manifold gives variance 97% / 3% / 0% in
   the top three axes; the participation-ratio effective dimensionality is **1.07** (naive per-event DOF
   = 5). Axis 1 is the POPULATION (|Spearman| 0.99 with chirp mass); the thin axis 2 is PRECISION
   (|Spearman| 0.51 with elongation). Orientation appears nowhere as an independent axis.

**Verdict: the catalog of black-hole mergers, as one geometric object, is essentially a population
sequence (chirp mass) dressed with a thin, law-determined measurement structure. Subtract the law and the
population remains -- population and measurement are geometrically separable, and here separated.**

## Honest reading (what is trivial vs what is not)
- The **95%/5% split and the effective-dimensionality ~1 are mass-range-dominated**, hence partly trivial:
  the catalog spans M_c ~ 5-60 M_sun, so of course events are far apart in location and the location term
  swamps the shape term. This is NOT the deep content and is not oversold.
- The **non-trivial result is the dimensionality COLLAPSE within the description**: a 2D Gaussian has 5
  degrees of freedom per event (mu:2, Sigma:3 = orientation, elongation, scale), but the catalog's
  geometric description needs far fewer, because **the E71 law slaves orientation to location** -- it is
  a deterministic function of the population coordinate, not free. The genuine axes are POPULATION
  (mass function) + PRECISION (SNR-driven elongation), with orientation supplied for free by the law.
- This is the rigorous, catalog-level form of the program's central thesis (E71 orientation = law(location);
  E72 residual physics-blind): the measurement optics occupy -- and remove -- exactly one geometric axis.

## Verification
- 4 contract tests (tests/test_e82_manifold.py): the Bures closed form matches a scipy.linalg.sqrtm
  computation to 1e-8; self-distance is zero; classical MDS recovers the true dimensionality of synthetic
  2D and 1D point sets. Full suite 41/41.
- The orientation-slaving number (median 1.26 deg) reproduces the locked E71/E67 residual exactly.
- 2-Wasserstein = location + Bures is a proper optimal-transport metric between Gaussians (closed form,
  exact for 2x2).

## Honesty / limits
- Gaussian approximation to each posterior (mean + covariance); real posteriors are mildly non-Gaussian,
  so the manifold is an approximation. The banana curvature (E71) is a within-event non-Gaussianity not
  captured by a single Gaussian -- a known limitation, and itself the reason orientation is interesting.
- Mass plane only. The full claim ("subtract measurement, get the population") should be tested in the
  full parameter space.
- Post-hoc / exploratory: this is an analysis of committed results, framed as such, not a locked test.

## Successor
Repeat the manifold construction in the FULL intrinsic parameter space (add spin, distance, inclination)
using the Fisher-Rao metric (idea: the sloppy-spectrum program, the deferred E80 prereg) to separate
population from measurement across ALL parameters, not just the mass plane -- and quantify how many
genuine population axes the catalog supports.

Code: src/e82_inference_manifold.py. Numbers: results/e82_inference_manifold_results.json.
Tests: tests/test_e82_manifold.py. Reuses E67+E71 per-event records + the O4a/O4b posterior samples.
