# E42 preregistration — black-hole population map + posterior-precision lawfulness

Status: LOCKED (Part B decision rules) before computing precision-vs-SNR. Date 2026-07-07.
Part A (population map) is descriptive exploration; Part B is the locked test. 76 LVK events.

## Part A - population exploration (descriptive, no gates)

From E38 per-event medians + GWOSC SNR: report the source-frame mass spectrum (primary mass m1,
total mass, chirp mass), the mass-ratio q distribution, the effective-spin chi_eff distribution
(fraction with chi_eff < 0 -> dynamical-formation signature; mean), the final-mass/spin, and
distance/redshift reach. Flag population landmarks (the ~35 Msun m1 peak, the pair-instability
region >~50-120 Msun, IMBH-scale remnants Mf > 100 Msun, BNS/NSBH low-mass systems). Rank the
geometric outliers (events far from the population in standardized per-plane rho/log-axis-ratio
space) and cross-reference with physical extremity (mass, q, chi_eff, distance z-scores).

## Part B - posterior-precision lawfulness (LOCKED)

Hypothesis: chirp-mass fractional precision follows the Fisher law sigma(Mc)/Mc ~ 1/SNR, i.e.
log10(sigma_Mc/Mc) = a + b*log10(SNR) with b ~ -1. sigma_Mc estimated from the stored chirp-mass
q16/q84 as (q84-q16)/2 (a robust ~1-sigma proxy). SNR = network matched-filter SNR (GWOSC).

Secondary (cycle-count): the inspiral cycle count N ~ Mc^{-5/3} predicts BETTER fractional
precision at LOWER mass, so at fixed SNR sigma_Mc/Mc should INCREASE with Mc (positive partial).

### Decision rules (LOCKED)

D1 (PRIMARY): Pearson r(log sigma_Mc/Mc, log SNR) is NEGATIVE with |r| >= 0.4 and p < 0.01.
   -> precision improves with SNR as Fisher requires. Fail = precision not SNR-controlled.
D2 (SLOPE): OLS slope b in [-1.5, -0.5] (consistent with the Fisher -1). Meeting D1 but not D2
   = SNR controls precision but with a non-Fisher exponent (report the value).
D3 (CYCLE, secondary): partial correlation of log(sigma_Mc/Mc) with log(Mc) controlling for
   log(SNR) is POSITIVE (higher mass -> worse fractional precision). Reported; not a gate.

## Interpretation

D1+D2 pass would COMPLETE the geometry-from-physics program: orientation (E40), correlation
sign (E41), and now SIZE/precision all predicted from physics for the chirp-mass-dominated
sector. A non-Fisher slope or failure is reported as-is (priors, non-Gaussian tails, or
heterogeneous detector networks would break the clean 1/SNR law).

## Provenance

results/e38_gw_black_hole_geometry_results.json (76 events, medians + q16/q84);
GWOSC network_matched_filter_snr (fetched, all 76 matched). No RNG.
