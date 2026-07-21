"""E97 contract tests - the principal-curve self-consistency battery. Data-free (synthetic posteriors)
except where the committed artifact is inspected. Seed 97."""
import ast
import json
import os

import numpy as np
import pytest

from src.e97_principal_curve_selfconsistency import (curve_pts, self_consistency, axis_of,
                                                     RESULT_JSON, GRID_SWEEP)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RNG = np.random.default_rng(97)


def _cloud(mc, w, n=60000, skew=0.0, rng=RNG):
    """Samples about the constant-Mc curve. skew shifts them off it along the local normal."""
    q = rng.uniform(0.3, 0.95, n)
    C = curve_pts(mc, q)
    fwd = curve_pts(mc, q + 1e-4) - C
    nrm = np.hypot(fwd[:, 0], fwd[:, 1])[:, None]
    t = fwd / nrm
    nv = np.column_stack([-t[:, 1], t[:, 0]])
    off = rng.normal(0, w, n) + skew * w
    P = C + nv * off[:, None]
    return P[:, 0], P[:, 1], q


def test_symmetric_scatter_about_the_curve_is_self_consistent():
    """If samples are symmetric about the curve, each curve point IS the mean of what projects to it,
    so the measured violation must be ~0. Otherwise the estimator invents a violation."""
    m1, m2, q = _cloud(25.0, 1.0)
    offs, means, pts = self_consistency(m1, m2, q, 25.0, 40, 40)
    assert len(means) >= 10
    scale = float(np.sqrt(np.linalg.eigvalsh(np.cov(np.column_stack([m1, m2]).T))[-1]))
    assert abs(np.mean(offs)) / scale < 0.01, np.mean(offs) / scale


def test_offset_scatter_is_detected_as_a_violation():
    """Shift the cloud off the curve along the normal: the violation must appear, with the right sign."""
    for skew in (+1.0, -1.0):
        m1, m2, q = _cloud(25.0, 1.0, skew=skew)
        offs, _, _ = self_consistency(m1, m2, q, 25.0, 40, 40)
        assert np.sign(np.mean(offs)) == np.sign(skew), (skew, np.mean(offs))
        assert abs(np.mean(offs)) > 0.4, np.mean(offs)


def test_offsets_are_measured_along_the_normal_not_the_tangent():
    """Sliding samples ALONG the curve is reparameterization, not a self-consistency violation, so it
    must not register as one."""
    m1, m2, q = _cloud(25.0, 1.0)
    q2 = np.clip(q * 1.02, 0.02, 1.0)                      # move along the curve
    C = curve_pts(25.0, q2)
    offs, _, _ = self_consistency(C[:, 0], C[:, 1], q2, 25.0, 40, 40)
    assert np.max(np.abs(offs)) < 0.15, np.max(np.abs(offs))


def test_no_hdf5_use():
    path = os.path.join(ROOT, "src", "e97_principal_curve_selfconsistency.py")
    tree = ast.parse(open(path).read())
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert "h5py" not in imported


@pytest.mark.skipif(not os.path.exists(RESULT_JSON), reason="battery not run in this checkout")
def test_headline_correlation_is_grid_robust():
    """The claim rests on a CORRELATION between two measured quantities, so it must not depend on the
    projection-grid tuning knob. Every grid in the sweep must show it."""
    d = json.load(open(RESULT_JSON))
    assert len(d["grid_sweep"]) == len(GRID_SWEEP)
    for k, v in d["grid_sweep"].items():
        assert v["n_events"] >= 50, (k, v["n_events"])
        assert v["spearman_violation_vs_residual"] > 0.5, (k, v)
        assert v["p_value"] < 1e-6, (k, v)


@pytest.mark.skipif(not os.path.exists(RESULT_JSON), reason="battery not run in this checkout")
def test_one_step_correction_is_not_claimed_out_of_sample_unless_both_directions_pass():
    """The in-sample iteration is grid-sensitive; the cross-family test is the honest bar. The verdict
    must not say 'supported' unless BOTH transfer directions improve at p<0.05."""
    d = json.load(open(RESULT_JSON))
    xs = d["cross_family"]
    both = bool(xs) and all(v["self_consistency_corrected_deg"] < v["pure_curve_deg"]
                            and v["wilcoxon_p"] < 0.05 for v in xs.values())
    claimed = d["verdict"]["one_iteration_improves_out_of_sample"] == "SUPPORTED"
    assert claimed == both, (claimed, xs)


@pytest.mark.skipif(not os.path.exists(RESULT_JSON), reason="battery not run in this checkout")
def test_grid_sensitivity_of_the_iteration_is_disclosed():
    """The in-sample improvement swings with the grid; the verdict text must say so rather than quote
    the most flattering value."""
    d = json.load(open(RESULT_JSON))
    its = [v["median_residual_after_one_iteration_deg"] for v in d["grid_sweep"].values()]
    assert max(its) - min(its) > 0.2, "grid sensitivity vanished; re-check the disclosure"
    assert "grid-sensitive" in d["verdict"]["statement"]
    assert "in-sample" in d["verdict"]["statement"]
