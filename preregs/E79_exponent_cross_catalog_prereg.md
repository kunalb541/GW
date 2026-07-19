# E79 preregistration — cross-catalog reproducibility of the geometric GR exponent (E78 successor)

**STATUS: DRAFT — to be LOCKED (committed) BEFORE the E78 exponent estimator is run on any GWTC-4/O4a
file.** E78 measured the GW inspiral's leading mass-combination exponent from posterior geometry on O4b
(exploratory: p̂ = 0.616 ± 0.011, consistent with GR's 0.600 at 1.3σ). This tests E78's on-record
successor prediction (REPORT_E78 / commit f3b99da): *the fitted exponent is reproducible across catalogs
and equals 0.600.* O4a is disjoint from O4b (E71 established the catalogs share zero events) and the
estimator has never been run on it — so O4a is blind for this test.

## Estimator (LOCKED — byte-identical to E78)
`src/e78_geometric_gr_exponent.py::fit_p` on each event's elongated (axr≥3) posterior: fit the exponent p
whose scale-free constant-Mc_p level-curve orientation (m1(q;p) ∝ q^{-p}(1+q)^{2p-1}) best matches the
measured principal-axis angle ψ_meas over the event's own q-marginal. Catalog estimate = mean over
elongated events; stat error = bootstrap; waveform systematic = spread of the per-family catalog means.
GR value p = 3/5 = 0.600. No parameter of the estimator is changed; only the input catalog changes.

## Data (LOCKED)
- Primary new catalog: **GWTC-4.0 / O4a PE, Zenodo 16053484** (86 events, per-event
  `*-combined_PEDataRelease.hdf5`, ~14.6 GB) — same file idiom as O4b, so the E71/E78 loader is a drop-in.
- Comparison (already computed): O4b p̂ = 0.616 ± 0.011 (E78 / results/e78_...json).
- GWTC-3 (older GWOSC per-event format) is a declared OPTIONAL third point, NOT required for the decision.

## Decision rules (LOCKED)
- **D1 (reproducibility).** The O4a catalog exponent p̂(O4a) is consistent with GR: |p̂(O4a) − 0.600| <
  3·σ(O4a) (σ = combined stat ⊕ waveform). PASS/FAIL.
- **D2 (cross-catalog consistency).** p̂(O4a) and p̂(O4b) agree: |p̂(O4a) − p̂(O4b)| < 3·√(σ_O4a² +
  σ_O4b²). PASS/FAIL. This is the actual "reproducible across catalogs" test.
- **D3 (descriptive).** Report p̂ per catalog, per-event distributions, elongated-event counts, injection
  bias on O4a, and the combined (O4a+O4b) exponent.

## Honesty commitments
- The E78 estimator is applied UNCHANGED; the injection/unbiasedness and waveform-systematic checks are
  rerun on O4a. Any elongated event missing a mass/q column is listed and dropped with reason.
- The known limitations carry over and will be restated: this is a methodologically independent CROSS-CHECK,
  not more sensitive than the LVK −1PN dipole bound; the q-marginal prior-dependence is uncontrolled; the
  ~1.2° curved-law residual sets a per-event floor (~0.04 in p) that averages down but could carry a small
  coherent offset the Gaussian injection would not catch.
- A per-catalog p̂ scattered around 0.600 CONFIRMS GR (closes the thread); a COHERENT, catalog-consistent
  departure from 0.600 (same sign, both catalogs, beyond 3σ) would be the real signal and would trigger a
  dedicated follow-up (waveform-family breakdown, prior study, GWTC-3 third point) before any claim.
- Seed 79 (bootstrap/injection).

## Verification plan
Independent re-derivation of p̂(O4a) through a second aggregation path; injection recovery on the O4a
q-marginals; the E78 contract tests remain green; disjointness of O4a from O4b reasserted from event dates.
