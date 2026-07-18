# E38 — Gravitational-Wave Black-Hole Posterior Geometry

Question: can real GW event posterior samples be explored using the same value/shape geometry
language as the cosmology atlas?

## Locked scope

This is a black-hole posterior-geometry experiment, not a quantum-gravity or no-hair test.

## Locked inputs

- Public GWOSC cumulative event catalog:
  `https://gwosc.org/eventapi/json/GWTC/`
- Cached public posterior HDF5 files under `data/chains/gw_posteriors/` when present. This
  directory is ignored by git; only derived compact results are committed.

For the first pass, use every completed `*_PE.h5` posterior chain cached in
`data/chains/gw_posteriors/`. The initial required anchors are:

- `GW190521_074359` — high-mass BBH anchor.
- `GW190814` — asymmetric mass-ratio anchor.

Use GWOSC summary rows for landmark context:

- `GW150914`
- `GW170817`
- `GW190521_074359`
- `GW190814`

## Locked planes

Compute mean/covariance geometry for available posterior-sample planes:

- `(mass_1_source, mass_2_source)`
- `(chirp_mass_source, mass_ratio)`
- `(mass_ratio, chi_eff)`
- `(final_mass_source, final_spin)`
- `(luminosity_distance, cos_iota)`
- `(redshift, total_mass_source)`

For each plane report `psi`, `rho`, axis ratio, medians, and 16/84% intervals.

## Decision

PASS if at least two actual posterior HDF5 chains are read and at least four geometry planes
are computed for each BBH-like chain with available columns.

## Interpretation

A PASS supports GW posterior geometry as a real extension of the observation-geometry atlas.
It does not support modified gravity, quantum gravity, or no-hair violation claims. Those require
dedicated LVK GR-test products such as inspiral-merger-ringdown consistency, ringdown tests,
modified dispersion, polarization, or parameterized-deviation posteriors.
