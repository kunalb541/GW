# NOVELTY — prior-art positioning for the curved chirp-mass law (claim 1)

Preliminary novelty scan (2026-07-18), **not** a systematic literature review — a proper related-work
search is still owed before submission. Purpose: state honestly what is textbook vs. what is the new
wedge, and attach a **verification status** to every external citation so none goes into the manuscript
on trust. (This file exists because a double-check caught a misattributed citation — see below.)

## What is NOT new (must not be claimed as ours)
Chirp mass is the best-measured mass combination of an inspiral; component-mass posteriors lie along
near-constant-chirp-mass ("banana") contours. This is textbook and appears throughout the literature.
- **Baird, Fairhurst, Hannam & Murphy (2013), PRD 87, 024035** ([arXiv:1211.0546](https://arxiv.org/abs/1211.0546)) —
  mass–spin degeneracy; chirp mass accurately determined at low mass. **[VERIFIED via arXiv.** NOTE: the
  pasted analysis attributed this to "Brown et al." — **wrong; it is Baird et al.** And it is about the
  mass–**spin** degeneracy, and explicitly caveats that at higher masses the degeneracy "is not so clearly
  characterised by constant chirp mass" — so it is a *weaker* anchor for "constant-Mc curves in the mass
  plane" than the pasted text implied. Do **not** cite it for the visual.]**
- **Hannam, Brown, Fairhurst, Fryer & Harry (2013), ApJL** ([arXiv:1301.5616](https://arxiv.org/abs/1301.5616)) —
  BH/NS distinguishability; the mass-ratio/spin degeneracy limits component-mass measurement; the (m1,m2)
  plane is central. **[Identity VERIFIED; that it *plots explicit constant-Mc curves* is UNVERIFIED — check
  the figures before citing for the visual. This is the likely intended anchor the pasted text meant.]**
- GWTC catalog papers routinely show Mc–q / m1–m2 banana posteriors (GWTC-3 [arXiv:2111.03606], GWTC-4
  [arXiv:2508.18080]). **[General knowledge; verify the exact sentences before quoting.]**
- Rapid-classification / observable-feature PE constrains masses near constant-Mc lines: MNRAS 515, 5718;
  ["Simple parameter estimation using observable features" arXiv:2304.03731](https://arxiv.org/abs/2304.03731).
  **[UNVERIFIED — 2304.03731 surfaced as a possible close neighbor; read it before positioning against it.]**

## What IS new (the novelty wedge)
Not "chirp mass controls the posterior" (textbook), but a **quantitative, catalog-scale posterior-geometry
law**:
- per-event **principal axis (PCA orientation)** of the (m1,m2) posterior is *predicted* by the
  constant-Mc **curve/chord**, using only the event's median source-frame Mc and its q marginal;
- the local **tangent** approximation leaves systematic residuals that **grow with arc length**; the
  **curve/chord** correction removes them (E65 mechanism, guarded by `test_curve_chord_rotates_with_arc_length`);
- **zero / near-zero fitted freedom** (no calibration constants anywhere);
- **locked out-of-sample** validation on a disjoint later catalog (E67/GWTC-4: D1 = 1.26°, prereg
  committed before any file opened), now being repeated on **GWTC-5/O4b** (E71).
My light search found only **qualitative/visual** neighbors (banana shape, Mc–q contours) — nothing doing
the PCA-orientation prediction + tangent-vs-curve residual + locked cross-catalog test. **That gap is the
wedge, but it rests on a non-systematic search — treat "new" as provisional until the related-work sweep.**

## Recommended claim phrasing (honest, referee-safe)
> While chirp-mass dominance is well known, we show that the full **event-by-event mass-plane posterior
> geometry across GW catalogs** obeys a **predictive constant-chirp-mass curve law**: the tangent
> approximation leaves systematic residuals; the curve/chord geometry removes them and passes a **locked
> out-of-sample test** on GWTC-4 (and, pending, GWTC-5).

## PTA side (claim 3) — treat as secondary/exploratory
Prior art already compares PTA amplitudes/spectral indices and pairwise consistency, and studies
spectral-index running. Our possible novelty is the **degeneracy-sliding anatomy + span-ordered γ** — but
frame it as secondary until replicated.
- IPTA DR2 isotropic-GWB search: **MNRAS 510, 4873** ([arXiv:2109.00296](https://arxiv.org/abs/2109.00296)).
  **[Identity VERIFIED; the specific "<3σ pairwise (logA,γ) separation" figure is UNVERIFIED — confirm in the paper.]**
- NANOGrav spectral-index running: arXiv:2408.10166. **[UNVERIFIED — did not surface in search; locate and read before citing.]**

## Action items before the manuscript
1. Read Hannam 2013 (1301.5616) figures + 2304.03731; confirm whether either does the *orientation-prediction*
   test (expected: no) — that pins the wedge.
2. Fix every "Brown et al." → "Baird et al." (1211.0546) in any draft/notes.
3. Verify the two PTA numbers before they enter claim 3.
4. Do the systematic related-work sweep; downgrade "new" to "to our knowledge, not previously done" unless the sweep is exhaustive.
