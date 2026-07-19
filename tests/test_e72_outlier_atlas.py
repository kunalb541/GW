"""E72 contract tests - guard the outlier-atlas machinery (null, injection, FDR, partial, Tukey).
Data-free; pure functions. Seed 72 for any synthetic construction."""
import numpy as np
from src.e72_gw_geometry_outlier_atlas import spearman, partial_spearman, bh_fdr, tukey_upper_fence

RNG = np.random.default_rng(72)

def test_null_random_axis_not_flagged():
    # a random axis uncorrelated with the residual must not survive BH-FDR (control false positives)
    r = RNG.normal(size=32)
    flagged = 0
    for _ in range(200):
        axis = RNG.normal(size=32)
        _, p = spearman(r, axis)
        reject, _ = bh_fdr([p], 0.05)
        flagged += int(reject[0])
    assert flagged / 200 < 0.10   # empirical false-positive rate near 0.05

def test_injection_correlated_axis_recovered():
    # an axis built to correlate with the residual is recovered as significant
    r = np.arange(32).astype(float)
    axis = r + RNG.normal(scale=2.0, size=32)   # strong monotone dependence
    rho, p = spearman(r, axis)
    assert rho > 0.8 and p < 1e-3

def test_bh_fdr_known_pvalues():
    # classic BH example: p sorted, threshold i/K*q
    p = [0.001, 0.008, 0.039, 0.041, 0.9]
    reject, qv = bh_fdr(p, 0.05)
    # 0.001<=1/5*.05=.01 yes; 0.008<=2/5*.05=.02 yes; 0.039<=3/5*.05=.03 no ... largest i passing:
    assert reject.tolist() == [True, True, False, False, False]
    assert qv[0] <= qv[1] <= qv[4]   # monotone q-values

def test_partial_removes_spurious_via_confound():
    # r and axis share ONLY the confound z (independent added noise) -> raw corr real, partial ~ 0.
    # (noise comparable to z keeps the partial well-conditioned; a near-deterministic construction
    #  makes partial correlation a 0/0 ratio and is not a valid test of the machinery.)
    z = RNG.normal(size=300)
    r = z + RNG.normal(size=300)
    axis = z + RNG.normal(size=300)
    raw, _ = spearman(r, axis)
    part = partial_spearman(r, axis, z)
    assert raw > 0.3                  # shared confound induces a real raw correlation
    assert abs(part) < 0.15          # controlling z removes essentially all of it

def test_partial_keeps_genuine_signal():
    # genuine r-axis link independent of z survives partialling
    z = RNG.normal(size=200); axis = RNG.normal(size=200)
    r = 2 * axis + 0.5 * z + RNG.normal(scale=0.1, size=200)
    assert abs(partial_spearman(r, axis, z)) > 0.6

def test_tukey_fence_flags_outlier_not_inlier():
    v = np.concatenate([RNG.normal(1.0, 0.3, 31), [12.0]])  # one gross outlier
    fence = tukey_upper_fence(v)
    assert 12.0 > fence               # outlier above fence
    assert (v[:31] < fence).all()     # inliers below fence
