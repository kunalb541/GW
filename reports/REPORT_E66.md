# E66 lab notebook - spectral-siren H0 obstruction: REFUTED at GWTC-3 precision (mu_g is the top lever, but small)

Prereg: preregs/E66_spectral_siren_obstruction_prereg.md (locked). The radical claim under test
(E61's obstruction logic transplanted to GW): the spectral-siren H0 program is obstructed by the
source-mass scale - an unmodeled drift of the ~33 Msun power-law+peak feature would move H0 by more
than the precision needed to arbitrate the CMB-vs-SH0ES tension. Test: linear-response couplings on
the REAL LVK GWTC-3 joint (cosmology + population) posterior (icarogw data release, Zenodo 5645777,
O3_icarogw_data_distro.json).

Primary chain: SNR_11 BBH power-law+gaussian, restricted flat-LCDM (n=13,533; H0 free in [65,77],
Om0 fixed; full mass function mu_g/sigma_g/lambda_peak/mmin/mmax/delta_m/alpha/beta + rate evolution
gamma/kappa/zp jointly sampled). H0 = 70.71 (sd 3.35, prior-clipped); mu_g = 32.50.

## Mid-run honesty catch (locked stop-and-diagnose rule fired)

D3(b) initially FAILED: the multivariate linear-response M = C_AB C_BB^-1 (a PARTIAL/conditional
coupling, holding the other 10 population parameters fixed) disagreed with the decile regression
(a MARGINAL slope) - not an estimator bug but an apples-to-oranges comparison in my implementation,
exposed exactly as the prereg's mandatory-second-estimator rule intended (the E61 steepest-ascent
lesson). Fix: the physically relevant number for "the true peak drifts and the fit follows the
degeneracy" is the MARGINAL track cov(H0, theta)/var(theta); the decile regression cross-checks
that like-for-like. After the fix all three D3 gates pass (mu_g in range; estimators agree in sign
and within 2x for the top-3 levers; top-lever sign reproduced in the wide-prior w0flatLCDM chain).
Both couplings are reported in the results JSON (partial kept as a diagnostic).

## Results

| param | dH0/dtheta (marginal) | dH0 per 1-sigma drift | decile check | group |
|---|---|---|---|---|
| mu_g   | -0.128 | -0.344 | -0.133 | MASS |
| gamma  | -0.105 | -0.175 | -0.100 | RATE |
| zp     | +0.111 | +0.107 | +0.116 | RATE |
| mmin   | -0.135 | -0.106 | -0.145 | MASS |
| (rest) | ... | <=0.10 | ... | |

| decision (locked) | outcome |
|---|---|
| D1: dH0(4 Msun mu_g drift) >= 2 km/s/Mpc confirms; < 1 refutes | **-0.51 km/s/Mpc -> REFUTED** |
| D2: dominant lever group | MASS 0.38 vs RATE 0.22 km/s/Mpc (quadrature, per-1sig); top lever = mu_g |
| D3: sanity gates (a/b/c) | all pass (after the estimator fix above) |
| robustness | dH0(4 Msun) = -0.41 (SNR10), -0.32 (SNR12); broken-powerlaw top mass proxy -0.10/1sig |

## Reading

The obstruction hypothesis is REFUTED at GWTC-3 precision: a 4 Msun coherent mis-modelling of the
peak location - the scale of the currently debated catalog-to-catalog peak differences - biases the
spectral-siren H0 by only ~0.5 km/s/Mpc, an order of magnitude below the CMB-vs-SH0ES gap and well
inside the ~3.3 statistical error of the restricted chain itself. The error budget is statistics-
dominated; the mass function is not yet the wall. What survives of the radical idea: mu_g IS the
single largest systematic lever (D2), ahead of every rate-evolution parameter, so the obstruction
becomes live when spectral-siren statistical precision reaches ~1 km/s/Mpc (O5/XG era) - at that
point an independently pinned peak (or a z-dependent peak model) becomes mandatory. The locked
conservative caveat stands: the restricted H0 prior [65,77] compresses couplings, so these are
lower bounds on the coupling strength - but even the SNR-10 variant (-0.41 per 4 Msun) sits far
from the 2 km/s/Mpc confirmation threshold, so the verdict does not hinge on the caveat.

Honest scope: GWTC-3-era icarogw analysis only; the GWTC-4 cosmology release should be re-tested
when public (flagged as the out-of-sample follow-up).

Code: src/e66_spectral_siren_obstruction.py. Numbers: results/e66_spectral_siren_obstruction_results.json.
Data: data/chains/e66/ (gitignored; Zenodo 5645777).
