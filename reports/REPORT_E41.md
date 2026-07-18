# E41 lab notebook - which GW posterior planes are geometrically lawful?

Prereg: preregs/E41_gw_plane_lawfulness_prereg.md. Extends E40 (m1-m2 chirp-mass law) to all 6
GW planes. Locked a-priori rho-sign predictions from 6 independent physicist agents (blind to
measured values) + 6 adversarial verifiers (workflow wf_a602622a-b52), tested against measured
WITHIN-EVENT rho across 76 LVK events.

## Scorecard: 3/6 HIT

| plane | predicted rho | measured med rho | pos/neg frac | verdict |
|---|---|---|---|---|
| m1_m2 | negative | -0.51 | 0.04/0.96 | HIT |
| chirp_q | positive | +0.26 | 0.84/0.16 | HIT |
| dL_cosi | ~0 linear (curved) | -0.01 | 0.45/0.52 | HIT |
| q_chieff | negative | +0.06 | 0.56/0.44 | WEAK |
| Mf_af | indeterminate | +0.22 | 0.81/0.19 | SIGNAL-MISSED |
| z_Mtot | positive | -0.51 | 0.00/0.99 | MISS (wrong sign) |

## Reading

Physics predicts the scale-free correlation SIGN where ONE mechanism dominates:
- m1_m2 HIT: the constant-chirp-mass anticorrelation (96% of events negative), the strongest
  and cleanest -- also confirmed independently via the psi test in E40.
- dL_cosi HIT: the distance-inclination degeneracy is strong but CURVED (amplitude ~ f(cos i)/dL
  with f even in cos i), so the LINEAR correlation is ~0 -- the derivation predicted exactly
  this "near-zero linear despite a strong nonlinear degeneracy", and the data agree (rho -0.01).
- chirp_q HIT: predicted weak positive, measured +0.26.

It fails or is weak where mechanisms compete or wash out:
- z_Mtot MISS: predicted positive (a population/measurement argument), but measured -0.51 (99%
  of events negative). The naive prediction was BACKWARDS -- the algebraic term M_source =
  M_det/(1+z), which the verifier flagged as opposing the prediction, actually DOMINATES the
  within-event posterior. A clean example of testing-against-data catching a confident-but-wrong
  derivation.
- q_chieff WEAK: the literature chi_eff-q anticorrelation is real but washes out in typical
  low-spin-information events (median rho +0.06, near a 56/44 coin flip); it would need a
  high-spin-informative subset to appear.
- Mf_af SIGNAL-MISSED: the derivation punted to "indeterminate", but there is real positive
  structure (rho +0.22, 81% positive) inherited from the NR mass/spin fits -- a prediction that
  should have been made.

## Methodological finding: raw psi is a units artifact on 4/6 planes

Raw-coordinate psi (E38) is scale-dependent. Measuring the ratio of raw axis widths Wx/Wy:

| plane | median Wx/Wy | psi is | 
|---|---|---|
| m1_m2 | 1.3 | physical |
| q_chieff | 1.3 | physical |
| chirp_q | 11.6 | units artifact (x-dominated, psi~0) |
| Mf_af | 80.9 | units artifact (x-dominated, psi~0) |
| dL_cosi | 860.2 | units artifact (x-dominated, psi~0/180) |
| z_Mtot | 0.02 | units artifact (y-dominated, psi~90) |

Only m1_m2 and q_chieff have comparable axis scales, so only their raw psi encodes the physical
degeneracy direction. For the other four, psi just points along the larger-variance (in raw
units) axis. => E40's use of raw psi was valid ONLY because m1_m2 has same-unit axes; for the
other planes the scale-free rho is the correct target, which is what E41 uses.

## Conclusion (ties the E34-E41 arc together)

Geometric lawfulness is real but plane-specific: posterior correlation structure is predictable
from first-principles physics WHERE a single mechanism dominates (m1_m2 chirp mass; dL_cosi
amplitude curvature) and fails where effects compete (z_Mtot) or wash out (q_chieff). This is
the same lesson as the cosmology nulls (E34/E35): it is the DOMINANCE of one clean physical
combination, not the geometry framework itself, that makes geometry predictable. GW gave one
strong positive (E40, m1_m2) and, at the plane level, a 3/6 map with two instructive failures.

## Caveats

- rho is WITHIN-EVENT posterior correlation; the chirp_q derivation partly argued population
  scatter -- its sign happened to match, but the mechanism attribution is uncertain (verifier
  flagged it "partly_flawed").
- Predictions are sign-level; magnitude was not gated. n~75 events; q_chieff/Mf_af verdicts
  could shift on informative-spin subsets.
- The z_Mtot and Mf_af misses are reported as-is (no post-hoc reinterpretation of the locked
  predictions).
