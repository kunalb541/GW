# Reconstructing compact-binary mass-posterior orientation from the mass-ratio marginal

**Kunal Bhatia** — Independent researcher, Meerut, India ·
ORCID [0009-0007-4447-6325](https://orcid.org/0009-0007-4447-6325)

A reproducible, pre-registered gravitational-wave methodology project. Analysis code, locked
predictions, per-event results, figures, and the manuscript for a single result, with every number in
the paper generated from a committed artifact rather than typed by hand.

> **License:** MIT (code and docs). Gravitational-wave data are not redistributed here; they are public
> GWOSC releases under CC-BY. The manuscript is provided for transparency and remains the author's work.
> See [`LICENSE`](LICENSE).

---

## The result

The component-mass posterior of a compact-binary coalescence is elongated along a contour of
near-constant chirp mass — a shape usually treated as a nuisance degeneracy. We show that its
**orientation** is quantitatively reconstructible from a single one-dimensional marginal of the same
posterior.

Evaluating the constant-chirp-mass curve over an event's own **mass-ratio marginal** predicts the
principal-axis position angle to a median **1.26°** on GWTC-4.0/O4a and **1.22°** on GWTC-5.0/O4b for
elongated posteriors (axis ratio ≥ 3), with **no coefficient calibrated on either catalog** and with the
prediction fixed on GWTC-3 before the later data were examined. The local tangent approximation used by
rapid parameter-estimation tools achieves 3.9–6.7° on the same events.

The reconstruction requires the event's *own* marginal (substituting another event's degrades it several-
fold; the achieved error lies below the minimum of 300 catalog-stratified permutations), and it transfers
between separately sampled waveform families, so it is not an artifact of shared Monte Carlo noise. The
predicted orientation is **exactly invariant to chirp mass** — rescaling the chirp mass is a dilation,
which leaves covariance eigenvectors unchanged — so the reconstruction has one input, the mass-ratio
marginal, not two.

It is presented as a measurement of posterior geometry and a systematics diagnostic, **not** as a test of
general relativity: the posteriors are generated with general-relativistic waveform models, so their
internal geometry cannot bound departures from the theory that produced them.

- **Manuscript:** [`paper/manuscript.pdf`](paper/manuscript.pdf) — 10 pp, two-column (Physical Review D
  format, `revtex4-2`).
- **Reader's guide:** [`docs/EXTERNAL_READER_PACKET.md`](docs/EXTERNAL_READER_PACKET.md) — the honest
  summary, strongest and weakest claims, and a reproduction checklist.

## Reproducing the numbers

Raw parameter-estimation data are **not** included in this repository.

- `data/` is gitignored (~68 GB of LVK PE releases). Every source is pinned with record numbers and DOIs
  in [`docs/DATA_AVAILABILITY.md`](docs/DATA_AVAILABILITY.md), with download helpers in `scripts/`.
- `results/e94_posterior_cache.npz` (~572 MB, gitignored) is a one-time extract of the released
  posteriors. It stores **every** usable sample (no subsampling), so a cache-backed number is a full-
  sample number. Rebuild it with `python3 src/e94_build_posterior_cache.py` (~104 s on the author's
  machine; one HDF5 pass, I/O-bound and machine-dependent). It is the single provenance source for the
  downstream batteries, which perform no HDF5 access of their own.

```bash
# regenerate every number and caption in the paper from the committed artifacts
python3 src/build_paper_numbers.py        # -> paper/numbers.tex
python3 src/build_manuscript_figures.py   # -> paper/fig_captions.tex
python3 src/build_doc_numbers.py          # -> generated blocks in the docs

# build the manuscript
cd paper && pdflatex manuscript.tex && pdflatex manuscript.tex

# contract tests are data-free and run anywhere (188 tests)
python3 -m pytest tests/ -q
```

An empty `git diff` after the three build scripts means the paper matches its committed artifacts exactly.
Every result number in the manuscript is a LaTeX macro emitted from a committed JSON; none is typed by
hand, and a test fails if the paper and the artifacts disagree.

## Claim status — read before citing any number

This repository contains an internal submission-gate audit of its own headline result. What is and is not
established:

| item | status |
|---|---|
| curved-law reconstruction | reproducible from the committed cache (`src/e94`, `src/e95`) |
| residual is a real systematic | ~1°, about 17× the Monte Carlo resolution — not sampling noise (`src/e92`) |
| finite posterior thickness | supported out-of-sample; **arc-variation NOT established** (`src/e96`) |
| self-consistency correction | in-sample only; does not clear the out-of-sample bar (`src/e97`) |
| precision law | **NOT PASSED — exploratory**; its mass-band split is post-hoc (`src/e93`) |
| geometric GR-exponent diagnostic | a naive 3.1σ offset, demoted to 1.5σ by two pre-committed checks (Appendix A) |
| E85 Bayesian ringdown | **RETRACTED** — its posterior was prior-dominated |

Two provenance caveats, stated plainly. The O4b preregistration is timestamped in this repository's public
history before the data were opened; the **O4a preregistration is not** independently timestamped — its
prereg and results entered in the same commit, so its out-of-sample status rests on a private history.
And O4a/O4b are *disjoint event catalogs*, not independent experiments: they share detectors, calibration,
waveform families and priors.

## Repository layout

```
GW/
├── paper/       manuscript (revtex4-2), generated numbers.tex and fig_captions.tex
├── src/         analysis code and the build_*.py generators
├── results/     numbers of record (JSON); the cache manifest (cache itself gitignored)
├── figures/     figures and their machine-readable sidecar JSONs
├── preregs/     locked pre-registrations
├── reports/     per-battery lab-notebook reports
├── tests/       data-free contract tests
├── scripts/     data fetchers
├── docs/        reference and working documentation — see docs/README.md
└── data/        parameter-estimation files (gitignored, not redistributed)
```

## Documentation

[`docs/README.md`](docs/README.md) indexes the reference documentation — data availability,
referee-readiness summary, citation verification, literature, workflow, testing. The project's internal
working record (planning notes, review rounds, dated lab notes) is kept out of the public tree; the
manuscript and the committed artifacts under `results/` are the authoritative record.

## How to cite

If you use this software or the analysis it reproduces, please cite both the manuscript and the software
record; see [`CITATION.cff`](CITATION.cff). Archival metadata for Zenodo is in [`.zenodo.json`](.zenodo.json).

## Acknowledgment

This research has made use of data or software obtained from the Gravitational Wave Open Science Center
(gwosc.org), a service of the LIGO Scientific Collaboration, the Virgo Collaboration, and KAGRA. This is
independent work; the author is not a member of the LIGO–Virgo–KAGRA Collaboration, and the Collaboration
has not reviewed this analysis and bears no responsibility for its conclusions.
