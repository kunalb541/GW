# E74 lab notebook - GW250114 deep-dive: the loudest event, a louder GW150914-twin, confirms Kerr spectroscopy

**This is a single-event characterization + literature synthesis, NOT a locked-decision battery.** The
O4b TGR / ringdown (pyRing) products are not public, so the ringdown spectroscopy and the no-hair
VERDICT are the PUBLISHED result, cited: Suzuki, Kubota, Morisaki, Motohashi & Watarai 2026
(arXiv:2605.03576, "Ringdown Analysis of GW250114 with Orthonormal Modes") and the LVK IMR analysis via
GWTC-5 (ref [15] therein). There is no prereg because nothing new is blind-tested on fresh data - this
report characterizes the event from the PE posterior I have, validates against the published numbers,
and adds one INDEPENDENT computation: the Kerr QNM spectrum the remnant predicts.

## GW250114 at a glance (PE posterior, NRSur7dq4 group, n=17253)
- Loudest GW event to date: network SNR ~77 (paper: ~80).
- Near-EQUAL-mass BBH: m1 = 33.8, m2 = 32.2 Msun (q ~ 0.96); chi_eff ~ -0.02 (low spin); z ~ 0.09.
- Remnant: Mf_source = 62.8 Msun, af = 0.679 (detector-frame Mf = 68.4 Msun).

## Published-value validation (my PE reproduces the published IMR remnant)
| quantity | this PE | published (Suzuki2026 / GWTC-5 IMR) | match |
|---|---|---|---|
| m1_source | 33.8 | 33.6 (+1.2/-0.8) | yes |
| m2_source | 32.2 | 32.2 (+0.8/-1.3) | yes |
| Mf_source | 62.8 | 62.7 (+1.0/-1.1) | yes |
| af | 0.679 | 0.68 (+/-0.01) | yes |
Column identity + parameter recovery confirmed against the publications (the mandatory data gate).

## Independent contribution: the Kerr QNM spectrum the remnant predicts
Propagating the (Mf_det, af) posterior through the Berti-Cardoso-Will (2006) l=m=2 fits gives the
no-hair (Kerr) prediction - the concrete frequencies/damping times the ringdown must match:
- **(2,2,0) fundamental**: f = 248.9 Hz (90% 247.8-250.2), tau = 4.10 ms
- **(2,2,1) first overtone**: f = 243.4 Hz (90% 242.4-244.5), tau = 1.35 ms (decays ~3x faster; low Q)
The QNM posteriors are tight (f_220 to ~1 Hz) because the remnant is measured to ~1.5%. This is what
makes GW250114 the first genuinely informative no-hair event: the Kerr targets are pinned.

## The published no-hair result (cited, not reproduced here)
Suzuki et al. 2026, using orthonormalized QNMs (which reduce the amplitude correlations that plague
non-orthogonal multi-mode fits), report for GW250114:
- the (2,2,1) **overtone is detected at 99.9%** (up from 82.5% in the non-orthogonal analysis);
- the Kerr-deviation parameters **df_221 and dgamma_221 are consistent with zero - no significant
  deviation from Kerr; the no-hair theorem is upheld** at this event's unprecedented SNR.

## GW250114 is a louder GW150914-twin
Reference check: a GW150914-like remnant (Mf_det = 68 Msun, af = 0.68) gives f_220 = 250.3 Hz,
tau_220 = 4.08 ms - essentially identical to GW250114's 248.9 Hz / 4.10 ms. GW250114 has nearly the
same remnant as the first-ever detection but ~3x the SNR (~80 vs ~24), which is exactly why the
overtone that was marginal/contested in GW150914 is now a 99.9% detection. The "black holes are Kerr"
program gets its cleanest single-event confirmation here.

## Curved-law note
GW250114 is near-equal-mass (q ~ 0.96) so its (m1,m2) posterior is near-round (axr ~ 2.0); the E71
constant-Mc geometry law's orientation is weakly defined for it and it is correctly outside the axr>=3
elongated set. The loudest event is, by luck of its symmetry, not a geometry-law probe.

## Verification
- QNM machinery: 4 contract tests (tests/test_e74_qnm.py) - GW150914-like reference (250 Hz/4 ms),
  f ~ 1/M scaling, f rises with spin, overtone damps faster. Full suite 27/27.
- Published-value validation: all four remnant/mass quantities match the publications (table above).
- Reference cross-check: the Kerr formula reproduces the canonical GW150914 220 mode.

## Honesty / limits
- I did NOT redo the strain ringdown spectroscopy; that (and the no-hair verdict) is the published
  result, cited. My independent piece is the PE characterization + the Kerr-QNM prediction + validation.
- Single event; not a locked battery (no blind decision rule on new data). The area theorem (independent
  inspiral-vs-ringdown horizon areas) needs the unreleased O4b TGR products - deferred with E45-E60.
- Detector-frame Mf used for observed QNM frequencies; source-frame quoted for the remnant.

Code: src/e74_gw250114_deepdive.py. Numbers: results/e74_gw250114_deepdive_results.json.
Data: data/chains/gwtc5/GW250114_082203-...hdf5 (gitignored). Published refs: arXiv:2605.03576; GWTC-5.
