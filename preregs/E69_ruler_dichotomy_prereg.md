# E69 preregistration — the ruler dichotomy: which layer does the H0 tension live in? (LOCKED 2026-07-17)

**The fork.** Every H0 measurement depends on one of two calibrations — or neither:
- **Class R (sound-horizon ruler):** early-universe methods whose H0 is set by the r_d ruler
  (a missing PRE-recombination ingredient changes r_d and moves this whole class together).
- **Class L (distance ladder):** SN Ia calibrated by stellar rungs (a ladder systematic moves
  this class, ruler methods unaffected).
- **Class F (free of both):** time-delay lensing, megamasers, cosmic chronometers, GW sirens.
  These are the ARBITERS: they inherit neither the ruler nor the ladder.

If the missing-early-ingredient hypothesis is right, F should side with L (high H0). If the
ladder-systematic hypothesis is right, F should side with R (low H0). E61/E64's obstruction arrow
points at early physics; E52 points at SH0ES — this battery makes the two hypotheses fight.

## Measurements (all previously vetted in E16/E52, plus one addition)
- R: Planck CMB 67.36 ± 0.54; DESI DR2 BAO + BBN (CMB-free ruler calibration) 68.51 ± 0.58
  [arXiv 2503.14738 — NEW to the table, standard published value].
- L: SH0ES Cepheid 73.04 ± 1.04; JWST-CCHP combined (TRGB/JAGB-calibrated SN) 69.96 ± 1.53
  (components not double-counted, per E52).
- F: cosmic chronometers 67.8 ± 3.0; TDCOSMO 2025 time-delay 71.6 ± 3.6; MCP megamasers
  73.9 ± 3.0 [Pesce et al. 2020 — NEW to the table, standard published value]; GW sirens
  69.3 ± 12.9 (E16 real GWTC-3 posterior).

## Method
Inverse-variance consensus per class (assumes independence within class — see honesty), internal
chi2/dof per class, pairwise class tensions t(X,Y) = |mu_X - mu_Y|/sqrt(sig_X^2 + sig_Y^2),
leave-one-out within class F (which arbiter drives the F consensus).

## Decision rules (LOCKED)
- **D1 (the fork).**
  - "RULER IMPLICATED (early ingredient)": t(F,R) >= 2 AND t(F, SH0ES) < 1.
  - "LADDER IMPLICATED (SH0ES systematic)": t(F,R) < 1 AND t(F, SH0ES) >= 2.
  - Anything else: "UNDERPOWERED/INCONCLUSIVE at current precision" — then D2 is the deliverable.
- **D2 (required precision).** Holding current central values fixed, solve for the sigma_F at
  which the F consensus discriminates R-center from SH0ES-center at 3 sigma. Compare with the
  actual sigma_F and with forecast improvements (TDCOSMO ~40 lenses, O5 sirens, more masers).
- **D3 (sanity gates).** (a) no measurement in two classes; (b) chi2/dof < 3 within each class
  (else the class consensus is flagged unreliable and the discordant member identified);
  (c) R-class internal consistency (Planck vs BBN-calibrated BAO) reported — a >2 sigma split
  WITHIN R would itself be evidence about the ruler.

## Honesty commitments
- Class F is heterogeneous and small; TDCOSMO's value depends on mass-profile assumptions
  (its error bar reflects the marginalized analysis); the maser sample is 6 galaxies. Within-class
  independence is an approximation (shared peculiar-velocity corrections etc.) — stated.
- Inverse-variance consensus is Gaussian; all inputs are published Gaussian summaries (synthesis
  tier per the E1 discipline — no chain-level information available for most).
- No new physics is claimed from this battery alone; it allocates BLAME between layers, with D2
  quantifying when the allocation becomes decisive.
- No RNG. All numbers of record in the results JSON.
