"""E89 contract tests - guard the population machinery and, above all, the two traps this battery fell
into before it produced a number. Data-free (synthetic populations). Seed 89."""
import numpy as np
import math
from scipy.stats import spearmanr, ks_2samp
from src.e89_mass_spin_hierarchical import (concentration, fit, nll, null_permute, null_forward,
                                            ks_from_prior, simulate_posterior, M_PIVOT)

RNG = np.random.default_rng(89)
NS = 400


def _population(n=120, true_slope=0.0, confound=False, rng=None, spin_aids_measurement=False):
    """Synthetic catalog built with the CORRECTED posterior model: a mixture of a concentrated
    component at the truth and the uniform prior, weight w = informativeness. Widening a Beta around
    the truth instead (the earlier version) makes low true spins pile against a_1 = 0 and look highly
    informative, which is not what real uninformative posteriors do -- they relax to the flat prior.

    `confound` makes heavier events less informative, calibrated to the real catalog's
    Spearman(ln m1, informativeness) ~ -0.5 rather than a near-deterministic coupling (which would
    leave stratified permutation with no within-stratum mass variation to shuffle).
    `spin_aids_measurement` additionally makes larger spins easier to measure - the real effect that
    makes an informativeness cut circular."""
    rng = rng or RNG
    m1 = np.exp(rng.uniform(math.log(6), math.log(110), n))
    lm = np.log(m1 / M_PIVOT)
    A = np.empty((n, NS))
    for i in range(n):
        mu = 1 / (1 + np.exp(-(-1.2 + true_slope * lm[i])))
        a_true = float(np.clip(rng.beta(mu * 4.0, (1 - mu) * 4.0), 1e-3, 1 - 1e-3))
        w = 0.75
        if confound:                       # heavier -> less informative, with real scatter
            w = float(np.clip(0.95 - 0.30 * lm[i] + rng.normal(0, 0.22), 0.02, 0.98))
        if spin_aids_measurement:
            # calibrated to the real catalog: across the 10 heaviest events, a_1 spans 0.40-0.90
            # while KS-from-prior spans 0.067-0.624, i.e. informativeness depends STEEPLY on spin
            w = float(np.clip(w * (0.10 + 2.0 * a_true ** 2), 0.02, 0.98))
        A[i] = simulate_posterior(a_true, w, NS, rng)
    return lm, A, m1


def test_concentration_flags_a_flat_posterior():
    """A uniform posterior is Beta(1,1): concentration ~2. This is how 'uninformative' is detected."""
    assert abs(concentration(RNG.uniform(0, 1, 20000)) - 2.0) < 0.15
    tight = np.clip(RNG.normal(0.3, 0.02, 20000), 1e-4, 1 - 1e-4)
    assert concentration(tight) > 50


def test_fit_recovers_a_true_slope():
    """Positive control: with good measurements and a real mass-spin correlation, recover it."""
    lm, A, _ = _population(n=140, true_slope=1.0, confound=False)
    _, b1, _, dl = fit(lm, A)
    assert 0.4 < b1 < 1.8, b1
    assert dl > 3.0, dl


def test_fit_is_unbiased_when_measurement_quality_is_mass_independent():
    lm, A, _ = _population(n=140, true_slope=0.0, confound=False)
    _, b1, _, _ = fit(lm, A)
    assert abs(b1) < 0.45, b1


def test_THE_TRAP_null_generator_must_relax_to_the_flat_prior():
    """THE modelling error that nearly made this battery under-report itself.

    A posterior must be simulated as a MIXTURE of truth and the uniform prior. Building it instead as
    a Beta CENTRED on the truth with low concentration makes a small true spin pile against a_1 = 0 --
    which looks informative, and is not what real data do (real heavy uninformative events sit at
    median a_1 = 0.474, i.e. the prior median 0.5). The wrong shape produced a spurious +0.42 slope in
    the null, which would have been subtracted from the real result as if it were estimator bias."""
    rng = np.random.default_rng(5)
    uninformative = simulate_posterior(0.05, 0.02, 6000, rng)      # true spin low, no information
    assert abs(np.median(uninformative) - 0.5) < 0.10, np.median(uninformative)
    informative = simulate_posterior(0.05, 0.98, 6000, rng)
    assert np.median(informative) < 0.15, np.median(informative)
    # the discarded shape: a low-concentration Beta at the truth piles at 0 and fakes information
    bad = rng.beta(0.05 * 2.5, 0.95 * 2.5, 6000)
    assert np.median(bad) < 0.10, np.median(bad)


