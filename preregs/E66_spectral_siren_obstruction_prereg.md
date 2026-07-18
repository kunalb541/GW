# E66 preregistration — is the spectral-siren H0 program obstructed by the mass scale? (LOCKED 2026-07-16)

**Claim under test (E61's obstruction logic, GW edition).** Spectral-siren H0 inference reads the
redshift of dark sirens off the source-frame mass scale (the ~33 M☉ power-law+peak feature acting as
a comoving "ruler"). If the mass function's peak location μ_g is uncertain — or, worse, drifts with
redshift (an actively debated possibility) — the H0 inference moves with it. E66 computes that
coupling as a linear-response map on the REAL LVK joint (cosmology + population) posterior, and asks
whether a plausible unmodeled mass-scale drift is large enough to prevent the spectral-siren program
from arbitrating the CMB-vs-SH0ES H0 tension.

## Data (public, downloaded)
LVK GWTC-3 cosmology data release (Zenodo 5645777), `O3_icarogw_data_distro.json`:
- PRIMARY: `SNR_11_BBH-powerlaw-gaussian_restricted-flatLCDM` (n=13,533) — flat ΛCDM, Om0 fixed,
  H0 free within the restricted prior [65, 77] km/s/Mpc, jointly sampled with the full
  power-law+peak mass function (μ_g, σ_g, λ_peak, m_min, m_max, δ_m, α, β) and rate evolution
  (γ, κ, z_p). CAVEAT locked up front: the H0 prior is bounded; correlations measured within this
  window are compressed relative to a wide prior — this makes the obstruction estimate
  CONSERVATIVE (an unbounded H0 would co-vary more, not less).
- SECONDARY (direction check): `SNR_11_BBH-powerlaw-gaussian_w0flatLCDM` (wide priors, H0 weakly
  constrained — sign/direction of couplings only).
- ROBUSTNESS: SNR_10/SNR_12 cuts and the broken-powerlaw mass model (same file).

## Method (identical to E61)
Weighted (uniform-weight samples) moments; A = {H0}, B = {mass-scale and rate params}.
Response vector M = C_AB C_BB⁻¹ (the linear-response H0 shift per unit coherent shift in each
population parameter, marginalized over the rest). Cross-check each M_j against a direct
conditional regression (H0 binned in θ_j deciles, slope of the mean) — the E61 lesson (steepest-
ascent bug) makes a second estimator mandatory.

## Decision rules (LOCKED)
- **D1 (obstruction).** Compute ΔH0(Δμ_g = ±4 M☉) = M_{μg}·(±4), the H0 shift induced by a coherent
  4 M☉ mass-peak drift (4 M☉ = the scale of the currently debated peak-location differences across
  catalogs/models; also ≈1.5σ of the chain's own μ_g posterior). OBSTRUCTION CONFIRMED iff
  |ΔH0| ≥ 2 km/s/Mpc — i.e. an unmodeled drift of plausible size exceeds the precision needed to
  arbitrate a 5.6 km/s/Mpc CMB-vs-SH0ES gap. REFUTED iff |ΔH0| < 1 km/s/Mpc (the program is robust);
  1–2 = inconclusive (reported as such).
- **D2 (dominant lever).** Rank all population parameters by |M_j|·σ_j (the H0 shift per 1σ coherent
  drift in θ_j). Report whether the mass-scale group (μ_g, m_max, m_min) or the rate-evolution group
  (γ, κ, z_p) dominates. No pass/fail — this identifies WHAT must be independently pinned before
  spectral sirens can arbitrate H0.
- **D3 (sanity gates).** (a) μ_g median in [30, 35] (consistent with the ~32–34 M☉ peak the release
  and populations papers report); (b) the two coupling estimators (linear response vs decile
  regression) agree in sign and within a factor 2 for the top-3 levers; (c) rank the same couplings
  in the SECONDARY wide-prior chain — signs must agree for the top lever. Any failure → stop and
  diagnose before interpreting D1.

## Honesty commitments
- The restricted H0 prior compresses co-variation → D1 is a LOWER BOUND on the coupling; stated in
  the report wherever ΔH0 is quoted.
- Linear response on a possibly non-Gaussian joint posterior — hence the mandatory decile-regression
  cross-check (D3b).
- This tests the GWTC-3-era icarogw analysis; GWTC-4-era spectral sirens may differ (out-of-scope,
  flagged for follow-up when the O4 cosmology release lands).
- Seed 66 for any resampling (none expected).
