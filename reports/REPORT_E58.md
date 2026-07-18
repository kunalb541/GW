# E58 lab notebook - massive graviton / Lorentz-violation bound from GWTC-3 (gravity via black holes)

Prereg: preregs/E58_massive_graviton_liv_prereg.md. LVK GWTC-3 Tests-of-GR LIV release (Zenodo
17461225, liv.zip, 7.40 GB). Modified GW dispersion E^2 = p^2c^2 + A*p^alpha; alpha=0 is the MASSIVE
GRAVITON (A = m_g^2 c^4), GR predicts no dispersion. 12 events x 8 orders alpha in
{0,0.5,1,1.5,2.5,3,3.5,4}, Aplus/Aminus branches. Parameter: log10(lambda_eff/m).

## Result: GR upheld; graviton-mass bound (per-event, robust)

| decision (locked) | outcome |
|---|---|
| D1 GR-consistent, no LIV detection | PASS (every event's log10lambda_eff reaches the prior edge; GR/large-lambda not excluded) |
| D2 per-event graviton bound < 1e-22 eV/c^2 | PASS (best single-event m_g < 6.7e-24) |

Per-event alpha=0 graviton bounds (90% one-sided):

| event | log10(lambda_g/m) > | m_g < [eV/c^2] |
|---|---|---|
| S200219ac | 17.27 | 6.7e-24 |
| S191222n | 17.20 | 7.9e-24 |
| S200208q | 17.06 | 1.1e-23 |
| ... | ... | ... |
| S191216ap | 15.95 | 1.4e-22 |

best single-event m_g < 6.7e-24 eV/c^2; median event 1.8e-23. These are consistent with the LVK
GWTC-3 single-event and combined bounds (combined 1.27e-23 eV/c^2).

## Honesty catch: the COMBINED bound is prior-dependent (do NOT quote the naive product)

A naive posterior-product combination gave m_g < 5.9e-27 (grid-unstable; ~3 orders tighter than the
LVK full-catalog bound) -- clearly WRONG. Cause: LVK sample the LIV coefficient with a flat-in-A
prior, which is NON-flat in log10lambda; multiplying the released POSTERIORS (not likelihoods)
over-counts that prior n times, and the prior samples are EMPTY in the release so it cannot be
divided out. The correct combined bound is the LVK flat-in-A result m_g <= 1.27e-23 eV/c^2, which I
quote rather than fabricate a tighter number. This battery therefore reports the PER-EVENT bounds
(prior is what it is per event -> robust) as its result, not a home-made combination. (Same class of
issue as the E47 histogram-product and E48 sliced-W bugs -- caught by the sanity check that a 12-event
bound cannot beat the full-catalog bound.)

## LIV bounds per dispersion order (per-event median / best log10lambda_eff lower bound)

| alpha | Aplus (med/best) | Aminus (med/best) |
|---|---|---|
| 0 | 16.85 / 17.27 | 16.67 / 16.87 |
| 0.5 | 19.9 / 20.61 | 19.63 / 20.06 |
| 1 | 26.41 / 27.08 | 26.0 / 26.37 |
| 1.5 | 44.77 / 46.03 | 44.63 / 44.79 |
| 2.5 | -39.55 / -39.01 | -39.64 / -39.43 |
| 3 | -16.78 / -16.42 | -16.83 / -16.75 |
| 3.5 | -14.58 / -14.44 | -14.6 / -14.56 |
| 4 | -7.78 / -7.59 | -7.78 / -7.69 |

(The log10lambda_eff scale is defined differently for alpha<2 vs alpha>2, hence the sign change; all
orders are GR-consistent bounds, no detection.)

## Conclusion

Gravity's propagation is Lorentz-invariant to within the GWTC-3 sensitivity: no modified-dispersion /
graviton-mass signal in any of the 12 events across 8 orders. The graviton is massless to
m_g < 6.7e-24 eV/c^2 (best single event; LVK combined 1.27e-23). This is a GW-PROPAGATION gravity
test, complementing E45-E47 (waveform deviations) and E57 (horizon area).

## Provenance

data/chains/tgr/IGWN-GWTC3-TGR-v1-liv.zip (Zenodo 17461225, 7.40 GB, size-verified, gitignored). No RNG.
