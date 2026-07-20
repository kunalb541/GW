# Gate C — first measurement (2026-07-21). Frame and parameterization audit.

Gate C of the [revised PAPER_PLAN](PAPER_PLAN.md): repeat the primary result in detector-frame masses,
report $(\log m_1,\log m_2)$ and $(\mathcal M_c,q)$ behaviour, state the angle convention, and characterize
the near-round-covariance limit. 265 events, all with both source- and detector-frame masses.

## C1. The result changes with frame and coordinates — as it must

A PCA angle is **not** reparameterization-invariant. The point is to say which statement is stable.

| coordinates | n (elongated) | median $|\Delta\psi|$ | median axr |
|---|---|---|---|
| $(m_1,m_2)$ **source** frame — locked primary | 79 | 1.04° | 4.6 |
| $(m_1,m_2)$ **detector** frame | 79 | **0.32°** | 9.9 |
| $(\log m_1,\log m_2)$ source | 79 | 0.77° | 3.6 |

Paired on the same events (elongated in both frames, n=79), the detector frame wins on **81%** of events,
Wilcoxon signed-rank $p=4.1\times10^{-9}$.

**Interpretation, and it is not the naive one.** Source-frame masses are detector-frame masses divided by
$(1+z)$, so they import redshift/distance uncertainty that is no part of the chirp-mass degeneracy. Removing
it makes posteriors markedly more elongated (median axr $4.6\to9.9$). Since orientation is better defined for
elongated posteriors (Gate B2, and C2 below), most of the apparent gain is **mediated by axis ratio**, not by
the frame being intrinsically better-suited to the curve model. At MATCHED axr:

| axr band | n (src) | source | n (det) | detector |
|---|---|---|---|---|
| 3–5 | 43 | **1.37°** | 20 | 2.93° |
| 5–8 | 24 | 0.71° | 21 | 0.81° |
| 8–15 | 6 | 0.43° | 51 | 0.29° |
| 15+ | 6 | 0.61° | 11 | 0.24° |

At matched elongation the two frames are comparable, and the detector frame is *worse* in the 3–5 band. So
the defensible sentence is:

> In the detector frame, where redshift uncertainty does not enter, component-mass posteriors are
> substantially more elongated (median axis ratio 9.9 vs 4.6) and the reconstruction is correspondingly more
> accurate (0.32° vs 1.04°, paired $p=4\times10^{-9}$). At matched axis ratio the two frames perform
> comparably, so the gain is attributable to elongation rather than to the frame per se.

**Status:** the detector-frame analysis is **post-hoc**. The locked preregs (E67/E71) fixed the source frame,
and that stays the primary score. Detector frame is reported as a robustness/interpretation result and must
be labelled as such.

**$(\mathcal M_c,q)$ coordinates:** degenerate by construction, not run as a scored comparison. A
constant-$\mathcal M_c$ curve is a vertical line in $(\mathcal M_c,q)$, so the "prediction" collapses to
$\psi=90°$ for every event and carries no per-event content. Worth one sentence in the paper to preempt the
question; it is not evidence either way.

## C2. Near a round covariance the angle is undefined — the axr gate is justified

| axr band | n | median $|\Delta\psi|$ |
|---|---|---|
| 1.0–1.5 | 99 | 14.50° |
| 1.5–2 | 51 | 7.17° |
| 2–3 | 36 | 5.98° |
| 3–5 | 43 | 1.37° |
| 5+ | 36 | 0.62° |

Smooth and monotone. As axr $\to1$ the principal axis genuinely does not exist and the score degrades toward
the mod-180° random baseline (~45°); it reaches only 14.5° at axr 1.0–1.5, so even near-round posteriors
retain some information. This is the physical justification for gating on elongation — the gate is not a
tuning knob (Gate B2 showed nothing special happens at 3).

## Convention (to be stated explicitly in the manuscript)

- `ang_of(v) = degrees(atan2(v_y, v_x)) mod 180` — principal axes are undirected, so angles live on
  $[0°,180°)$.
- `adiff(a,b) = |((a-b+90) mod 180) - 90|` — wraps to $[0°,90°]$. **This is an ABSOLUTE value**; a signed
  residual requires $((a-b+90)\bmod180)-90$ without the absolute value. (An earlier pass in
  [GATE_B](GATE_B_FIRST_MEASUREMENT.md) used `adiff` for a sign test and produced a tautological
  "100% positive" result. Recorded so it is not repeated.)
- The eigenvector of the larger eigenvalue is taken as the principal axis; near a round covariance the two
  eigenvalues cross and the choice becomes arbitrary — hence C2.

## Gate C verdict

Passed in the sense required: the frame and parameterization dependence is now measured and explained rather
than assumed away. Nothing here invalidates the primary result; it constrains how it may be phrased. The
paper must not describe the measured Euclidean PCA angle as coordinate-invariant, and must not invoke
Fisher–Rao or Čencov unless an actual Fisher–Rao quantity is computed (it is not).

Outstanding: Gate D (preregistration timestamps, per-waveform-family and per-pipeline reporting),
Gate E (the precision law's direct multivariate fit, or its removal).
