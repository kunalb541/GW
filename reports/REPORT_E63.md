# E63 lab notebook - value/shape geometry transferred to the neutron-star mass-radius plane

Prereg: preregs/E63_neutron_star_eos_prereg.md. First cross-domain transfer of the cosmo2 value/shape
machinery (mean-offset "value" vs covariance "shape/orientation", plus the QI shape toolbox) out of
cosmology and into the neutron-star dense-matter equation of state. Working plane: (M [Msun], R [km]).
Real public posteriors, all equally weighted:

- NICER X-ray pulse-profile, low-mass star **J0030** (M~1.4): Riley 2019 X-PSI ST+PST
  (Zenodo 3386449; col1=M col2=R verified M=1.336+/-0.146, R=12.70+/-1.12 vs published 1.34/12.71);
  Miller 2019 Illinois-Maryland 2-oval and 3-oval (Zenodo 3473466).
- NICER X-ray pulse-profile, high-mass star **J0740** (M~2.08): Riley 2021 X-PSI STU NICERxXMM
  (Zenodo 5735003 run11; M=2.071+/-0.065, R=12.30+/-0.94 vs published 2.08/12.39); Miller 2021
  NICER+XMM (Zenodo 4670689; R=14.05+/-2.08 - the known broad-Miller radius).
- GW tidal, **GW170817** (LIGO-P1800370 GWTC-1 low-spin IMRPhenomPv2NRT): per component, source-frame
  mass (z=0.0099) and Lambda -> compactness via the quasi-universal C-Love relation
  (C = 0.360 - 0.0355 lnL + 0.000705 (lnL)^2), R = 1.4766 M/C. Pooled: R=11.35+/-1.87, lambda_tilde
  median ~406 (published <=630 at 90%). **Mapping-derived - reported apart from the model-independent
  NICER (M,R).**

## Headline methodological finding: in (M,R) there is no metric-free orientation ANGLE

Unlike the cosmology (Om, sigma8) plane - two comparably scaled dimensionless axes, where the
degeneracy angle psi carried the "shape" story - the (M,R) plane has **incommensurate units**
(solar masses vs kilometres). The principal-axis angle is then metric-dependent (whitening by the
average covariance forces the two long axes orthogonal by construction: an artifact, not a signal;
it gave a spurious psi_gap=90 deg on every pair until caught). The scale-free shape invariant that
survives is the **correlation rho(M,R)** (invariant under independent rescaling of either axis).
This is a real lesson about porting the framework: use rho, not psi, whenever the plane's axes are
not commensurable.

## D1 - pipeline/model dependence of a single star is VALUE-dominated

Same star, same data, different analysis pipeline (Riley X-PSI vs Miller Illinois-Maryland) or spot
model (2-oval vs 3-oval). Decomposed with the E48 control ladder (raw / joint-whitened /
orientation-only value fraction) + scale-free delta-rho + precision(volume) ratio + the E48
empirical-vs-Gaussian sliced-Wasserstein faithfulness gate.

| pair (same star) | sigma | vf_orient | delta_rho | vol ratio | Gauss-faithful | verdict |
|---|---|---|---|---|---|---|
| J0030 Riley19 vs Miller 2-oval | 0.74 | 0.96 | 0.05 | 1.05 | yes (0.95) | value-dominated |
| J0030 Riley19 vs Miller 3-oval | 0.88 | 1.00 | 0.02 | 1.01 | yes (1.00) | value-dominated |
| J0030 Miller 2-oval vs 3-oval  | 0.36 | 0.90 | 0.03 | 0.96 | yes (0.82) | value-dominated |
| J0740 Riley21 vs Miller21      | 1.09 | 0.91 | 0.08 | 3.16 | yes (0.97) | value-dominated |

Every pipeline/model difference is a **central-value offset at fixed orientation** (delta-rho <= 0.08;
orientation-only value fraction 0.90-1.00). The J0740 Riley-vs-Miller case is the sharpest: a +1.75 km
radius offset (Miller 14.05 vs Riley 12.30, ~0.77 sigma_R) **plus** a 3.2x larger Miller error ellipse
- a value + precision difference, not a reoriented posterior. This is the **opposite** of the
cosmology analog: the KiDS statistic-dependence (E48) was a precision/shape artifact, whereas the
NICER pipeline systematic is a genuine value offset. All pairs pass the non-Gaussian gate (the
Gaussian moment distance is faithful to the sample-cloud distance to within 5-18%).

