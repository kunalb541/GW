# E72 preregistration — the second-order curvature law and what the residual knows (LOCKED 2026-07-18)

**Question.** E65/E67 established that the (m1,m2) posterior lies along the constant-Mc CURVE
(median 0.8–1.3 deg residual on elongated events). E72 upgrades the law to second order and asks
what physics the remaining residual carries:
(A) the tangent-vs-curve ROTATION should be a per-event zero-free-parameter prediction (not just
a median improvement), driven by the q-marginal's width through the curve's geometry;
(B) the residual AFTER the curve (psi_meas − psi_curve) should carry the sub-leading physics —
the 1.5PN spin–mass-ratio degeneracy: the measured phase combination bends with chi_eff, so
events with larger |chi_eff| should show larger residuals (the principal-curve-vs-Mc-curve
deviation, in the pasted framework's language).

## Data
Per-event angles reused UNCHANGED from the results of record: results/e65_*.json (GWTC-3, 75
events: psi_meas, psi_chirp = tangent, psi_curve, axr) and results/e67_*.json (GWTC-4, 86 events:
same fields). One new HDF5 pass extracts per-event q-marginal stats (sigma_q, skewness) and
chi_eff stats (mean, sd) from the same datasets those batteries used. No angle is recomputed.

## Decision rules (LOCKED)
Signed angles: rot_meas = wrap(psi_meas − psi_tangent), rot_pred = wrap(psi_curve − psi_tangent),
resid = wrap(psi_meas − psi_curve), wrap = shortest signed arc, degrees.
Elongated set = axr >= 3 (both catalogs pooled; expected n ~ 47).

- **D1 (per-event law).** On the elongated set: least-squares slope of rot_meas on rot_pred in
  [0.8, 1.2] AND R^2 > 0.8. (E67 tested medians; this locks the per-event proportionality with
  slope fixed at unity by theory.) PASS/FAIL.
- **D2 (mechanism scaling).** |rot_pred| against sigma_q on the elongated set: log–log regression
  explains R^2 > 0.6 and the fitted power's 95% bootstrap CI excludes 0 (rotation is q-width
  driven). The fitted power is REPORTED with its CI (second-order geometry suggests ~2 for
  symmetric marginals; skewness can pull it toward 1 — both stated up front, no lock on the
  value). Adding q-skewness as a second regressor: report delta-R^2. Descriptive verdict.
- **D3 (the residual knows chi_eff).** Partial Spearman of |resid| vs |mean chi_eff|,
  controlling 1/axr (roundness confound), on the elongated set:
  rho >= 0.30 with p < 0.01 -> 1.5PN-bending CONFIRMED as the residual driver;
  |rho| < 0.15 -> REFUTED (residual is noise/other systematics); between -> inconclusive.
- **D4 (contract).** Synthetic curve samples with symmetric q-marginal: recovered rotation
  matches the generated chord-vs-tangent rotation; zero-width marginal -> zero rotation;
  wrap conventions exact. Pytest.

## Honesty commitments
- D1 reuses angles from committed results (no re-derivation freedom); the new measurement is
  only the q/chi_eff moments — column names recorded, events missing fields listed.
- The chi_eff hypothesis in D3 is directional in SIZE only (|resid| vs |chi_eff|); the SIGN
  structure is exploratory (reported, not decided) because deriving it at 1.5PN with precession
  is model-dependent.
- Elongation gate reused from E40/E65/E67 (same control logic); pooled-catalog Spearman assumes
  exchangeability across catalogs — GWTC-3-only and GWTC-4-only splits reported as robustness.
- Seed 72 (bootstrap CIs only).
