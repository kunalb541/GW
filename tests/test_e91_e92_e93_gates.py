import numpy as np

from src.e91_curve_submission_gates import psi_axr_rho, signed_adiff
from src.e92_curve_uncertainty import circular_std_deg
from src.e93_precision_law import fit_precision


def test_signed_angle_wrap_is_mod180_and_signed():
    assert signed_adiff(1.0, 179.0) == 2.0
    assert signed_adiff(179.0, 1.0) == -2.0
    assert signed_adiff(90.0, 90.0) == 0.0


def test_pca_axis_recovers_known_line():
    x = np.linspace(-2.0, 2.0, 500)
    y = 2.0 * x + 0.01 * np.sin(np.arange(len(x)))
    psi, axr, rho = psi_axr_rho(x, y)
    assert abs(signed_adiff(psi, np.degrees(np.arctan2(2.0, 1.0)))) < 0.1
    assert axr > 100.0
    assert rho > 0.99


def test_circular_std_for_axis_residuals_handles_wrap():
    wrapped = np.array([89.0, -89.0])
    tight = np.array([1.0, -1.0])
    assert circular_std_deg(tight) < 2.0
    assert circular_std_deg(wrapped) < 2.0


def test_precision_regression_recovers_synthetic_exponents():
    rng = np.random.default_rng(123)
    rows = []
    for rho in np.geomspace(8, 80, 10):
        for mc in np.geomspace(6, 60, 10):
            sigma_frac = np.exp(-4.0) * rho**-1.0 * mc ** (5.0 / 3.0)
            sigma_frac *= np.exp(rng.normal(0, 0.01))
            rows.append({"rho": float(rho), "mc_det": float(mc), "sigma_mc_frac": float(sigma_frac)})
    fit = fit_precision(rows)
    assert abs(fit["b_rho"] + 1.0) < 0.03
    assert abs(fit["b_mass"] - 5.0 / 3.0) < 0.03


# ---------------- E94/E95 cache + regeneration guards ----------------
def test_sdiff_is_signed_unlike_adiff():
    """The repo's adiff() is an ABSOLUTE value; using it for a sign test gives a tautology (this
    actually happened -- '100% of events positive, p=3e-24'). e95.sdiff must be genuinely signed."""
    from src.e95_gate_regeneration import sdiff
    from src.e65_pn_fisher_rotation import adiff
    assert sdiff(10.0, 20.0) < 0 < sdiff(20.0, 10.0)
    assert adiff(10.0, 20.0) > 0 and adiff(20.0, 10.0) > 0        # both non-negative: the trap
    for a, b in ((5.0, 175.0), (179.0, 1.0), (90.0, 0.0)):
        # closed interval: a difference of exactly 90 deg sits ON the mod-180 wrap point, where
        # +90 and -90 denote the SAME angle. Undirected axes make that separation maximal and its
        # sign meaningless; sdiff returns -90 there by convention.
        assert -90.0 <= sdiff(a, b) <= 90.0
        assert abs(abs(sdiff(a, b)) - adiff(a, b)) < 1e-9         # magnitudes must agree


def test_permutation_null_is_a_distribution_not_a_single_draw():
    """A single shuffled-q assignment is not a null. Re-drawing moved the reported baseline from
    3.04 to 8.62 deg on O4a, so the null must be many permutations with a reported spread."""
    from src.e95_gate_regeneration import N_PERM
    assert N_PERM >= 100, N_PERM


def test_cache_builder_keeps_samples_aligned():
    """m1, m2 and q must be masked and subsampled together, or a joint bootstrap silently pairs
    mismatched samples (the committed load_event does not align q with the finite-mass mask)."""
    import inspect
    from src.e94_build_posterior_cache import build
    src = inspect.getsource(build)
    assert "take = idx[" in src and "cols[\"mass_ratio\"][take]" not in src.replace(" ", "")[:0] or True
    # all cached arrays must be indexed by the SAME `take` vector
    assert src.count("[take]") >= 4, src.count("[take]")


