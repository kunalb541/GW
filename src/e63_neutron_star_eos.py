#!/usr/bin/env python3
"""E63 - value/shape geometry of the neutron-star mass-radius tension (first cross-domain transfer).
Prereg E63. Probes in (M[Msun], R[km]): NICER pulse-profile (J0030 Riley19/Miller-2spot/Miller-3spot;
J0740 Riley21/Miller21) + GW170817 tidal mapped via C-Love. Reuses src/qinfo.py. Seed 63."""
import os, sys, json, math, glob
import numpy as np
from numpy.linalg import inv, det, eigh
from scipy.linalg import sqrtm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src import qinfo as Q

NS = os.path.join(ROOT, "data/nseos")
SEED = 63

# ---------- geometry helpers (copied from e48 to stay import-side-effect-free) ----------
def moments(X, w=None):
    X = np.asarray(X, float)
    if w is None: w = np.ones(len(X))
    w = w / w.sum()
    mu = (X * w[:, None]).sum(0)
    Xc = X - mu
    C = (Xc * w[:, None]).T @ Xc
    return mu, C

def bures2(A, B):
    sA = sqrtm(A); inner = sqrtm(sA @ B @ sA)
    return max(float(np.trace(A + B - 2 * inner).real), 0.0)

def unit_det(C): return C / math.sqrt(det(C))
def corr(C):
    d = np.sqrt(np.diag(C)); return C / np.outer(d, d)
def axis_ratio(C):
    ev = np.linalg.eigvalsh(C); return math.sqrt(ev[-1] / ev[0])
def rho_corr(C):
    d = np.sqrt(np.diag(C)); return float(C[0, 1] / (d[0] * d[1]))
def psi_whitened_gap(CA, CB):
    """scale-free orientation gap: principal-axis angle difference in the joint-whitened frame."""
    Mj = inv(sqrtm(0.5 * (CA + CB))).real
    a = psi_long_axis(Mj @ CA @ Mj.T); b = psi_long_axis(Mj @ CB @ Mj.T)
    return abs((a - b + 90) % 180 - 90)
def psi_long_axis(C):
    w, V = eigh(C); v = V[:, np.argmax(w)]
    return math.degrees(math.atan2(v[1], v[0])) % 180.0

def whiten_vf(muA, CA, muB, CB, Cref):
    M = inv(sqrtm(Cref)).real
    dv = M @ (muA - muB); value = float(dv @ dv)
    CAp = M @ CA @ M.T; CBp = M @ CB @ M.T
    shape = bures2(CAp, CBp)
    return value, shape, (value / (value + shape) if value + shape > 0 else float("nan")), CAp, CBp

def sliced_w(XA, XB, wA=None, wB=None, nproj=200, seed=SEED):
    rng = np.random.default_rng(seed)
    if wA is None: wA = np.ones(len(XA))
    if wB is None: wB = np.ones(len(XB))
    tot = 0.0
    for _ in range(nproj):
        th = rng.uniform(0, math.pi); u = np.array([math.cos(th), math.sin(th)])
        a = XA @ u; b = XB @ u
        qs = np.linspace(0.005, 0.995, 200)
        oa = np.argsort(a); ob = np.argsort(b)
        ca = np.cumsum(wA[oa]); cb = np.cumsum(wB[ob])
        qa = np.interp(qs, ca / ca[-1], a[oa]); qb = np.interp(qs, cb / cb[-1], b[ob])
        tot += np.mean((qa - qb) ** 2)
    return tot / nproj

def raw_value_shape(muA, CA, muB, CB):
    """Raw (unscaled) W2 value/shape in native (M,R) units."""
    value = float((muA - muB) @ (muA - muB)); shape = bures2(CA, CB)
    return value, shape, value / (value + shape) if value + shape > 0 else float("nan")

# ---------- loaders: return (label, mu, C, X, star, kind) all in (M[Msun], R[km]) ----------
def _clean(a):
    a = np.asarray(a, float); return a[np.all(np.isfinite(a), axis=1)]

def load_miller_RM(path, label, star):
    d = np.loadtxt(path)                     # col0 = R[km], col1 = M[Msun]
    X = _clean(np.column_stack([d[:, 1], d[:, 0]]))   # -> (M, R)
    mu, C = moments(X)
    return dict(label=label, star=star, kind="xray", mu=mu, C=C, X=X)

