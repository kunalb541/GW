# E38 lab notebook — gravitational-wave black-hole posterior geometry

Pre-registration: `preregs/E38_gw_black_hole_geometry_prereg.md`

Command:

```bash
python -m src.e38_gw_black_hole_geometry
```

## Question

Can we use actual GW event chains to explore black holes and gravity with the same geometry
language as the cosmology atlas?

## Data

E38 reads every public posterior HDF5 sample cached from GWOSC/Zenodo under
`data/chains/gw_posteriors/`. The cache now holds ALL 76 confident GWTC-1/2.1/3 events
(fetched by scripts/fetch_gw_chains.py; ~8.4 GB, gitignored), up from the original 14.
(Initial writeup below reflects the first 14-event pass; the expanded set is used by E40.)

Raw HDF5 files live under `data/chains/gw_posteriors/`, which is ignored by git. The committed
artifact is only the compact derived geometry JSON.

## Result

Expanded run: 76 posterior chains read successfully, 1,541,342 total samples, 74/76 producing
all six planes. (Original 14-event pass detail retained below.) Two anchor examples:

- `GW190521_074359`: 8,111 posterior samples read from `C01:Mixed/posterior_samples`
- `GW190814`: 78,224 posterior samples read from `C01:Mixed/posterior_samples`

Most events produced geometry across all six black-hole planes:

- masses: `(mass_1_source, mass_2_source)`
- source chirp mass vs mass ratio
- mass ratio vs effective spin
- final mass vs final spin
- distance vs inclination proxy
- redshift vs total source mass

Selected geometry:

| event | plane | psi | rho | axis ratio |
|---|---:|---:|---:|---:|
| GW190521_074359 | `(mass_1_source, mass_2_source)` | 131.3 | -0.365 | 1.5 |
| GW190521_074359 | `(final_mass_source, final_spin)` | 0.2 | +0.322 | 103.8 |
| GW190814 | `(mass_1_source, mass_2_source)` | 175.5 | -0.945 | 36.7 |
| GW190814 | `(mass_ratio, chi_eff)` | 99.8 | -0.955 | 19.1 |
| GW190814 | `(final_mass_source, final_spin)` | 0.9 | +0.789 | 78.8 |

The expanded run also shows a repeated population-level pattern: many BBH events have a very
elongated final-mass/final-spin geometry and a near-vertical redshift/total-mass geometry, while
mass-ratio/spin geometry separates asymmetric systems such as `GW190814` from more ordinary BBH
events.

## Interpretation

Supported:

- GW event posteriors can be reduced to the same value/shape geometry objects as cosmology
  posteriors.
- Landmark events occupy distinct black-hole geometry regimes: high-mass BBH vs asymmetric
  mass-ratio systems are not geometrically interchangeable.

Disfavored:

- "All compact-binary events have the same posterior geometry."
- Any immediate claim that this is a quantum-gravity or GR-violation test.

Still open:

- Event-family clustering over many GWTC posterior files.
- True strong-gravity tests using LVK GR-test products: IMR consistency, ringdown, modified
  dispersion, polarization, or parameterized deviations.
- Standard-siren gravity/cosmology using distance-redshift likelihoods.
