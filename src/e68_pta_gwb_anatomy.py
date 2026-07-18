#!/usr/bin/env python3
"""E68 - cross-PTA anatomy of the nanohertz GWB in (log10_A, gamma). Prereg E68 (locked).
Probes: NANOGrav 15yr HD, EPTA DR2full HD (primary; DR2new robustness), PPTA DR3 CRN.
Metrics: pairwise significance + E48 ladder + delta-rho; coherence (degeneracy-sliding vs
spectral); per-PTA z(gamma=13/3); E48 sliced-W Gaussianity gate. Seed 68."""
import os, sys, json, math
import numpy as np
from numpy.linalg import inv, det, eigh
from scipy.linalg import sqrtm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
PTA = os.path.join(ROOT, "data/chains/pta")
SEED = 68

# ---------- loaders: X = samples in (log10_A, gamma) ----------
def load_nanograv():
    d = np.load(os.path.join(PTA, "figure1_data/nano15_hd_chain_long_050523.npy"))
    return np.column_stack([d[:, 1], d[:, 0]])          # cols were (gamma, log10A) -> (A, gamma)

def load_epta(sub):
    base = os.path.join(PTA, f"epta_{sub}/hd_pl")
    pars = [l.strip() for l in open(base + "/pars.txt")]
    d = np.loadtxt(base + "/chain_1.txt")
    burn = len(d) // 4
    iA, ig = pars.index("gw_hd_log10_A"), pars.index("gw_hd_gamma")
    return np.column_stack([d[burn:, iA], d[burn:, ig]])

def load_ppta():
    pars = [l.strip() for l in open(os.path.join(PTA, "ppta_dr3_crn_freegam_DE440_pars.txt"))]
    d = np.load(os.path.join(PTA, "ppta_dr3_crn_freegam_DE440.npy"))
    iA = pars.index("gw_pl_nocorr_freegam_log10_A"); ig = pars.index("gw_pl_nocorr_freegam_gamma")
    return np.column_stack([d[:, iA], d[:, ig]])

# ---------- geometry (self-contained, as in e63) ----------
def moments(X):
    mu = X.mean(0); Xc = X - mu
    return mu, Xc.T @ Xc / len(X)

def bures2(A, B):
    sA = sqrtm(A); inner = sqrtm(sA @ B @ sA)
    return max(float(np.trace(A + B - 2 * inner).real), 0.0)

def unit_det(C): return C / math.sqrt(det(C))
def rho_of(C): return float(C[0, 1] / math.sqrt(C[0, 0] * C[1, 1]))
def psi_of(C):
    w, V = eigh(C); v = V[:, np.argmax(w)]
    return math.degrees(math.atan2(v[1], v[0])) % 180.0

def sliced_w(XA, XB, nproj=200, seed=SEED):
    rng = np.random.default_rng(seed); tot = 0.0
    for _ in range(nproj):
        th = rng.uniform(0, math.pi); u = np.array([math.cos(th), math.sin(th)])
        a = np.sort(XA @ u); b = np.sort(XB @ u)
        qs = np.linspace(0.005, 0.995, 200)
        qa = np.quantile(a, qs); qb = np.quantile(b, qs)
        tot += np.mean((qa - qb) ** 2)
    return tot / nproj