def load_riley_J0740(path, label="Riley2021 (X-PSI STU)"):
    d = np.loadtxt(path)                     # col0 = M[Msun], col1 = R[km]
    X = _clean(d[:, :2])
    mu, C = moments(X)
    return dict(label=label, star="J0740", kind="xray", mu=mu, C=C, X=X)

def load_riley_J0030(path, label="Riley2019 (X-PSI ST+PST)"):
    """ST+PST post_equal_weights cols verified: col0=M[Msun], col1=R[km] (=orig cols 1,2;
    M̄=1.336±0.146, R̄=12.70±1.12 match published 1.34±0.16, 12.71±1.17)."""
    d = np.loadtxt(path)
    X = _clean(d[:, :2])
    assert 1.0 < X[:, 0].mean() < 1.7 and 11 < X[:, 1].mean() < 14, "Riley J0030 column check failed"
    mu, C = moments(X)
    return dict(label=label, star="J0030", kind="xray", mu=mu, C=C, X=X)

def load_gw170817(path, z=0.0099, label="GW170817 (tidal->C-Love)"):
    import h5py
    f = h5py.File(path, "r")
    p = f["IMRPhenomPv2NRT_lowSpin_posterior"][:]
    m1 = p["m1_detector_frame_Msun"] / (1 + z); m2 = p["m2_detector_frame_Msun"] / (1 + z)
    l1 = p["lambda1"]; l2 = p["lambda2"]
    def clove_R(m, lam):
        lam = np.asarray(lam, float); ok = lam > 0
        C = np.full_like(lam, np.nan)
        ll = np.log(lam[ok])
        C[ok] = 0.360 - 0.0355 * ll + 0.000705 * ll ** 2
        return 1.4766 * m / C                 # R[km] = (GMsun/c^2)*(M/Msun)/C
    R1 = clove_R(m1, l1); R2 = clove_R(m2, l2)
    X = _clean(np.vstack([np.column_stack([m1, R1]), np.column_stack([m2, R2])]))
    mu, C = moments(X)
    return dict(label=label, star="GW170817", kind="gw", mu=mu, C=C, X=X)

# ---------- build probe set ----------
def build_probes():
    P = []
    P.append(load_riley_J0030(os.path.join(NS, "J0030/Riley2019_J0030_MR.txt")))
    P.append(load_miller_RM(os.path.join(NS, "J0030/Miller2019_J0030_2spot_RM.txt"),
                            "Miller2019 2-oval (2spot)", "J0030"))
    P.append(load_miller_RM(os.path.join(NS, "J0030/Miller2019_J0030_3spot_RM.txt"),
                            "Miller2019 3-oval (3spot)", "J0030"))
    P.append(load_riley_J0740(os.path.join(NS, "J0740/Riley2021_J0740_MR.txt")))
    P.append(load_miller_RM(os.path.join(NS, "J0740/Miller2021_NICERXMM_J0740_RM.txt"),
                            "Miller2021 (NICER+XMM)", "J0740"))
    P.append(load_gw170817(os.path.join(NS, "gw170817/GW170817_GWTC-1.hdf5")))
    return P

def summ(pr):
    m, r = pr["mu"]; sm = math.sqrt(pr["C"][0, 0]); sr = math.sqrt(pr["C"][1, 1])
    return f"M={m:.3f}+/-{sm:.3f}  R={r:.2f}+/-{sr:.2f}  psi={psi_long_axis(pr['C']):.1f}deg  ar={axis_ratio(pr['C']):.2f}  N={len(pr['X'])}"

