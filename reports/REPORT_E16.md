# E16 lab notebook — complete H0-axis map (all instruments, real GW posterior)

Pre-registration: `preregs/E16_h0_axis_all_instruments_prereg.md`. Regenerate:
`python -m src.e16_h0_axis`. GW is a REAL posterior computed from the public LVK gwcosmo
per-event H0 data (Zenodo 5645777), not a literature quote.

## All H0 instruments vs the CMB early value (67.36+/-0.54)
| instrument | H0 | tension vs CMB | class |
|---|---|---|---|
| DESI+CMB chain | 67.0 | 0.49s | standard-ruler |
| cosmic chronometers | 67.8 | 0.14s | rd-free |
| JWST CCHP JAGB | 67.8 | 0.16s | rd-free (ladder) |
| JWST CCHP TRGB | 68.8 | 0.63s | rd-free (ladder) |
| **GW dark-siren GWTC-3 (real)** | **69.3+/-12.9** | **0.15s** | rd-free (ladder-free) |
| JWST CCHP combined | 70.0 | 1.60s | rd-free (ladder) |
| TDCOSMO 2025 | 71.6 | 1.16s | rd-free (ladder-free) |
| SH0ES HST Cepheid | 73.0 | **4.85s** | rd-free (ladder) |

**Outcome: SH0ES-outlier.** Across all 8 independent instruments, SH0ES is the ONLY anchor
>2.5 sigma from the early value. Every other probe -- including the two most independent
(GW standard sirens, ladder-free AND sound-horizon-free; and TDCOSMO time delays) -- sits
within 2.5 sigma of the CMB/early value. The GW real posterior (69.3+/-12.9 from 46 GWTC-3
dark sirens) is broad but centered on the early value (0.15 sigma). So the H0 tension is
SH0ES-specific across the full instrument set, not a generic early-vs-late excess.

## Why GW is here and not in S8
Standard sirens measure absolute distance -> H0 only. They have no structure-growth
(sigma8) information, so they belong on the H0 axis / (H0,rd) rd-free class, NOT in the
(Om,s8) S8 consensus (E15). This is the correct home for GW in the framework.
