# Gate A — first measurement (2026-07-21). VERDICT: PASSES, with one mechanism claim demoted.

> **SUPERSEDED IN PART — 2026-07-21.** This note records what was measured when it was written and is
> kept unedited as a record. The numbers it carries as prose have since been regenerated from
> committed artifacts (`results/e95_gate_regeneration_results.json`), and the cross-family transfer moved from 2.08/2.78 to **2.25/2.93** once a proper 300-draw
> permutation null and both transfer directions were stored. The paper quotes the
> artifacts, never this file. See [EXTERNAL_READER_PACKET.md](EXTERNAL_READER_PACKET.md) for the
> table of corrections.


The [revised PAPER_PLAN](PAPER_PLAN.md) sets Gate A as a submission gate: show the curved reconstruction is
non-trivial against declared baselines, quantify how much comes from the event's own $q$ marginal, and run
a cross-waveform transfer test. All three are now measured, using the committed E71 machinery
(`psi_axr_rho`, `tangent_angles`, `curve_psi`) unmodified. Scores are median $|\Delta\psi|$ in degrees.

## A1. Baselines, all three catalogs (elongated, axr $\ge3$)

| catalog | n | own-$q$ | pooled-$q$ | shuffled-$q$ | tangent | const-$M_{\rm tot}$ |
|---|---|---|---|---|---|---|
| GWTC-3 | 28 | **0.80** | 10.02 | 9.40 | 4.68 | 25.28 |
| O4a | 19 | **1.26** | 3.47 | 3.04 | 6.73 | 23.37 |
| O4b | 32 | **1.22** | 3.50 | 6.56 | 4.63 | 17.36 |

The event's own $q$ marginal wins everywhere, by $2.5$–$12\times$ over a pooled or shuffled one. On GWTC-3
a wrong $q$ marginal is *actively harmful* — worse than the tangent, which uses no $q$ information at all —
but that is **catalog-dependent**: in O4a and O4b pooled/shuffled still beat the tangent. So part of the
curve's advantage is generic (a curve is a better model than a tangent) and part is event-specific. Both
parts are real; the earlier GWTC-3-only scout overstated the "actively harmful" framing.

## A2. Cross-waveform transfer — the answer to same-posterior circularity

The strongest available test: use waveform family A's median $\mathcal M_c$ and $q$ marginal to reconstruct
family **B's independently inferred** principal axis. A = IMRPhenomXPHM(-SpinTaylor), B = SEOBNRv4/v5PHM,
pooled over all three catalogs: **246 events with both families, 64 elongated in both** (GWTC-3 17, O4a 16,
O4b 31).

| configuration | all | elongated |
|---|---|---|
| A→A within-family | 6.26 | **0.92** |
| B→B within-family | 4.97 | 1.20 |
| **A→B CROSS-family** | 5.70 | **2.08** |
| **B→A CROSS-family** | 6.66 | **2.78** |
| tangent A→A | 9.01 | 5.51 |
| tangent A→B cross | 7.80 | 3.57 |
| tangent B→A cross | 9.88 | 6.25 |

**The two families' own measured axes differ from each other by 1.99°.** The cross-family reconstruction
error (2.08°) is therefore essentially at that floor: the reconstruction transfers about as well as it
possibly could, and the +1.16° penalty over within-family is accounted for by the families genuinely
disagreeing, not by the method failing. **And the curve still beats the tangent cross-family in both
directions** (2.08 vs 3.57; 2.78 vs 6.25).

This answers the circularity objection. The reconstruction is not an artifact of reusing the same
posterior's sampling noise — inputs from one inference predict a *different* inference's geometry.

*(An n=18 GWTC-3-only scout of this test suggested the curve barely beat the tangent cross-family, 3.22 vs
3.57. That was small-sample noise; it does not survive at n=64. Recorded because it was nearly acted on.)*

## A3. The arc-length mechanism — DEMOTE

The audit did not raise this, but it is the weakest link. REPORT_E67 and REPORT_E71 assert *"tangent error
grows with arc length; curve absorbs it."* That was **never measured on real data** — the guarding test
(`test_curve_chord_rotates_with_arc_length`) runs on synthetic ideal constant-$\mathcal M_c$ curves, and no
results JSON contains any per-event arc-length or $q$-range quantity. Measured here for the first time, with
arc length proxied by the 5–95% $q$-range:

| catalog | n | $\rho$(tangent err, $q$-range) | $\rho$(curve err, $q$-range) | $\rho$(tangent err, axr) |
|---|---|---|---|---|
| GWTC-3 | 75 | **+0.260** | −0.018 | −0.416 |
| O4a | 86 | **+0.022** | −0.090 | −0.403 |
| O4b | 104 | **+0.115** | −0.098 | −0.695 |

The *direction* is right in all three and the curve does absorb the dependence ($\rho\approx0$ throughout),
but the tangent-error/arc-length correlation is **weak and inconsistent out of sample** ($+0.26$ in the
training catalog, $+0.02$ and $+0.12$ in the two validation catalogs). It cannot carry the mechanism figure
as a quantitative claim. Either state it as the synthetic geometric demonstration it is, or find a better
arc-length proxy (the 5–95% $q$-range may be a poor one — arc length along the curve is not linear in $q$).

**Related correction (the audit's point 6, verified):** the paper must NOT say tangent residuals grow with
*axis ratio*. Measured Spearman(error, axr) is negative in all three catalogs (−0.416, −0.403, −0.695):
orientation becomes *better* defined as elongation increases. Arc length and axis ratio are different
quantities and were being conflated, including in the previous plan.

## Where this leaves the paper

Gate A **passes**. The defensible claim, in the audit's framing:

> Two one-dimensional summaries of a component-mass posterior — its median chirp mass and its mass-ratio
> marginal — reconstruct the orientation of the full two-dimensional posterior to $\sim1^\circ$ on elongated
> events, with no coefficient calibrated on the validation catalogs. Substituting another event's mass-ratio
> marginal degrades this by $2.5$–$12\times$. The reconstruction transfers across waveform families: inputs
> from one waveform family recover a different family's independently inferred axis to $2.1^\circ$, against
> a $2.0^\circ$ floor set by the families' own mutual disagreement.

Still outstanding: Gate B (bootstrap uncertainties, coverage, threshold-sensitivity curve), Gate C (frame
and parameterization audit), Gate D (preregistration timestamps, per-waveform-family reporting), Gate E
(the precision law's direct multivariate fit, or its removal).
