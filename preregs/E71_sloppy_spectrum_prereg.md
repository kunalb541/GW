# E71 preregistration — are GW posteriors sloppy? The eigenvalue-ladder test (LOCKED 2026-07-18)

**Hypothesis (imported from sloppy-model theory, Sethna/Transtrum).** Multiparameter fits
generically have Fisher/covariance spectra whose eigenvalues are roughly GEOMETRICALLY spaced
(log-uniform ladders) spanning decades — "stiff" to "sloppy" — and the posterior is a
hyperribbon with a geometric hierarchy of widths. E40/E65/E67 established the 2D projection
(stiff = chirp mass, sloppy = mass ratio). E71 tests the claim at FULL dimensionality, per event,
across two catalogs: is the eigenvalue ladder (a) wide (decades), (b) log-uniform, and (c)
UNIVERSAL in shape across events?

## Data
All local events: GWTC-2.1/3 (76, `data/chains/gw_posteriors/*_PE.h5`, preferred dataset via the
E38 helper) and GWTC-4.0 (86, `data/chains/gwtc4/*.hdf5`, Mixed-largest per the E67 rule).

## Parameter set (LOCKED — fixed 7D across all events)
{ln chirp_mass, mass_ratio, chi_eff, a_1, a_2, ln luminosity_distance, cos theta_jn}
(detector-frame Mc; ln for the two positive scale parameters; angles as cosines). Events missing
any field are dropped AND listed (honesty rule; no silent drops). Spectrum = eigenvalues of the
weighted CORRELATION matrix (unit diagonal — unit-free, so the ladder measures pure degeneracy
structure, not unit choices).

## Statistics (per event)
- span = log10(lambda_max / lambda_min);
- gap uniformity: relative CV of consecutive log-eigenvalue gaps, gapCV = std(gaps)/mean(gaps)
  (0 = perfectly geometric ladder);
- normalized ladder: (log lambda_i − mean)/(span) — a 7-vector describing ladder SHAPE.

## Decision rules (LOCKED)
- **D1 (sloppy scale-separation).** Median span across events >= 2.0 decades. PASS/FAIL.
- **D2 (log-uniformity).** Median gapCV < 0.75 AND smaller than the median gapCV of the
  two-scale null (a "stiff+degenerate cluster" spectrum: one large eigenvalue, six equal small
  ones, matched span — the natural non-sloppy alternative). PASS/FAIL.
- **D3 (universality).** Median pairwise RMS distance between events' normalized ladders < 0.10
  (ladders collapse to one shape after location-scale normalization), AND the GWTC-3 mean ladder
  equals the GWTC-4 mean ladder within RMS 0.05 (cross-catalog out-of-sample flavor). PASS/FAIL.
- **D4 (contract).** Synthetic isotropic Gaussian -> span ~ 0 (machinery cannot manufacture
  sloppiness); synthetic geometric ladder recovered with gapCV < 0.05. Pytest.
- Descriptive (no pass/fail): span vs elongation/SNR-proxy; which eigenvector is stiffest
  (prediction from theory: dominated by ln Mc).

## Honesty commitments
- Correlation-matrix spectra measure DEGENERACY geometry, not raw Fisher information; the choice
  is locked because it is unit-invariant. The alternative (log-parameter covariance) is reported
  as a robustness column, not used for decisions.
- Sky location, polarization, and phase are excluded (multimodal/periodic — would break the
  Gaussian spectral summary); stated scope: the 7D intrinsic+distance+inclination block.
- The sloppy prediction is an empirical regularity, not a theorem — D1-D3 failing is a
  publishable anti-sloppiness result, not an error.
- Prior art: the Mc-stiff direction is classic (Cutler & Flanagan 1994); the NEW content is the
  catalog-scale ladder statistics and universality. Seed 71 (no RNG in main path).
