# E87 lab notebook - E85's ringdown posterior was the PRIOR; two covariance bugs, 33x lost SNR, and the corrected measurement (validated against LVK's own pyRing)

**CHARACTERIZATION (no prereg).** This is a correction battery. It retracts E85's numbers, finds and fixes
the cause, and then passes the validation gate E85 failed. Supersedes `reports/REPORT_E85.md`.

## How the error surfaced (the check that caught it)
E85 reported f220 = 253.9 [167, 333] Hz, called it "honestly wide," and noted the IMR remnant sat inside.
The gate was a network test: **adding L1 to H1 left the 90% width unchanged (162.0 vs 160.0 Hz single).**
Adding an independent detector *must* tighten a posterior. It cannot fail to - unless there is no
information to add. Diagnostics:

| | lnL range over the whole (f,tau) grid | fraction of f-grid within 2 lnL of the peak | peak |
|---|---|---|---|
| H1 real | 3.9 | **1.00** | 160 Hz (**grid edge**) |
| L1 real | 3.9 | **1.00** | 160 Hz (**grid edge**) |
| loud synthetic injection | 1470 | 0.02 | 250 Hz (truth) |

The entire 160-340 Hz grid sat inside 4 lnL. **The "90% CI" was the grid.** That is why the IMR value fell
inside it (vacuous), why H1 and L1 medians differed by 33 Hz (a 4 lnL ripple moves a weighted median
freely), and why the network could not tighten. Both detectors railed at the grid's LOW edge - the
signature of a likelihood fitting low-frequency residual power, not a ringdown.

## Root cause: two defects in the noise covariance, ~33x of matched-filter SNR
An injection ladder into REAL off-source H1 noise through the identical code path settled it: at the
measured GW250114 ringdown amplitude the E85 pipeline registered **SNR ~ 0**, and even at 10x that
amplitude only SNR 1.9. The machinery worked (it recovered f=252 Hz exactly at SNR 11), so the loss was in
the covariance:

1. **`acf *= np.linspace(1, 0, nwin)**2`** - an ACF taper applied to force positive-definiteness. It
   crushes the off-diagonal correlations while preserving `acf[0]`, driving C toward sigma^2*I with sigma =
   the **broadband** rms of 25-Hz-high-passed strain (dominated by 25-60 Hz seismic power). A matched
   filter at 250 Hz is then charged the broadband noise instead of the in-band noise. **Cost: 8x.**
2. **`C[diag] += 1e-3 * acf[0]`** - a ridge of 1e-3 x the **broadband** variance is itself a white-noise
   floor far above the true in-band noise at 250 Hz. **Cost: a further ~3.5x** (ridge scan converges
   below 1e-6).

Fix: the noise ACF is the Wiener-Khinchin transform of a Welch PSD - **positive-definite by construction**
(nonnegative spectrum), so no taper is needed and the noise colour survives intact; ridge -> 1e-6.
Measured on real H1 noise, the corrected covariance gives SNR ~10.5 at the measured ringdown amplitude
(1.24e-21, read off the 100-400 Hz bandpassed envelope at t_peak+3 ms) - the right order for this event.

**A bug I introduced while fixing it, caught by check 1:** the one-sided Welch PSD must be halved before
the inverse FFT (`irfft(psd*fs/2)`). Without the /2 the covariance is **exactly 2x too large**, which
tempers the likelihood and inflates every credible interval by sqrt(2) **without moving the peak** - so no
peak-location check can see it. Caught only by testing acf[0] against the empirical variance (ratio was
2.0012; now 1.0006). Now a contract test.

## Controls (all pass)
- **Null:** pure real noise -> width 161 Hz = the prior. This *reproduces E85's real-data result exactly*,
  which is the cleanest statement of what was wrong: E85's output was indistinguishable from no signal.
- **Real-noise injections** (truth 252 Hz): amp 6e-22 -> 244.8 [211.6, 277.3]; 1.2e-21 -> 247.8
  [236.8, 258.5]; 2.5e-21 -> 249.7 [245.1, 254.2]. Truth inside the 90% CI throughout; width scales ~1/SNR.
- **Off-source nulls** at t_merger +/- 20-60 s on real data: widths 138-163 Hz, no false detections.
- **Time-reversal** of the same window (destroys the ringdown, keeps the noise colour): width 52 -> 165 Hz.
- **H1/L1 peak separation** 2.44 ms, within the 10 ms light-travel baseline.
- **Network now tightens**, as it must: 14.6 Hz vs 21.4 (H1) / 19.0 (L1) at t_peak+3 ms.

