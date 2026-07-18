#!/usr/bin/env python3
"""E66 - spectral-siren H0 obstruction: linear-response coupling of H0 to the mass scale
on the real LVK GWTC-3 joint (cosmology+population) posterior (icarogw). Prereg E66. Seed 66."""
import os, sys, json, math
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, "data/chains/e66/O3_icarogw_data_distro.json")

PRIMARY = "SNR_11_BBH-powerlaw-gaussian_restricted-flatLCDM"
SECONDARY = "SNR_11_BBH-powerlaw-gaussian_w0flatLCDM"
ROBUST = ["SNR_10_BBH-powerlaw-gaussian_restricted-flatLCDM",
          "SNR_12_BBH-powerlaw-gaussian_restricted-flatLCDM",
          "SNR_11_BBH-broken-powerlaw_restricted-flatLCDM"]
MASS = ["mu_g", "sigma_g", "lambda_peak", "mmin", "mmax", "delta_m", "alpha", "beta"]
RATE = ["gamma", "kappa", "zp"]

def chain(d, key):
    c = d[key]
    pars = [p for p in MASS + RATE if p in c]
    X = np.column_stack([np.asarray(c[p], float) for p in pars])
    h = np.asarray(c["H0"], float)
    ok = np.isfinite(h) & np.all(np.isfinite(X), axis=1)
    return h[ok], X[ok], pars

def response(h, X):
    """M = C_AB C_BB^-1 : dH0/dtheta_j (marginal linear response)."""
    Xc = X - X.mean(0); hc = h - h.mean()
    C_AB = (hc[:, None] * Xc).mean(0)                    # 1 x k
    C_BB = (Xc.T @ Xc) / len(Xc)
    return C_AB @ np.linalg.inv(C_BB)

def decile_slope(h, x):
    """cross-check: slope of E[H0 | x] across deciles of x (robust to non-Gaussianity)."""
    qs = np.quantile(x, np.linspace(0, 1, 11))
    mids, means = [], []
    for i in range(10):
        m = (x >= qs[i]) & (x <= qs[i + 1])
        if m.sum() > 50:
            mids.append(x[m].mean()); means.append(h[m].mean())
    if len(mids) < 4: return float("nan")
    A = np.vstack([mids, np.ones(len(mids))]).T
    return float(np.linalg.lstsq(A, np.array(means), rcond=None)[0][0])

def analyze(d, key):
    h, X, pars = chain(d, key)
    M = response(h, X)                                    # PARTIAL (conditional) coupling
    sd = X.std(0)
    hc = h - h.mean(); Xc = X - X.mean(0)
    per = {}
    for j, p in enumerate(pars):
        marg = float((hc * Xc[:, j]).mean() / Xc[:, j].var())   # MARGINAL slope cov/var
        per[p] = dict(dH0_dtheta_partial=float(M[j]), sigma_theta=float(sd[j]),
                      dH0_dtheta_marginal=marg,
                      dH0_per_sigma=float(marg * sd[j]),         # per-1sig via the marginal track
                      decile_slope=decile_slope(h, X[:, j]))
    return h, pars, per