def test_confound_alone_does_not_manufacture_a_slope():
    """With the corrected posterior shape and NO true mass-spin correlation, mass-dependent
    measurement quality alone must NOT produce a positive slope. This is what makes the observed
    +1.18 attributable to the population rather than to the estimator."""
    slopes = []
    for s in range(5):
        lm, A, _ = _population(n=110, true_slope=0.0, confound=True,
                               rng=np.random.default_rng(400 + s))
        slopes.append(fit(lm, A)[1])
    assert abs(np.mean(slopes)) < 0.45, np.mean(slopes)


def test_slope_is_recovered_even_with_the_confound_present():
    """A real mass-spin correlation must survive mass-dependent measurement quality."""
    lm, A, _ = _population(n=140, true_slope=1.2, confound=True, rng=np.random.default_rng(21))
    _, b1, _, dl = fit(lm, A)
    assert b1 > 0.4, b1
    assert dl > 3.0, dl


def test_stratified_permutation_null_is_centred_near_zero():
    """NULL B must destroy a true mass-spin link while holding measurement quality fixed. It only has
    power when informativeness and mass are not near-deterministically coupled: with a coupling of
    -0.98 every event inside a stratum has the same mass and the permutation shuffles nothing. The
    real catalog's coupling is -0.52, which the fixture reproduces."""
    lm, A, _ = _population(n=100, true_slope=1.2, confound=True, rng=np.random.default_rng(31))
    kap = np.array([concentration(a) for a in A])
    b1s, dls = null_permute(lm, A, kap, 10, np.random.default_rng(7))
    assert abs(b1s.mean()) < 0.6, b1s.mean()


def test_THE_OTHER_TRAP_informativeness_cut_is_circular():
    """Splitting on 'how far is this posterior from its prior' looks like the E85 lesson applied well,
    and is circular: among heavy events spin is well measured precisely WHEN IT IS LARGE.
    Stated directly, without a population draw: take a set of equally heavy events spanning the whole
    spin range, where a LOW spin cannot be measured at all (a short, heavy signal carries almost no
    spin imprint) while a LARGE spin is measurable. Selecting the "informative" half then keeps the
    high-spin half by construction, with no underlying mass-spin correlation anywhere.

    Note KS-from-prior ~ w * max(a, 1-a) is U-shaped in a, so a well-measured LOW spin is also
    'informative'. The circularity comes specifically from w itself rising with spin.
    """
    rng = np.random.default_rng(13)
    a_true = np.linspace(0.05, 0.95, 40)
    w = 0.10 + 0.85 * a_true                    # heavy events: only sizeable spins are measurable
    post = [simulate_posterior(float(a), float(wi), 4000, rng) for a, wi in zip(a_true, w)]
    a_med = np.array([np.median(p) for p in post])
    ks = np.array([ks_from_prior(p, rng) for p in post])
    assert spearmanr(a_med, ks)[0] > 0.5, spearmanr(a_med, ks)[0]
    keep = ks > np.median(ks)
    assert np.median(a_med[keep]) > np.median(a_med) + 0.10, \
        (np.median(a_med[keep]), np.median(a_med))


def test_flat_posteriors_contribute_almost_nothing_to_the_model_comparison():
    """The analytic intuition (a flat posterior gives the same ln-likelihood under every population,
    so it cannot bias the comparison) is TRUE only in the exact-flat limit -- which is why it failed
    to protect the real fit, where posteriors are merely near-flat."""
    lm = np.array([-1.0, 0.0, 1.0])
    flat = RNG.uniform(0, 1, (3, 40000))
    a = nll(np.array([-1.0, 0.0, math.log(4)]), lm, flat)
    b = nll(np.array([-1.0, 1.5, math.log(4)]), lm, flat)
    assert abs(a - b) < 0.5, (a, b)   # residual is Monte-Carlo noise on a spiky density
