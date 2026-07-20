# E88 lab notebook - the 221 overtone in GW250114: a significant two-mode preference that is NOT the overtone

**CHARACTERIZATION (no prereg).** Built on the E87-corrected covariance (E85's was prior-dominated and
could not have supported this). The question: does GW250114's ringdown require a second QNM? The answer is
a **negative with a named cause** - the data do prefer two modes at high significance, but the preference
does not behave the way a real overtone must, so it cannot be attributed to the 221.

## The geometry first: why this is hard, computed before looking
At the IMR remnant the 221 sits **5.5 Hz** from the 220 (243.1 vs 248.6 Hz) but decays **3x faster**
(1.35 vs 4.10 ms). Over a 40 ms window the two bases are **~76% collinear**: most of the overtone is
something the 220 can already absorb. Only the ORTHOGONALIZED overtone SNR, `SNR_perp`, is available. With
each mode's amplitude propagated from t_peak by its OWN decay (the ratio fades with a 2.01 ms e-folding):

| t_0 | 0M | 2M | 3M | 4M | 6M | 8M | 12M |
|---|---|---|---|---|---|---|---|
| A221/A220 | 1.000 | 0.715 | 0.605 | 0.512 | 0.366 | 0.262 | 0.134 |
| SNR_perp (A221/A220 = 1 at peak) | 6.92 | 4.20 | 3.27 | 2.55 | 1.55 | 0.94 | 0.35 |
| SNR_perp (ratio 0.5 at peak) | 3.46 | 2.10 | 1.64 | 1.27 | 0.77 | 0.47 | 0.17 |

Detection needs SNR_perp >~ 3-4, so **any overtone evidence must live at 0-3M and be gone by 6M**. This was
computed from mode structure, the measured envelope amplitude, and the real noise covariance, with no
reference to any published result. It then predicts LVK's own evidence profile (below), which is the
strongest sign it is right.

## Two method results that had to be fixed before any measurement was meaningful
**(1) A Bayes factor needs a proper amplitude prior.** E85/E87 marginalized the linear amplitudes with a
flat (improper) prior - fine for a posterior on (f, tau), meaningless for model comparison. Replaced by
N(0, sigma_A^2), giving `lnB = 0.5 b^T (G + I/sigma_A^2)^-1 b - 0.5 ln det(I + sigma_A^2 G)`, **verified
against brute-force 2-D numerical integration to 3e-14**.

**(2) The naive multi-detector model destroys the test.** Giving each detector its own free 221 amplitude
adds 4 linear parameters and costs **~11 lnB of pure Occam penalty on signal-free data** (measured, not
assumed) - enough to hide any real overtone. But the 221 and the 220 pass through the SAME antenna pattern
in a given detector, so the complex ratio **rho = A221/A220 is shared across detectors** while each
detector keeps a free complex amplitude. Writing the model as `Re[A_det (T220 + rho T221)]` keeps it linear
in `A_det` for fixed rho via `M_red = M_full @ K(rho)` (**exact to 8e-16**). Both models then carry exactly
two linear amplitudes per detector, so:
- the linear-amplitude Occam factor **cancels** - across every start time and rho_max the sigma_A
  sensitivity over a 33x range is at most **0.32** (median 0.13);
- the entire extra cost of the overtone is the rho prior volume. On SYNTHETIC injections whose true rho is
  contained inside every disc tested, widening R = 1 -> 3 costs **2.00 / 2.12 / 1.83** against the expected
  ln(9) = 2.20. On the REAL data the same widening costs 1.01-2.06 (median 1.52) - smaller, because the rho
  posterior is not fully contained, which is itself the statement that rho is weakly measured;
- the signal-free Occam penalty falls from ~11 to **+0.9**.

## The dominant systematic: the remnant absorbs the overtone
With (Mf, af) **pinned** at the truth, an injected |rho| = 1 overtone gives dlnB = **+21.22**. With
(Mf, af) **marginalized** - the honest analysis - it collapses to **-0.05**. The single-mode model simply
moves the remnant: given an injected 220+221 it peaks at **(Mf, af) = (54.0, 0.150)**, whose 220 mode is
**f = 234.8 Hz, tau = 3.04 ms**, versus the true 248.6 Hz / 4.10 ms.

| injected \|rho\| | dlnB, remnant PINNED | dlnB, marginalized | absorbed |
|---|---|---|---|
| 0.5 | +0.77 | -1.71 | (all) |
| 1.0 | +21.22 | -0.05 | **~100%** |
| 2.0 | +110.01 | +15.12 | 86% |

(These are the values written by `src/e88_overtone_evidence.py` into the results JSON, at off-source
-150 s with injection phase 0.7. An earlier draft of this report quoted +24.93 / +0.21 / +96.93 / +14.75
from an exploratory run that used a different noise stretch and injection phase; those were not
reproducible from the committed code and are withdrawn. The conclusion is unchanged, and slightly
stronger: at |rho| = 1 the remnant freedom absorbs essentially ALL of the overtone.)

**This is E87's early-time bias, seen from the other side.** E87 found the single-220 fit returns ~230 Hz
at t_peak instead of the 251 Hz plateau; here a *known injected* overtone drives the single-mode fit to
234.8 Hz. Same mechanism, two independent batteries. Window length does not rescue it: dlnB stays ~0-1 for
windows from 20 ms to 320 ms, so the degeneracy is structural, not a windowing artifact.

