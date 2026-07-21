# Gates D and E — first measurement (2026-07-21)

> **BANNER 2026-07-21 — numbers superseded, verdicts unchanged.** Kept unedited as a record. Its values
> come from the retired posterior cache (4000 samples per row drawn *with replacement*); the cache now
> stores every sample exactly. The residual/resolution ratio quoted here as ~6× is **17.2×** against the
> current artifact, and Gate B's other values moved with it. The gate VERDICTS (B passes on threshold,
> E is NOT PASSED) are unaffected. Measurements of record are the committed `results/*.json`; the
> reader-facing summaries in [REFEREE_READINESS.md](REFEREE_READINESS.md) are generated from them.


Closes the remaining submission gates in the [revised PAPER_PLAN](PAPER_PLAN.md). Gate D: preregistration
provenance and per-pipeline reporting. Gate E: the precision law must be fit directly or removed.

---

# Gate D — provenance and pipeline dependence

## D1. Preregistration lock — verifiable for ONE of the two out-of-sample scores

| battery | prereg committed | result committed | gap | verifiable here? |
|---|---|---|---|---|
| **E71** (O4b) | 2026-07-18 21:16:43 (`d19a7a8`, *"LOCKED before any GWTC-5 file opened"*) | 2026-07-19 14:36:28 (`e90a77a`) | **~17 h** | **YES** |
| **E67** (O4a) | 2026-07-18 20:45:56 (`180a62d`) | 2026-07-18 20:45:56 (`180a62d`) | **0 — same commit** | **NO** |

E67's prereg and its results entered this repository in the *same* commit — the bulk port from the private
parent repo `cosmo2`. Its lock is real but is attested only by that private history, so **from the public
record E67's out-of-sample status rests on assertion, not on a verifiable timestamp**. E71's does not: it
has a 17-hour separation and an explicit locking commit message.

**This must be stated plainly in the manuscript.** The honest phrasing: one locked out-of-sample validation
with a publicly verifiable timestamp (O4b), and one whose lock is documented but not publicly timestamped
(O4a). Do not present the two as equivalent evidence.

## D2. The law does not depend on the analysis-group choice — PASSES

The locked primary uses the Mixed/largest posterior group. Scored instead on every waveform family present
(elongated events, median $|\Delta\psi|$):

| catalog | group | n | curve | tangent |
|---|---|---|---|---|
| GWTC-3 | C01:IMRPhenomXPHM | 26 | 0.78 | 8.18 |
| GWTC-3 | C01:Mixed | 27 | 0.88 | 4.83 |
| GWTC-3 | C01:SEOBNRv4PHM | 19 | 1.15 | 5.79 |
| O4a | C00:IMRPhenomXPHM-SpinTaylor | 18 | 1.29 | 6.63 |
| O4a | C00:Mixed | 17 | 1.27 | 6.93 |
| O4a | C00:SEOBNRv5PHM | 16 | 1.20 | 6.94 |
| O4b | C00:IMRPhenomXPHM-SpinTaylor | 33 | 1.08 | 5.23 |
| O4b | C00:IMRPhenomXPNR | 33 | 0.93 | 5.35 |
| O4b | C00:SEOBNRv5PHM | 31 | 1.14 | 4.43 |

The curve stays within **0.78–1.29°** across all nine catalog/family combinations while the tangent spans
4.43–8.18°. The result is not an artifact of the preferred-group choice.

## D3. Terminology
O4a and O4b contain **disjoint events** but share detector calibration, waveform families, priors and LVK
analysis conventions. Call them **disjoint event catalogs**, never independent experiments.

---

# Gate E — the precision law, fit directly. ~~PASSES~~ **SUPERSEDED — see the regenerated
section at the end of this file. STATUS: NOT PASSED (exploratory).** The provisional numbers
below were hand-run and are retained only as the record; the E93 artifact supersedes them.

E42 measured an SNR slope and a partial correlation; it never fit the joint exponents. The audit required
$\log(\sigma_{\mathcal M}/\mathcal M)=b_0+b_\rho\log\rho+b_M\log\mathcal M+\epsilon$ with uncertainties and
tests of $b_\rho=-1$, $b_M=5/3$, plus an out-of-sample check — or removal of the claim.

Run on O4a+O4b, where per-detector `optimal_snr` is in-file (network $\rho=\sqrt{\sum_{\rm det}\rho_{\rm det}^2}$,
$\sigma_{\mathcal M}=(q_{84}-q_{16})/2$, detector-frame $\mathcal M_c$ since cycle count is set in the
detector frame). This is **out-of-sample relative to E42**, which used GWTC-3.

| sample | n | $b_\rho$ | $b_M$ | $z(b_\rho{+}1)$ | $z(b_M{-}5/3)$ | $R^2$ |
|---|---|---|---|---|---|---|
| O4a | 86 | $-0.936\pm0.145$ | $+1.452\pm0.059$ | +0.44 | −3.63 | 0.887 |
| O4b | 18 | $-1.106\pm0.175$ | $+1.840\pm0.158$ | −0.61 | +1.09 | 0.929 |
| pooled | 104 | $-0.918\pm0.106$ | $+1.485\pm0.057$ | +0.77 | −3.17 | — |

