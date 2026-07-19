# E72 preregistration — GW geometry outlier atlas (where does the chirp-curve law break?)

**STATUS: DRAFT — to be LOCKED (committed) BEFORE any residual↔axis correlation is computed.**
As of locking, only the E71/E67 curve residuals exist; NO correlation between residual and any
physical/systematic axis has been looked at. This prereg fixes the axes, the multiple-comparison
control, and the decision rules in advance — an 8-axis search is a look-elsewhere machine otherwise
(the E47/E58 false-alarm lesson, WORKFLOW.md).

## Question
Among events where the curved chirp-mass law's residual is *well-defined*, does the residual
correlate with any physical property or systematic — i.e. is there a source class where the
zero-parameter geometry (E65/E67/E71) stops being sufficient? Output an **anomaly atlas + candidate
flags**, NOT a new-physics claim (user framing: "not 'we found PBHs,' a clean geometry anomaly score").

## Sample (locked)
The **32 elongated O4b events** (axis_ratio ≥ 3) from E71 (results/e71_gwtc5_curved_law_results.json).
Rationale: `err_curve` = |ψ_curve − ψ_meas| is only meaningful where the posterior has a defined
orientation; E71 documented that the largest *raw* residuals are all near-round (axr≈1) posteriors —
an orientation artifact, not physics — so those are excluded by the same axr≥3 gate D1 uses. O4a
extension (E67's 19 elongated events) is a declared future option requiring the GWTC-4 re-download
(14.6 GB); NOT in this locked run.

## Metric (locked)
Per elongated event, the residual `r = err_curve` (from the LOCKED E71 results; not recomputed).

## Axes (pre-declared, K=9; computed from the event's picked-group posterior samples)
1. `chi_p` (precession) — median
2. `chi_eff` (aligned spin) — median; also |chi_eff|
3. `mass_ratio` q — median
4. `redshift` — median
5. loudness — `network_matched_filter_snr` median if present, else quadrature sum of per-detector
   `*_optimal_snr` medians (the proxy actually used is recorded)
6. `chirp_mass_source` — median
7. `total_mass_source` — median
8. `mass_2_source` — median (NSBH / mass-gap proxy; also record a flag m2 < 5 M⊙)
9. `waveform_disagreement` — stdev of ψ_meas across the event's available waveform families (deg)

**Out of scope (declared): eccentricity and higher-mode content** — absent from the released O4b
posterior columns; would require dedicated reanalyses. Not tested; not counted in K.

## Decision rules (LOCKED)
- **D1 (correlation, exploratory).** For each of the K=9 axes, Spearman ρ(r, axis) over the 32 events,
  with **Benjamini–Hochberg FDR at q = 0.05** across the K axes. ALSO partial-Spearman of (r, axis)
  **controlling for axis_ratio** (the E71-documented confound). An axis is a **CANDIDATE** only if it
  survives BH-FDR *and* its partial correlation keeps the same sign with |ρ_partial| ≥ 0.3. Report all
  ρ, p, q_BH, ρ_partial; list surviving axes (expected: none — this is a search, not a hypothesis).
- **D2 (outliers).** Flag any elongated event with r above the **Tukey upper fence** Q3 + 1.5·IQR
  (fence computed on the 32 residuals). List flagged events with all axis values. If none: record
  "no curve-law outliers among O4b elongated events" (a clean null strengthening claim 1).
- **D3 (coherence lens on any D2 flag).** For each flagged event, recompute ψ_meas across ALL its
  waveform families; if the across-waveform spread ≥ r, classify **SYSTEMATIC** (waveform-driven, per
  the E59 coherence rule); else **CANDIDATE-physics** (waveform-coherent anomaly worth follow-up).

## Honesty commitments
- N = 32 is low power for a 9-axis search; BH-FDR + the partial-correlation + coherence gates are
  there precisely so a chance correlation is not sold as a discovery. A null is the expected, honest,
  and paper-useful outcome ("the law holds uniformly across O4b source classes within our power").
- No naive cross-event products; per-event axis values only.
- The axr≥3 gate and the axr partial-control together remove the trivial round-posterior residual
  inflation (E71). No event silently dropped: any elongated event missing an axis column is listed.
- Seed 72 (bootstrap CIs, if reported, use seed 72; main correlation path has no RNG).

## Verification plan
Contract tests tests/test_e72_*.py: (null) a random axis is not flagged above the FDR false-positive
rate; (injection) an axis built to correlate with r is recovered; (FDR) BH on known p-values gives the
known rejection set; (partial) an axis that is a pure function of axr loses its spurious correlation
after partialling axr; (Tukey) a known outlier is fenced, an inlier is not. Plus independent
re-derivation of every D1 ρ and the D2 fence through a second code path.