## Result on GW250114, and why it is not the overtone
Network H1+L1, sigma_A = 1e-20, rho uniform on |rho| <= 2, (Mf, af) integrated over
Mf in [45,115], af in [0,0.95] (evidence integral converged: dlnB drifts 2.30 -> 2.47 under 8x refinement).

| t_0 | 0M | 1M | 2M | 3M | 4M | 6M | 8M | 10M | 12M |
|---|---|---|---|---|---|---|---|---|---|
| **ours** | 6.15 | 6.09 | 6.33 | 5.88 | 3.43 | 4.59 | 4.94 | -0.46 | -2.14 |
| LVK pyRing | 20.77 | 10.09 | 5.67 | 0.67 | 1.76 | 1.22 | 5.52 | -1.31 | -2.21 |
| **genuine injected overtone, \|rho_0\| = 1.5** | **+4.45** | **-2.19** | -1.20 | -0.57 | -2.31 | -2.21 | -1.24 | -1.73 | -1.94 |
| injected pure 220 | -0.70 | +0.29 | -1.94 | -1.46 | -2.26 | -1.96 | -0.13 | -0.78 | -1.94 |

Nulls, from 13-14 injections into real off-source noise at the measured amplitude:
- **pure-220 null (the relevant one):** dlnB = **-2.06 +/- 0.98**; the observed +6.15 is **8.4 sigma** above
  it and **0/13** null realizations reach it. So the two-mode preference is real and not a noise artifact.
- signal-free null: +0.91 +/- 0.58. This is the WRONG null (it contains no 220 either) and is reported only
  to show the difference: against it the result would look like 9.4 sigma, flattering and meaningless.
- **detection power is poor:** with |rho| = 1 genuinely injected, dlnB = +1.17 +/- 4.32.

**The discriminator.** A genuine 221 must fade with a 2.01 ms e-folding, so its dlnB must collapse within a
few M_f - and it does: the injected |rho_0| = 1.5 template falls **+5.69** from 0M to 8M (from +4.45 to
-1.24, i.e. it is undetectable already by 1M). The observed preference falls only **+1.21**, sitting at
~5-6 from 0M all the way to 8M, where SNR_perp = 0.94 and **no overtone can survive**.

**Verdict: the observed two-mode preference does not decay like an overtone, so it is not the overtone.**
By the standing coherence lens - an anomaly that fails to behave as the physics demands is a systematic -
this is a systematic in our pipeline, of roughly constant size ~+5 across 0-8M. At 0M the observed value is
numerically compatible with |rho| ~ 1.5-2, but since the same preference is present at 8M where no overtone
exists, the overtone-attributable excess at 0M is small and we do not claim it.

**LVK's profile, by contrast, does decay** (20.77 -> 10.09 -> 5.67 -> 0.67 over 0-3M), which is the
behaviour a real overtone must show, and it matches the SNR_perp prediction above. Their analysis, not
ours, is the one that supports an overtone claim here. We reproduce them well at 2M (6.33 vs 5.67), 8M
(4.94 vs 5.52), 10M (-0.46 vs -1.31) and 12M (-2.14 vs -2.21), and differ most at 0-1M.

## Honesty / limits
- **We do not identify the systematic.** Candidates: our free per-detector complex amplitude (no sky
  position, polarization or inclination, so the two detectors are only loosely tied), residual PSD
  mis-estimation, and non-stationarity. Naming it is the successor battery, not a result here.
- We do NOT reproduce LVK's dlnB = 20.77 at 0M (we get 6.15). Our model is looser than theirs in exactly
  the ways listed above, and our test has only modest power; this is a limitation of our analysis, not a
  challenge to theirs.
- The absorption and shape studies use injections at a single off-source stretch (-150 s) and a single
  reference phase; the nulls use 13-14 stretches but one phase draw each.
- Fixed 40 ms window and 25 Hz high-pass, inherited from E87. Grid-limited: (Mf, af) at 1.0 Msun / 0.025,
  rho on a 25x25 disc.
- `<|rho|>` is NOT reported as a measurement: on pure noise it returns 1.31, essentially the prior mean
  (4/3 for a disc of radius 2), so it carries little information at this SNR.

## Verification
- 10 contract tests (`tests/test_e88_overtone.py`): the K-reduction is exact; rho = 0 reduces to the
  220-only model; the evidence formula matches brute-force integration; **shared-rho keeps the signal-free
  Occam penalty small** (guards against reverting to the design that failed); sigma_A nearly cancels; the
  rho prior volume costs ~ln(area); the overtone is mostly collinear with the 220; a loud overtone IS
  detected; a pure 220 does not fake one; and **a genuine overtone's dlnB decays with start time** - the
  discriminator this battery turned on.
- One test had to be fixed after it failed for the right reason: injecting |rho| = 2 puts the truth OUTSIDE
  the R = 1 disc, so widening to R = 3 both dilutes the prior and newly captures the truth, and the two
  cancel (measured -0.56). The test now injects |rho| = 0.8, contained in every disc.
- Full suite 80/80.

Code: `src/e88_overtone_evidence.py`. Numbers: `results/e88_overtone_evidence_results.json`.
Tests: `tests/test_e88_overtone.py`. Data: `data/strain/`, `data/lvk_tgr/` (gitignored).
Successor: identify the flat ~+5 systematic (sky-position-tied amplitudes are the first suspect).
