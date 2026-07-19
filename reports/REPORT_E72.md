# E72 lab notebook - GW geometry outlier atlas: no physical source-class breaks the curved law (O4b)

Prereg: preregs/E72_gw_geometry_outlier_atlas_prereg.md - locked (commit 0d1cebf) BEFORE any
residual-axis correlation was computed. Sample: the 32 elongated O4b events (axr>=3) from the LOCKED
E71 results; residual r = err_curve (not recomputed). Nine pre-declared axes, BH-FDR (q=0.05) +
partial-Spearman controlling axr, Tukey outlier fence, E59 coherence lens. Anomaly atlas, NOT a
new-physics claim (per the user framing: "a clean geometry anomaly score, not 'we found PBHs'").

## Locked outcomes

| decision (locked) | outcome |
|---|---|
| **D1 - correlation of residual with any axis** (BH-FDR q=0.05, partial-axr) | **No PHYSICAL axis survives.** Only `waveform_disagreement` (a systematic) survives: rho=-0.64, p=1e-4, q_BH=0.001, partial(axr)=-0.63 |
| D2 - Tukey upper fence (Q3+1.5 IQR = 3.23 deg) | 1 marginal outlier: GW240507_041632 (r=3.37 deg, 0.14 above fence) |
| D3 - coherence lens on the outlier | GW240507: wf-disagreement 0.88 < residual 3.37 -> CANDIDATE-physics (but weak; see below) |

## The primary result: a clean physical null
None of the seven physical axes correlates with the curve residual after multiple-comparison control:
chi_p (precession) rho=-0.40 q_BH=0.074; |chi_eff| -0.36 (0.077); mass_ratio -0.08; redshift +0.17;
chirp_mass +0.39 (0.074); total_mass +0.38 (0.074); mass_2 (NSBH/mass-gap proxy) +0.33 (0.103) -
**all fail FDR.** So within O4b there is NO precession-, spin-, mass-ratio-, mass-, redshift-, or
NSBH-driven breakdown of the constant-chirp-mass geometry. This strengthens claim 1: the law is not
hiding a source-class-dependent failure; its residuals are not organized by any physical parameter.

## The one surviving correlate is a SYSTEMATIC, and its sign says "not physics"
`waveform_disagreement` (stdev of psi_meas across an event's waveform families) survives FDR strongly
(rho=-0.64, q_BH=0.001) and is robust (drop-one changes rho by <=0.036; not a leverage artifact;
0.1-2.5 deg real spread; unchanged by partialling axr). But the correlation is NEGATIVE: the events
the curve fits BEST (r ~ 0.01-0.2 deg: GW240915_001357, GW240910_103535, GW240601_231004) are exactly
those where the waveform families disagree MOST about the orientation, while the largest residuals
(GW240507, GW240930) occur where waveforms AGREE. Interpretation (measurement optics, not physics, and
flagged as interpretation): the constant-Mc curve tracks the waveform-ENSEMBLE consensus better than
any single waveform tracks another, so the picked-waveform residual is smallest precisely where the
ensemble is most scattered. This is the E59/coherence lesson in a new guise - the residual structure
that exists is a waveform-model systematic, not a physical signal. All residuals remain tiny (<=3.4 deg).

## The single Tukey outlier is marginal, not a breakdown
GW240507_041632 sits 0.14 deg above the fence (3.37 vs 3.23); it is a low-SNR (network MF SNR ~9.7),
strongly asymmetric event (m1=31.1, m2=8.5, q~0.27). The coherence lens calls it CANDIDATE-physics
(its own waveforms agree: 0.88 < 3.37), i.e. a clean-measurement small offset rather than a
waveform artifact - but at 3.4 deg with low SNR it is most consistent with measurement noise. Recorded
as a WEAK, preregisterable successor target: if the constant-Mc curve genuinely fails for asymmetric
low-SNR mergers, GW240507-like events should show the same small positive offset in the O4a+O4b joint
set and in O5. No claim is made here.

## Verification
- Contract tests tests/test_e72_outlier_atlas.py: 6/6 (null false-positive rate <10%; injected
  correlation recovered; BH-FDR on textbook p-values; partial correlation removes a confound-induced
  link and keeps a genuine one; Tukey fences an outlier, spares inliers). Full suite 23/23.
- Independent re-derivation: the D1 headline Spearman(r, waveform_disagreement) reproduced by a
  hand-coded rank-Pearson (-0.641, exact); the D2 Tukey fence reproduced by numpy percentile (3.23,
  same single event above).
- Robustness: drop-one influence on the surviving correlation <=0.036; not leverage.

## Honesty / limits
- N=32 is low power for a 9-axis search; BH-FDR + partial-axr + the coherence lens are exactly why a
  chance correlation is not sold as a discovery. The physical null is the honest, paper-useful outcome.
- `loudness_snr` axis is DATA-LIMITED: only 6/32 picked groups (the SEOBNRv5PHM groups lack it) carry a
  network SNR column, so its correlation (rho=-0.60, p=0.21) is uninformative and did not enter any
  verdict. Recorded, not worked around.
- Eccentricity and higher-mode content: out of scope - absent from the released O4b posterior columns.
- The axr>=3 gate + axr partial-control remove the E71-documented round-posterior residual inflation
  (the largest RAW residuals across all 104 events are near-round artifacts, correctly excluded here).
- E72 outputs an atlas + one weak flag; it is not a detection.

Code: src/e72_gw_geometry_outlier_atlas.py. Numbers: results/e72_gw_geometry_outlier_atlas_results.json.
Data: data/chains/gwtc5/ (gitignored; Zenodo 20276106 + 20348006). Depends on locked E71 residuals.
