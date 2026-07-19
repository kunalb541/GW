"""E74 contract tests - guard the Kerr QNM machinery (Berti-Cardoso-Will l=m=2 fits).
Data-free. Validated against the well-established GW150914-like ringdown (Mf_det~68 Msun, af~0.68
-> f220 ~ 250 Hz, tau220 ~ 4 ms)."""
import math
from src.e74_gw250114_deepdive import qnm

def test_gw150914_like_reference():
    # canonical: Mf_det=68 Msun, af=0.68 -> f_220 ~ 250 Hz, tau_220 ~ 4 ms
    f, tau = qnm(68.0, 0.68, "220")
    assert 240 < f < 262, f
    assert 3.6e-3 < tau < 4.4e-3, tau

def test_frequency_scales_inverse_mass():
    f1, _ = qnm(68.0, 0.68, "220")
    f2, _ = qnm(136.0, 0.68, "220")
    assert abs(f2 - f1 / 2) / f1 < 1e-6   # f proportional to 1/M

def test_frequency_increases_with_spin():
    lo, _ = qnm(68.0, 0.30, "220")
    hi, _ = qnm(68.0, 0.90, "220")
    assert hi > lo                        # QNM frequency rises with remnant spin

def test_overtone_damps_faster_than_fundamental():
    _, tau220 = qnm(68.0, 0.68, "220")
    _, tau221 = qnm(68.0, 0.68, "221")
    assert tau221 < tau220                # first overtone decays faster (lower Q)
