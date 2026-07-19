# LITERATURE — related work, the gap, and why it matters (curved chirp-mass law)

Full citation-verified literature review for the paper's spine result (the constant-M_c posterior-geometry
law: E40 tangent → E65 curve → E67 O4a 1.26° → E71 O4b 1.22°; E72 physics-blind null). Supersedes the
preliminary scan in [NOVELTY.md](NOVELTY.md) (which caught the "Brown et al." → **Baird et al.**
mis-citation). Each citation was checked against arXiv/journal pages; items not fully re-fetched are marked
**UNVERIFIED**. The single most load-bearing neighbor (Ohme et al. 2013) was independently re-verified for
this file: PCA on PN coefficients, no (m1,m2) posterior-orientation prediction, no catalog test — confirmed.

## Established prior art (verified)
- **Cutler & Flanagan (1994)**, PRD 49, 2658 (gr-qc/9402014) — founding Fisher-matrix PE; M_c measured to
  ~0.1–1% and dominates the inspiral phase. Origin of "M_c is best-measured." Textbook, not novelty.
- **Poisson & Will (1995)**, PRD 52, 848 (gr-qc/9502040, arXiv id UNVERIFIED) — 2PN Fisher with spin terms;
  the mass-ratio error is inflated by the mass–spin correlation. The mass-ratio/spin degeneracy, quantified.
- **Baird, Fairhurst, Hannam & Murphy (2013)**, PRD 87, 024035 (arXiv:1211.0546) — mass–SPIN degeneracy;
  explicitly caveats that **constant-M_c stops characterizing the degeneracy at high mass** (merger/ringdown).
  Bounds where a constant-M_c geometric law is expected to hold. (Correct attribution — NOT "Brown et al.")
- **Ohme, Nielsen, Keppel & Lundgren (2013)**, PRD 88, 042002 (arXiv:1304.7017) — **PCA of the PN phase
  coefficients** confirms M_c is the dominant measured direction. THE closest "PCA + chirp-mass" work — but the
  PCA is on PN/physical parameters, not (m1,m2) posterior samples; predicts no per-event posterior orientation
  angle; no catalog validation. (Re-verified independently for this review.)
- **Hannam, Brown, Fairhurst, Fryer & Harry (2013)**, ApJL 766 L14 (arXiv:1301.5616) — **plots constant-M_c
  curves** in the (m1,m2) plane and notes uncertainty regions lie along them, but only **qualitatively**; no
  orientation prediction, no catalog test. The "closest neighbor" for the visual; ours is its predictive form.
- **Fairhurst, Hoy, Green, Mills & Usman (2023)** `simple-pe`, PRD 108, 082006 (arXiv:2304.03731) — computes a
  metric **error ellipse** in (M_c, q) assuming a **Gaussian** posterior. This is exactly the local **tangent/
  linear** approximation our curve term corrects: a Gaussian ellipse's principal axis IS the tangent.
- **Lee, Morisaki & Tagoshi (2022)** (arXiv:2203.05216, published coords UNVERIFIED) — PCA of the Fisher matrix
  for **sampling efficiency** in mass–spin, not to predict (m1,m2) posterior orientation.
- **Roulet & Zaldarriaga (2019)**, MNRAS 484, 4216 (arXiv:1806.10610); **Roulet et al. (2024)**, PRX 14,
  021005 (author list UNVERIFIED) — work in (M_c, q, χ_eff); characterize where posteriors sit, not the
  per-event (m1,m2) orientation geometry.
- **Waveform-systematics-as-inconsistency** (PRD 106, 044042; GWTC-4.0 cross-catalog comparison arXiv:2512.19513,
  author lists UNVERIFIED) — flag events via **Jensen–Shannon divergence between two waveform posteriors**;
  the closest existing "systematics detector," but a different observable (model-vs-model), not a geometric law.
  Consistent with E72's null (only waveform-model disagreement correlates with the orientation residual).
- **Ghosh, Hoy, Hannam & Ohme (2026)** PhenomDECO (arXiv:2606.31350, lightly verified) — catalog-scale robustness
  diagnostics via an added compactness parameter + TF residuals; different observable, not posterior geometry.

