# E57 lab notebook - black-hole area theorem (Hawking's 2nd law) from GWTC-3 mergers

Prereg: preregs/E57_bh_area_theorem_prereg.md. Kerr horizon area A = 8*pi*M^2*(1+sqrt(1-a^2)).
A_initial from the INSPIRAL segment (progenitor source-frame masses + spins), A_final from the
POSTINSPIRAL (ringdown) segment (remnant) -- disjoint data, independent (Isi et al. 2021 setup).

## Result: area theorem HELD (no violations), modest significance

Only 4 of 18 IMR events carry a postinspiral remnant (final_mass_source, final_spin) -- the loud
events with a measurable ringdown. Per event, P(A_final > A_initial):

| event | P(dA>0) | median frac area increase | A_init | A_final |
|---|---|---|---|---|
| GW170814 | 0.529 | 0.05 | 83777 | 95567 |
| S190814bv (GW190814) | 0.725 | 0.25 | 27513 | 34689 |
| GW150914 | 0.738 | 0.22 | 130031 | 162370 |
| GW170104 | 0.916 | 0.79 | 69507 | 125900 |

| decision (locked) | outcome |
|---|---|
| D1 no event with P(dA>0)<0.05 (no violation) | PASS (0 violations) |
| D2 >=1 strong single-event confirmation P(dA>0)>0.90 | PASS (GW170104, 0.916) |
| D3 stacked combined significance (area increases) | 0.92 sigma |

## Reading

The black-hole area theorem is CONFIRMED at the qualitative level: all four loud events have the
horizon area INCREASING (median fractional increase 5-79%), none violates it (all P>0.5), and
GW170104 gives a clean single-event confirmation (0.92). This is a genuine test of classical BH
gravity / the 2nd law of black-hole mechanics, distinct from the E45-E47 waveform-deviation tests.

## Honest limitations (this is a modest, not a strong, result)

- Only 4 loud events have an independent ringdown remnant; the test is intrinsically single-event-
  ish (as in the literature) and the stacked significance is only 0.92 sigma.
- My GW150914 P=0.738 is BELOW Isi et al. 2021's 0.97. The gap is method: I use a crude independent
  random-pairing of the two posteriors with the default BROAD spin priors on the inspiral, and the
  horizon area depends strongly on spin (the factor 1+sqrt(1-a^2) ranges 1..2), so a poorly-measured
  inspiral spin inflates A_initial's spread and washes out the increase. The careful Isi analysis
  (specific frequency cuts, marginalisation) recovers the stronger 0.97.
- So E57 confirms the area theorem holds and is violation-free in this sample, but does NOT reach
  the literature's precision; it should be read as a consistency check, not a stringent bound.

## Provenance

data/chains/tgr/IGWN-GWTC3-TGR-v1-imr.zip inspiral + postinspiral posteriors (source-frame). Seed 57.
