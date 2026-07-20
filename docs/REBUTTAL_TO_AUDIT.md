# Rebuttal to the referee audit of PAPER_DIRECTION (2026-07-21)

Response to the hostile-referee audit in [PAPER_PLAN.md](PAPER_PLAN.md). Every claim in the audit was
checked against the committed results rather than accepted or rejected on argument. All five required gates
have now been run: [A](GATE_A_FIRST_MEASUREMENT.md), [B](GATE_B_FIRST_MEASUREMENT.md),
[C](GATE_C_FIRST_MEASUREMENT.md), [D and E](GATE_DE_FIRST_MEASUREMENT.md).

**Summary: the audit is accepted almost entirely. Two of its recommendations are declined on the strength of
new measurements, one of its own citations is flagged as unverified, and the audit missed a weakness worse
than the one it identified.**

---

## 1. Accepted without qualification — the audit was right and we were wrong

**1a. "Do not say the tangent residual grows with axis ratio."** Correct, and verified: Spearman(angular
error, axis ratio) is **negative** in all three catalogs (−0.415 GWTC-3, −0.402 O4a, −0.695 O4b).
Orientation becomes *better* defined as elongation increases. The previous plan asserted the opposite.

**But the audit understated the problem.** The published claim was never about axis ratio — REPORT_E67 and
REPORT_E71 assert *"tangent error grows with **arc length**; curve absorbs it"*, which is a different
quantity. That claim had **never been measured on real data**: its guarding test
(`test_curve_chord_rotates_with_arc_length`) runs on synthetic ideal curves, and no results JSON contains
any per-event arc-length quantity. Measured for the first time (5–95% $q$-range proxy):
$\rho$(tangent error, $q$-range) $=+0.260 / +0.022 / +0.115$ across the three catalogs, with
$\rho$(curve error, $q$-range) $\approx0$ throughout. Direction right, curve does absorb it, but **weak and
inconsistent out of sample**. So the mechanism story is in worse shape than the audit alleged, and the
correction is larger: demote the arc-length mechanism to the synthetic demonstration it is.

**1b. "Zero calibrated parameters, not zero-parameter prediction."** Accepted. `curve_psi()` takes the
event's own $q$ posterior samples; REPORT_E65 already said so plainly. This is a reconstruction/compression
result, not prediction from source medians.

**1c. Not an independent test of GR** (E78/E79 fit an effective exponent to posteriors produced *by* GR
waveform models); **not coordinate-invariant** (a PCA angle is not); **no invocation of Fisher–Rao or Čencov**
without computing such a quantity; **"disjoint event catalogs," not independent experiments.** All accepted
and now enforced in the Gate C convention section.

**1d. No ringdown validation appendix.** Accepted. E87 validates a pipeline the narrowed paper does not use.

---

## 2. Declined, on the strength of new measurements

