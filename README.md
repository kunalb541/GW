# GW — The Geometry of Gravitational-Wave Inference

**Kunal Bhatia** — Independent researcher, Meerut, India ·
ORCID [0009-0007-4447-6325](https://orcid.org/0009-0007-4447-6325)

Paper project distilling the gravitational-wave program developed inside
[`cosmo2`](https://github.com/kunalb541/cosmo2) (experiments E38–E68) into a standalone
manuscript. The organizing thesis: the *uncertainty geometry* of GW measurements is lawful —
predictable from first principles, usable as a systematics detector, and transferable as a
diagnostic of cross-experiment consistency.

## The four results forming the paper's spine

1. **The curved chirp-mass law** (cosmo2 E40 → E65 → E67). The (m₁, m₂) posterior of a compact
   binary *is* the constant-chirp-mass curve — location set by the measured M_c, extent by the
   mass-ratio marginal, zero free parameters. Confirmed **out-of-sample** on GWTC-4.0:
   median |Δψ| = 1.26° on elongated O4a events, prediction locked before the data were opened.
2. **Coherence as a systematics detector** (E45–E47, E55, E57–E60). Across the GR-test battery,
   apparent anomalies that are *coherent across events* are method artifacts, not physics —
   the lens that kept three naive-combination false alarms out of the record; GR passes every test.
3. **Cross-experiment anatomy of the PTA background** (E68). Four pulsar-timing arrays: universal
   constraint geometry, inter-PTA offsets 94.6–99.9% along the common A–γ degeneracy
   (degeneracy-sliding, not disagreement); γ = 13/3 excluded by NANOGrav alone; γ̂ strictly
   monotonic in observing span — a bending-spectrum signature, with a preregisterable successor
   prediction for IPTA DR3.
4. **What sirens can and cannot arbitrate** (E66). On the real LVK joint chains the mass-scale
   is the top systematic lever of spectral-siren H₀ but contributes ≲0.5 km/s/Mpc today;
   the lever goes live at ~1 km/s/Mpc precision (O5/XG era).

## Status

- [x] All underlying batteries locked-preregistered, run, independently re-derived (in cosmo2).
- [x] **Full port complete**: all 18 GW experiments (E38, E40–E47, E55, E57–E60, E65–E68) plus the
      GW-adjacent set (E63 NS-EOS via GW170817; E16/E52/E69 H0-anchor context; qinfo) live here
      self-contained — preregs/, src/, results/ (numbers of record), reports/, 17 tests, fetch scripts.
      All files byte-identical copies; originals remain in cosmo2.
- [x] GW lab notebook: [`paper/gw_lab_notebook.pdf`](paper/gw_lab_notebook.pdf) (19 GW-data entries incl. E63).
- [ ] Figures (curved-law gallery, coherence battery, PTA (A,γ) plane, siren lever budget).
- [ ] Manuscript draft.

## Layout (cosmo2 conventions)

```
GW/
├── preregs/    locked pre-registrations for any NEW battery run for the paper
├── src/        self-contained analysis code (ported + frozen from cosmo2)
├── results/    numbers of record (JSON)
├── reports/    lab-notebook reports
├── docs/       WORKFLOW (battery discipline), TESTING, HANDOFF, SCOPE, DATA_AVAILABILITY
├── paper/      manuscript
├── scripts/    data fetchers
├── tests/      contract tests
└── data/       chains/posteriors (gitignored)
```

## Working in this repo

Start with [`docs/WORKFLOW.md`](docs/WORKFLOW.md) (the locked-prereg battery cycle + the
GW-specific rules learned the hard way), [`docs/TESTING.md`](docs/TESTING.md) (run: `python3 -m
pytest tests/ -q`; 17 data-free contract tests), [`docs/HANDOFF.md`](docs/HANDOFF.md) (current
state, data routes, next steps), and [`docs/DATA_AVAILABILITY.md`](docs/DATA_AVAILABILITY.md)
(every source pinned with record numbers). Next free experiment number: **E71**.

## License

MIT.
