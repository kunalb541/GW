# E55 lab notebook - multi-waveform robustness: E40 is waveform-robust; E45/E46 check data-blocked

Prereg: preregs/E55_multiwaveform_robustness_prereg.md. Local PE files carry two independent
waveform families (IMRPhenomXPHM, SEOBNRv4PHM); 59 events have both.

## Result: E40's chirp-mass lawfulness is WAVEFORM-ROBUST

| decision (locked) | outcome |
|---|---|
| D1 chirp-mass law holds for BOTH waveforms (median |dpsi_chirp|<12) | PASS (phenom 9.11, seob 6.09) |
| D2 orientation agrees across waveforms (elongated inter-wf |dpsi|<8) | PASS (3.31 deg) |

The (m1,m2) mass-plane orientation from IMRPhenomXPHM and SEOBNRv4PHM agree to a median 4.68 deg
(3.31 deg on the elongated, well-defined-orientation subset), and the constant-chirp-mass prediction
holds for both (E40 all-events with the Mixed waveform was 7.49 deg). E40's positive
geometric-lawfulness result is a real property of the posterior, not a waveform artifact.

## The instructive contrast (and an honest data-block)

- A REAL geometric result (E40 chirp-mass orientation) is waveform-robust (inter-waveform 3-5 deg).
- E46's coherent +dchi0 (low-PN) deviation, by contrast, is attributed in the literature to a
  WAVEFORM systematic -- exactly the kind of thing that would NOT be waveform-robust. That is the
  expected signature: real geometry survives a waveform change, a low-PN systematic does not.

DATA-BLOCK (honest): the direct multi-waveform replication of the E45/E46 GR-test coherences is NOT
possible with GWTC-3 data. The GWTC-3 parameterized-deviation set (par.zip) is FTI/SEOBNRv4_ROM-only
-- "only FTI was applied to events in GWTC-3 because of delays upgrading TIGER with IMRPhenomX" -- so
there is NO same-event IMRPhenom dchi_i set for the GWTC-3 events analysed in E46; the IMR-consistency
set (E45) is single-waveform. A true SEOBNR-vs-IMRPhenom replication of the E46 dchi0 coherence would
need the GWTC-2 TIGER release, which covers DIFFERENT events (not a same-event control). So E46's
"waveform systematic" attribution rests on the literature + the E55 contrast, NOT on a same-event
GWTC-3 multi-waveform test. This is a real limitation of the available data, reported as such.

## Caveats

- 59 events with both waveform families (not all 76; SEOBNRv4PHM absent for some).
- Waveform-robustness of the mass-plane orientation does not by itself confirm E45/E46's systematic
  origin -- it confirms the CONTRASTING (real, robust) case and leaves the systematic case
  data-blocked.

## Provenance

data/chains/gw_posteriors/*.h5 (C01:IMRPhenomXPHM, C01:SEOBNRv4PHM groups). No downloads, no RNG.
