# E47 preregistration — ringdown 221-overtone no-hair test in the value/shape framework

Status: LOCKED. Date 2026-07-07. Third strong-gravity battery (black-hole spectroscopy).
Data: Zenodo 17461225, IGWN-GWTC3-TGR-v2-rin.zip, pyring Kerr_221_domega_dtau analyses.

## Setup

The no-hair theorem: a Kerr black hole's quasi-normal-mode spectrum is fixed by its mass and spin
alone. The ringdown test measures fractional deviations of the 221 first-overtone frequency
(domega_221) and damping time (dtau_221) from the Kerr prediction; GR predicts (0,0). 22 events
have the JOINT 2D (domega_221, dtau_221) posterior. The value/shape reading: per event VALUE =
displacement of the deviation posterior mean from (0,0); SHAPE = orientation/correlation.

## Quantities (per event, from posterior samples)

- 2D mean (domega, dtau), covariance -> rho, psi (ellipse orientation).
- GR credible level Q = fraction of (KDE) posterior mass with density > density at (0,0).
- mean-deviation direction phi = atan2(dtau_mean, domega_mean); value distance sigma-from-GR.

## Decision rules (LOCKED) -- mirrors E45

D1 (POPULATION COMBINED no-hair): multiply the 22 events' 2D deviation densities on a common grid
   -> combined posterior. Kerr/GR consistent if (0,0) has combined credible level Q_comb < 0.90.
   FAIL = combined deviation excludes GR at >90% (population no-hair-violation/systematic flag).

D2 (PER-EVENT): count events with Q < 0.90 (consistent) and Q > 0.95 (individually discrepant).
   Note: the 221 overtone is weakly constrained in most events -> broad posteriors -> expect ~all
   individually consistent.

D3 (DIRECTIONAL COHERENCE): Rayleigh test on the per-event mean-deviation directions phi.
   p_Rayleigh > 0.05 = isotropic (GR-consistent scatter); < 0.05 = coherent direction (systematic
   or new-physics flag; the framework's added test). Report mean direction if significant, and
   check alignment with per-event ellipse axis (shape vs value coherence, as in E45).

## Interpretation

Expected under GR: D1 consistent, D2 ~all consistent, D3 isotropic. A coherent D3 would be flagged
as a systematic candidate (as in E45/E46, waveform/overtone-modelling), NOT claimed as new physics.
Any no-hair "violation" treated with extreme skepticism (overtone modelling + start-time
systematics dominate ringdown tests). Reported as-is.

## Provenance

data/chains/tgr/IGWN-GWTC3-TGR-v2-rin.zip (Zenodo 17461225, 2.21 GB, size-verified, gitignored).
22 Kerr_221_domega_dtau posteriors. No RNG (Rayleigh analytic).