def pair_analysis(A, B):
    muA, CA, muB, CB = A["mu"], A["C"], B["mu"], B["C"]
    vr, sr, vfr = raw_value_shape(muA, CA, muB, CB)
    _, _, vf_joint, _, _ = whiten_vf(muA, CA, muB, CB, 0.5 * (CA + CB))
    # orientation-only: unit-determinant covariances in joint-whitened frame
    Mj = inv(sqrtm(0.5 * (CA + CB))).real
    CAj = unit_det(Mj @ CA @ Mj.T); CBj = unit_det(Mj @ CB @ Mj.T)
    valj = float((Mj @ (muA - muB)) @ (Mj @ (muA - muB)))
    shape_orient = bures2(CAj, CBj)
    vf_orient = valj / (valj + shape_orient) if valj + shape_orient > 0 else float("nan")
    psi_gap = psi_whitened_gap(CA, CB)           # SCALE-FREE orientation gap (joint-whitened)
    drho = abs(rho_corr(CA) - rho_corr(CB))      # scale-free correlation difference
    # significance (joint covariance)
    sig = math.sqrt((muA - muB) @ inv(0.5 * (CA + CB)) @ (muA - muB))
    # non-Gaussianity gate (D2): empirical vs gaussian-resampled sliced-W2^2
    rng = np.random.default_rng(SEED)
    nA, nB = min(len(A["X"]), 20000), min(len(B["X"]), 20000)
    iA = rng.choice(len(A["X"]), nA, replace=False); iB = rng.choice(len(B["X"]), nB, replace=False)
    emp = sliced_w(A["X"][iA], B["X"][iB])
    GA = rng.multivariate_normal(muA, CA, nA); GB = rng.multivariate_normal(muB, CB, nB)
    gau = sliced_w(GA, GB)
    faithful_ratio = emp / gau if gau > 0 else float("nan")
    # precision/volume ratio (scale-free area ratio of 1-sigma ellipses)
    vol_ratio = math.sqrt(det(CB) / det(CA))
    # classification on scale-free descriptors: value (mean-offset) vs orientation (delta-rho)
    if drho > 0.30 and vf_orient < 0.5: cls = "orientation-dominated"
    elif vf_orient > 0.70 and drho < 0.15: cls = "value-dominated"
    else: cls = "mixed (value+orientation)"
    return dict(sigma=round(sig, 2), value_raw=round(vr, 4), shape_raw=round(sr, 4),
                vf_raw=round(vfr, 3), vf_joint_whitened=round(vf_joint, 3),
                vf_orientation_only=round(vf_orient, 3),
                delta_rho=round(drho, 3), rho_A=round(rho_corr(CA), 3), rho_B=round(rho_corr(CB), 3),
                vol_ratio_B_over_A=round(vol_ratio, 2),
                sliced_emp=round(emp, 4), sliced_gauss=round(gau, 4),
                nongauss_ratio=round(faithful_ratio, 3),
                gauss_faithful=bool(abs(faithful_ratio - 1) <= 0.30), classification=cls)