## D3 - the M-R correlation is organized by MASS REGIME, robustly across pipelines

| probe | rho(M,R) |
|---|---|
| J0030 Riley19 (low mass) | +0.837 |
| J0030 Miller 2-oval      | +0.891 |
| J0030 Miller 3-oval      | +0.857 |
| J0740 Riley21 (high mass)| +0.294 |
| J0740 Miller21           | +0.211 |
| GW170817 (C-Love)        | +0.276 |

Low-mass J0030 sits at rho ~ +0.86 (a steep, strongly correlated M-R banana); high-mass J0740 at
rho ~ +0.25 (the near-flat top of the M-R curve, R almost independent of M). The regime split is
**delta-rho = 0.61**, and rho is **consistent across independent pipelines within each star**
(J0030: 0.84/0.89/0.86; J0740: 0.29/0.21) - so the orientation is set by where the star sits on the
mass-radius curve (the measurement geometry x EOS-curve location), not by the analysis choice. This is
the NS analog of "the kernel sets orientation": here the organizing variable is mass regime.

## D4 - cross-messenger (X-ray J0030 vs GW170817 at ~1.4 Msun) is MIXED (flagged)

| pair at M~1.4 | sigma | vf_orient | rho: X-ray -> GW | verdict |
|---|---|---|---|---|
| J0030 Miller 3-oval vs GW170817 | 1.11 | 0.58 | +0.86 -> +0.28 | mixed (value+orientation) |
| J0030 Riley19 vs GW170817       | 1.15 | 0.62 | +0.84 -> +0.28 | mixed (value+orientation) |

At the same ~1.4 Msun the X-ray and GW probes differ in **both** central radius (GW R~11.3 km ~1.5-1.7
km smaller than NICER-J0030 R~13 km, a mild ~1.1 sigma value offset that matches the known
GW170817-prefers-smaller-R discussion) **and** correlation (rho 0.86 -> 0.28). CAVEAT (locked): the GW
rho is C-Love-mapping-induced. The physical reading is that the tidal-derived R~const-in-M gives low
rho (tracking the flat true M-R curve), while NICER-J0030's high rho is a pulse-profile measurement
degeneracy (the banana) - but I do not over-claim this split; D4 is exploratory, the value offset is
the defensible part, the orientation part is mapping-dependent.

## D5 - QI shape figures of merit

All six posteriors are near-pure density matrices rho=C/Tr(C) (purity 0.990-0.996, von Neumann
entropy 0.013-0.031) - i.e. highly anisotropic error ellipses, as expected for a strong M-R
degeneracy. Miller J0740 is the most anisotropic (purity 0.996) - its large-but-thin banana. The
per-probe purity/vN entropy are basis-invariant figures of merit that survive the unit-incommensurability
that kills psi. As flagged in E62, the classical equal-covariance Chernoff exponent = sigma^2/8 remains
a monotone of significance (repackaging), so it is reported but not headlined.

## Contract tests

tests/test_e63_ns_eos.py (5 pass): a probe vs itself -> ~0 sigma and delta-rho~0 (no manufactured
tension); a pure mean shift -> value-dominated with unchanged rho; a pure orientation change -> shows
up as delta-rho; the C-Love map gives R in 10.5-12.5 km at (M=1.4, L=300); rho is scale-invariant
under arbitrary unit changes. Every headline number independently re-derived through a separate
np.corrcoef / direct-moment code path.

## Net

The value/shape framework **transfers** to the neutron-star EOS, with one genuine adaptation and two
clean physical results. Adaptation: the shape descriptor must be the scale-free correlation rho, not
the metric-dependent angle psi, because (M,R) axes are not commensurable. Results: (D1) the NICER
pipeline/model systematic is a value offset at fixed orientation (unlike cosmology's precision-driven
KiDS case, E48); (D3) the M-R correlation is organized by mass regime and is robust across independent
pipelines - the measurement-plane shape tracks the EOS curve. Honest limits carried up front:
NICER posteriors are non-Gaussian (D2 gate passed for the pair distances but the marginals, esp.
J0030, are multimodal), the GW (M,R) is C-Love-mapping-derived (D4 flagged), and the QI Chernoff is
sigma^2/8 repackaging (D5). Machinery and every number verified (independent re-derivation + 5 contract
tests). Data: data/nseos/ (gitignored). Code: src/e63_neutron_star_eos.py. Numbers:
results/e63_neutron_star_eos_results.json.