def pair(XA, XB, muA, CA, muB, CB):
    d = muA - muB
    sig = float(math.sqrt(d @ inv(CA + CB) @ d))
    # E48 ladder
    val_raw = float(d @ d); shp_raw = bures2(CA, CB)
    vf_raw = val_raw / (val_raw + shp_raw)
    Mj = inv(sqrtm(0.5 * (CA + CB))).real
    dj = Mj @ d; valj = float(dj @ dj)
    CAj, CBj = Mj @ CA @ Mj.T, Mj @ CB @ Mj.T
    vf_joint = valj / (valj + bures2(CAj, CBj))
    shp_or = bures2(unit_det(CAj), unit_det(CBj))
    vf_orient = valj / (valj + shp_or)
    # Gaussianity gate
    rng = np.random.default_rng(SEED)
    nA, nB = min(len(XA), 20000), min(len(XB), 20000)
    XAs = XA[rng.choice(len(XA), nA, replace=False)]; XBs = XB[rng.choice(len(XB), nB, replace=False)]
    emp = sliced_w(XAs, XBs)
    gau = sliced_w(rng.multivariate_normal(muA, CA, nA), rng.multivariate_normal(muB, CB, nB))
    ratio = emp / gau if gau > 0 else float("nan")
    return dict(sigma=round(sig, 2), vf_raw=round(vf_raw, 3), vf_joint=round(vf_joint, 3),
                vf_orientation_only=round(vf_orient, 3),
                delta_rho=round(abs(rho_of(CA) - rho_of(CB)), 3),
                dmu_log10A=round(float(d[0]), 3), dmu_gamma=round(float(d[1]), 3),
                nongauss_ratio=round(ratio, 3), gauss_faithful=bool(abs(ratio - 1) <= 0.30))

