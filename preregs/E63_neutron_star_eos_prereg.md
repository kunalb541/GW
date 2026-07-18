# E63 preregistration — value/shape geometry of the neutron-star mass–radius tension (LOCKED 2026-07-16)

**First cross-domain transfer of the value/shape framework** from cosmology to the neutron-star
dense-matter equation of state (EOS). The organizing question is the same as V1/cosmo2, in a new
plane: each probe of the NS EOS constrains a different functional of the mass–radius (M–R) relation
through a different *measurement kernel* — X-ray pulse-profile modelling (NICER) fixes a
compactness-dominated M–R band; gravitational-wave tidal phasing (GW170817) fixes the tidal
deformability Λ, a different M–R combination. We ask whether the disagreements between these
measurements are **value** (different central R at fixed M → genuinely different EOS stiffness) or
**shape** (different degeneracy orientation / precision → measurement-kernel artefact), using the
identical Gaussian W₂²/Bures decomposition, orientation angle ψ, and QI toolbox as the cosmology work.

## Working plane
All posteriors expressed in **(M [M☉], R [km])**. M = gravitational mass; R = equatorial
circumferential radius.

## Probes (real public posteriors)
X-ray pulse-profile (NICER), each an equally-weighted 2-D sample cloud in (M,R):
- **J0030** (M≈1.4): Riley 2019 X-PSI ST+PST (Zenodo 3386449); Miller 2019 Illinois–Maryland
  2-oval "2spot" and 3-oval "3spot" (Zenodo 3473466). Same star, same NICER data, *independent
  pipelines and spot models* → the analysis-dependence axis.
- **J0740** (M≈2.08): Riley 2021 X-PSI STU NICER×XMM (Zenodo 5735003, run11 post_equal_weights,
  col1=mass col2=radius, verified M̄=2.071±0.065, R̄=12.30±0.94 vs published 2.08/12.39); Miller 2021
  Illinois–Maryland NICER+XMM (Zenodo 4670689, RM file col1=R col2=M).

GW tidal (GW170817), mapping-derived (M,R):
- GWTC-1 low-spin IMRPhenomPv2NRT posterior (LIGO-P1800370). Per component i∈{1,2}: source-frame mass
  m_i = m_i^det/(1+z), z=0.0099 (host NGC 4993, LOCKED); Λ_i = lambda1/lambda2. Map Λ→compactness via
  the quasi-universal **C–Love** relation (Yagi & Yunes 2017 review fit):
  C = M/R (geometrized) = 0.360 − 0.0355·ln Λ + 0.000705·(ln Λ)²,  then
  R[km] = 1.4766·(M/M☉)/C. Keep only Λ_i>0. Pool both components. This is EOS-insensitive to a few %
  but introduces a modelling step absent from NICER → the GW (M,R) is reported as **mapping-derived**,
  separately from the model-independent NICER core.

## Decision rules (LOCKED before running)

**D1 — analysis-dependence (analog of E48 KiDS statistic-dependence).** For each star, decompose every
pairwise pipeline/model difference {J0030: Riley19 | Miller-2spot | Miller-3spot; J0740: Riley21 |
Miller21} into value (‖Δμ‖) and shape (Bures²) with the full E48 control ladder: raw W₂ value-fraction,
joint-whitened, volume-stripped, and **orientation-only** (unit-determinant covariances). LOCKED lesson
from E48/E56: the raw W₂ "shape" term is precision-inflated; the robust orientation measure is the
scale-free ψ gap + orientation-only value-fraction. **Classification:** a pipeline difference is
*value-dominated* iff orientation-only vf > 0.5 AND ψ-gap < 20°; *orientation/shape-dominated* iff
ψ-gap > 20°.

**D2 — non-Gaussianity gate (analog of E48 sliced-Wasserstein check).** NICER (M,R) posteriors are
non-Gaussian (J0030 notably multimodal). For each pair, compare the empirical sliced-W₂² between the
actual sample clouds against the sliced-W₂² of Gaussian-resampled clouds with matched moments. If the
ratio departs from 1 by >30%, the Gaussian W₂ decomposition is flagged *unfaithful* and the empirical
sliced-W₂ (and its value/shape split via empirical means/covariances) leads.

**D3 — measurement-kernel orientation.** Report ψ (M–R long-axis angle) for every posterior. A
"kernel orientation split" between the X-ray-pulse-profile class and the GW-tidal class holds iff they
differ by >20° in the common whitened frame. Exploratory/descriptive (no pass/fail), like E56.

**D4 — cross-messenger value/shape at ~1.4 M☉.** NICER J0030 vs GW170817-derived (M,R): is the
X-ray↔GW difference value (different R at 1.4 → EOS stiffness) or shape? Reported with the C–Love
model-dependence caveat.

**D5 — QI shape figures of merit (reuse src/qinfo.py).** Per-probe purity/vN entropy (basis-invariant
anisotropy/concentration FoM); pairwise quantum shape-distinguishability (relent/fidelity/chernoff on
ρ=C/TrC) vs classical Gaussian Chernoff (value+shape). LOCKED honest note (from E62): classical
equal-covariance Chernoff = σ²/8 — a monotone of significance, not a new invariant.

## PASS / transfer criterion
The framework **transfers to NS-EOS** iff (a) the value/shape decomposition + ψ + precision controls +
non-Gaussianity gate all run and are interpretable on NS posteriors, and (b) at least one
physically-meaningful classification emerges (e.g. a pipeline difference is orientation/shape while a
cross-messenger R difference is value, or vice versa). This is a *demonstration-of-transfer* battery,
not a claim-kill. Honest limits reported up front: non-Gaussian posteriors (D2 gate), C–Love model
dependence (GW only), and the σ²/8 QI repackaging (D5).

## Falsifiers / honesty commitments
- If the Gaussian W₂ is unfaithful for the headline pairs (D2), do **not** quote Gaussian value
  fractions as the result — lead with empirical distances.
- Verify Riley/Miller (M,R) column identifications against each paper's published M,R credible
  intervals before any decomposition (column-swap is the obvious failure mode).
- The GW (M,R) is mapping-derived; never present it as on par with the model-independent NICER (M,R).
- Seed 63 for any resampling/sliced-projection draws.
