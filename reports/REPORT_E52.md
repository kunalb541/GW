# E52 lab notebook - H0 anchor leave-one-out: the tension is SH0ES-sensitive (claim SURVIVES)

Prereg: preregs/E52_h0_leave_one_out_prereg.md. Inputs = E16 anchor table (no anchor re-derived).
Non-redundant independent late-time set: cosmic chronometers, JWST-CCHP combined, GW dark sirens,
TDCOSMO, SH0ES (CCHP components JAGB/TRGB folded into "combined" once, not double-counted).
CMB/early reference 67.36 +/- 0.54.

## Result: PASS all three -- an adversarial test the H0 finding survives, now quantified

| decision (locked) | outcome |
|---|---|
| D1 SH0ES sole >2.5sigma outlier | PASS (SH0ES 4.85sigma; all others <=1.6sigma) |
| D2 dropping SH0ES collapses tension >2.5 -> <2.0 | PASS (4.51sigma -> 1.75sigma) |
| D3 non-SH0ES anchors mutually consistent | PASS (chi2/dof 0.24, max pairwise 0.81sigma) |

Individual tension vs CMB: chronometers 0.14, GW sirens 0.15, TDCOSMO 1.16, JWST-CCHP combined 1.60,
SH0ES 4.85. Only SH0ES exceeds 2.5sigma.

Full late-time inverse-variance consensus H0 = 71.73 +/- 0.80 (4.51sigma vs CMB). Leave-one-out:

| dropped anchor | consensus H0 | tension vs CMB |
|---|---|---|
| cosmic chronometers | 72.03 | 4.70 |
| JWST-CCHP combined | 72.40 | 4.63 |
| GW dark sirens | 71.74 | 4.51 |
| TDCOSMO | 71.73 | 4.43 |
| SH0ES | 69.77 | 1.75 |

Only dropping SH0ES moves the needle: it takes the late-time consensus from 71.73 (4.51sigma) to
69.77 (1.75sigma). Every other single drop leaves the tension at 4.4-4.7sigma.

## Reading

The H0 tension is a SH0ES-anchor phenomenon. The independent non-SH0ES late-time anchors (JWST-CCHP,
chronometers, GW sirens, TDCOSMO) are mutually consistent (chi2/dof 0.24) and cluster at
H0 = 69.77 +/- 1.27, only 1.75sigma from the early value. This is an adversarial robustness test the
E10/E16 headline SURVIVES cleanly, and it puts a number on it: SH0ES contributes ~2.8sigma of the
4.5sigma late-vs-early tension.

## Caveats (honest)

- The residual 1.75sigma without SH0ES is NOT zero -- it is mild, driven mainly by JWST-CCHP combined
  (69.96) and TDCOSMO (71.6) sitting slightly high. "Balanced/mild without SH0ES", not "no tension".
- Anchors are summary (H0 +/- sigma) inputs, Gaussian-combined; a chain-level combination is not done.
- Independent-anchor choice: CCHP "combined" folds JAGB+TRGB+Cepheid; using the components separately
  would over-weight the CCHP ladder. Leave-two-out (SH0ES + each) stored in the JSON; none brings the
  tension back above 2.5sigma.

## Provenance

results/e16_h0_axis_results.json anchor values. No new downloads, no RNG.
