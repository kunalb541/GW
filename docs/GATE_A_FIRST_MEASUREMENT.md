# Gate A, first measurement (2026-07-21) — the audit's central concern, quantified

The [revised PAPER_PLAN](PAPER_PLAN.md) requires, before drafting, that the curved reconstruction be shown
non-trivial against declared baselines, and specifically: *"Quantify how much accuracy comes from the
event's own $q$ marginal. Report the degradation when it is replaced by a pooled or shuffled marginal."*

Run as a scout on GWTC-3 (75 events, the training catalog) using the committed E71 machinery
(`psi_axr_rho`, `tangent_angles`, `curve_psi`) with no modification. Median $|\Delta\psi|$, degrees:

| baseline | all 75 | elongated (axr $\ge3$, n=28) |
|---|---|---|
| curved, event's **OWN** $q$ marginal | 4.85 | **0.80** |
| curved, **POOLED** $q$ marginal (all events) | 13.86 | 10.02 |
| curved, **SHUFFLED** $q$ (another event's) | 12.68 | 9.40 |
| median-point tangent (no $q$ marginal) | 7.49 | 4.68 |
| constant-total-mass ($135^\circ$) | 20.38 | 25.28 |

Own-$q$ beats pooled on 93% and shuffled on 89% of elongated events.

## What this establishes, and what it costs

**Establishes (good):** the reconstruction is strongly **event-specific**. It is not the trivial result that
all mass posteriors point in a similar direction — a wrong $q$ marginal is not merely unhelpful, it is
*actively harmful*, degrading the curve to $9.4^\circ$, i.e. WORSE than the $4.7^\circ$ median-point tangent
that uses no $q$ information at all. So the curve geometry and the arc it is evaluated over must match the
event for the method to work. The shuffled/pooled baselines are exactly the controls a referee would demand,
and the result passes them decisively.

**Costs (the honest reframing):** the event's own $q$ marginal carries most of the accuracy —
$0.80^\circ$ vs $9.40^\circ$, a $12\times$ degradation. The improvement over the tangent
($4.68^\circ\to0.80^\circ$) is bought **entirely** by supplying the correct arc. The claim must therefore be
stated as the audit insists: a **posterior-compression / reconstruction** law with **zero calibrated
parameters**, whose inputs are the event's median $\mathcal M_c$ and its own $q$ marginal — NOT a prediction
of posterior orientation from source medians alone, and not from physics external to the posterior.

The defensible sentence is roughly:

> Two one-dimensional summaries of a component-mass posterior — its median chirp mass and its mass-ratio
> marginal — suffice to reconstruct the orientation of the full two-dimensional posterior to $0.8^\circ$ on
> elongated events, using no information from the $(m_1,m_2)$ covariance and no coefficient calibrated on
> the validation catalogs. Substituting any other event's mass-ratio marginal destroys the reconstruction.

## Still outstanding from Gate A
- Repeat on O4a and O4b (this scout is the training catalog only).
- The cross-waveform transfer test (family A's $\mathcal M_c$ + $q$ marginal → family B's measured axis),
  which is the strongest available answer to the same-posterior circularity objection. Not run.
- Bootstrap uncertainties on every angle (Gate B).

## A gap the audit did not name
**The arc-length mechanism has never been measured on real data.** `test_curve_chord_rotates_with_arc_length`
verifies it on *synthetic* ideal constant-$\mathcal M_c$ curves, and no results JSON contains any per-event
arc-length or $q$-range quantity (checked: 0 occurrences across e65/e67/e71 results). REPORT_E67 and
REPORT_E71 assert "tangent error grows with arc length; curve absorbs it" as narrative. Since the mechanism
figure is Figure 1 of the narrowed paper, the per-event arc-length dependence needs to be measured, or the
mechanism claim must be demoted to the synthetic demonstration it currently is.

**Related correction, and the audit is right:** the paper must NOT say tangent residuals grow with axis
ratio. Measured Spearman(error, axr) is **negative** in all three catalogs ($-0.415$, $-0.402$, $-0.694$):
orientation becomes *better* defined as elongation increases. Arc length (the $q$-range) and axis ratio are
different quantities and were being conflated — including in the previous version of the paper plan.