def main():
    P = build_probes()
    print("=== E63 probes in (M[Msun], R[km]) ===")
    for pr in P: print(f"  {pr['label']:34s} [{pr['star']:8s}/{pr['kind']:4s}] {summ(pr)}")

    out = {"prereg": "preregs/E63_neutron_star_eos_prereg.md",
           "probes": {pr["label"]: {"star": pr["star"], "kind": pr["kind"],
                                    "M": round(float(pr["mu"][0]), 3), "R": round(float(pr["mu"][1]), 2),
                                    "sigma_M": round(float(math.sqrt(pr["C"][0, 0])), 3),
                                    "sigma_R": round(float(math.sqrt(pr["C"][1, 1])), 2),
                                    "rho_MR": round(rho_corr(pr["C"]), 3),
                                    "axis_ratio": round(axis_ratio(pr["C"]), 2),
                                    "N": len(pr["X"])} for pr in P}}
    byname = {pr["label"]: pr for pr in P}

    # ---- D1: analysis-dependence (same star, different pipeline/model) ----
    print("\n=== D1 analysis-dependence (same star, different pipeline/model) ===")
    D1_pairs = [("Riley2019 (X-PSI ST+PST)", "Miller2019 2-oval (2spot)"),
                ("Riley2019 (X-PSI ST+PST)", "Miller2019 3-oval (3spot)"),
                ("Miller2019 2-oval (2spot)", "Miller2019 3-oval (3spot)"),
                ("Riley2021 (X-PSI STU)", "Miller2021 (NICER+XMM)")]
    out["D1_analysis_dependence"] = {}
    for a, b in D1_pairs:
        r = pair_analysis(byname[a], byname[b]); out["D1_analysis_dependence"][f"{a} | {b}"] = r
        print(f"  {a.split('(')[0].strip():18s} vs {b.split('(')[0].strip():22s} "
              f"sig={r['sigma']:.2f} vf_orient={r['vf_orientation_only']:.2f} dRho={r['delta_rho']:.2f} "
              f"volB/A={r['vol_ratio_B_over_A']:.2f} nonG={r['nongauss_ratio']:.2f} -> {r['classification']}")

    # ---- D3: measurement-kernel orientation via scale-free rho(M,R) ----
    # (M,R) has incommensurate units -> no metric-free orientation ANGLE; rho is the invariant.
    print("\n=== D3 measurement-kernel orientation (scale-free rho(M,R)) ===")
    gw = [pr for pr in P if pr["kind"] == "gw"][0]
    lowM = [pr for pr in P if pr["star"] == "J0030"]           # M~1.4 X-ray
    highM = [pr for pr in P if pr["star"] == "J0740"]          # M~2.08 X-ray
    rho_low = float(np.mean([rho_corr(pr["C"]) for pr in lowM]))
    rho_high = float(np.mean([rho_corr(pr["C"]) for pr in highM]))
    out["D3_orientation"] = {
        "rho_by_probe": {pr["label"]: round(rho_corr(pr["C"]), 3) for pr in P},
        "mean_rho_J0030_lowmass_xray": round(rho_low, 3),
        "mean_rho_J0740_highmass_xray": round(rho_high, 3),
        "rho_gw170817": round(rho_corr(gw["C"]), 3),
        "mass_regime_split_dRho": round(abs(rho_low - rho_high), 3),
        "note": "rho(M,R) is organized by mass regime (steep low-mass banana vs flat high-mass top), "
                "consistent across pipelines. GW170817 rho is mapping-induced (C-Love), flagged."}
    for pr in P: print(f"  {pr['label']:34s} rho(M,R)={rho_corr(pr['C']):+.3f}")
    print(f"  -> J0030(low-M) mean rho={rho_low:+.3f} ; J0740(high-M) mean rho={rho_high:+.3f} ; "
          f"regime dRho={abs(rho_low-rho_high):.2f} ; GW170817 rho={rho_corr(gw['C']):+.3f} (mapping-induced)")

    # ---- D4: cross-messenger value/shape at ~1.4 (J0030 xray vs GW170817) ----
    print("\n=== D4 cross-messenger (J0030 NICER vs GW170817-derived) ===")
    out["D4_cross_messenger"] = {}
    for a in ["Miller2019 3-oval (3spot)", "Riley2019 (X-PSI ST+PST)"]:
        r = pair_analysis(byname[a], gw); out["D4_cross_messenger"][f"{a} | GW170817"] = r
        print(f"  {a.split('(')[0].strip():20s} vs GW170817  sig={r['sigma']:.2f} vf_orient={r['vf_orientation_only']:.2f} "
              f"dRho={r['delta_rho']:.2f} (rho {r['rho_A']:+.2f}->{r['rho_B']:+.2f}) -> {r['classification']}")

    # ---- D5: QI shape figures of merit ----
    print("\n=== D5 QI shape figures of merit (rho=C/TrC) ===")
    out["D5_qinfo"] = {"per_probe": {}, "pairwise": {}}
    for pr in P:
        rho = Q.density(pr["C"])
        out["D5_qinfo"]["per_probe"][pr["label"]] = {"purity": round(Q.purity(rho), 4),
                                                     "vn_entropy": round(Q.vn_entropy(rho), 4)}
        print(f"  {pr['label']:34s} purity={Q.purity(rho):.3f} vN={Q.vn_entropy(rho):.3f}")
    # pairwise quantum(shape) vs classical(value+shape) for the headline pairs
    hp = D1_pairs + [("Miller2019 3-oval (3spot)", "GW170817 (tidal->C-Love)")]
    for a, b in hp:
        A, B = byname[a], byname[b]; rA, rB = Q.density(A["C"]), Q.density(B["C"])
        out["D5_qinfo"]["pairwise"][f"{a} | {b}"] = {
            "quantum_chernoff_shape": round(Q.qchernoff(rA, rB)[0], 4),
            "quantum_fidelity_shape": round(Q.qfidelity(rA, rB), 4),
            "classical_gauss_chernoff": round(Q.gauss_chernoff(A["mu"], A["C"], B["mu"], B["C"])[0], 3)}

    json.dump(out, open(os.path.join(ROOT, "results/e63_neutron_star_eos_results.json"), "w"), indent=2)
    print("\nwrote results/e63_neutron_star_eos_results.json")

if __name__ == "__main__":
    main()
