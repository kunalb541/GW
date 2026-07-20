# E86 lab notebook - the band-resolved chirp-mass boundary, closed from both sides (definitive negative)

**CHARACTERIZATION (no prereg).** E84 found the band-resolved chirp mass infeasible on a HEAVY event
(GW250114 sweeps 64->200 Hz in <25 ms, faster than any STFT window) and PREDICTED the complementary
failure for LIGHT events ("too faint per-slice"). E86 tests that prediction on the best case that exists
in the catalog, and closes the method.

## The test case (chosen to give the method every advantage)
**GW241011_233834**: the **most elongated event in the catalog** (axr 17.3; curved-law residual 0.62 deg),
q = 0.32, Mc_src = 9.08, network SNR ~36, and a **~1.2 s inspiral - 7x longer than GW250114's ~0.17 s**.
Public H1 *and* V1 strain. If ridge-based band-resolved measurement works anywhere, it works here.

## Result: it fails here too, and the rescue is degenerate
**(1) Only the lowest band tracks a real chirp.** Ridge monotonicity - Spearman(t, f), which is ~+1 for a
genuine rising chirp - by band:

| window | band | n | monotonicity | Mc_det |
|---|---|---|---|---|
| 0.50 s | 30-50 Hz | 26 | **+0.82** | 8.35 |
| 0.25 s | 30-55 Hz | 38 | **+0.80** | 6.77 |
| 0.25 s | 40-70 Hz | 51 | -0.34 | - |
| 0.125 s | 50-90 Hz | 27 | -0.02 | 0.54 |
| 0.06 s | 80-150 Hz | 60 | -0.38 | - |

Above ~55 Hz the "ridge" is not a chirp at all (monotonicity <= 0) - it is line and noise structure. The
conditioning already whitens *and* notches a measured line forest (60.00 Hz sits **~400x** above the local
median; also 35.5, 41, 46, 89-91, 177-180, 299-303 Hz). This is exactly E84's predicted per-slice-SNR
failure for light events.

**(2) The natural rescue is degenerate.** A slow low-frequency sweep can afford a LONG window (0.5 s),
which the heavy event could not - so the 30-50 Hz band does yield a monotonic track. But injections of
known chirps into the REAL off-source noise, run through the identical conditioning, show the estimator
barely responds to the truth:

| true Mc_det | recovered | ratio | monotonicity |
|---|---|---|---|
| 8.0 | 7.60 | 0.95 | +0.97 |
| 10.9 | 7.89 | **0.72** | +0.89 |
| 14.0 | 4.88 | 0.35 | +0.53 |

**A 36% change in the true chirp mass moves the recovered value by 4% - a response slope of 0.11** (1.0 =
unbiased, 0 = no information). The real measurement, Mc_det = 8.35 (monotonicity +0.82, n=26), is
"consistent" with the true ~10.9 only in the vacuous sense that this estimator maps everything in that
range to ~8. **The one surviving band carries essentially no chirp-mass information.**

## Verdict
**Ridge / spectrogram methods cannot deliver a band-resolved chirp mass for ANY event class**, for three
distinct and now-measured mechanisms:
1. **Heavy events** - the sweep crosses the upper bands faster than any usable window (E84, GW250114);
2. **Light events** - per-slice SNR is too low and the line forest dominates above ~55 Hz (E86, GW241011);
3. **The long-window rescue** - buys monotonicity at low frequency but is *degenerate* (slope 0.11).

The frequency-geometry observable - "does the chirp-mass geometry agree band to band?" - therefore
**requires matched-filter or banded Bayesian PE**. That is now a measured requirement, not a guess, and it
is the scoped successor (the E85 truncated-likelihood machinery is the natural foundation: the same
analytic linear-amplitude marginalization applies to a band-limited inspiral basis).

## Verification
- 5 contract tests (tests/test_e86_boundary.py): slope-inversion roundtrip; the notch chain suppresses a
  planted 60 Hz line below 5x the off-line median; **monotonicity discriminates an injected chirp from
  pure noise** (the chirp/no-chirp gate the band scan relies on); the estimator IS ~unbiased in the regime
  where the window is adequate (light, slow sweep: ratio within 30%); and **the compressed response slope
  is itself a contract test** (<0.75), so the boundary result is regression-guarded. Full suite 61/61.
- Injections use REAL off-source noise from the same file and the identical conditioning chain.

## Honesty / limits
- H1 only (V1 is far less sensitive; not used for the ridge). Single conditioning chain; a matched-filter
  or chirplet basis is exactly the method this result says is required, so its absence is the point, not
  an oversight.
- The GPS time was located empirically (145-sigma transient, 0.87 s from the arithmetic estimate); the
  band scan is insensitive to that offset since all times are referenced to the measured peak.
- Negative results of this kind close an avenue; they do not prove no signal-processing method could work
  - only that ridge/spectrogram tracking, the natural template-free approach, cannot.

Code: src/e86_band_resolved_boundary.py. Numbers: results/e86_band_resolved_boundary_results.json.
Tests: tests/test_e86_boundary.py. Data: data/strain/ (gitignored). Closes the E84 boundary; successor is
banded Bayesian PE on the E85 foundation.
