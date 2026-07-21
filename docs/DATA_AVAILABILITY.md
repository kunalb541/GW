# DATA_AVAILABILITY — the gate table (all sources public; verified working at port time)

## Data used by the manuscript, and how to cite it

The paper is a reanalysis of **public** parameter-estimation posteriors. It uses no proprietary or
embargoed products and generates no new observational data. Three releases enter the manuscript:

| release | obtained from | cite in the paper as | used for |
|---|---|---|---|
| GWTC-2.1 posterior samples | GWOSC / Zenodo (per-event) | Abbott et al., PRD **109**, 022001 (2024), arXiv:2108.01045 | training catalog (with GWTC-3) |
| GWTC-3 posterior samples | GWOSC / Zenodo (per-event) | Abbott et al., PRX **13**, 041039 (2023), arXiv:2111.03606 | training catalog |
| GWTC-4.0 / O4a PE | Zenodo **16053484** | the Zenodo record (see caveat below) | locked out-of-sample test 1 |
| GWTC-5.0 / O4b PE | Zenodo **20276106**, **20348006** | the Zenodo records (see caveat below) | locked out-of-sample test 2 |

Plus the GWOSC service itself: Abbott et al., ApJS **267**, 29 (2023), arXiv:2302.03676.

> ⚠️ **Open citation item.** The GWTC-4.0 and GWTC-5.0 *catalog papers* are cited in the manuscript only
> through their Zenodo data records, because their journal/arXiv coordinates have **not** been verified at
> full text in this repo. `docs/NOVELTY.md` carries `arXiv:2508.18080` for GWTC-4.0 flagged as general
> knowledge. Per the repo rule that nothing enters the manuscript on trust, the catalog-paper references
> must be looked up and verified before submission. Data-record citation is correct and sufficient in the
> meantime; a catalog paper reference is additionally expected by the collaboration and should be added.

### Licence and acknowledgment obligations

GWOSC strain and PE data are released under a **Creative Commons Attribution** licence. Using them
carries two obligations, both of which the manuscript now discharges in its Acknowledgments paragraph:

1. **Acknowledge GWOSC and the LVK collaborations** (LIGO Scientific, Virgo, KAGRA), and their funders
   (NSF for LIGO; CNRS/INFN/Nikhef and European partners for Virgo; MEXT/JSPS, NSTC, MSIT for KAGRA).
2. **Cite the data release(s)** and the catalog papers they come from — the table above.

The manuscript also states explicitly that the LVK has not reviewed this analysis and bears no
responsibility for it, which matters because this is independent, non-collaboration work.

> ⚠️ **Before submission:** replace the acknowledgment paragraph with the *exact current wording* that
> GWOSC asks users to include (gwosc.org). The text in the manuscript is written to satisfy the same
> obligations but is the author's own phrasing, not a verified copy of the mandated boilerplate.

---


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
