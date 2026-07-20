# Gate B — first measurement (2026-07-21). Threshold PASSES; a real sub-degree systematic is exposed.

Gate B of the [revised PAPER_PLAN](PAPER_PLAN.md): put uncertainty on every angle, score the
uncertainty-normalized residual, show coverage, and replace the hard axr $\ge3$ cut with a
threshold-sensitivity curve. 265 events, 200 bootstrap resamples each.

**Method note.** $\psi_{\rm meas}$ and $\psi_{\rm curve}$ are computed from the SAME posterior samples, so
their bootstrap errors are correlated. Each resample therefore draws one index set and recomputes BOTH the
measured axis and the curve inputs from it, bootstrapping the *difference* directly. $m_1$, $m_2$, $q$ and
$\mathcal M_c$ are kept sample-aligned for this (the committed `load_event` does not align $q$ with the
finite-mass mask, so a fresh aligned loader was used).

## B1. The reconstruction is NOT exact up to sampling noise

| quantity (elongated, axr $\ge3$, n=79) | value |
|---|---|
| median $|\Delta\psi|$ | 0.96° |
| median bootstrap $\sigma$ on $\Delta\psi$ | **0.24°** |
| median $|\Delta\psi|/\sigma$ | **4.91** |
| coverage $|z|<1$ (nominal 68%) | **5%** |
| coverage $|z|<2$ (nominal 95%) | **16%** |

The ~1° accuracy is **not** sampling noise: it is ~5× larger, and the coverage is badly under-nominal. The
constant-$\mathcal M_c$ curve is an excellent but **imperfect** description of the posterior's orientation,
and the paper must say so. This is the most important thing Gate B found.

## B1b. The residual is SIGNED — after correcting an error of mine

**Error caught, recorded deliberately.** The repo's `adiff(a,b) = abs((a-b+90)%180-90)` returns an
**absolute** value. A first pass used it to test for a signed bias and reported "100% of elongated events
positive, sign test $p=3\times10^{-24}$." That is a tautology — every value is non-negative by
construction — and it was very nearly written up as a spectacular result. Re-run with a genuinely signed
difference, $(a-b+90)\bmod 180-90$:

| set | n | median signed $\Delta\psi$ | fraction positive | sign-test $p$ |
|---|---|---|---|---|
| all elongated | 79 | **−0.725°** | 20% | $<0.001$ |
| GWTC-3 | 28 | −0.720° | 4% | $<0.001$ |
| O4a | 19 | −1.171° | 21% | 0.019 |
| O4b | 32 | −0.602° | 34% | 0.110 |

So there IS a consistent signed offset — the curve **under-rotates** relative to the measured axis by
roughly 0.6–1.2° — but it is strongest in the training catalog and only marginal in the newest one
(4% → 21% → 34% positive across GWTC-3 → O4a → O4b). Do not overstate it: significant in two catalogs,
$p=0.11$ in the third. Weak correlations with $\mathrm{axr}$ ($+0.33$), $\mathcal M_c$ ($-0.21$), median $q$
($+0.09$).

## B1c. Candidate mechanism, tested synthetically

The pure-curve model has **zero thickness**; a real posterior has finite width perpendicular to the curve.
Synthetic samples spread along a constant-$\mathcal M_c$ curve with controlled perpendicular width:

| perpendicular thickness | thickness taper along arc | $\psi_{\rm meas}-\psi_{\rm curve}$ |
|---|---|---|
| 0 | – | 0.000° |
| 0.5 | none | 0.029° |
| 2.0 | none | 0.233° |
| 0.5 | 0.8 | 0.067° |
| **2.0** | **0.8** | **1.412°** |
| 2.0 | −0.8 | 0.609° |

Uniform thickness barely rotates the axis; thickness **varying along the arc** rotates it by ~1.4°, the
right order for the observed residual. That is a concrete, testable next-order term, not hand-waving — and
it is a better use of the residual than ignoring it.

## B2. Threshold sensitivity — axr $\ge3$ is NOT tuned

| axr threshold | n | curve | tangent |
|---|---|---|---|
| 1.5 | 170 | 2.17 | 6.14 |
| 2.0 | 114 | 1.37 | 5.79 |
| 2.5 | 87 | 1.07 | 5.40 |
| **3.0** | **79** | **0.96** | **5.20** |
| 4.0 | 49 | 0.72 | 4.03 |
| 5.0 | 36 | 0.68 | 2.60 |
| 6.0 | 25 | 0.67 | 1.78 |
| 8.0 | 12 | 0.54 | 1.02 |
| 10.0 | 9 | 0.51 | 0.99 |

Monotone and smooth: nothing special happens at 3, so the locked primary score is not threshold-tuned.
Note the curve's *advantage* over the tangent shrinks at extreme elongation (5.4× at axr $\ge3$, 1.9× at
axr $\ge10$) — worth a sentence, since it is the opposite of what a naive "longer arc, bigger curvature
effect" story would predict and should be checked against the arc-length demotion in
[GATE_A](GATE_A_FIRST_MEASUREMENT.md).

## Where this leaves the claim

Gate B is passed in the sense that the analysis is now honest, but it **narrows the claim**:

> The reconstruction recovers the orientation to ~1° on elongated events. That 1° is a genuine systematic,
> ~5× the sampling uncertainty, with a signed component of ~−0.7° whose magnitude is reproduced by the
> posterior's finite, arc-varying thickness — a term the zero-thickness curve model omits by construction.

Outstanding: Gate C (frame and parameterization audit), Gate D (prereg timestamps, per-waveform-family
reporting), Gate E (precision-law multivariate fit or removal). The thickness term is the natural
next battery and would upgrade the paper from "a good reconstruction" to "a reconstruction with a
quantified, explained residual."
