# HANDOFF — state of the GW paper repo

Date: 2026-07-18
Repo: `/Users/kunalbhatia/Desktop/Research/GW` (local git, branch `main`, **no remote yet**)
Parent: all content ported from `kunalb541/cosmo2` (private); originals remain there untouched.

## What this repo is

The standalone home of the gravitational-wave program (paper: *The Geometry of Gravitational-Wave
Inference*). 22 experiment sets, each complete (prereg + src + results JSON + report), all files
byte-identical md5-verified against cosmo2 at port time (commits 180a62d, 27034fd):

- **GW core (18, in the notebook PDF):** E38, E40–E47, E55, E57–E60, E65, E66, E67, E68
- **GW-adjacent support (4, in repo, NOT in PDF):** E63 (NS-EOS; IS in the PDF under its own
  group), E16/E52/E69 (H0-anchor context for the siren section) — plus `src/qinfo.py` (E63 dep)
  and `src/build_report_pdf.py` (utility).

`paper/gw_lab_notebook.pdf` (committed, 4 pp, 19 entries) is the consolidated record; the
per-battery truth lives in `reports/` and `results/`.

## Data — none is committed; how to get it

`data/` is empty and gitignored. Two routes:
1. **Copy from cosmo2** (fastest, everything already on this machine):
   `cosmo2/data/chains/gw_posteriors/` (76 GWTC-2.1/3 PE, ~8 GB), `gwtc4/` (86 O4a events,
   ~14.6 GB), `pta/` (NANOGrav/EPTA/PPTA chains), `e66/O3_icarogw_data_distro.json` (84 MB),
   `e70/` is cosmology (not needed), TGR zips (imr/par/rin/liv, ~16 GB, some batteries only).
   NS-EOS for E63: `cosmo2/data/nseos/` (110 MB analysis-ready).
2. **Re-fetch** via `scripts/fetch_gw_chains.py` + `scripts/fetch_tgr_*.sh` and the DOIs in
   docs/DATA_AVAILABILITY.md.
Path expectation: batteries read `ROOT/data/chains/...` relative to this repo — mirror the
cosmo2 subdirectory names exactly.

## What is done / verified

- All 165 contract tests pass in-repo with no cosmo2 on the path (17 at the time of the port).
- All 24 src files compile; all intra-repo imports resolve (e65→e38 helper, e67→e65, e63→qinfo).
- Every results-JSON prereg pointer and report prereg reference resolves in-repo.
- Notebook: every entry extracted brace-balanced and verified verbatim against cosmo2's tex.

## Next steps (in order)

1. **Figures** (nothing exists yet): curved-law gallery (E40 fit + E67 out-of-sample table as
   figure), tangent-vs-curve residual vs elongation, PTA (log10A, γ) ellipses + degeneracy
   projection + γ-vs-span, siren lever budget, coherence-battery summary. Data needed: GWTC PE +
   PTA chains (route 1 above).
2. **Manuscript** in `paper/` (docs/SCOPE.md has the claim table; README the four-result spine).
3. Optional: create private remote `kunalb541/GW` and push (user has gh auth as kunalb541).
4. Watch list: GWTC-4 TGR release (re-run E45–E60 out-of-sample); IPTA DR3 / NG 20yr (prereg the
   γ-vs-span successor prediction — see WORKFLOW "standing predictions").

## Gotchas for whoever picks this up

- Read docs/WORKFLOW.md first — the "GW-specific rules learned the hard way" section is the
  distilled cost of three near-miss false alarms; do not re-learn them.
- **E-numbering FORKED on 2026-07-19** (two sessions worked in parallel): this repo and cosmo2
  now have SEPARATE sequences. GW-repo numbers in use: E71 (gwtc5 curved law) + E71 (sloppy-spectrum
  prereg, deferred), E72 (outlier atlas) + E72 (curvature-law prereg, deferred), E73 (information
  anatomy), E74 (GW250114), E78/E79 (GR exponent). cosmo2 numbers: through E75 (its E73 = curved
  S8 law — different from GW-E73). RULE going forward: qualify cross-repo references as
  "GW-E<n>" / "cosmo2-E<n>". Taken since: **E82** (inference manifold — catalog-as-one-object). E80/E81
  stay reserved for the deferred sloppy/curvature preregs (renumbered when run). Also taken: **E83**
  (from-scratch strain pipeline / GW250114 ringdown validation), **E84** (data-driven chirp mass +
  band-resolved feasibility boundary), and **E85** (Bayesian ringdown — **RETRACTED, superseded by E87**),
  and **E86** (band-resolved boundary closed from both
  sides on GW241011 — definitive negative; ridge methods carry no band-resolved chirp-mass information),
  and **E87** (E85 corrected: two covariance bugs cost ~33x matched-filter SNR and left E85's posterior
  equal to the PRIOR; the corrected pipeline reproduces LVK's own pyRing Kerr_220 start-time scan to a
  median 2.0 Hz over 2M–18M), and **E88** (221 overtone: a two-mode preference significant at 8.4σ vs a
  pure-220 null but FLAT in start time, so not a decaying overtone — an unidentified ~+5 systematic;
  plus the measured fact that remnant freedom absorbs 99% of an injected overtone).
  and **E89** (spin magnitude rises with mass across 265 events: hierarchical-assembly signature,
  b1=+1.19, beyond all 300 null trials; two analysis traps found and removed; selection effects NOT modelled).
  Next free HERE: **E90**.
  Do not renumber committed batteries; **`git log` before claiming a number**.
- The user's standing instructions: lean orchestration (no agent swarms), always double-check /
  independently re-derive, comprehensive data sweeps in one pass, lab-notebook (never
  paper-style) reports.
