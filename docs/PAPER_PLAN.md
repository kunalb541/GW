# PAPER PLAN — *The Geometry of Gravitational-Wave Inference* (2026-07-21)

Follows [PAPER_DIRECTION.md](PAPER_DIRECTION.md) (research round) and supersedes the ordering in
[SCOPE.md](SCOPE.md). One thesis, two directions:

> **Posterior geometry is LAWFUL where a dominant physical combination exists, and DIAGNOSTIC where one
> does not.** Where the data collapse onto a single physical direction, the posterior's orientation and
> size are predictable with zero fitted parameters. Where they do not, the same geometric reading tells
> you that an inference is not measuring what it appears to measure — and we give a taxonomy of five
> distinct failure modes, each caught in this programme on a real case where it changed the answer.

## Full-text verification done this round
- **Coleman & Finch, arXiv:2512.08098** (the closest neighbour to E88) — read. They FIX the remnant in
  their Bayesian amplitude analysis ("note that here the remnant mass and spin were fixed"), give NO
  pinned-vs-marginalized Bayes factor, address only overtone↔overtone correlations (not
  overtone↔remnant), and use NR simulations ONLY, no detector data. They name the gap as future work:
  *"A more complete picture could be obtained via full Bayesian parameter estimation…where all
  parameters…are sampled over."* **E88's injection measurement sits in that gap.**
- **arXiv:2605.18595** (sky-localization uncertainty in ringdown) **[abstract-level]** — makes the same
  GENUS of argument for a different parameter: fixing sky location "artificially break[s] degeneracies
  and underestimat[es] the true uncertainty of mode-amplitude values." Cite as the closest precedent for
  the *idea*; our contribution is the remnant, quantified. **Also the prime suspect for E88's
  unidentified systematic.**

## The critical scoping decision for E88
**Include the INJECTION result; exclude the real-data claim.**
- IN: with an injected $|\rho|=1$ overtone, remnant PINNED gives $\Delta\ln B=+21.2$ and remnant
  MARGINALIZED gives $-0.05$ — essentially ALL of the overtone's evidence is absorbed by the freedom in
  $(M_f,a_f)$; at $|\rho|=2$, $+110.0\to+15.1$ (86%). Controlled, reproducible, and in a verified gap.
  This EXPLAINS why overtone evidence is so start-time-fragile without entering the controversy.
- OUT: the real-data $8.4\sigma$ two-mode preference. It does not decay like an overtone and its
  systematic is UNIDENTIFIED. It stays in the lab notebook. Publishing it would be indefensible.

## Structure

| § | content | source batteries | status |
|---|---|---|---|
| 1 | Introduction — the thesis above | — | to write |
| 2 | **The curved chirp-mass law**: per-event $(m_1,m_2)$ principal axis predicted by the constant-$\mathcal{M}_c$ curve, zero fitted parameters; tangent-vs-curve residuals grow with elongation; LOCKED out-of-sample across three disjoint catalogs (GWTC-3 → O4a $1.26^\circ$ → O4b $1.22^\circ$) | E40, E65, E67, E71 | results done; needs figures + prose |
| 3 | **The precision law**: $\sigma_{\mathcal M}/\mathcal M \sim \mathcal{M}^{5/3}/\mathrm{SNR}$; partial correlation $+0.94$ with the cycle-count term at fixed SNR | E42 | done; needs figure |
| 4 | **A taxonomy of geometric failure modes** (the honest core) | see below | all measured; needs prose |
| 5 | Methods & discipline: locked preregs, contract tests, coherence lens, no naive posterior products | WORKFLOW | to write |
| A | Appendix: pipeline validation — from-scratch ringdown reproduces LVK pyRing Kerr_220 to median 2.0 Hz over 2–18$M_f$, widths tracking ($16.4$ vs $16.3$ Hz at $12M$) | E87 | done |

### §4 — the five failure modes (each a distinct geometric statement)
1. **Shared-degeneracy stacking.** Multiplying per-event posteriors ignores the common degeneracy
   direction. → E47's fake 99.9% "no-hair violation," corrected by a Mahalanobis cross-check.
2. **Deviation along the catalog's own spread.** An apparent GR deviation lying in the direction the
   catalog already scatters is a systematic. → E79's $3.1\sigma \to 1.5\sigma$.
3. **The posterior fills the prior volume.** The credible interval IS the prior. Three cheap checks:
   does adding independent data tighten it (it must); what fraction of the grid lies within 2 lnL of the
   peak; does the identical pipeline return the same width on signal-free data. → E85 retracted by E87
   (whole grid within 4 lnL; adding L1 did not tighten).
4. **Signal direction degenerate with a nuisance direction.** → the remnant absorbs the overtone
   ($+21.2 \to -0.05$). Explains the start-time fragility of overtone claims.
5. **Estimator bias when informativeness tracks the covariate.** Two sub-cases, both from E89: an
   "informative events" cut is CIRCULAR when measurability rises with the measured quantity
   (Spearman $a_1$ vs KS $=+0.93$ among the 10 heaviest); and a null generator that models posteriors as
   centred-on-truth rather than relaxing-to-prior invents a $+0.42$ slope bias.

## Work plan, in order

**1. Figures — the blocking gap (nothing exists).**
   1a. Curved-law gallery: a few representative $(m_1,m_2)$ posteriors with the predicted constant-$\mathcal{M}_c$
       curve overlaid, plus the three-catalog out-of-sample table rendered as a figure.
   1b. Tangent-vs-curve residual vs elongation (the mechanism figure — the single most persuasive plot).
   1c. Precision law: $\log \sigma_{\mathcal M}/\mathcal M$ vs $\log$ SNR with the Fisher slope.
   1d. §4 summary figure: one panel per failure mode, each showing the "before" (apparent result) and
       "after" (what the geometric check revealed).
   Follow the repo's plotting conventions; every number sourced from `results/*.json`, none retyped.

**2. Manuscript restructure.** The current `paper/manuscript.tex` is a 5-page draft on the old ordering.
   Rebuild against the table above; §4 is new and is the paper's distinguishing content.

**3. Full-text citation verification.** [PAPER_DIRECTION.md](PAPER_DIRECTION.md) is abstract-level except
   Coleman & Finch. Before submission verify at full text: Hannam 2013 (1301.5616) figures — does it plot
   constant-$\mathcal{M}_c$ curves; Ohme 2013 (1304.7017); `simple-pe` (2304.03731); the overtone-controversy
   chain; 2605.18595. Carry the NOVELTY.md convention: every citation marked VERIFIED / UNVERIFIED.

**4. Optional upgrade (only if cheap).** Tie per-detector amplitudes to a sky position in E88. If the flat
   ~+5 systematic collapses, the real-data result becomes publishable and §4.4 gains a second panel. If it
   does not, that is itself worth a sentence. 2605.18595 says this is the right suspect.

## Explicitly NOT in this paper
- E89 mass–spin (not novel; selection effects unmodelled). Standalone note later, after a 1G+2G mixture
  and a selection function — that is the version that could test whether a 2G subpopulation sits at 0.69.
- E90 superradiance (null; did not survive calibration — logged as a scout only).
- E88's real-data two-mode preference (unidentified systematic).
- Any ringdown *physics* claim. We reproduce known results; that is an appendix, not a contribution.