def main():
    P = {"NANOGrav15 (HD)": load_nanograv(),
         "EPTA DR2full (HD)": load_epta("DR2full"),
         "PPTA DR3 (CRN)": load_ppta()}
    ROB = {"EPTA DR2new (HD)": load_epta("DR2new")}
    M = {k: moments(X) for k, X in P.items()}
    MR = {k: moments(X) for k, X in ROB.items()}

    print("=== probes in (log10_A @ 1/yr, gamma) ===")
    out = {"prereg": "preregs/E68_pta_gwb_anatomy_prereg.md", "probes": {}, "pairs": {}}
    for k, (mu, C) in {**M, **MR}.items():
        z433 = (13.0 / 3.0 - mu[1]) / math.sqrt(C[1, 1])
        out["probes"][k] = {"log10A": round(float(mu[0]), 3), "gamma": round(float(mu[1]), 3),
                            "sd_log10A": round(math.sqrt(C[0, 0]), 3), "sd_gamma": round(math.sqrt(C[1, 1]), 3),
                            "rho": round(rho_of(C), 3), "psi_deg": round(psi_of(C), 1),
                            "z_gamma_13_3": round(float(z433), 2), "n": int(len((P | ROB)[k]))}
        v = out["probes"][k]
        print(f"  {k:20s} A={v['log10A']:.2f}+/-{v['sd_log10A']:.2f} gam={v['gamma']:.2f}+/-{v['sd_gamma']:.2f} "
              f"rho={v['rho']:+.2f} psi={v['psi_deg']:.0f} z(13/3)={v['z_gamma_13_3']:+.2f}")

    # ---- D1 pairwise ----
    names = list(P)
    print("\n=== D1 pairwise consistency ===")
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            r = pair(P[a], P[b], *M[a], *M[b])
            out["pairs"][f"{a} | {b}"] = r
            print(f"  {a:18s} vs {b:18s} sig={r['sigma']:.2f} vf_orient={r['vf_orientation_only']:.2f} "
                  f"dRho={r['delta_rho']:.2f} dA={r['dmu_log10A']:+.2f} dgam={r['dmu_gamma']:+.2f} "
                  f"nonG={r['nongauss_ratio']:.2f}")
    flagged = [k for k, v in out["pairs"].items() if v["sigma"] >= 2]
    D1 = "all pairs < 2 sigma (consistent)" if not flagged else f"flagged >=2 sigma: {flagged}"
    print(f"  D1 -> {D1}")

    # ---- D2 degeneracy universality + coherence ----
    rhos = {k: rho_of(C) for k, (mu, C) in M.items()}
    all_neg = all(r < 0 for r in rhos.values())
    # common degeneracy direction: mean principal axis (unit vector) in whitened-by-nothing plane
    axes = []
    for k, (mu, C) in M.items():
        w, V = eigh(C); v = V[:, np.argmax(w)]
        axes.append(v if v[1] >= 0 else -v)
    u_deg = np.mean(axes, axis=0); u_deg /= np.linalg.norm(u_deg)
    fracs = {}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            d = M[names[i]][0] - M[names[j]][0]
            f_par = float((d @ u_deg) ** 2 / (d @ d)) if d @ d > 0 else float("nan")
            fracs[f"{names[i]} | {names[j]}"] = round(f_par, 3)
    mean_frac = float(np.mean(list(fracs.values())))
    coh = "degeneracy-sliding (band/convention)" if mean_frac >= 2 / 3 else "spectral (real)"
    out["D2"] = {"rho_all_negative": bool(all_neg), "rhos": {k: round(v, 3) for k, v in rhos.items()},
                 "common_axis": [round(float(x), 3) for x in u_deg],
                 "offset_frac_along_degeneracy": fracs, "mean_frac": round(mean_frac, 3),
                 "classification": coh}
    print(f"\n=== D2 ===\n  rho negative for all: {all_neg} ; offset power along common degeneracy: "
          f"{fracs} ; mean={mean_frac:.2f} -> {coh}")

    # ---- D3 gamma = 13/3 ----
    n_gt2 = sum(1 for k in P if abs(out['probes'][k]['z_gamma_13_3']) > 2)
    out["D3"] = {"z_scores": {k: out['probes'][k]['z_gamma_13_3'] for k in P},
                 "n_PTAs_z_gt_2": n_gt2}
    print(f"\n=== D3 gamma=13/3 ===  z-scores: {out['D3']['z_scores']}  (n>2sig: {n_gt2}/3)")

    # ---- robustness: EPTA internal DR2new vs DR2full ----
    r = pair(ROB["EPTA DR2new (HD)"], P["EPTA DR2full (HD)"], *MR["EPTA DR2new (HD)"], *M["EPTA DR2full (HD)"])
    out["robustness_epta_internal"] = r
    print(f"\nEPTA internal (DR2new vs DR2full): sig={r['sigma']:.2f} dA={r['dmu_log10A']:+.2f} "
          f"dgam={r['dmu_gamma']:+.2f} (labeled robustness, same telescopes different span)")

    # ---- POST-HOC (exploratory, NOT preregistered): gamma vs observing span ----
    # published spans: EPTA DR2new 10.3 yr, NANOGrav15 16.03 yr, PPTA DR3 18 yr, EPTA DR2full 24.7 yr
    spans = {"EPTA DR2new (HD)": 10.3, "NANOGrav15 (HD)": 16.03, "PPTA DR3 (CRN)": 18.0,
             "EPTA DR2full (HD)": 24.7}
    gams = {k: out["probes"][k]["gamma"] for k in spans}
    order = sorted(spans, key=lambda k: spans[k])
    mono = all(gams[order[i]] < gams[order[i + 1]] for i in range(len(order) - 1))
    out["posthoc_span_ordering"] = {"label": "EXPLORATORY post-hoc, not preregistered",
        "spans_yr": spans, "gammas": gams, "perfectly_monotonic": bool(mono),
        "note": ("gamma-hat strictly increasing with time span across all 4 datasets; the signature "
                 "of a bending (non-power-law) spectrum or span-correlated systematic - exactly the "
                 "ambiguity the D2 caveat names. 4 datasets, 2 not independent (EPTA subsets); "
                 "p~1/24 one-sided if independent, weaker here. To be preregistered against "
                 "IPTA DR3 / NG20yr when public.")}
    print(f"\n=== POST-HOC (exploratory): gamma vs span ===")
    for k in order: print(f"  {spans[k]:5.1f} yr  gamma={gams[k]:.2f}  {k}")
    print(f"  strictly monotonic: {mono}")

    json.dump(out, open(os.path.join(ROOT, "results/e68_pta_gwb_anatomy_results.json"), "w"), indent=2)
    print("\nwrote results/e68_pta_gwb_anatomy_results.json")

if __name__ == "__main__":
    main()
