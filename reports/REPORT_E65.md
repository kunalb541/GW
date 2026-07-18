# E65 lab notebook - the E40 mass-plane law derived: locked Fisher-rotation REFUTED, curvature is the real story

Prereg: preregs/E65_pn_fisher_rotation_prereg.md (locked before running). Question: can the E40
empirical law (the (m1,m2) posterior lies along the constant-chirp-mass tangent, median |dpsi| 7.5
deg over 75 events) plus its residual pattern (heavy events fail, total-mass wins) be DERIVED from
PN Fisher geometry - the hypothesis being a rotation from the constant-Mc tangent toward the
constant-Mtot tangent as the merger-band information share grows with detector-frame total mass?

Model (locked): two-direction Fisher mixture Gamma = Wc*g_c g_c^T + kappa*Wt*g_t g_t^T, with
Wc = 0PN lnMc phase Fisher over the inspiral band [20 Hz, f_ISCO], Wt = merger-band SNR^2
[f_ISCO, 4 f_ISCO], analytic aLIGO PSD (Ajith 2011 fit), f_ISCO = 4397 Hz/(Mt_det/Msun).
One global constant kappa fit ONLY on the 14 locked E40-prereg events (kappa* = 6.31), frozen,
then scored out-of-sample on the remaining 61. Detector-frame medians from the local PE files
(75/75 present; transient errno-60 disk stall on GW191129 handled by retry - same failure class
as E43's, caught before it could silently drop an event).

## Locked outcomes

| decision (locked) | threshold | outcome |
|---|---|---|
| D1 out-of-sample: mixture beats pure-chirp tangent (n=61) | median smaller | PASS - marginal (7.45 vs 7.72 deg) |
| D2 heavy test events (Mt_src>60, n=29): >30% error cut | < 0.7x | FAIL (9.91 vs 9.62 deg - no gain) |
| D3 parameter-free sign test: psi_meas between psi_chirp and psi_total in >=70% (n=48 gated), Spearman(rot_frac, Mt_det)>0.3 | both | FAIL (between-fraction 0.25; Spearman 0.16, p=0.28) |

Per the locked interpretation rule: D3 fail means the E40 residuals are NOT mass-organized
Fisher-mixture structure. The rotation-toward-total hypothesis is REFUTED. E40 stands as empirical.

## What the failure revealed (the D3 table)

The gated events do not sit between the chirp and total tangents - the rotation fractions are
mostly NEGATIVE: light, elongated events overshoot PAST the chirp tangent, on the side AWAY from
constant-Mtot (e.g. GW190728: psi_chirp 149.4, psi_total 135, psi_meas 163.4 -> rot_frac -0.97).
A rotation model cannot produce that sign. What can: the posterior does not lie along the TANGENT
line - it lies along the constant-Mc CURVE, which is convex in (m1,m2); the principal axis of
samples spread along a curved arc is the CHORD, which is rotated off the median-point tangent in
exactly the observed direction, by an amount growing with arc length (the q-range).

## POST-HOC (exploratory, NOT preregistered): the curved law

Zero-free-parameter prediction: psi_curve = principal axis of the constant-Mc curve
m1(q) = Mc (1+q)^(1/5) q^(-3/5), m2 = q m1, evaluated at the event's median SOURCE-frame Mc and
sampled over the event's own q posterior. Uses only {Mc median, q marginal} - no orientation
information from the (m1,m2) covariance.

| set | curved law | tangent (E40) |
|---|---|---|
| all 75 | 4.85 deg | 7.49 deg |
| elongated (axr>=3, n=28) | **0.81 deg** | 4.68 deg |
| head-to-head wins | 43/75 | - |

For every well-measured (elongated) posterior the curved law is essentially exact: the median
residual drops from 4.68 to 0.81 deg - a 6x improvement, with GW190728's 14-deg "violation"
reproduced to 1 deg. The E40 residual-vs-elongation anticorrelation (Spearman -0.42, re-confirmed
here) was never evidence of a second physical direction: round posteriors have ill-defined psi
(large scatter), elongated ones follow the curve (small tangent error, near-zero curve error).

## Reading

- The mass-plane geometry of GW posteriors is even MORE lawful than E40 claimed, but the law's
  correct form is "the posterior IS the constant-Mc curve, thickness ~0, extent set by the q
  marginal" - not "the long axis is the tangent at the median".
- The tangent's residuals were curvature artifacts (chord vs tangent), not new information about
  a second measured direction; the locked attempt to explain them as inspiral/merger Fisher mixing
  is refuted by its own sign test (D3), which is the outcome the parameter-free test was built for.
- Honest status: the curved law is POST-HOC on these 75 events. It is the natural out-of-sample
  prediction for GWTC-4 (O4a events, disjoint): median |psi_curve - psi_meas| < 2 deg for
  elongated events. That prediction is on record here before any GWTC-4 data is touched.
- D1's marginal pass (0.27 deg) is not evidence for the mixture: with D2/D3 failed, it reflects a
  small average rotation absorbed by kappa, not the hypothesized mass-dependent structure.

## Contract tests

tests/test_e65_fisher_rotation.py (5 pass): kappa->0 recovers the chirp tangent and kappa->inf the
total tangent exactly; mod-180 angle conventions; Fisher weights positive with the correct mass
trend (heavier -> relatively more merger information); and the chord-vs-tangent rotation grows with
arc length (the mechanism behind the post-hoc finding). Headline numbers independently re-derived
from the results JSON + a by-hand recomputation of GW190728's psi_curve (162.33 both paths).

Code: src/e65_pn_fisher_rotation.py. Numbers: results/e65_pn_fisher_rotation_results.json.
