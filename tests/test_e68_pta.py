"""Contract tests for E68 (PTA GWB anatomy machinery)."""
import numpy as np
import math
from numpy.linalg import eigh
from src.e68_pta_gwb_anatomy import moments, pair, rho_of, psi_of


def _gauss(mu, C, n=20000, seed=0):
    return np.random.default_rng(seed).multivariate_normal(mu, C, n)


C_PTA = np.array([[0.04, -0.045], [-0.045, 0.16]])   # A-gamma-like anticorrelated


def test_self_pair_no_tension_and_faithful():
    XA = _gauss([-14.2, 3.2], C_PTA, seed=1); XB = _gauss([-14.2, 3.2], C_PTA, seed=2)
    r = pair(XA, XB, *moments(XA), *moments(XB))
    assert r["sigma"] < 0.1
    assert r["gauss_faithful"]


def test_offset_along_degeneracy_projects_to_one():
    mu, C = np.array([-14.2, 3.2]), C_PTA
    w, V = eigh(C); u = V[:, np.argmax(w)]          # degeneracy direction
    d = 0.5 * u                                      # offset purely along it
    frac = float((d @ u) ** 2 / (d @ d))
    assert abs(frac - 1.0) < 1e-12
    d_perp = 0.5 * V[:, np.argmin(w)]
    frac_perp = float((d_perp @ u) ** 2 / (d_perp @ d_perp))
    assert frac_perp < 1e-12


def test_rho_and_psi_conventions():
    assert rho_of(C_PTA) < -0.5                      # anticorrelated
    psi = psi_of(C_PTA)
    assert 90 < psi < 180                            # negative-correlation long axis


def test_pure_mean_shift_is_value_dominated():
    XA = _gauss([-14.2, 3.2], C_PTA, seed=1); XB = _gauss([-13.9, 2.7], C_PTA, seed=2)
    r = pair(XA, XB, *moments(XA), *moments(XB))
    assert r["vf_orientation_only"] > 0.9
    assert r["delta_rho"] < 0.05
