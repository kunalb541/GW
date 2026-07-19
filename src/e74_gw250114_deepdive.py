#!/usr/bin/env python3
"""E74 - GW250114 deep-dive: the loudest O4b event (network SNR ~80), a near-equal-mass BBH.
NOT a locked-decision battery: O4b TGR/ringdown products are not public, so the ringdown spectroscopy
+ no-hair VERDICT are the PUBLISHED result (Suzuki et al. 2026, arXiv:2605.03576, orthonormal QNMs;
LVK IMR via GWTC-5). This script's INDEPENDENT contribution: from the PE remnant posterior, compute the
Kerr QNM spectrum (the concrete frequencies/damping times the no-hair test confirms) and validate the
characterization against published values. Seed 74 (no RNG). Berti-Cardoso-Will 2006 (gr-qc/0512160)
l=m=2 fitting coefficients."""
import os, sys, json, math
import numpy as np
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FP = os.path.join(ROOT, "data/chains/gwtc5/GW250114_082203-combined_PEDataRelease.hdf5")
MSUN_S = 4.925490947e-6   # G M_sun / c^3 in seconds

# Berti-Cardoso-Will (2006) fits: M*omega_R = f1 + f2 (1-j)^f3 ; Q = q1 + q2 (1-j)^q3   (l=m=2)
BCW = {"220": dict(f1=1.5251, f2=-1.1568, f3=0.1292, q1=0.7000, q2=1.4187, q3=-0.4990),
       "221": dict(f1=1.3673, f2=-1.0260, f3=0.1628, q1=0.1000, q2=0.5436, q3=-0.4731)}

def qnm(Mf_det_msun, j, mode):
    """Kerr QNM observed frequency [Hz] and damping time [s] for detector-frame remnant mass & spin j."""
    c = BCW[mode]; x = np.clip(1.0 - j, 1e-6, 1.0)
    MomegaR = c["f1"] + c["f2"] * x**c["f3"]          # dimensionless M*omega_R
    Q = c["q1"] + c["q2"] * x**c["q3"]
    M_s = Mf_det_msun * MSUN_S
    f = MomegaR / (2 * math.pi * M_s) if np.isscalar(M_s) else MomegaR / (2 * math.pi * M_s)
    tau = Q / (math.pi * f)
    return f, tau

def med_ci(v):
    v = v[np.isfinite(v)]
    return float(np.median(v)), float(np.percentile(v, 5)), float(np.percentile(v, 95))

