#!/usr/bin/env python3
"""E78 - a posterior-GEOMETRY test of GR: measure the GW inspiral's leading mass-combination exponent.
EXPLORATORY / POST-HOC (developed and run on O4b in one pass; labelled as such per WORKFLOW.md). The
constant-chirp-mass curve m1(q) = Mc (1+q)^(1/5) q^(-3/5) has exponents fixed by the 0PN phase
(phase ~ Mc^(-5/3), Mc = (m1 m2)^(3/5) (m1+m2)^(-1/5)). Generalize to a one-parameter family
Mc_p = (m1 m2)^p (m1+m2)^(1-2p) [GR: p=3/5=0.600] and MEASURE p from the posterior orientation alone.
Orientation is SCALE-FREE: m1(q;p) ~ q^(-p) (1+q)^(2p-1) (the Mc prefactor cancels), so p is isolated
from the mass scale. Deviation from 0.600 would signal modified inspiral phasing (dipole radiation,
varying-G). Successor (preregisterable): the fitted p is reproducible across GWTC-3/O4a/O4b and = 0.600.
Seed 78."""
import os, sys, json, math
import numpy as np
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e65_pn_fisher_rotation import ang_of, adiff
from src.e71_gwtc5_curved_law import psi_axr_rho

GW5 = os.path.join(ROOT, "data/chains/gwtc5")
E71 = os.path.join(ROOT, "results/e71_gwtc5_curved_law_results.json")
GR_P = 0.600

def curve_pts(q, p):
    q = np.clip(q[np.isfinite(q)], 0.02, 1.0)
    m1 = q**(-p) * (1 + q)**(2*p - 1); m2 = q * m1
    return np.column_stack([m1, m2])

def psi_of(P):
    P = P - P.mean(0); _, V = np.linalg.eigh(P.T @ P / len(P)); return ang_of(V[:, 1])

def curve_psi_p(q, p):
    return psi_of(curve_pts(q, p))

def fit_p(q, psi):
    """exponent p whose scale-free level-curve orientation best matches psi_meas (mod 180)."""
    ps = np.linspace(0.30, 0.95, 131); e = [adiff(curve_psi_p(q, p), psi) for p in ps]
    p0 = ps[int(np.argmin(e))]
    ps2 = np.linspace(p0 - 0.02, p0 + 0.02, 81); e2 = [adiff(curve_psi_p(q, p), psi) for p in ps2]
    return float(ps2[int(np.argmin(e2))])

def load_q(event, group):
    with h5py.File(os.path.join(GW5, f"{event}-combined_PEDataRelease.hdf5"), "r") as h:
        return np.asarray(h[group]["posterior_samples"]["mass_ratio"], float)

def main():
    R = json.load(open(E71))
    elong = [r for r in R["per_event"] if r["axr"] >= 3]
    rng = np.random.default_rng(78)

    # per-event fitted exponent from the picked group (uses locked E71 psi_meas)
    fits = []
    for r in elong:
        fits.append({"event": r["event"], "axr": r["axr"], "p_star": fit_p(load_q(r["event"], r["group"]), r["psi_meas"])})
    ps = np.array([f["p_star"] for f in fits])
    boot = np.array([rng.choice(ps, len(ps), replace=True).mean() for _ in range(4000)])
    p_hat, stat = float(ps.mean()), float(boot.std())

    # waveform systematic: catalog-mean p_hat computed independently per waveform family
    WFS = ["C00:SEOBNRv5PHM", "C00:IMRPhenomXPHM-SpinTaylor", "C00:IMRPhenomXPNR", "C00:NRSur7dq4"]
    wf_means = {}
    for wf in WFS:
        pl = []
        for r in elong:
            try:
                with h5py.File(os.path.join(GW5, f"{r['event']}-combined_PEDataRelease.hdf5"), "r") as h:
                    if wf not in h: continue
                    d = h[wf]["posterior_samples"]
                    if any(c not in d.dtype.names for c in ["mass_1_source", "mass_2_source", "mass_ratio"]): continue
                    m1 = np.asarray(d["mass_1_source"], float); m2 = np.asarray(d["mass_2_source"], float)
                    q = np.asarray(d["mass_ratio"], float)
                ok = np.isfinite(m1) & np.isfinite(m2); psi, axr, _ = psi_axr_rho(m1[ok], m2[ok])
                if axr >= 3: pl.append(fit_p(q, psi))
            except Exception: pass
        if pl: wf_means[wf] = float(np.mean(pl))
    wf_syst = (max(wf_means.values()) - min(wf_means.values())) / 2 if len(wf_means) > 1 else float("nan")

    # injection: recover known p from synthetic GR posteriors (curve + perpendicular width -> measured axr)
    def inject(p_true):
        out = []
        for r in elong:
            q = load_q(r["event"], r["group"]); P = curve_pts(q, p_true)
            Pc = P - P.mean(0); _, V = np.linalg.eigh(Pc.T @ Pc / len(Pc)); minor = V[:, 0]
            maj = np.std(Pc @ V[:, 1]); Psim = P + np.outer(rng.normal(0, maj / max(r["axr"], 1e-6), len(P)), minor)
            out.append(fit_p(q, psi_of(Psim)))
        return float(np.mean(out))
    inj = {f"{pt:.2f}": inject(pt) for pt in (0.55, 0.60, 0.65)}
    bias_at_gr = inj["0.60"] - 0.60

    tot = math.sqrt(stat**2 + (wf_syst if wf_syst == wf_syst else 0)**2)
    sigma = abs(p_hat - GR_P) / tot
    print(f"E78 geometric GR exponent (n={len(elong)} elongated O4b events; GR p=0.600)")
    print(f"  p_hat = {p_hat:.3f} +/- {stat:.3f} (stat) +/- {wf_syst:.3f} (waveform syst)")
    print(f"  injection bias at GR = {bias_at_gr:+.4f} (estimator {'UNBIASED' if abs(bias_at_gr)<0.005 else 'BIASED'})")
    print(f"  -> {sigma:.1f} sigma from GR: {'CONSISTENT with GR' if sigma < 3 else 'DEVIATION'}")
    print(f"  waveform-family means: {{{', '.join(f'{k.split(chr(58))[-1]}:{v:.3f}' for k,v in wf_means.items())}}}")
    print(f"  injection recovery: {inj}")

    json.dump({"battery": "E78 geometric GR exponent (EXPLORATORY/post-hoc)",
               "gr_value": GR_P, "n_elong": len(elong),
               "p_hat": p_hat, "stat_err_bootstrap": stat, "waveform_syst": wf_syst,
               "sigma_from_GR": sigma, "consistent_with_GR": bool(sigma < 3),
               "injection_recovery": inj, "estimator_bias_at_GR": bias_at_gr,
               "waveform_family_means": wf_means,
               "successor_prediction": "the fitted exponent is reproducible across GWTC-3/O4a/O4b and = 0.600 "
                                       "(preregisterable when those catalogs are re-scored)",
               "per_event": fits},
              open(os.path.join(ROOT, "results/e78_geometric_gr_exponent_results.json"), "w"), indent=2)
    print("\nwrote results/e78_geometric_gr_exponent_results.json")

if __name__ == "__main__":
    main()
