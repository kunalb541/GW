# SCOPE — what this paper is and is not (draft, 2026-07-18)

## Working title
*The Geometry of Gravitational-Wave Inference: a lawful anatomy of posteriors, systematics, and
cross-experiment consistency.*

## Claim structure (each claim already has a locked-prereg battery behind it in cosmo2)

| # | claim | evidence | status |
|---|---|---|---|
| 1 | The (m1,m2) posterior IS the constant-Mc curve (zero free params) | E40 (75 events) + E65 (derivation attempt + curvature diagnosis) + **E67 out-of-sample PASS on GWTC-4 (1.26 deg, prereg locked before data)** | strongest; publication-grade |
| 2 | Event-coherence separates method artifacts from physics | E59 (ringdown overtone: 22/22 coherent shift = systematic), E47/E48/E58 naive-combination catches; GR upheld across E45-E60 | solid; frame as methodology + null result |
| 3 | PTA inter-experiment differences are pure degeneracy-sliding; gamma monotone in span | E68 (4 arrays, offsets 94.6-99.9% along common degeneracy; span-ordering exact) | solid + carries a falsifiable successor prediction (IPTA DR3) |
| 4 | Spectral-siren H0: mass-scale is the top lever, dormant until ~1 km/s/Mpc | E66 (real icarogw joint chains, marginal-track + decile estimator pair) | solid; forward-looking |

## What is NEW work for this repo (not yet done anywhere)
- Self-contained port: freeze the relevant cosmo2 src/ + results JSONs here so the paper does not
  depend on a private repo's history.
- Figure suite: (a) curved-law gallery (GWTC-3 fit + GWTC-4 out-of-sample table as a figure);
  (b) tangent-vs-curve residuals vs elongation; (c) PTA (log10A, gamma) ellipses + degeneracy
  projection; (d) gamma-vs-span; (e) siren lever budget bar chart; (f) coherence-battery summary.
- A first-principles APPENDIX for the curved law: why thickness ~0 (0PN Fisher) and what sets the
  q-marginal extent — the honest half-derivation E65 left open (the rotation model is dead; the
  curve-support argument survives and should be written cleanly).
- Optional new battery (prereg here if run): GWTC-4 TGR products out-of-sample re-run of the
  E45-E60 gravity battery when the O4a TGR release lands.

## What this paper is NOT
- Not a detection claim, not a GR-violation claim, not a Hubble-tension resolution.
- No naive cross-event or cross-experiment posterior products (the E47/E58 lesson is part of the
  paper's METHODS section, stated as a rule).

## Data of record (all public; fetch scripts to be ported)
- GWTC-1: LIGO-P1800370 (GW170817). GWTC-2.1/3 PE: GWOSC eventapi -> Zenodo (76 events local).
- GWTC-4.0 PE: Zenodo 16053484 (86 events, per-event combined hdf5).
- LVK TGR products: Zenodo 17461225 (imr/par/rin/liv).
- GWTC-3 cosmology (icarogw joint): Zenodo 5645777.
- PTA: NANOGrav 15yr fig-1 release (via nanograv/15yr_stochastic_analysis); EPTA DR2 Zenodo
  8091568; PPTA DR3 github danielreardon/PPTA-DR3. CPTA: no public GWB chain (noted).

## Discipline (inherited unchanged)
Locked preregs before any new run; independent re-derivation of every headline; contract tests;
synthetic nulls where applicable; honest-limits sections mandatory; no silent data drops.