## The gap (precise)
The literature has (i) the **qualitative** "banana along constant-M_c" picture (textbook; Hannam 2013; GWTC
figures) and (ii) **local, linear** Fisher/metric predictions of an error-*ellipse* orientation requiring
waveform derivatives (Cutler–Flanagan; Poisson–Will; `simple-pe`; Ohme 2013's PN-coefficient PCA). **To our
knowledge no published work provides (a) a per-event quantitative prediction of the (m1,m2) posterior's PCA
principal-axis angle from the constant-M_c CURVE at the event's own median M_c over its q-marginal, with zero
fitted parameters; (b) a tangent-vs-curve (chord) residual decomposition showing the linear approximation
leaves residuals that grow with posterior elongation while the curve removes them; nor (c) a catalog-scale,
LOCKED, out-of-sample validation across independent catalogs (GWTC-3 → O4a → O4b).** Existing PCA work is on
waveform/PN or TGR-deformation parameters, or PCA for sampling — none predicts the (m1,m2) posterior's own
orientation and validates it as a law.

## Closest neighbors — and the delta
| Prior work | What it does | The paper's delta |
|---|---|---|
| Hannam et al. 2013 (ApJL 766 L14) | Draws constant-M_c curves; notes posteriors lie along them | Qualitative → **predictive zero-parameter angle**; residual/curvature analysis; catalog validation |
| Ohme et al. 2013 (PRD 88, 042002) | PCA of **PN coefficients**; M_c dominant | Operates on PN params, not (m1,m2) samples; no per-event ψ; no out-of-sample catalog test |
| Cutler–Flanagan 1994 / Poisson–Will 1995 | Fisher covariance → *local* ellipse, M_c long axis | Local **tangent** only; needs derivatives (not zero-param); no curvature; not validated vs full-PE at scale |
| `simple-pe` (Fairhurst 2023) | Metric ellipse, **Gaussian** posterior | The Gaussian ellipse's axis IS the tangent we show is biased for elongated events; we add the curve correction |
| JS-divergence / waveform-systematics | Flags model-vs-model posterior disagreement | Different observable; ours is a geometric orientation law (and E72 *connects* the two) |

Every neighbor supplies one ingredient (chirp-mass dominance, the banana, a local ellipse, PCA-of-something-else,
a systematics flag). None combines them into a zero-parameter, curved, per-event orientation prediction that is
locked and validated out-of-sample across catalogs and used as a physics-blind measurement-optics diagnostic.

## Why it matters
1. **Reproducible zero-parameter predictivity across independent catalogs** — locked, no fitted params, holds at
   ~1.2° on O4a (1.26°) and O4b (1.22°) after derivation on GWTC-3. A genuinely falsifiable, out-of-sample-tested
   law — rare in GW PE, where "laws" are usually untested Fisher heuristics.
2. **Identifies what SETS the posterior geometry (measurement optics)** — orientation fixed by the measurement
   (the constant-M_c curve), not astrophysics; E72's null (no physical axis drives the residual) makes it an
   instrument/likelihood property cleanly separable from source physics.
3. **A fast, principled systematics/outlier detector** — because the law is uniform and physics-blind, departures
   are informative; the one correlate is waveform-model disagreement → a cheap per-event geometric flag,
   complementary to JS-divergence and PhenomDECO diagnostics.
4. **The tangent→curve correction quantifies a real bias** — shows the Gaussian/metric approximation (the
   `simple-pe`/Fisher workhorse) leaves residuals growing with elongation, and how to fix the orientation for
   free; directly actionable for rapid-PE and forecasting.
5. **Population inference & selection functions** — a closed-form curved orientation enables fast, faithful
   (non-Gaussian) single-event likelihood surrogates, sanity-checks on imported posteriors, and analytic
   reasoning about how mass-plane covariance propagates into p(m1,m2) and V(θ).
6. **Low-latency / rapid PE** — orientation from just median M_c and the q-marginal (microseconds) → instant
   curvature-correct uncertainty regions for alerts and an instant consistency check on low-latency posteriors.
7. **Complements, not competes with, full Bayesian PE** — an analytic expectation for one geometric feature,
   turned into a validated diagnostic + fast surrogate on top of standard sampling.

## Threats / overlaps
- **No paper found that makes the core claim** (per-event orientation from the M_c curve; tangent-vs-curve
  residual; locked cross-catalog validation). Novelty stated as "to our knowledge."
- Partial overlaps to cite defensively (none undercuts the claim): Ohme 2013 (distinguish PCA-of-PN from
  PCA-of-posterior), `simple-pe` (frame our curve as its tangent's correction), Hannam 2013 (qualitative→
  quantitative), Cutler–Flanagan/Poisson–Will (tangent ancestors).
- Honest boundary (Baird 2013): constant-M_c weakens at high mass (merger/ringdown) — consistent with our
  axr≥3 restriction and residual-vs-elongation framing; cite Baird 2013 to pre-empt "does it hold for heavy
  systems?".
- Checked and dismissed as unrelated: Makinen et al. 2026 "Degeneracy Distillery" (arXiv:2606.23838, ML/cs.LG).

## Referee-safe framing sentence
> We show that the principal-axis orientation of each compact-binary source-frame (m1,m2) posterior is
> quantitatively predicted, with no fitted parameters, by the constant-chirp-mass curve at the event's own median
> M_c over its mass-ratio marginal; that the local constant-M_c tangent (the Fisher/metric approximation
> underlying rapid-PE tools) leaves residuals that grow with posterior elongation while the curve/chord term
> removes them; and that this law, derived on GWTC-3 and locked before opening later catalogs, predicts the
> measured orientation out-of-sample on GWTC-4/O4a and GWTC-5/O4b to median |Δψ|≈1.2°. While chirp-mass
> dominance and the qualitative "banana" geometry are textbook (Cutler & Flanagan 1994; Poisson & Will 1995;
> Hannam et al. 2013), and PCA has been applied to post-Newtonian/waveform parameters (Ohme et al. 2013), to our
> knowledge no prior work predicts the per-event mass-posterior orientation from the chirp-mass curve, decomposes
> the tangent-vs-curve residual against elongation, or validates such a zero-parameter geometric law out-of-sample
> across independent catalogs — nor exploits it as a physics-blind measurement-optics diagnostic for systematics.

## Before submission (verify on ADS)
Poisson–Will arXiv id; Lee 2022 published PRD coords; Roulet 2024 PRX + GWTC-4.0 author lists (all UNVERIFIED).
Address Ohme 2013 head-on in related work; cite `simple-pe` generously as the tangent our curve corrects.
