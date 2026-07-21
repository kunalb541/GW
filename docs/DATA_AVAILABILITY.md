# DATA_AVAILABILITY — the gate table (all sources public; verified working at port time)

## Data used by the manuscript, and how to cite it

The paper is a reanalysis of **public** parameter-estimation posteriors. It uses no proprietary or
embargoed products and generates no new observational data. Three releases enter the manuscript:

| release | obtained from | cite in the paper as | used for |
|---|---|---|---|
| GWTC-2.1 posterior samples | GWOSC / Zenodo (per-event) | Abbott et al., PRD **109**, 022001 (2024), arXiv:2108.01045 | training catalog (with GWTC-3) |
| GWTC-3 posterior samples | GWOSC / Zenodo (per-event) | Abbott et al., PRX **13**, 041039 (2023), arXiv:2111.03606 | training catalog |
| GWTC-4.0 / O4a PE | Zenodo **16053484** | arXiv:**2508.18082** + the Zenodo record | locked out-of-sample test 1 |
| GWTC-5.0 / O4b PE | Zenodo **20276106**, **20348006** | arXiv:**2605.27225** + the Zenodo records | locked out-of-sample test 2 |

Plus the GWOSC **data papers**, which is the citation GWOSC itself asks for (verified at
<https://gwosc.org/acknowledgement/>, 2026-07-21). One per observing run, and this analysis spans three:

| run | data used here | cite |
|---|---|---|
| O3 | GWTC-2.1 / GWTC-3 | ApJS **267**, 29 (2023), arXiv:2302.03676 |
| O4a | GWTC-4.0 | ApJ **1004**, 2329 (2026) — *Open Data ... First Part of the Fourth Observing Run* |
| O4b | GWTC-5.0 | arXiv:2605.27090 — *Open Data ... Second Part of the Fourth Observing Run* |

> **This was a real gap.** The manuscript initially cited only the O3 data paper while using O4a and O4b
> data. Both O4 papers are now cited, and a test fails if either citation disappears.

> ✅ **Closed 2026-07-21.** The GWTC-4.0 and GWTC-5.0 catalog papers are now cited, verified at their
> arXiv abstract pages (title and collaboration author form checked for both):
> **arXiv:2508.18082** — *GWTC-4.0: Updating the Gravitational-Wave Transient Catalog with Observations
> from the First Part of the Fourth LIGO--Virgo--KAGRA Observing Run*; and
> **arXiv:2605.27225** — *GWTC-5.0: Observations from the Second Part of the Fourth LIGO--Virgo--KAGRA
> Observing Run and Updates to the Gravitational-Wave Transient Catalog*.
>
> Note `docs/NOVELTY.md` carried **2508.18080**, which is a *different* GWTC-4.0 companion paper. The
> correct catalog reference is **18082**. That is exactly the kind of transposition the "verify before
> citing" rule exists to catch. Corroborating detail: the GWTC-4.0 abstract reports 86 candidates with
> FAR < 1/yr, which is precisely the O4a event count this analysis scores (`n_scored = 86`).
>
> Neither paper shows a journal reference yet; both are cited as arXiv preprints and should be upgraded
> if they are published before submission.

### Licence and acknowledgment obligations

GWOSC strain and PE data are released under a **Creative Commons Attribution** licence. Using them
carries two obligations, both of which the manuscript now discharges in its Acknowledgments paragraph:

1. **Acknowledge GWOSC and the LVK collaborations** (LIGO Scientific, Virgo, KAGRA), and their funders
   (NSF for LIGO; CNRS/INFN/Nikhef and European partners for Virgo; MEXT/JSPS, NSTC, MSIT for KAGRA).
2. **Cite the data release(s)** and the catalog papers they come from — the table above.

The manuscript also states explicitly that the LVK has not reviewed this analysis and bears no
responsibility for it, which matters because this is independent, non-collaboration work.

### Authorship: the LVK are acknowledged, not added as authors

**Checked, because it is a reasonable thing to worry about.** Using GWOSC open data does **not** confer
or require collaboration authorship. The GWOSC acknowledgement page states attribution and citation
requirements and imposes no authorship condition; the data are CC-BY, which is satisfied by attribution.
Independent reanalysis of public LVK data published without LVK authors is routine and well established
(the IAS group's independent catalogs are the standard example). The same pattern is used in the sibling
`camels` repo in this workspace: the CAMELS collaboration is acknowledged and its data portal cited, and
the paper is single-author.

What the manuscript does instead, and what actually matters for an independent author, is state
explicitly that the author is *not* a collaboration member, that the collaboration has not reviewed the
analysis, and that it bears no responsibility for the conclusions. A test enforces the presence of that
disclaimer.

### Acknowledgment wording — now verbatim

The manuscript's acknowledgment now opens with GWOSC's **mandated sentence verbatim** ("This research has
made use of data or software obtained from the Gravitational Wave Open Science Center (gwosc.org), a
service of the LIGO Scientific Collaboration, the Virgo Collaboration, and KAGRA"), followed by the
funding-agency sentences for NSF/LIGO, EGO--CNRS--INFN--Nikhef/Virgo and MEXT--JSPS--NRF--MSIT--AS--NSTC/
KAGRA. Verified against <https://gwosc.org/acknowledgement/> on 2026-07-21. Re-check at submission time,
since the boilerplate is updated as new runs are released.

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
