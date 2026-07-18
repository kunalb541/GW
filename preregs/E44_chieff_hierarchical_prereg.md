# E44 preregistration — hierarchical chi_eff population: does it require support below zero?

Status: LOCKED before fitting. Date 2026-07-07. The rigorous follow-up to the E43 per-event null.
E43 found no single securely-negative event; E44 asks whether the POPULATION distribution of
chi_eff, marginalizing over every event's measurement uncertainty, requires a negative component.

## Model

Standard Gaussian effective-spin population (Roulet & Zaldarriaga 2019; LVK default):
  chi_eff ~ Normal(mu, sigma)   truncated to the physical range [-1, 1].
Hierarchical Monte-Carlo likelihood using each event's posterior samples:
  L(mu, sigma) = Prod_i [ (1/N_i) Sum_j Normal(chi_eff_ij; mu, sigma) ]
evaluated on a grid mu in [-0.2, 0.3], sigma in [0.01, 0.40], flat hyperprior. This treats the
per-event effective prior as ~flat over the chi_eff bulk; because the true induced chi_eff prior
is PEAKED at 0, NOT reweighting biases sigma LOW -> a CONSERVATIVE (lower-bound) estimate of the
population width and of the negative fraction. (Reweighting by the induced prior would only
broaden sigma and increase the negative fraction.)

Negative fraction: f_neg = Phi(-mu/sigma) (Gaussian mass below 0), computed per grid point and
propagated to a posterior via the (mu,sigma) posterior weights.

## Decision rules (LOCKED)

D1 (SPREAD REQUIRED): the marginal posterior on sigma has 90% credible LOWER bound > 0.05
   -> the population has intrinsic chi_eff spread (not a spike at mu).
D2 (NEGATIVE SUPPORT): the negative fraction f_neg has 90% credible LOWER bound > 0.05
   -> the population robustly places at least ~5% of sources at chi_eff < 0.
D3 (DECISIVE, truncation comparison): fit the SAME model truncated to chi_eff >= 0 (a strictly
   non-negative population) and compare max log-likelihood. If the free model beats the
   positive-truncated model by delta_lnL >= 3 (a ~e^3 ~ 20x likelihood ratio), the data PREFER
   support below zero. Reported as the cleanest "requires negatives" statistic.

## Interpretation

D1 & D2 pass (and D3 favouring the free model) = the BBH population requires a chi_eff<0
component even though NO single event is individually secure (E43) -- the standard hierarchical
result, and a clean demonstration that population inference sees what per-event counts cannot.
If D3 does not favour the free model, the negatives are not required and E43's null stands at the
population level too. Reported as-is either way.

## Honest scope

- Effective-prior treated as flat (conservative for width, as argued); not the full induced
  chi_eff prior reweighting.
- No selection-function / detection-bias modelling (selection mildly disfavours negative chi_eff,
  so accounting for it would push mu/f_neg slightly HIGHER, i.e. more negatives -- our omission is
  again conservative for the existence claim).
- Gaussian population form assumed (standard); a broader model class is not explored.

## Provenance

data/chains/gw_posteriors/*.h5 (74 usable events, chi_eff samples). No downloads, no RNG.
