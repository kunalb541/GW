"""E96 contract tests - guard the thickness-mechanism battery. Data-free (synthetic posteriors)
except where the committed artifact is inspected. Seed 96."""
import inspect
import json
import math
import os

import numpy as np
from scipy.stats import spearmanr

from src.e96_curve_thickness_mechanism import (curve_pt, normal_at, thickness_profile, taper_model,
                                               psi_curve_with_thickness, cross_family, verdict,
                                               RESULT_JSON, MIN_GOOD_BINS)

RNG = np.random.default_rng(96)


def _cloud(mc, q_lo, q_hi, wfun, n=60000, rng=RNG):
    """Samples spread along a constant-Mc curve with a controlled perpendicular width."""
    q = rng.uniform(q_lo, q_hi, n)
    c1, c2 = curve_pt(mc, q)
    nx, ny = normal_at(mc, q)
    off = rng.normal(0, 1, n) * np.asarray(wfun(q), float)
    return c1 + nx * off, c2 + ny * off, q


def test_constant_thickness_does_not_force_monotonic_w():
    """THE artifact check. If the estimator manufactured monotonic w(q), the observed
    Spearman(w,q) ~ +1 on real events would be meaningless. Constant true thickness must give a
    RANDOM-signed, near-flat profile -- never a systematic +1."""
    rhos = []
    for mc, w0 in ((25.0, 1.0), (25.0, 3.0), (10.0, 0.5), (60.0, 2.0), (40.0, 1.5)):
        m1, m2, q = _cloud(mc, 0.25, 0.95, lambda qq: np.full_like(qq, w0))
        mid, w = thickness_profile(m1, m2, q, mc)
        assert len(mid) >= MIN_GOOD_BINS
        rho = spearmanr(mid, w)[0]
        rhos.append(rho)
        assert not np.isclose(rho, 1.0), f"constant thickness produced a perfect ramp: {rho}"
        assert abs(w[-1] - w[0]) < 0.25 * w0, (w[0], w[-1])   # profile is flat to within noise
    assert min(rhos) < 0, f"all signs positive => a systematic bias exists: {rhos}"


def test_growing_thickness_is_detected():
    """Converse: a genuinely growing width must give a strongly positive Spearman and a rising w."""
    for slope in (0.5, 1.5):
        m1, m2, q = _cloud(25.0, 0.25, 0.95,
                           lambda qq: 1.0 + slope * (qq - 0.25) / 0.7)
        mid, w = thickness_profile(m1, m2, q, 25.0)
        assert spearmanr(mid, w)[0] > 0.8, spearmanr(mid, w)[0]
        assert w[-1] > w[0] * 1.2, (w[0], w[-1])


def test_cross_family_prediction_cannot_access_target_thickness():
    """The out-of-sample test is only meaningful if the target family's width never enters. Guard
    structurally: thickness_profile must be called on the SOURCE arrays only, and the target must
    contribute nothing but its Mc median, its q marginal and its measured axis."""
    src = inspect.getsource(cross_family)
    assert 'thickness_profile(src["m1s"]' in src.replace("'", '"'), src
    assert 'tgt["m1s"]' not in src and 'tgt["m2s"]' not in src, "target masses leak into the model"
    # only these target fields may be read
    used = {m for m in ("mcs", "q", "m1s", "m2s") if f'tgt["{m}"]' in src}
    assert used <= {"mcs", "q"}, f"target fields used: {used}"


def test_nuisance_tapers_are_fitted_to_the_same_widths():
    """'Any taper helps' must be distinguishable from 'the measured taper helps', so constant,
    linear and quadratic must be fitted to the SAME source widths and scored on the same events."""
    mid = np.linspace(0.3, 0.9, 6)
    w = 1.0 + 1.5 * (mid - 0.3)
    qq = np.linspace(0.3, 0.9, 50)
    vals = {k: taper_model(mid, w, k)(qq) for k in ("measured", "constant", "linear", "quadratic")}
    assert np.allclose(vals["constant"], np.mean(w))                 # constant ignores the ramp
    assert np.corrcoef(vals["linear"], qq)[0, 1] > 0.99              # linear tracks it
    assert np.allclose(vals["linear"], vals["measured"], atol=0.05)  # exact ramp: linear == measured
    src = inspect.getsource(cross_family)
    assert 'for k in kinds' in src and 'kinds = ("measured", "constant", "linear", "quadratic")' in src


def test_zero_thickness_reproduces_the_pure_curve():
    """Sanity: with w = 0 the thickness model must collapse onto the plain curve reconstruction."""
    from src.e71_gwtc5_curved_law import curve_psi
    from src.e65_pn_fisher_rotation import adiff
    rng = np.random.default_rng(1)
    q = rng.uniform(0.3, 0.95, 20000)
    a = psi_curve_with_thickness(25.0, q, lambda qq: np.zeros_like(qq), rng)
    assert adiff(a, curve_psi(25.0, q)) < 0.5


def test_verdict_separates_finite_thickness_from_arc_variation():
    """A result where a CONSTANT taper does as well as the measured one must NOT be reported as
    'arc-varying thickness explains the residual'."""
    cross = {t: {"n": 60, "pure_curve": 1.20, "measured": 0.95,
                 "measured_vs_pure_wilcoxon_p": 0.001,
                 "constant": 0.94, "linear": 0.90, "quadratic": 0.92} for t in ("AtoB", "BtoA")}
    v = verdict(cross)
    assert v["finite_thickness"] == "SUPPORTED OUT-OF-SAMPLE"
    assert v["arc_variation"] == "NOT ESTABLISHED"
    assert "do not quote a fraction" in v["statement"].lower()


def test_committed_artifact_does_not_overclaim():
    """The shipped result must not assert arc-variation or a fraction-of-residual explained."""
    if not os.path.exists(RESULT_JSON):
        return
    d = json.load(open(RESULT_JSON))
    v = d["verdict"]
    assert set(v) >= {"finite_thickness", "arc_variation", "statement"}
    if v["arc_variation"] != "SUPPORTED":
        assert "NOT established" in v["statement"] or "NOT ESTABLISHED" in v["statement"].upper()
    assert "caveat" in d["in_sample"]
