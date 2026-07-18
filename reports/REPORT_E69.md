# E69 lab notebook - the ruler dichotomy: arbiters lean ladder-ward, verdict needs sigma_F <= 1.0

Prereg: preregs/E69_ruler_dichotomy_prereg.md (locked). The fork: classify every H0 measurement by
which calibration it inherits - the sound-horizon RULER (early-universe methods; a missing
pre-recombination ingredient moves this class), the distance LADDER (SN calibrated by stellar
rungs; a calibration systematic moves this class), or NEITHER (the arbiters: time-delay lensing,
megamasers, chronometers, GW sirens). If the early-ingredient hypothesis is right the arbiters
should side high (with the ladder); if the ladder-systematic hypothesis is right they should side
low (with the ruler). Inputs: the E16/E52-vetted table + two standard published additions (DESI DR2
BAO+BBN 68.51 +/- 0.58, arXiv 2503.14738; MCP megamasers 73.9 +/- 3.0, Pesce et al. 2020).

## Class consensuses (inverse-variance; all chi2 gates pass)

| class | H0 | chi2/dof |
|---|---|---|
| R - sound-horizon ruler (Planck; BAO+BBN) | 67.89 +/- 0.40 | 2.1/1 |
| L - distance ladder (SH0ES; JWST-CCHP) | 72.07 +/- 0.86 | 2.8/1 |
| **F - arbiters (TDCOSMO, masers, chronometers, sirens)** | **71.01 +/- 1.81** | 2.1/3 |

Pairwise: t(R,L) = 4.41 (the tension, restated between calibration classes);
**t(F,R) = 1.68 ; t(F,SH0ES) = 0.97**.

## Locked outcomes

| decision | outcome |
|---|---|
| D1 fork (ruler implicated / ladder implicated / underpowered) | **UNDERPOWERED/INCONCLUSIVE** (neither locked condition met) |
| D2 required precision | to reject R at 3 sigma the arbiters need sigma_F <= **0.96** (currently 1.81); rejecting SH0ES at 3 sigma is IMPOSSIBLE from the current F center (gap 2.0 < 3 x 1.04) |
| D3 sanity | all class chi2 pass; R-internal Planck-vs-BAO+BBN split 1.45 sigma (ruler internally consistent) |

## The refinement of E16 (the actually interesting part)

E16's per-anchor framing said "every non-SH0ES probe sits within 2.5 sigma of the early value" -
true, but driven by the arbiters' large individual error bars. The CLASS CONSENSUS tells a
different story: collectively the arbiters sit at 71.0, **closer to SH0ES (1.0 sigma) than to the
ruler (1.7 sigma)**. Leave-one-out inside F: the pull is not one-instrument -
- drop chronometers -> F = 72.84 (t vs SH0ES = 0.08, t vs R = 2.15): the three distance-based
  arbiters (lenses, masers, sirens) essentially SIT ON SH0ES;
- drop masers -> F = 69.36 (leans ruler-ward, 0.63): the maser point is the strongest high-puller;
- chronometers are the only low member - and they are the one F-member that is not a direct
  geometric distance (differential galaxy ages, own systematics tier).

So the current arbiter evidence, weak as it is, leans AGAINST the pure-SH0ES-systematic reading
and toward something real in the late-time distance scale - opposite to the naive reading of E52
("drop SH0ES and the tension fades"), because the arbiters that remain agree more with SH0ES than
with the ruler. Both statements are true simultaneously: SH0ES carries the STATISTICAL WEIGHT of
the tension (E52), while the weight-free DIRECTION of the arbiters leans SH0ES-ward (E69). This is
exactly the distinction the dichotomy was built to expose.

## When does it become decisive?

sigma_F <= 0.96 settles the fork at 3 sigma (if the F center holds). Roadmap arithmetic: TDCOSMO's
40-lens program targets ~2% (sigma ~1.5 alone); the maser program and O5-era sirens (E66: sirens
approach ~1 km/s/Mpc in the 2030s) each add comparable weight - the combination crosses the 0.96
threshold around the turn of the decade. The fork is answerable, on a known timetable, without any
new theory.

## Honesty

Class F is small and heterogeneous; TDCOSMO depends on mass-profile marginalization; masers are 6
galaxies; within-class independence approximate. All inputs are published Gaussian summaries
(synthesis tier). This battery allocates blame between calibration layers - it does not measure
new physics. Independent hand re-derivation of every consensus and tension (exact match);
3 contract tests pass.

Code: src/e69_ruler_dichotomy.py. Numbers: results/e69_ruler_dichotomy_results.json.
