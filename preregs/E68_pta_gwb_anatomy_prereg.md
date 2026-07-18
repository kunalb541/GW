# E68 preregistration — cross-PTA anatomy of the nanohertz GW background (LOCKED 2026-07-17)

**New GW band for the framework.** Four pulsar-timing arrays have measured a common-spectrum
process consistent with a GW background. Two questions the value/shape machinery is built for:
(1) are the PTAs' (log10_A, gamma) posteriors mutually consistent, and where they differ, is the
difference value or shape — and is it COHERENT (all offsets along the A–gamma degeneracy = shared
convention/band artifact) or incoherent (real spectral disagreement)? (2) how strongly does each
PTA disfavor the circular-GW-driven SMBH-binary prediction gamma = 13/3?

## Probes (real public chains; power-law common process, A referenced at f = 1/yr)
- **NANOGrav 15yr** (Zenodo 8423265 tarball): the HD-correlated power-law GWB chain if present in
  the release, else the common-spectrum (CURN) free-gamma chain; recorded which.
- **EPTA+InPTA DR2** (Zenodo 8091568 chains.zip, paper-III chains): the DR2full common red noise /
  GWB free-gamma chain; recorded which.
- **PPTA DR3** (github danielreardon/PPTA-DR3): chain_commonNoise_pl_nocorr_freegam_DE440
  (VERIFIED against published: gamma = 3.87 ± 0.37, log10A = −14.50 ± 0.16); HD-vs-CRN comparison
  chain as robustness.
- **CPTA DR1**: only if a public chain exists; otherwise their published summary appears as a
  labeled overlay, NOT in the battery.

## Decision rules (LOCKED)
- **D1 (mutual consistency).** Pairwise Mahalanobis significance in (log10_A, gamma) with the full
  E48 ladder (vf_raw, joint-whitened, orientation-only) + delta-rho. All pairs < 2 sigma →
  "consistent" (expected); any pair >= 2 sigma → flagged and decomposed value vs shape.
- **D2 (degeneracy universality + coherence).** (a) rho(log10_A, gamma) is negative for every PTA
  (the common f_ref = 1/yr degeneracy); report psi too (axes are both dimensionless — usable here,
  unlike E63's (M,R)). (b) COHERENCE: project each pairwise mean offset onto the common degeneracy
  direction (mean principal axis); if >= 2/3 of the offset power (averaged over pairs) lies along
  the degeneracy, the inter-PTA differences are classified "degeneracy-sliding" (band/convention),
  else "spectral" (real). Both thresholds locked here.
- **D3 (SMBHB gamma = 13/3).** Per-PTA marginal z-score of gamma = 13/3 and the count of PTAs with
  z > 2. Descriptive; no combined-PTA number is fabricated (the E58 lesson — no naive posterior
  products across experiments with different priors).
- **D4 (Gaussianity gate).** E48 empirical-vs-Gaussian sliced-W2 check on every pair; any ratio off
  1 by >30% → the Gaussian numbers for that pair are flagged and the empirical distance leads.

## Honesty commitments
- Different PTAs probe different frequency bands; a common power-law fit referenced at 1/yr makes
  (A, gamma) comparable, but band-dependence of a NON-power-law true spectrum would appear as
  degeneracy-sliding — D2's classification cannot distinguish those two; stated in the report.
- Chains have different samplers/priors; no evidence combination, comparisons only.
- All chain files, parameter-name mappings, and any fallbacks recorded in the results JSON.
- Seed 68 for sliced-W projections.
