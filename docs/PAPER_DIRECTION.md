# PAPER DIRECTION — what the paper should be about (research round, 2026-07-21)

Scope of this round: decide whether the 2026-07-20/21 work (E87 ringdown correction, E88 overtone,
E89 mass–spin) should reshape the paper, or whether the existing curved-chirp-mass-law spine stands.
Method: targeted literature search (no agent swarm), plus re-reading the existing
[LITERATURE.md](LITERATURE.md) / [NOVELTY.md](NOVELTY.md). Citations below are **search-surfaced and
lightly verified** — abstracts read, not full texts, except where noted. Treat as provisional.

## Verdict

**The paper stays the curved chirp-mass law + posterior geometry. The ringdown work does NOT become
the paper, and E89 does not go in it.**

---

## 1. Ringdown / overtone (E87, E88) — do not build the paper here

The field is crowded, actively contested, and our specific findings are largely **reproductions**.

**Start-time bias is established prior art.** Multiple sources state that the fundamental mode alone
cannot recover the true remnant mass and spin unless the fit starts very late, and that including
overtones removes the bias. That is exactly E87's plateau result (230 Hz at $t_{\rm peak}$ → 251 Hz at
12–18 $M_f$). We reproduced a known effect with our own machinery — valuable as validation, not as a
claim.
- Coleman & Finch, *High-overtone ringdown fits: start time, no-hair tests, and correlations*,
  arXiv:2512.08098 (Dec 2025). **[abstract verified]** Bayesian PE on overtone amplitudes/phases;
  finds strong correlations make individual high overtones unmeasurable, but the joint correlation
  structure is informative. Closest neighbour to E88 — but their correlations are **among overtone
  amplitudes**, not between the overtone and the **remnant** $(M_f,a_f)$.
- Giesler, Isi, Scheel & Teukolsky, *Black hole ringdown: the importance of overtones*, PRX 9, 041060
  (arXiv:1903.08284). **[identity verified]** The origin of the overtone programme.

**The overtone controversy is 6+ years old, unresolved, and has many entrants.** Sequence, as far as
the search shows: Isi et al. 2019 claim the 221 in GW150914 at 3.6σ → Cotesta, Carullo, Berti &
Cardoso dispute it (evidence appears only when the fit starts before merger, where a QNM description
is invalid) → Isi & Farr Comment → arXiv:2312.14118 / PRD 110, L041501 marginalizes over **merger time
and sky location** and finds low evidence (BF $2.3\pm0.1$) → a gating-and-inpainting frequency-domain
reanalysis (PRD, 2025) → Coleman & Finch (2025). There are already GW250114-specific ringdown papers:
LVK's own (arXiv:2509.08054), an orthonormal-mode analysis (arXiv:2605.03576), and an extended
parameterized-spin-expansion analysis (arXiv:2606.22580). **[all abstract-level only]**

**Our own critique is already in the literature.** The search surfaced the statement that the overtone
Bayes factor "can be made to take different values with suitable adjustments to the prior range," and
that comparing two models neither of which fully describes the data is conceptually fraught. That is
E88's prior-sensitivity point, already made by others.

**And we would be the weakest entrant.** E88's two-mode preference is significant (8.4σ vs the correct
null) but does **not decay like an overtone**, and the responsible systematic is **unidentified**. Our
model has no sky position, no antenna patterns, no inclination — precisely the parameters the 2312.14118
line of work shows are decisive. Entering this fight with an unidentified systematic and a looser model
would be indefensible.

**What E87 IS good for:** a *validation appendix*. A from-scratch pipeline that reproduces LVK's own
pyRing Kerr_220 start-time scan to a **median 2.0 Hz over 2–18 $M_f$**, with credible-interval widths
that track ($16.4$ vs $16.3$ Hz at $12M$), is strong evidence that our machinery is sound. That supports
the paper's "we build and check our own tools" posture without claiming ringdown physics.

## 2. Prior-domination diagnostics — the concept is NOT novel

The idea of testing whether a posterior is prior-dominated is standard: the KL divergence between prior
and posterior is the usual informativeness statistic, JS divergence is used with a threshold (0.007) to
flag informative posteriors, and prior-dominated posteriors have been reported explicitly for black-hole
kicks in GW150914/GW170729. **[abstract-level]** So "detect prior-dominated inference" cannot be sold as
a new method.

What remains ours, and is worth stating as *practice* rather than as a new statistic: the specific
**geometric** checks — does adding an independent detector tighten the posterior (it must); what
fraction of the parameter grid sits within 2 lnL of the peak; does the peak rail against a grid edge;
what does the identical pipeline return on signal-free data. These are cheap and they caught a real
error (E85). Methods-section material, not a headline.

## 3. E89 mass–spin — real physics, but not for this paper

Not novel (mass/spin correlation and the hierarchical-merger reading are both discussed in the
literature), **selection effects unmodelled** — which is the first thing a referee would attack — and it
pulls a geometry paper into population astrophysics. Note also arXiv:2509.08657, *Decisive Evidence for
the First Overtone Mode in the Ringdown Signal of GW231028* **[abstract-level]** — GW231028 is one of
E89's high-spin heavy events ($a_1=0.787$), which is a nice consistency touch but also shows how fast
this space is being worked. Hold E89 for a standalone note once the 1G+2G mixture and a selection
function exist.

## 4. What the paper should be

Unchanged spine, with this session supplying reinforcement rather than new headline claims:

1. **The curved chirp-mass law** (E40 → E65 → E67 → E71). The gap in [LITERATURE.md](LITERATURE.md) is
   precise and citation-verified: no published work predicts the per-event $(m_1,m_2)$ posterior
   principal-axis angle from the constant-$\mathcal{M}_c$ **curve** with zero fitted parameters, decomposes
   tangent-vs-curve residuals against elongation, and validates it **locked and out-of-sample across three
   disjoint catalogs**. This remains the strongest, least-contested claim in the programme.
2. **Posterior size is lawful too** (E42: $\sigma_{\mathcal M}/\mathcal M$ vs SNR, partial correlation
   $+0.94$ with the cycle-count term).
3. **The same geometric lens separates artifacts from physics** — now with an unusually strong case list,
   every one of them a real caught error: E47's naive posterior product (a fake 99.9% no-hair violation),
   E79's 3σ that was a catalog-spread systematic, E85→E87's posterior that **was the prior**, E88's
   two-mode preference that **does not decay like an overtone**, E89's **circular** informativeness cut and
   its **null generator whose posterior-shape assumption manufactured a bias**. This is the honest core of
   "the geometry of inference" and it is what the programme actually has that others do not: not a new
   statistic, but a disciplined, reproducible catalog of how posterior geometry misleads.
4. Optional/secondary: PTA degeneracy-sliding (E68), already flagged in SCOPE as secondary.

**Recommended framing:** geometry *predicts* posteriors where a dominant physical combination exists
(1, 2), and geometry *catches* inference failures where it does not (3). One idea, two directions.

## Action items
- Do NOT draft a ringdown section as a claim; write E87 as a validation appendix instead.
- Before submission: read Coleman & Finch (2512.08098) in full to confirm the remnant-vs-overtone
  degeneracy is genuinely un-addressed there, in case E88 is worth a short separate note.
- Verify every citation in this file at full-text level before any of it enters the manuscript
  (this round is abstract-level only).
