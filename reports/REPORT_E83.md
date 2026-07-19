# E83 lab notebook - a from-scratch strain pipeline, validated on GW250114

**CAPABILITY + CONSISTENCY CHECK (not a precision Bayesian ringdown; no prereg).** "Science first": build
the strain-level analysis capability that the exotic-test class (data-driven frequency geometry,
ringdown-geometry bridge, echo/DM-rotation with controls) all require, and validate it on the loudest
event. Built with numpy/scipy/h5py only (gwpy/gwosc are not installed).

## The pipeline
Download GWOSC O4b strain -> whiten with an off-source Welch PSD -> bandpass -> instantaneous frequency
(Hilbert) for the chirp; post-peak dominant-frequency + log-envelope damping for the ringdown. All
functions are reusable (`whiten`, `bandpass`, `inst_frequency`, `ringdown_fit`).

## GW250114 validation
- Whitened peak amplitude **388 sigma** (the loudest event to date; H1 alone).
- **Chirp recovered**: instantaneous frequency rising through merger -- 89 Hz (-10 ms) -> 117 (-5 ms) ->
  187 (0 ms) -> 220 Hz (+5 ms).
- **Ringdown recovered**: dominant frequency **241 Hz** (E74 Kerr prediction 248.9 Hz, **3.2%**), damping
  **4.7 ms** (E74 4.10 ms, 14%). **CONSISTENT with the E74 Kerr prediction.**

This independently cross-checks E74: the ringdown frequency measured directly from strain matches the Kerr
QNM computed from the INSPIRAL-derived remnant (Mf, af via PE + Berti-Cardoso-Will). Inspiral -> remnant ->
ringdown closes in the actual data, not just in the waveform model.

## Verification
- 4 contract tests (tests/test_e83_ringdown.py): a synthetic damped sinusoid (250 Hz, 4 ms) injected into
  noise is recovered by `ringdown_fit` to <10 Hz and <25% in tau; whitening flattens red noise; the
  bandpass suppresses out-of-band tones by >1000x; the instantaneous-frequency of a linear chirp rises.
  Full suite 45/45.
- The recovered ringdown reproduces E74's independent (PE-based) Kerr prediction to a few percent.

## Honesty / limits
- This is a **consistency check, not a measurement of record.** The ringdown fit is single-detector
  (H1 only), single-mode (no 221 overtone), fixed-start (at the whitened peak), and a point estimate --
  so it carries a few-percent frequency bias and ~10-15% damping bias versus a proper Bayesian,
  multi-mode, start-time-marginalized ringdown (which is the LVK/pyRing standard and E74's published input).
- The early chirp track (-20 ms, 72 Hz) is noisy at the band edge; the rise from -5 ms is clean.
- No exotic claim is made or attempted here -- this is the pipeline's *validation*, deliberately on a
  known, GR-consistent event.

## Successor (the whole point)
With the pipeline validated, the legitimate next steps are: (1) a proper Bayesian multi-mode ringdown;
(2) the **data-driven frequency-geometry test** (the E73 successor -- measure where information actually
arrives vs the GR-Fisher prediction); (3) the ringdown-geometry bridge (does inspiral mass-plane geometry
predict the remnant Kerr geometry). The exotic-echo / dark-matter-frequency-rotation tests come ONLY AFTER
the pipeline is validated on multiple events and run with the coherence lens + waveform/systematic controls
-- because, per E79/E72, any positive there is far likelier a systematic than new physics.

Code: src/e83_strain_ringdown.py. Numbers: results/e83_strain_ringdown_results.json.
Tests: tests/test_e83_ringdown.py. Data: data/strain/ (gitignored; GWOSC O4b_4KHZ_R1, GW250114).