def main():
    h = h5py.File(FP, "r")
    groups = [k for k in h.keys() if isinstance(h[k], h5py.Group) and "posterior_samples" in h[k]]
    # NRSur7dq4 preferred for remnant (used by the published IMR reference); else any with remnant cols
    pref = [g for g in groups if "NRSur" in g] or [g for g in groups if "final_mass" in h[g]["posterior_samples"].dtype.names]
    g = pref[0]; ds = h[g]["posterior_samples"]
    def col(c): return np.asarray(ds[c], float) if c in ds.dtype.names else None
    m1s, m2s = col("mass_1_source"), col("mass_2_source")
    Mf_det, Mf_src, af = col("final_mass"), col("final_mass_source"), col("final_spin")
    z = col("redshift"); chi_eff = col("chi_eff"); q = col("mass_ratio")
    snr = col("network_optimal_snr");  snr = col("network_matched_filter_snr") if snr is None else snr

    char = {"group": g, "n_samples": len(ds),
            "m1_source": med_ci(m1s), "m2_source": med_ci(m2s), "mass_ratio": med_ci(q),
            "chi_eff": med_ci(chi_eff), "redshift": med_ci(z),
            "network_snr": med_ci(snr) if snr is not None else None,
            "Mf_source": med_ci(Mf_src), "Mf_detector": med_ci(Mf_det), "final_spin_af": med_ci(af)}

    # INDEPENDENT: Kerr QNM spectrum propagated through the remnant posterior (observed / detector frame)
    f220, tau220 = qnm(Mf_det, af, "220")
    f221, tau221 = qnm(Mf_det, af, "221")
    qnm_out = {"f_220_Hz": med_ci(f220), "tau_220_ms": med_ci(tau220 * 1e3),
               "f_221_Hz": med_ci(f221), "tau_221_ms": med_ci(tau221 * 1e3),
               "note": "Kerr (no-hair) prediction from (Mf_det, af); the published ringdown measures these "
                       "and finds df221,dgamma221 ~ 0 (no deviation); 221 overtone detected at 99.9%."}

    # published-value validation (Suzuki 2026 / GWTC-5 IMR ref)
    pub = {"m1_source": (33.6, 32.8, 34.8), "m2_source": (32.2, 30.9, 33.0),
           "Mf_source": (62.7, 61.6, 63.7), "af": (0.68, 0.67, 0.69), "snr": 80}
    def close(a, b, tol): return abs(a - b) <= tol
    valid = {"m1_match": close(char["m1_source"][0], pub["m1_source"][0], 0.6),
             "m2_match": close(char["m2_source"][0], pub["m2_source"][0], 0.6),
             "Mf_match": close(char["Mf_source"][0], pub["Mf_source"][0], 0.6),
             "af_match": close(char["final_spin_af"][0], pub["af"][0], 0.02)}

    # reference cross-check: GW150914-like remnant (Mf_det~68, af~0.68) -> f220~250 Hz, tau220~4 ms
    ref_f, ref_tau = qnm(68.0, 0.68, "220")

    print(f"GW250114 [{g}], n={len(ds)}, loudest O4b (network SNR ~{char['network_snr'][0]:.0f})")
    print(f"  m1={char['m1_source'][0]:.1f} m2={char['m2_source'][0]:.1f} Msun (q={char['mass_ratio'][0]:.2f}), "
          f"chi_eff={char['chi_eff'][0]:.2f}, z={char['redshift'][0]:.2f}")
    print(f"  remnant Mf_src={char['Mf_source'][0]:.1f} Msun, af={char['final_spin_af'][0]:.3f} "
          f"(Mf_det={char['Mf_detector'][0]:.1f})")
    print(f"  published-value validation vs Suzuki2026/GWTC-5 IMR: {valid}")
    print(f"\nIndependent Kerr QNM spectrum (observed frame) from the remnant posterior:")
    print(f"  (2,2,0): f = {qnm_out['f_220_Hz'][0]:.1f} Hz  (90% {qnm_out['f_220_Hz'][1]:.1f}-{qnm_out['f_220_Hz'][2]:.1f}),"
          f"  tau = {qnm_out['tau_220_ms'][0]:.2f} ms")
    print(f"  (2,2,1): f = {qnm_out['f_221_Hz'][0]:.1f} Hz  (90% {qnm_out['f_221_Hz'][1]:.1f}-{qnm_out['f_221_Hz'][2]:.1f}),"
          f"  tau = {qnm_out['tau_221_ms'][0]:.2f} ms")
    print(f"  ref check (Mf_det=68, af=0.68): f220={ref_f:.1f} Hz, tau220={ref_tau*1e3:.2f} ms "
          f"(GW150914-like ~251 Hz/4 ms -> GW250114 is a louder near-twin remnant)")

    json.dump({"event": "GW250114_082203", "role": "loudest O4b event (deep-dive; not a locked battery)",
               "published_refs": {"ringdown": "Suzuki et al. 2026 arXiv:2605.03576 (orthonormal QNMs)",
                                  "imr": "GWTC-5 / ref [15] therein"},
               "published_ringdown_result": {"overtone_221_significance": "99.9% (orthonormal) vs 82.5% (nonorthogonal)",
                                             "kerr_deviation": "df221, dgamma221 consistent with 0 (no-hair upheld)"},
               "characterization": char, "kerr_qnm_prediction": qnm_out,
               "published_value_validation": valid,
               "ref_check_GW150914like": {"f220_Hz": ref_f, "tau220_ms": ref_tau * 1e3},
               "curved_law_note": "near-equal-mass (q~0.95) -> near-round posterior (axr~2) -> geometry-law "
                                  "orientation weakly defined; correctly outside the E71 axr>=3 elongated set."},
              open(os.path.join(ROOT, "results/e74_gw250114_deepdive_results.json"), "w"), indent=2)
    print("\nwrote results/e74_gw250114_deepdive_results.json")
    h.close()

if __name__ == "__main__":
    main()
