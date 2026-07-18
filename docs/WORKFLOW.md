# WORKFLOW — the battery discipline (inherited from cosmo/cosmo2/camels2, GW-adapted)

Every experiment ("battery") in this repo follows the same locked cycle. No step is optional.
The E-numbering continues cosmo2's sequence (next free number: E71).

## The cycle

1. **PREREGISTER, then lock.** Write `preregs/E<n>_<slug>_prereg.md` BEFORE running anything:
   the question, the data (exact records/DOIs), the method, numbered decision rules (D1, D2, ...)
   with thresholds, and honesty commitments. If the battery tests a prediction from an earlier
   battery, the prereg must cite the commit where that prediction went on record (e.g. E67 cites
   E65/8d09cbf) and must be COMMITTED AND PUSHED before the new data are opened.
2. **Implement.** One file: `src/e<n>_<slug>.py`. Seed = the E-number. No RNG unless declared.
   Writes exactly one `results/e<n>_<slug>_results.json` — the numbers of record, including the
   prereg path, per-decision verdicts, and any fallbacks taken.
3. **Verify — three legs, all mandatory:**
   - contract tests in `tests/test_e<n>_*.py` (see docs/TESTING.md for what they must cover);
   - **independent re-derivation of every headline number** through a second code path
     (np.corrcoef/np.cov one-liners, an awk pipeline, or a by-hand recomputation of one
     event/probe end-to-end — E67 did both);
   - validation of loaded data against published values BEFORE analysis (column-identification
     is the #1 failure mode: e.g. Riley J0740 col0=M col1=R verified against 2.08/12.39).
4. **Report.** `reports/REPORT_E<n>.md` — plain lab-notebook style (NEVER paper-shaped: no
   abstract/sections): what ran, the locked-decision table with outcomes, what it means, and an
   honesty/limits paragraph. Post-hoc findings are allowed but must be LABELLED post-hoc and
   framed as the next battery's preregisterable prediction.
5. **Notebook.** Add one `\entry{}` to `paper/gw_lab_notebook.tex`, rebuild the PDF, keep it
   committed. Mid-entry tables: close the body with `:}` before `tabular`; post-table prose must
   not be brace-wrapped (recurring "Too many }'s" trap).
6. **Commit** everything from one battery in one commit; push if a remote exists.

## GW-specific rules learned the hard way (violate = redo)

- **No naive posterior products** across events or experiments (E47 histogram product, E58
  graviton-mass combination, E48 sliced-W factor — three false alarms). Combine only with the
  correct hierarchical machinery, or report per-event/per-experiment numbers + the published
  combined value.
- **Coherence lens before any violation claim**: if an apparent anomaly is coherent across
  events (same sign everywhere, e.g. E59's 22/22 Mf shift), it is a systematic, not physics.
- **Two-estimator rule** for any degeneracy/response slope: cov/var marginal track AND decile
  regression must agree in sign and within ×2 (E66's partial-vs-marginal confusion was caught by
  this). Boundary (upper-limit) posteriors additionally get an upper-half sensitivity slope.
- **Precision ladder** for any value/shape claim: raw, joint-whitened, orientation-only value
  fractions + Δρ (the E48/E56 lesson: raw Bures "shape" is precision-inflated). In planes with
  incommensurable axes (e.g. (M,R)), ψ is metric-dependent — use ρ (E63).
- **Gaussianity gate**: empirical-vs-Gaussian-resampled sliced-W² ratio within 30% or the
  Gaussian numbers are flagged and empirical distances lead.
- **Transient errno-60 HDF5 stalls** (macOS disk under load): retry ×4 with backoff; never let a
  read failure silently drop an event (E43 lost one event to this; E65 caught it with retries).
- **Downloads**: Zenodo throttles per connection — ≤6 parallel workers, verify every HDF5 with
  h5py after download, re-fetch stragglers sequentially; no `curl -C -` resume (corrupts).
- **Waveform choice**: use the catalog's Mixed samples where present (largest if variants);
  record the dataset name per event in the results JSON.

## Numbering map (ported record; full detail in cosmo2)

E38 atlas · E40–E44 mass-plane laws + χ_eff · E45–E47 GR trilogy · E55 multi-waveform ·
E57–E60 area/graviton/ringdown · E63 NS-EOS (GW170817 tidal) · E65 curved-law derivation ·
E66 spectral-siren lever · E67 GWTC-4 out-of-sample PASS · E68 PTA anatomy.
Support (not GW batteries): E16/E52/E69 H0-anchor context, qinfo.

## Standing on-record predictions (next out-of-sample opportunities)

- Curved law: elongated events in ANY future catalog follow the constant-Mc curve to <2°
  (confirmed once on GWTC-4; re-scoreable on GWTC-5/O4b at zero cost).
- PTA span-ordering: longer-span subsets of the same array fit steeper γ (prereg the day
  IPTA DR3 / NANOGrav 20yr chains are public).
- GWTC-4 TGR products: re-run E45–E60 unchanged when the O4a TGR release lands.
