# E84 lab notebook - data-driven chirp mass from strain: a ballpark measurement, an honest bias, and a feasibility boundary

**CHARACTERIZATION (no prereg; one template-free measurement + one negative result).** First use of the
E83 strain pipeline for physics: fit the textbook 0PN law f^(-8/3)(t) = K(tc - t) to the spectrogram
RIDGE of GW250114's whitened H1 strain, extracting the detector-frame chirp mass with NO waveform
templates. Then attempt the band-resolved version (the "frequency geometry" observable) and map where it
breaks.

## Result 1 - template-free chirp mass (with its honesty label)
- Ridge track: 39 confident time-frequency points, 32-192 Hz over the last ~170 ms.
- **Raw full-track fit: Mc_det = 33.0 Msun vs PE 31.1 (+6%).**
- **BUT the estimator is biased**: on physical synthetics (amplitude ~ f^(2/3), mild noise) it recovers
  +15% (Mc=10), +17% (15), +29% (30) HIGH - frequency quantization (df=16 Hz) plus window smearing in an
  accelerating sweep bias the f^(-8/3) slope, worse for faster (heavier) sweeps. Bin-collapse and finer
  bins do not cure it.
- **Honest claim: the strain-only chirp mass is BALLPARK consistent with PE (~20-30% template-free
  systematic); the raw +6% agreement is partly fortuitous and is NOT a precision validation.** The
  double-check (injection calibration) caught this before it was banked as "few-% agreement" - the E79
  lesson operating again.

## Result 2 - the band-resolved feasibility boundary (negative result, mechanism understood)
The E84 target observable was Mc PER FREQUENCY BAND (does the geometry emerge in-band as GR predicts?).
Infeasible via ridge methods, for a reason E73 PREDICTED:
- 32-64 Hz: 34 ridge points (fit possible, bias-dominated); 64-110 Hz: 4 points; 110-200 Hz: 1 point.
- GW250114 sweeps 64->200 Hz in <25 ms - less than ONE 62.5-ms STFT window. Heavy events compress the
  information anatomy into a sliver of time (E73's Spearman -1.00 compression, observed in data).
- Light events have the opposite failure: the sweep is long but per-slice SNR is tiny (ridge tracking
  needs per-window contrast; total SNR spread over thousands of cycles gives none).
- **Conclusion: band-resolved frequency geometry requires band-limited Bayesian PE (a major build) -
  template-free ridge methods cannot deliver it for any event class.**

## What E84 establishes
1. The strain pipeline can do template-free physics (a chirp-mass in the right ballpark from pure phase
   evolution) - with a fully characterized systematic, published alongside the number.
2. The E73 information-anatomy compression is now OBSERVED in data, not just predicted from the model.
3. The road to the data-driven frequency-geometry test is precisely scoped: banded Bayesian PE or
   matched-filter methods, not more signal processing.

## Verification
- 5 contract tests (tests/test_e84_chirp.py): slope-inversion roundtrip exact; negative slope -> nan;
  end-to-end synthetic recovery WITHIN the characterized bias envelope (1.0-1.4x, never low); the bias
  GROWS with Mc (mechanism guard); ridge false-positive rate in pure noise < 15%. Full suite 50/50.
- A time-bookkeeping bug (scipy stft window-center offset double-added) was caught by the contract tests
  and fixed; slope (hence Mc) was invariant but the pre-merger cut was mis-placed by 31 ms.
- The injection-bias table is computed inside the battery and stored in the results JSON.

## Honesty / limits
- Single detector (H1), 0PN law only, point estimates; the bias calibration uses idealized synthetics
  (white noise, no calibration lines) and is indicative, not a rigorous correction - hence "ballpark,"
  not a bias-corrected number.
- The 32-64 Hz band fit (38.7) is bias-dominated (synthetic 30 Msun gives 38.7 - consistent with pure
  bias), so no band-consistency claim is made in either direction.

Code: src/e84_data_driven_chirp.py. Numbers: results/e84_data_driven_chirp_results.json.
Tests: tests/test_e84_chirp.py. Data: data/strain/ (gitignored). Builds on E83; confirms E73 in data.
