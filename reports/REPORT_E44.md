# E44 lab notebook - hierarchical chi_eff population (NULL: negatives not required here)

Prereg: preregs/E44_chieff_hierarchical_prereg.md. Gaussian effective-spin population fit over 75
events' chi_eff posteriors, both flat-effective-prior (locked primary) and prior-reweighted
(pre-anticipated; induced chi_eff prior simulated per event from the isotropic-spin prior, seed 44),
plus a positive-truncation model comparison.

## Result: FAILS all three gates under both prior treatments

| quantity | flat (locked primary) | prior-reweighted |
|---|---|---|
| mu (MAP, 90% CI) | 0.060 [0.038, 0.078] | 0.090 [0.063, 0.120] |
| sigma (MAP, 90% CI) | 0.045 [0.026, 0.067] | 0.061 [0.033, 0.115] |
| f_neg (median, 90% CI) | 0.093 [0.010, 0.233] | 0.094 [0.004, 0.232] |
| free - truncated(chi_eff>=0) delta lnL | -1.0 | -0.74 |

| decision (locked) | flat | reweighted |
|---|---|---|
| D1 sigma 90% lower > 0.05 | FAIL (0.026) | FAIL (0.033) |
| D2 f_neg 90% lower > 0.05 | FAIL (0.010) | FAIL (0.004) |
| D3 free beats truncated by >=3 lnL | FAIL (-1.0) | FAIL (-0.74) |

## Reading

The population mean effective spin is positive and well-constrained (mu ~ 0.06-0.09); the
intrinsic spread is small (sigma ~ 0.05-0.06). The DECISIVE test D3: a population truncated at
chi_eff >= 0 (strictly non-negative, i.e. no dynamical/anti-aligned component) fits the data as
well or slightly BETTER than the free Gaussian (delta lnL negative both ways). So the ~9% Gaussian
negative fraction is an artifact of assuming Gaussian tails, NOT something the data require.
Prior-reweighting broadened sigma (0.045 -> 0.061) and raised mu as anticipated, but not enough to
demand support below zero.

Conclusion: with this 75-event sample and this method, the chi_eff population is consistent with a
narrow, marginally-positive distribution; a negative-chi_eff component is NOT required. This
reinforces the per-event null E43 at the population level.

## Honest scope (important - do NOT read as overturning the dynamical channel)

The published LVK result DOES find the chi_eff distribution extends slightly below zero (a small
negative tail / minority dynamical component). This battery does not overturn that; it shows that
a SIMPLIFIED independent pipeline does not independently REQUIRE it. Differences from the full
analysis that plausibly explain why:
- Gaussian population form only (the real negative tail is often captured by heavier-tailed or
  mixture models; a Gaussian's symmetric tail is what D3 penalises).
- chi_eff prior simulated with per-event MEDIAN mass ratio (not sample-by-sample q), amax=0.99,
  histogram density -> an approximate reweighting; my reweighted sigma (0.061) sits below the
  literature ~0.12, suggesting my prior division is incomplete (would push toward more negatives if
  fuller).
- No selection-function modelling. (Selection disfavours negative chi_eff, so a proper correction
  pushes the intrinsic distribution toward MORE negatives -- our omission is conservative for the
  existence claim, yet we still find none required.)
- 75-event confident subset with combined-waveform (C01:Mixed) posteriors, which are conservative.

## chi_eff thread summary (E42 -> E43 -> E44)

- E42: 34-36% of events have MEDIAN chi_eff < 0 (read as a dynamical hint).
- E43: NO single event is individually secure-negative (P(<0)>0.9 / 95% CI) -> medians over-count.
- E44: the POPULATION does not require a negative component either (truncation at 0 not rejected),
  under a Gaussian fit with approximate prior reweighting.
Consistent honest arc: this dataset+method do not establish negative chi_eff; the literature's
small negative tail rests on fuller selection-corrected, flexible-model inference not reproduced here.

## Provenance

data/chains/gw_posteriors/*.h5 (75 usable of 76). Prior sim seed 44 (deterministic). No downloads.
