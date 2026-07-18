# E45 preregistration — strong-gravity IMR-consistency test in the value/shape framework

Status: LOCKED. Date 2026-07-07. The handoff's "true strong-gravity" battery.
Data: LVK GWTC-3 Tests-of-GR data release (Zenodo 17461225), IMR-consistency (imrct) posteriors.

## Setup

For each event the release provides a 2D posterior pdf on the grid
(final_mass_deviation dMf/Mf-bar, final_spin_deviation daf/af-bar) in [-2,2] x [-2,2], 401x401.
GR predicts (0,0): the final mass/spin inferred from the inspiral and from the post-inspiral must
agree. The value/shape framework reads each event's deviation posterior as: VALUE = displacement
of the mean from (0,0); SHAPE = orientation psi / correlation rho of the deviation ellipse.

## Quantities (per event)

- GR credible level Q = fraction of posterior mass with pdf > pdf(0,0). Q < 0.90 => GR inside the
  90% region (consistent); Q > 0.95 => >2-sigma tension.
- mean deviation vector (mx, my); direction phi = atan2(my, mx); value distance in "sigma-from-GR".
- deviation-ellipse psi, rho.

## Tests / decision rules (LOCKED)

D1 (POPULATION GR CONSISTENCY, primary): multiply all per-event pdfs on the common grid -> the
   COMBINED deviation posterior. GR is consistent if (0,0) has combined credible level Q_comb <
   0.90. (Standard LVK combination; the population strong-gravity test.) FAIL = the combined
   deviation excludes GR at >90% -> a population-level GR-violation/systematic flag.

D2 (PER-EVENT): count events with Q < 0.90 (GR-consistent) and Q > 0.95 (individually discrepant).
   Under GR + noise, expect ~all consistent and ~5% above 0.95 by chance.

D3 (DIRECTIONAL COHERENCE, the framework's added test): Rayleigh test on the per-event
   mean-deviation directions phi. Under GR the mean deviations scatter ISOTROPICALLY about (0,0)
   (measurement noise has no preferred deviation direction), so p_Rayleigh > 0.05 = isotropic
   (GR-consistent). p_Rayleigh < 0.05 = the deviations share a preferred direction -> a coherent
   systematic or new-physics direction (value/shape VALUE-coherence signature). Reported with the
   mean resultant direction if significant.

## Interpretation

Expected under GR: D1 consistent (Q_comb < 0.90), D2 ~all consistent, D3 isotropic. The novel
contribution over the standard per-event LVK test is D3 (is any residual deviation coherent across
events?) plus the value/shape reading. A coherent D3 direction with a consistent D1 would say
"individually GR-consistent but with a shared sub-threshold pull" -- worth flagging. All reported
as-is; a GR-violation is NOT expected and would be treated with extreme skepticism (systematics
first).

## Provenance

data/chains/tgr/IGWN-GWTC3-TGR-v1-imr.zip (Zenodo 17461225, 4.12 GB, size-verified; gitignored).
Uses imr_*_posterior_samples.h5 imrct grids. No RNG (Rayleigh test is analytic).
