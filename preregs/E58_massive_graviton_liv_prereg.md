# E58 preregistration — massive graviton / Lorentz-violation bound from GWTC-3 (LOCKED 2026-07-07)

Gravity via black holes: the GW dispersion relation E^2 = p^2c^2 + A*p^alpha (Mirshekari-Yunes-Will)
tests Lorentz invariance of gravity. alpha=0 is the MASSIVE GRAVITON (A = m_g^2 c^4). GR predicts no
dispersion (A=0, i.e. the LIV wavelength lambda_A -> infinity). Data: LVK GWTC-3 Tests-of-GR LIV
release (Zenodo 17461225, liv.zip), 12 events x 8 dispersion orders alpha in {0,0.5,1,1.5,2.5,3,3.5,4}
(alpha=2 = GR excluded), Aplus/Aminus sign branches. Measured parameter: log10(lambda_eff/m).

## Method

For alpha=0 (graviton) ONLY the Aplus branch is physical (m_g^2 >= 0). Per event: log10lambda_eff
posterior gives a one-sided LOWER bound on lambda_g (GR = large lambda). Combine events by
multiplying the posterior densities on a common grid (flat-in-log prior) -> combined lower bound.
Graviton mass: m_g c^2 [eV] = (h*c/e)/lambda_g = 1.2398e-6 / lambda_g[m].
For other alpha: report the combined log10lambda_eff bound per order (Aplus and Aminus) as the LIV
constraint.

## Decision rules (LOCKED)

D1 (GR-CONSISTENT, no LIV detection): for every event, the 95th percentile of log10lambda_eff
   reaches the prior upper edge (GR / large-lambda not excluded). FAIL if any event EXCLUDES the
   GR limit (posterior 95th percentile well below the prior edge -> a LIV preference).
D2 (GRAVITON MASS BOUND): the combined alpha=0 90% lower bound on log10(lambda_g/m) yields an
   upper bound m_g < ~1e-22 eV/c^2 (order-of-magnitude consistent with the LVK GWTC-3 combined
   bound m_g <~ 1.3e-23 eV/c^2). Report the actual number.
D3 (LIV ORDERS): report the combined log10lambda_eff lower bounds for all 8 alpha orders.

## Interpretation

Expected under GR: D1 all GR-consistent (bounds, not detections), D2 a graviton-mass upper bound of
order 1e-23 eV, D3 finite bounds per order. A genuine LIV detection (D1 fail) would be extraordinary
and treated with extreme skepticism. Reported as-is. This is a GW-PROPAGATION gravity test (distinct
from the E45-E47 waveform-deviation and E57 horizon-area tests).

## Provenance

data/chains/tgr/IGWN-GWTC3-TGR-v1-liv.zip (Zenodo 17461225, 7.40 GB, size-verified, gitignored).
No RNG.