**$b_\rho=-1$ is confirmed** everywhere ($|z|<1$): the Fisher $1/\rho$ scaling holds. **$b_M=5/3$ is
rejected pooled** at $3.2\sigma$. But splitting by chirp mass explains exactly why:

| $\mathcal M_{c,\rm det}$ band | n | $b_\rho$ | $b_M$ | $z(b_M-5/3)$ |
|---|---|---|---|---|
| **0–20** (inspiral in band) | 27 | $-1.199\pm0.191$ | $\mathbf{+1.661\pm0.149}$ | **−0.04** |
| 20–40 | 33 | $-1.073\pm0.153$ | $+0.957\pm0.424$ | −1.68 |
| 40+ (merger in band) | 44 | $-0.698\pm0.141$ | $+0.697\pm0.128$ | −7.58 |

For light systems $b_M=1.661\pm0.149$ against a predicted $1.667$ — agreement to **0.04σ**. The exponent
then softens monotonically with mass, and $b_\rho$ softens too ($-1.20\to-0.70$). This is the expected
behaviour: pure-inspiral cycle counting ($N\propto\mathcal M_c^{-5/3}$) assumes the signal is inspiral
between a fixed $f_{\rm low}$ and merger; for heavy systems the merger–ringdown enters band and the
assumption fails.

**~~Verdict: keep the precision law~~ — WITHDRAWN.** The mass-band edges were chosen after seeing the
pooled rejection, so the light-band agreement is post-hoc and is not confirmation. See the regenerated
Gate E section below.

**Caveats.** (i) $f_{\rm low}$ and waveform duration are NOT controlled, as the audit asked; the mass-band
split is consistent with the physical explanation but does not isolate it. (ii) Only 104/190 O4a+O4b events
carry `optimal_snr` in the preferred group, an unmodelled selection. (iii) O4b contributes only 18 usable
events, so the per-catalog O4b row is weak on its own. (iv) $\sigma_{\mathcal M}$ from a symmetric quantile
half-width ignores posterior skew.

---

## Status of all five gates

| gate | verdict |
|---|---|
| A — non-triviality, baselines, cross-waveform transfer | **PASS** — cross-family transfer at 2.08° vs a 1.99° floor |
| B — uncertainty, threshold | **PASS on threshold** (artifact: e92); ~1° systematic at ~6× Monte Carlo resolution; coverage language withdrawn |
| C — frame and parameterization | **PASS** — dependence measured; detector-frame gain is axis-ratio-mediated |
| D — provenance and pipeline | **PASS on pipeline**; E67's prereg lock is not publicly timestamped |
| E — precision law | **NOT PASSED — exploratory** (post-hoc mass split; see regenerated section) |

No gate broke the central result. Each narrowed how it may be stated. **Gates A-D are reproducible from
committed artifacts (E92/E94/E95); Gate E is NOT passed.** Manuscript drafting waits on Gate E or on
dropping the precision law.


---

# Gate E — REGENERATED from the E93 artifact. **STATUS: NOT PASSED (exploratory).**

Read from `results/e93_precision_law_results.json`, produced by `src/e93_precision_law.py` from the E94
cache (no HDF5 access). Model: log(σ_Mc/Mc) = b0 + b_ρ log ρ + b_mass log Mc_det, HC1-robust SE.

| sample | n | b_ρ | b_mass | z(b_ρ+1) | z(b_mass−5/3) |
|---|---|---|---|---|---|
| pooled | 116 | -0.943 ± 0.112 | +1.475 ± 0.055 | +0.51 | **-3.48** |
| mc_0_20_POSTHOC | 29 | -1.250 ± 0.132 | +1.591 ± 0.101 | -1.89 | -0.75 |
| mc_20_40_POSTHOC | 36 | -1.049 ± 0.126 | +1.078 ± 0.653 | -0.39 | -0.90 |
| mc_40_inf_POSTHOC | 51 | -0.942 ± 0.268 | +0.597 ± 0.172 | +0.22 | -6.21 |

**b_ρ ≈ −1 is supported** in the selected sample (-0.943 ± 0.112, z = +0.51).

**b_mass = 5/3 is REJECTED pooled** (z = -3.48). Agreement appears only in the light band,
and **the band edges (20, 40 M⊙) were chosen after seeing the pooled rejection**. Failure to reject inside
a data-selected subset is not positive evidence for the predicted exponent. The provisional hand-run
reported the light band as 1.661 ± 0.149 (z = −0.04); the artifact gives +1.591 ± 0.101
(z = -0.75) — weaker, and the earlier "0.04σ confirmation" phrasing is withdrawn.

**SNR missingness is now accounted for**: 116 events kept, 150 dropped for lack of a usable
`*_optimal_snr` field. Kept/dropped median Mc_det = 37.2/34.3, Mann–Whitney
p = 0.142 — no significant evidence that availability selects on mass. That addresses one of
the four requirements; three remain.

**To pass Gate E** still requires: (i) the expected exponent from the actual Fisher integral (detector PSD,
event-specific f_low, mass-dependent upper cutoff) rather than the heuristic cycle count; (ii) a continuous
transition model with a physically declared transition variable instead of hand-placed bins; (iii) held-out
or preregistered validation. Until then: **b_ρ ≈ −1 supported; the mass exponent is inconsistent with a
single 5/3 law and shows an exploratory mass dependence.**