**2a. "Remove the precision law rather than presenting a correlation as an exponent measurement."**
*Declined — the required fit was run and it passes.* The audit was right that E42 never fit the exponents.
Fit directly on O4a+O4b (where `optimal_snr` is in-file, hence out-of-sample relative to E42's GWTC-3):

$$\log(\sigma_{\mathcal M}/\mathcal M)=b_0+b_\rho\log\rho+b_M\log\mathcal M_{c,\rm det}$$

- $b_\rho=-0.918\pm0.106$ — the Fisher $1/\rho$ scaling, **confirmed** ($z=+0.77$).
- $b_M=+1.485\pm0.057$ pooled — $5/3$ rejected at $3.2\sigma$… **until split by mass**:
  for $\mathcal M_{c,\rm det}<20$, where the inspiral dominates the band,
  $b_M=\mathbf{+1.661\pm0.149}$ against a predicted $1.667$ — **agreement to $0.04\sigma$** — softening
  monotonically to $+0.70\pm0.13$ for $\mathcal M_{c,\rm det}>40$ as the merger enters band.

The cycle-count law holds to sub-tenth-sigma precision inside its domain of validity and breaks down
predictably outside it. That is a *sharper* claim than E42's correlation, not a weaker one. **Keep it, with
the domain stated.** Caveats recorded: $f_{\rm low}$/duration uncontrolled (as the audit asked and we did
not do), 104/190 events carry in-file SNR, O4b contributes only 18 usable events.

**2b. "No five-failure-mode taxonomy in this paper."** *Accepted for this paper, declined as a verdict on
the material.* The audit is right that E47, E85/E87, E88 and E89 use different likelihoods and maturity
levels and would read as a research diary here. They are removed from this manuscript. But the taxonomy is
not withdrawn — it is a separate methods paper, and the session that produced it also produced two live
demonstrations of its value (the `adiff` tautology in §4 below, and E89's circular cut).

---

## 3. One of the audit's own claims is unverified

The audit cuts E88 partly on this basis:

> "Dey et al. (arXiv:2605.18595) already sample remnant mass, spin, amplitudes, phases, and extrinsic
> parameters jointly on GW250114; they find same-$(\ell,m)$ amplitude ratios relatively robust to sky
> treatment."

**This has not been verified at full text, and it is doing real work in the argument.** Our own check of
2605.18595 was abstract-level only and returned a different emphasis — that fixing sky localization
"artificially break[s] degeneracies and underestimat[es] the true uncertainty of mode-amplitude values."
Under this repo's convention (NOVELTY.md) every citation carries a VERIFIED/UNVERIFIED label; this one
entered unlabelled. The conclusion (cut E88 from this paper) is accepted anyway on independent grounds —
E88's real-data systematic is unidentified — but **the stated reason must be marked UNVERIFIED** rather than
propagated as settled prior art.

For the record, the closest neighbour *was* verified at full text: Coleman & Finch (arXiv:2512.08098) fix the
remnant in their Bayesian amplitude analysis, give no pinned-vs-marginalized Bayes factor, address only
overtone↔overtone correlations, and use NR simulations only.

---

## 4. What the gates found that the audit did not anticipate

**4a. E67's preregistration lock is not publicly verifiable.** The audit asked for prereg timestamps,
presumably expecting them to exist. E71's does: prereg `2026-07-18 21:16:43` (d19a7a8, *"LOCKED before any
GWTC-5 file opened"*), result `2026-07-19 14:36:28` — a 17-hour gap in separate commits. **E67's prereg and
results entered in the same commit** (180a62d, the bulk port from the private cosmo2 repo). The lock is real
but attested only by a private history. The two out-of-sample scores are **not equivalent evidence** and the
manuscript must say so.

**4b. The ~1° accuracy is a real systematic, not sampling noise.** Bootstrapping (200 resamples/event,
resampling measured axis and curve inputs jointly): median $|\Delta\psi|=0.96°$ against a median bootstrap
$\sigma$ of $0.24°$ — a ratio of **4.91** — with coverage **5% / 16%** against nominal 68% / 95%. The audit
asked for uncertainty-normalized residuals without predicting this; it is the single most claim-narrowing
result of the exercise.

**4c. A signed residual exists, and finding it required catching an error of ours.** The repo's
`adiff(a,b)=|((a-b+90)\bmod180)-90|` returns an **absolute** value. A first pass used it for a sign test and
produced "100% of elongated events positive, $p=3\times10^{-24}$" — a tautology, nearly written up as a
universal result. Re-run signed: median $-0.725°$, 80% negative, significant in GWTC-3 ($p<0.001$) and O4a
($p=0.019$), **marginal in O4b ($p=0.110$)**.

**4d. The detector-frame gain is axis-ratio-mediated.** The audit asked for the detector-frame repeat
because "source-frame masses introduce redshift uncertainty." Correct in motivation, but the effect runs
through elongation: detector-frame posteriors are far more elongated (median axr 9.9 vs 4.6) and therefore
better reconstructed (0.32° vs 1.04°, paired $p=4\times10^{-9}$), yet **at matched axis ratio the frames are
comparable and the detector frame is worse in the 3–5 band**. Not evidence the detector frame suits the
curve model better.

**4e. Gate A passes, decisively.** Cross-waveform transfer (246 events, 64 elongated): family A's median
$\mathcal M_c$ + $q$ marginal reconstructs family B's *independently inferred* axis to **2.08°**, against a
**1.99°** floor set by the two families' own mutual disagreement, still beating the tangent in both
directions. The circularity objection — the audit's central threat — is answered. Own-$q$ beats
pooled/shuffled by 2.5–12×.

**4f. The residual has a partly identified cause.** The pure-curve model has zero thickness; real posteriors
have perpendicular width that is ~35% of the total spread and **grows along the arc in every single event**
(median Spearman thickness-vs-$q$ = $+1.000$). Rebuilding the model as curve + measured per-$q$ thickness
improves the reconstruction from $1.038°$ to $0.803°$, better on 71% of events, Wilcoxon $p=3.4\times10^{-4}$.
**Partial, not complete** — it removes roughly a quarter of the residual, and per-event residual does not
track per-event taper ($\rho=+0.069$). Reported as a partial mechanism, not a solution.

---

## 5. Net effect on the paper

The audit's core judgement — narrow to the curved chirp-mass result, drop the taxonomy, the ringdown
appendix and the GR-test framing — is **correct and adopted**. Its proposed removal of the precision law is
**declined**, because the fit it demanded vindicates the law rather than killing it.

No gate broke the result. Each narrowed how it may be stated:

> Two one-dimensional summaries of a component-mass posterior — its median chirp mass and its mass-ratio
> marginal — reconstruct the orientation of the full two-dimensional posterior to ~1° on elongated events,
> with no coefficient calibrated on the validation catalogs. Substituting another event's marginal degrades
> this 2.5–12×; the reconstruction transfers across waveform families to 2.08° against a 2.0° floor set by
> those families' mutual disagreement; it is stable across nine catalog/waveform-family combinations
> (0.78–1.29°) and across elongation thresholds. The residual ~1° is a genuine systematic at ~5× the
> sampling uncertainty, roughly a quarter of which is attributable to the posterior's arc-varying thickness,
> a term the zero-thickness curve model omits by construction.

That is a narrower claim than the one the audit attacked, and a considerably harder one to dismiss.
