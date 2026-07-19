"""E73 contract tests - guard the information-anatomy + dipole-Fisher machinery. Data-free."""
import math
from src.e73_information_anatomy import anatomy, sigma_beta

def test_anatomy_ordering_Mc_eta_chi():
    a = anatomy(10.0, 10.0)
    assert a["Mc"][0] < a["eta"][0] < a["chi"][0]        # Mc learned earliest, spin latest
    assert a["Mc"][1] < a["chi"][1]                       # holds at f90 too

def test_frequency_scales_inverse_total_mass():
    light = anatomy(5.0, 5.0); heavy = anatomy(50.0, 50.0)
    assert heavy["f_isco"] < light["f_isco"]             # f_isco ~ 1/M
    assert heavy["Mc"][0] < light["Mc"][0]               # heavier -> everything at lower f

def test_sigma_beta_scales_inverse_snr():
    s15 = sigma_beta(10.0, 10.0, rho=15.0); s30 = sigma_beta(10.0, 10.0, rho=30.0)
    assert abs(s30 - s15 / 2) / s15 < 1e-6               # Fisher error ~ 1/rho

def test_lighter_binary_gives_tighter_dipole_bound():
    # longer inspiral (lighter) -> more low-frequency cycles -> better dipole (-1PN) sensitivity
    assert sigma_beta(3.0, 3.0) < sigma_beta(40.0, 40.0)

def test_sigma_beta_positive_finite():
    s = sigma_beta(20.0, 12.0)
    assert math.isfinite(s) and s > 0
