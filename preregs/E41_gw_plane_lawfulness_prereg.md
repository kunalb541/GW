# E41 preregistration — which GW posterior planes are geometrically lawful?

Status: LOCKED. Date 2026-07-07. Extends E40 (m1-m2 chirp-mass law) to all 6 GW planes.

## Setup

E38 computes, per plane and per event, the WITHIN-EVENT posterior correlation rho and the
raw-coordinate ellipse angle psi. rho is scale-free; psi is scale-dependent (dominated by the
larger-variance axis when the two axes have mismatched natural units). Test target = the
scale-free rho SIGN, predicted a priori from compact-binary physics.

## Locked a-priori predictions

Derived by 6 independent physicist agents (blind to the measured rho values) and adversarially
verified by 6 more (which corrected two of the derivations). FINAL locked predicted rho sign
and whether raw psi is a units artifact for that plane:

| plane | predicted rho sign | raw psi units-artifact |
|---|---|---|
| m1_m2 (mass_1_source, mass_2_source) | negative | no (comparable scales) |
| chirp_q (chirp_mass_source, mass_ratio) | positive | yes |
| q_chieff (mass_ratio, chi_eff) | negative | no |
| Mf_af (final_mass_source, final_spin) | indeterminate | yes |
| dL_cosi (luminosity_distance, cos_iota) | indeterminate / ~0 linear (curved degeneracy) | yes |
| z_Mtot (redshift, total_mass_source) | positive | yes |

Key mechanisms (locked): m1_m2 = constant-chirp-mass anticorrelation (0PN Mc precise, q poor);
chirp_q = population/measurement structure (weak positive); q_chieff = 1.5PN chi_eff-q
anticorrelation; dL_cosi = amplitude A ~ f(cos i)/dL with f even in cos i -> strong but CURVED
(nonlinear) degeneracy, so LINEAR rho ~ 0; z_Mtot = predicted positive (measurement effect),
NOTE the algebraic M_source=M_det/(1+z) term is negative and opposes this.

## Decision rules (LOCKED, per plane)

Measured = median within-event rho over the ~75 events + fraction of events with each sign.
- predicted pos/neg -> HIT if measured majority (>=60% of events) has the predicted sign AND
  |median rho| >= 0.15. MISS if measured majority is the opposite sign. WEAK if same sign but
  |median rho| < 0.15 or majority < 60%.
- predicted indeterminate/~0 -> HIT if |median rho| < 0.15 (correctly no linear correlation);
  SIGNAL-MISSED if |median rho| >= 0.15 (there was structure the prediction did not call).

## Interpretation contract

Count HITs. The thesis (from E34/E35/E40): geometry is lawfully predictable where ONE physical
mechanism dominates; it fails where competing effects or units dominate. A mixed scorecard
(some HIT, some MISS) is the expected and honest outcome and directly maps the lawfulness
landscape. No result is massaged: a wrong-sign prediction (e.g. z_Mtot) is reported as a MISS.

## Provenance

results/e38_gw_black_hole_geometry_results.json (76 events). No new data. No RNG.
Predictions from workflow wf_a602622a-b52 (12 agents), agents blind to measured rho.
