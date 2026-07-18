# DATA_AVAILABILITY — the gate table (all sources public; verified working at port time)

| dataset | source (exact) | size | used by | notes |
|---|---|---|---|---|
| GWTC-1 GW170817 PE | dcc.ligo.org LIGO-P1800370 → `GW170817_GWTC-1.hdf5` | 2.4 MB | E63 | lowSpin IMRPhenomPv2NRT has lambda1/2 |
| GWTC-2.1/3 PE (76 events) | GWOSC eventapi → per-event Zenodo; `scripts/fetch_gw_chains.py` | ~8 GB | E38, E40–E44, E55, E65 | IMRPhenomXPHM + SEOBNRv4PHM per event |
| GWTC-4.0 PE (86 O4a events) | Zenodo **16053484**, per-event `*-combined_PEDataRelease.hdf5` | 14.6 GB | E67 | Mixed samples; ≤6 parallel curls, h5py-verify each |
| LVK TGR products | Zenodo **17461225**: imr (4.1 GB), par (2.5), rin (2.2), liv (7.4) | ~16 GB | E45–E47, E57–E60 | GWTC-3 par is FTI/SEOBNR-only (E55 block note) |
| GWTC-3 cosmology joint (icarogw) | Zenodo **5645777** → `O3_icarogw_data_distro.json` | 88 MB | E66 | restricted-flatLCDM H0 prior [65,77] — caveat locked in prereg |
| NANOGrav 15yr GWB chain | github `nanograv/15yr_stochastic_analysis` → fig-1 Google-Drive tarball → `nano15_hd_chain_long_050523.npy` | 209 MB | E68 | Zenodo 8423265 tarball = timing data ONLY, no GWB chain |
| EPTA DR2 GWB chains | Zenodo **8091568** `chains.zip` → `DR2full/hd_pl`, `DR2new/hd_pl` | 650 MB | E68 | 25% burn-in on chain_1.txt |
| PPTA DR3 GWB chain | github `danielreardon/PPTA-DR3` → `analysis_codes/data/all/chains/chain_commonNoise_pl_nocorr_freegam_DE440.npy` (+pars.txt) | 6 MB | E68 | verified γ=3.87±0.37, log10A=−14.50 |
| CPTA DR1 | Zenodo 13828113 | — | — | **no public GWB chain** (single-pulsar noise plots only); excluded, documented |
| NICER/NS-EOS (E63) | Zenodo 3386449 (Riley J0030), 3473466 (Miller J0030), 5735003 (Riley J0740), 4670689 (Miller J0740) | ~110 MB kept | E63 | analysis-ready 2-col files in cosmo2/data/nseos |
| H0 anchors (E16/E52/E69) | published Gaussian summaries (synthesis tier) in-code | — | E16/E52/E69 | + `gw_H0_posterior.npz` computed in cosmo2 |

Validation rule (locked, repo-wide): after ANY download, (a) open every HDF5 with h5py before
analysis, (b) reproduce at least one published headline number from the file (masses, γ, H0)
before running a battery on it. Both failures happened once each (corrupt resume-downloads;
column swaps) — the gate exists because of them.
