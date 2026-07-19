"""E82 contract tests - guard the inference-manifold machinery (Bures closed form, MDS). Data-free."""
import numpy as np
from scipy.linalg import sqrtm
from src.e82_inference_manifold import bures2, classical_mds

RNG = np.random.default_rng(82)

def _spd():
    A = RNG.normal(size=(2, 2)); return A @ A.T + 0.5 * np.eye(2)

def test_bures_closed_form_matches_sqrtm():
    for _ in range(50):
        Si, Sj = _spd(), _spd()
        s = sqrtm(Si); inner = sqrtm(s @ Sj @ s)
        ref = np.trace(Si) + np.trace(Sj) - 2 * np.real(np.trace(inner))
        assert abs(bures2(Si, Sj) - ref) < 1e-8, (bures2(Si, Sj), ref)

def test_bures_self_is_zero():
    for _ in range(20):
        S = _spd(); assert bures2(S, S) < 1e-9

def test_mds_recovers_true_dimensionality():
    # points genuinely in a 2D plane embedded in higher-D distance space -> 2 dominant MDS eigenvalues
    P = RNG.normal(size=(40, 2))
    D2 = ((P[:, None, :] - P[None, :, :]) ** 2).sum(-1)
    w, Y = classical_mds(D2)
    assert w[0] > 0 and w[1] > 0
    assert w[2] / w[0] < 1e-6            # third dimension is empty

def test_mds_1d_line():
    # points on a line -> a single dominant MDS eigenvalue
    x = np.linspace(0, 1, 30); D2 = (x[:, None] - x[None, :]) ** 2
    w, _ = classical_mds(D2)
    assert w[1] / w[0] < 1e-6
