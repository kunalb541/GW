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

- 17/17 contract tests pass in-repo with no cosmo2 on the path.
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
- E-numbering is shared with cosmo2 history; next free number is **E71** (E70 is cosmology, in
  cosmo2 only). Do not renumber ported batteries.
- The user's standing instructions: lean orchestration (no agent swarms), always double-check /
  independently re-derive, comprehensive data sweeps in one pass, lab-notebook (never
  paper-style) reports.