def main():
    d = json.load(open(F))
    h, pars, per = analyze(d, PRIMARY)
    print(f"=== PRIMARY {PRIMARY}  n={len(h)} ===")
    print(f"H0 = {np.median(h):.2f} (sd {h.std():.2f}, prior-restricted [65,77])")
    print(f"mu_g median = {np.median(np.asarray(d[PRIMARY]['mu_g'],float)):.2f}")
    print(f"\n{'param':12s} {'marginal':>9s} {'partial':>9s} {'sigma':>8s} {'dH0/1sig':>9s} {'decile':>9s}  group")
    ranked = sorted(per.items(), key=lambda kv: -abs(kv[1]["dH0_per_sigma"]))
    for p, v in ranked:
        grp = "MASS" if p in MASS else "RATE"
        print(f"{p:12s} {v['dH0_dtheta_marginal']:9.3f} {v['dH0_dtheta_partial']:9.3f} {v['sigma_theta']:8.3f} "
              f"{v['dH0_per_sigma']:9.3f} {v['decile_slope']:9.3f}  {grp}")

    # ---- D1: obstruction (mu_g drift of +/- 4 Msun) ----
    dH0_4 = per["mu_g"]["dH0_dtheta_marginal"] * 4.0   # marginal degeneracy track (decile-validated)
    D1 = "CONFIRMED" if abs(dH0_4) >= 2.0 else ("REFUTED" if abs(dH0_4) < 1.0 else "INCONCLUSIVE")
    print(f"\nD1: dH0(4 Msun mu_g drift) = {dH0_4:+.2f} km/s/Mpc  (>=2 confirm, <1 refute) -> {D1}")

    # ---- D2: dominant lever ----
    mass_tot = math.sqrt(sum(per[p]["dH0_per_sigma"] ** 2 for p in per if p in MASS))
    rate_tot = math.sqrt(sum(per[p]["dH0_per_sigma"] ** 2 for p in per if p in RATE))
    top = ranked[0][0]
    print(f"D2: |dH0| per-1sig quadrature: MASS group {mass_tot:.2f} vs RATE group {rate_tot:.2f} "
          f"km/s/Mpc; top lever = {top}")

    # ---- D3 sanity ----
    mu_med = float(np.median(np.asarray(d[PRIMARY]["mu_g"], float)))
    s3a = 30 <= mu_med <= 35
    top3 = [p for p, _ in ranked[:3]]
    s3b = all(np.sign(per[p]["dH0_dtheta_marginal"]) == np.sign(per[p]["decile_slope"]) and
              (abs(per[p]["decile_slope"]) / max(abs(per[p]["dH0_dtheta_marginal"]), 1e-12) < 2 and
               abs(per[p]["dH0_dtheta_marginal"]) / max(abs(per[p]["decile_slope"]), 1e-12) < 2)
              for p in top3 if np.isfinite(per[p]["decile_slope"]))
    _, _, per2 = analyze(d, SECONDARY)
    s3c = np.sign(per2[top]["dH0_dtheta_marginal"]) == np.sign(per[top]["dH0_dtheta_marginal"]) if top in per2 else None
    print(f"D3: (a) mu_g median {mu_med:.2f} in [30,35]: {s3a}  (b) estimators agree top-3: {s3b}  "
          f"(c) top-lever sign agrees in wide-prior chain: {s3c}")

    # ---- robustness ----
    rob = {}
    for k in ROBUST:
        if k not in d: continue
        _, _, perk = analyze(d, k)
        if "mu_g" in perk:
            rob[k] = round(perk["mu_g"]["dH0_dtheta_marginal"] * 4.0, 2)
        else:  # broken powerlaw has no mu_g; use mmax as the mass-scale proxy
            proxy = max((p for p in perk if p in MASS), key=lambda p: abs(perk[p]["dH0_per_sigma"]))
            rob[k] = {"proxy": proxy, "dH0_per_sigma": round(perk[proxy]["dH0_per_sigma"], 2)}
    print(f"robustness dH0(4Msun) / proxies: {rob}")

    json.dump({"prereg": "preregs/E66_spectral_siren_obstruction_prereg.md",
               "primary": PRIMARY, "n": int(len(h)),
               "H0_median": float(np.median(h)), "H0_sd": float(h.std()), "mu_g_median": mu_med,
               "response": {p: {k: (None if isinstance(v2, float) and not np.isfinite(v2) else v2)
                                for k, v2 in v.items()} for p, v in per.items()},
               "D1": {"dH0_4Msun": float(dH0_4), "verdict": D1},
               "D2": {"mass_group_quad": mass_tot, "rate_group_quad": rate_tot, "top_lever": top},
               "D3": {"mu_g_in_range": bool(s3a), "estimators_agree": bool(s3b),
                      "secondary_sign_agrees": None if s3c is None else bool(s3c)},
               "robustness": rob},
              open(os.path.join(ROOT, "results/e66_spectral_siren_obstruction_results.json"), "w"),
              indent=2)
    print("\nwrote results/e66_spectral_siren_obstruction_results.json")

if __name__ == "__main__":
    main()