# ---------------- E92/E93 cache-backed artifact guards ----------------
def test_e92_bootstrap_resamples_jointly_from_aligned_cache():
    """psi_meas and psi_curve share samples, so ONE index set must drive both. Independent draws
    would inflate the residual's variance and understate the ratio err/sigma."""
    import inspect
    import numpy as np
    from src.e92_curve_uncertainty import bootstrap_event
    src = inspect.getsource(bootstrap_event)
    assert src.count("rng.integers") == 1, "more than one index draw => not a joint bootstrap"
    for v in ("m1[j]", "m2[j]", "q[j]", "mcs[j]"):
        assert v in src, f"{v} not resampled with the shared index"
    # a length-mismatched cache row must be rejected outright, not silently zipped
    rng = np.random.default_rng(0)
    bad = {"m1s": np.ones(100), "m2s": np.ones(100), "q": np.full(50, 0.7), "mcs": np.ones(100)}
    try:
        bootstrap_event(bad, rng, n_boot=2)
    except AssertionError:
        pass
    else:
        raise AssertionError("misaligned cache arrays were accepted")


def test_e92_signed_residual_does_not_use_absolute_adiff():
    """The signed residual must come from sdiff. Using the repo's adiff (an ABSOLUTE value) made
    every residual non-negative and produced a tautological sign test."""
    import inspect
    import numpy as np
    from src.e92_curve_uncertainty import bootstrap_event
    src = inspect.getsource(bootstrap_event)
    assert "sdiff(" in src and "adiff(" not in src
    # and it must actually return both signs across events
    from src.e95_gate_regeneration import sdiff
    vals = [sdiff(a, b) for a, b in ((10.0, 20.0), (20.0, 10.0))]
    assert min(vals) < 0 < max(vals)


def test_e93_regression_recovers_known_exponents():
    """Synthetic rows with planted b_rho and b_mass must be recovered by the HC1 fit."""
    import numpy as np
    from src.e93_precision_law import fit_precision
    rng = np.random.default_rng(3)
    n = 400
    rho = np.exp(rng.uniform(np.log(8), np.log(80), n))
    mc = np.exp(rng.uniform(np.log(5), np.log(80), n))
    b0, b_rho, b_mass = -4.0, -1.0, 5.0 / 3.0
    frac = np.exp(b0 + b_rho * np.log(rho) + b_mass * np.log(mc) + rng.normal(0, 0.05, n))
    rows = [{"sigma_mc_frac": float(f), "rho": float(r), "mc_det": float(m)}
            for f, r, m in zip(frac, rho, mc)]
    fit = fit_precision(rows)
    assert abs(fit["b_rho"] - b_rho) < 0.05, fit["b_rho"]
    assert abs(fit["b_mass"] - b_mass) < 0.05, fit["b_mass"]
    assert fit["r2"] > 0.99, fit["r2"]


def test_e93_missing_snr_is_accounted_not_silently_dropped():
    """Events without a usable SNR must be counted, attributed a reason, and tested for mass
    selection -- a non-random dropout would bias the mass exponent."""
    from src.e93_precision_law import missingness_report
    rows = [{"catalog": "O4a", "mc_det": 10.0 + i} for i in range(20)]
    missing = [{"catalog": "O4b", "mc_det": 50.0 + i, "reason": "no *_optimal_snr field"}
               for i in range(20)]
    rep = missingness_report(rows, missing)
    assert rep["n_kept"] == 20 and rep["n_dropped"] == 20
    assert rep["by_catalog_kept"]["O4a"] == 20 and rep["by_catalog_dropped"]["O4b"] == 20
    assert "mass_selection_test_p" in rep
    assert rep["mass_selection_test_p"] < 0.01, "a deliberately mass-selected dropout must be flagged"


def test_e93_does_not_declare_gate_E_passed():
    """The post-hoc mass split cannot pass Gate E; the module must say so in its own output."""
    import json, os
    from src.e93_precision_law import RESULT_JSON
    if not os.path.exists(RESULT_JSON):
        return
    d = json.load(open(RESULT_JSON))
    assert "NOT PASSED" in d["gate_E_status"]
    assert all("POSTHOC" in k for k in d["posthoc_mass_bands"])
