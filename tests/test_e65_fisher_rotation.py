"""Contract tests for E65 (PN-Fisher rotation + curved-law machinery).

Guard the geometry, not the physics verdict: kappa limits must reproduce the two tangents,
angle helpers must respect mod-180 conventions, and the Fisher weights must be positive and
mass-ordered the right way (heavier -> relatively more merger information).
"""
import numpy as np
from src import e65_pn_fisher_rotation as e


def test_kappa_limits_recover_tangents():
    m1, m2 = 20.0, 10.0
    M = m1 + m2
    # kappa -> 0: long axis = constant-Mc tangent (perpendicular to grad Mc)
    g_c = np.array([0.6 / m1 - 0.2 / M, 0.6 / m2 - 0.2 / M])
    tang_c = e.ang_of(np.array([-g_c[1], g_c[0]]))
    assert e.adiff(e.psi_pred(m1, m2, 1.0, 1.0, 1e-12), tang_c) < 0.1
    # kappa -> inf: long axis = constant-Mtot tangent = 135 deg
    assert e.adiff(e.psi_pred(m1, m2, 1.0, 1.0, 1e12), 135.0) < 0.1


def test_adiff_mod180():
    assert e.adiff(179.0, 1.0) == 2.0
    assert e.adiff(90.0, 90.0) == 0.0
    assert abs(e.adiff(10.0, 100.0) - 90.0) < 1e-12


def test_between_frac():
    fr, ok = e.between_frac(140.0, 150.0, 130.0)   # halfway on the shortest arc
    assert ok and abs(fr - 0.5) < 1e-9
    fr, ok = e.between_frac(160.0, 150.0, 130.0)   # beyond chirp, away from total
    assert (not ok) and fr < 0


def test_weights_positive_and_mass_trend():
    Wc1, Wt1 = e.weights(10.0, 25.0)     # light: inspiral-dominated
    Wc2, Wt2 = e.weights(40.0, 100.0)    # heavy: merger matters more
    assert Wc1 > 0 and Wt1 > 0 and Wc2 > 0 and Wt2 > 0
    assert (Wt2 / Wc2) > (Wt1 / Wc1)     # heavier -> relatively more merger information


def test_curve_chord_rotates_with_arc_length():
    # points on a constant-Mc curve: longer arc (wider q range) -> chord rotates away
    # from the median tangent; short arc -> chord ~ tangent.
    mc = 15.0
    def psi_arc(qlo, qhi):
        qs = np.linspace(qlo, qhi, 500)
        m1 = mc * (1 + qs) ** 0.2 * qs ** -0.6
        m2 = qs * m1
        P = np.column_stack([m1, m2]); P = P - P.mean(0)
        _, V = np.linalg.eigh(P.T @ P / len(P))
        return e.ang_of(V[:, 1])
    qmid = 0.7
    m1 = mc * (1 + qmid) ** 0.2 * qmid ** -0.6; m2 = qmid * m1; M = m1 + m2
    g_c = np.array([0.6 / m1 - 0.2 / M, 0.6 / m2 - 0.2 / M])
    tang = e.ang_of(np.array([-g_c[1], g_c[0]]))
    d_short = e.adiff(psi_arc(0.68, 0.72), tang)
    d_long = e.adiff(psi_arc(0.2, 1.0), tang)
    assert d_short < 0.5                  # short arc: chord == tangent
    assert d_long > 2.0 * max(d_short, 0.05)   # long arc: real rotation