## Result: the start-time scan, and the trap at early times
Network (H1+L1), start times in units of the remnant light-crossing time M_f = 0.337 ms:

| t_0 | f220 [90% CI] | width | reading |
|---|---|---|---|
| 0-3 M | 230 Hz | **8-9 Hz** | **tight but WRONG** - biased low |
| 6-12 M | 238 -> 249 | 11-15 | climbing out of contamination |
| **12-18 M** | **251-254** | 16-26 | **plateau** |
| >24 M | - | 59-155 | signal decayed; back to the prior |

The single-220 fit is biased low at early times (overtone / nonlinear content), rises, and plateaus once
that content has decayed. **The tightest interval is the one that most confidently excludes the right
answer** - an 8 Hz CI at t_0 = 0 that is ~20 Hz low. Precision without a start-time scan is a trap, and
this is exactly the terrain of the overtone controversy.

## Validation gate vs LVK's own pyRing (Zenodo 17018009) - PASSED
LVK's release contains their pyRing **Kerr_220 posteriors at 19 start times** - the same scan. They sample
(Mf, af), so their samples are mapped to f220 through the **same** BCW relation this pipeline uses. Read
from the tarball at runtime, not quoted.

| t_0 | THIS (from scratch) | LVK pyRing | delta |
|---|---|---|---|
| 0M | 230.3 [226.2, 234.4] | 223.9 [220.2, 227.4] | +6.4 |
| 2M | 229.9 [225.3, 234.4] | 228.2 [224.6, 231.6] | +1.7 |
| 6M | 237.9 [232.1, 243.3] | 237.4 [231.7, 242.8] | +0.5 |
| 10M | 244.0 [236.9, 250.7] | 245.8 [239.5, 251.7] | -1.8 |
| 12M | 251.4 [243.0, 259.4] | 249.4 [240.8, 257.1] | +2.0 |
| 18M | 254.3 [240.3, 266.6] | 251.2 [236.5, 263.8] | +3.1 |

**Median |offset| 2.0 Hz over 2M-18M (max 5.8 Hz); LVK's median falls inside our 90% CI at 10/11 start
times.** The **widths** track as well (11.2 vs 11.1 at 6M; 16.4 vs 16.3 at 12M; 26.2 vs 27.4 at 18M) -
that is the stronger statement, since it says the covariance is correctly *calibrated*, not merely that
the peak lands in the right place. Both scans also show the same rise from ~224-230 Hz to ~250 Hz.

## Honesty / limits
- **The "251.7 +5.1/-5.0 Hz" figure used earlier in this session was never sourced** - it is not in this
  data release, and it is withdrawn. All comparison here is against LVK's actual posterior samples.
- Single damped sinusoid only; no 221 overtone, no quadratic 220Q mode. This battery therefore does NOT
  arbitrate the overtone question - it establishes that the pipeline is now good enough to try.
- Two detectors, no sky localization or antenna patterns; per-detector free amplitude/phase is what makes
  the lnL surfaces additive. Fixed 40 ms window; grid (1.5 Hz, 0.4 ms), so quoted widths are grid-limited
  below ~2 Hz.
- Agreement with LVK is a consistency check against *one* pipeline, not independent confirmation of the
  physics: both analyze the same strain with related likelihood constructions.
- The ringdown amplitude 1.24e-21 is an envelope read, used only to set the expected SNR scale.

## Verification
- 9 contract tests (`tests/test_e87_ringdown_corrected.py`), each encoding a defect that actually
  occurred: the WK factor-2 normalization; PD-without-taper; **the corrected covariance must beat the E85
  construction by >5x**; **pure noise must give an uninformative posterior**; the inherited E85 pre-window
  burst leak guard; injection recovery; **adding a detector must not broaden the posterior**; Kerr
  inversion roundtrip; peak location.
- The synthetic-noise fixture is **calibrated, not arbitrary**: a gentle 60x spectral step reproduces only
  a 1.8x taper penalty, while real H1 shows ~20x, so the fixture was steepened until it reproduced ~40x,
  and its ASD at 250 Hz (5.97e-24) matches real H1 (3.88e-24) within 1.5x. A fixture too tame to exhibit
  the bug would have made the regression test vacuous - the same failure mode as the bug itself.

Code: `src/e87_ringdown_corrected.py`. Numbers: `results/e87_ringdown_corrected_results.json`.
Tests: `tests/test_e87_ringdown_corrected.py`. Data: `data/strain/`, `data/lvk_tgr/` (gitignored).
Supersedes E85. Successor: the 221 overtone and 220Q quadratic mode, now on a validated foundation.
