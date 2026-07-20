#!/usr/bin/env python3
"""E88 - the 221 overtone in GW250114: how much evidence there is, and why it can only live at t_peak.

Built on the E87-corrected covariance (E85's was prior-dominated and could not have supported this).
Four things are done here that E85/E87 could not do:

 1. **Kerr parameterization.** The nonlinear parameters are the remnant (Mf, af); every mode's frequency
    and damping time follows from the BCW fits. 220-only vs 220+221 is then a comparison at the same
    remnant, not a comparison of unrelated free (f, tau) pairs.

 2. **A PHYSICAL, and therefore fair, model comparison.** The 221 and the 220 pass through the SAME antenna
    pattern in a given detector, so the complex amplitude RATIO rho = A221/A220 is shared across detectors
    even though each detector's overall complex amplitude is free. Writing the model as
    Re[A_det (T220 + rho T221)] makes it linear in A_det for any fixed rho, via
        M_red = M_full @ K(rho),   K(rho) = [[1,0],[0,-1],[Re rho,-Im rho],[-Im rho,-Re rho]]
    (verified exact to 8e-16). Both models then carry exactly TWO linear amplitudes per detector, so the
    linear-amplitude Occam factor CANCELS in the Bayes factor and the extra cost of the overtone is
    exactly the prior volume of rho - which is what it should be. Letting each detector have its own free
    221 amplitude instead (4 extra linear parameters) costs ~11 lnB units of pure Occam penalty on
    signal-free data and destroys the test; that was measured, not assumed.

 3. **A PROPER amplitude prior.** E85/E87 marginalized amplitudes with a flat (improper) prior - fine for a
    posterior on (f, tau), but it makes a Bayes factor undefined. Here amplitudes carry N(0, sigma_A^2):
        ln B = 0.5 b^T (G + I/sigma_A^2)^-1 b - 0.5 ln det(I + sigma_A^2 G)
    verified against brute-force numerical integration to 3e-14. sigma_A is scanned; because both models
    share the same linear dimension it should very nearly cancel, and that is checked rather than assumed.

 4. **An a-priori feasibility calculation.** At the IMR remnant the 221 sits only 5.5 Hz from the 220 but
    decays 3x faster, so over a 40 ms window the bases are ~76% collinear: most of the overtone is
    something the 220 can already absorb. What matters is the ORTHOGONALIZED overtone SNR, SNR_perp -
    computed from mode structure, the measured envelope amplitude, and the real noise covariance, with NO
    reference to any published result.

CHARACTERIZATION (no prereg). Seed 88."""
import os, sys, json, math
import numpy as np
from scipy.linalg import cho_solve

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e87_ringdown_corrected import (RingdownFit, find_peak, load_detector, DETECTORS,
                                        FS, NWIN, IMR, TGR_TARBALL)
from src.e74_gw250114_deepdive import qnm

MODES = ("220", "221")
MF_GRID = np.arange(45.0, 115.1, 1.0)
AF_GRID = np.arange(0.0, 0.9501, 0.025)
SIGMA_A_SCAN = (3e-21, 1e-20, 3e-20, 1e-19)
SIGMA_A_DEFAULT = 1e-20
RHO_MAX_SCAN = (1.0, 2.0, 3.0)
RHO_MAX_DEFAULT = 2.0
RHO_N = 25                                   # per axis, over the square, masked to the disc
A_PEAK = 1.95e-21                            # measured 100-400 Hz envelope at t_peak
START_TIMES_M = (0, 1, 2, 3, 4, 6, 8, 10, 12)
T_M_MS = IMR["Mf_det"] * 4.925490947e-6 * 1e3


def kerr_basis(tt, Mf, af, modes=MODES):
    cols = []
    for m in modes:
        f, tau = qnm(Mf, af, m)
        e = np.exp(-tt / tau)
        cols += [e * np.cos(2 * math.pi * f * tt), e * np.sin(2 * math.pi * f * tt)]
    return np.column_stack(cols)


def gb(fit, Mf, af):
    M = kerr_basis(fit.tt, Mf, af)
    return M.T @ cho_solve(fit.cho, M), M.T @ cho_solve(fit.cho, fit.d)


def rho_grid(rho_max=RHO_MAX_DEFAULT, n=RHO_N):
    g = np.linspace(-rho_max, rho_max, n)
    R, I = np.meshgrid(g, g, indexing="ij")
    keep = (R ** 2 + I ** 2) <= rho_max ** 2
    return R[keep], I[keep]


def kmats(rr, ri):
    """Stack of K(rho) matrices, shape (nrho, 4, 2)."""
    K = np.zeros((len(rr), 4, 2))
    K[:, 0, 0] = 1.0
    K[:, 1, 1] = -1.0
    K[:, 2, 0] = rr
    K[:, 2, 1] = -ri
    K[:, 3, 0] = -ri
    K[:, 3, 1] = -rr
    return K


def ln_eff_stack(Gr, br, sigma_A):
    """Vectorized log Bayes factor (signal vs noise) for a stack of reduced 2x2 systems."""
    k = Gr.shape[-1]
    A = Gr + np.eye(k) / sigma_A ** 2
    sol = np.linalg.solve(A, br[..., None])[..., 0]
    _, ld = np.linalg.slogdet(np.eye(k) + sigma_A ** 2 * Gr)
    return 0.5 * np.einsum("...i,...i->...", br, sol) - 0.5 * ld


def snr_perp(fit, Mf, af, a220, a221):
    """Overtone SNR ORTHOGONAL to the full 220 subspace, in the C^-1 metric - the only part of the 221
    the 220 model cannot already absorb. Detection needs roughly SNR_perp > 3-4."""
    B = kerr_basis(fit.tt, Mf, af)
    B0, s1, s0 = B[:, :2], a221 * B[:, 2], a220 * B[:, 0]
    G0 = B0.T @ cho_solve(fit.cho, B0)
    perp = s1 - B0 @ np.linalg.solve(G0, B0.T @ cho_solve(fit.cho, s1))
    ip = lambda x, y: x @ cho_solve(fit.cho, y)
    return (math.sqrt(max(0.0, ip(s0, s0))), math.sqrt(max(0.0, ip(s1, s1))),
            math.sqrt(max(0.0, ip(perp, perp))))


def evidence(fits, sigmas=(SIGMA_A_DEFAULT,), rho_maxes=(RHO_MAX_DEFAULT,)):
    """Integrate over (Mf, af) for the 220-only model and over (Mf, af, rho) for 220+221, with flat
    priors (rho uniform on the disc |rho| <= rho_max). G, b are built ONCE per grid point and reused
    across every sigma_A and rho, so the scans are nearly free.

    Returns {(sigma, rho_max): dict(lnB_220, lnB_221, dlnB)} plus the rho posterior at the defaults."""
    grids = {rm: rho_grid(rm) for rm in rho_maxes}
    Ks = {rm: kmats(*grids[rm]) for rm in rho_maxes}
    K0 = kmats(np.zeros(1), np.zeros(1))

    nmf, naf = len(MF_GRID), len(AF_GRID)
    L220 = {s: np.empty((nmf, naf)) for s in sigmas}
    L221 = {(s, rm): np.empty((nmf, naf, len(grids[rm][0]))) for s in sigmas for rm in rho_maxes}

    for i, Mf in enumerate(MF_GRID):
        for j, af in enumerate(AF_GRID):
            gbs = [gb(f, Mf, af) for f in fits]
            # the K-reductions depend only on (K, G, b) -- hoist them out of the sigma_A scan
            red0 = [(np.einsum("rab,ac,rcd->rbd", K0, G, K0), np.einsum("rab,a->rb", K0, b))
                    for G, b in gbs]
            red = {rm: [(np.einsum("rab,ac,rcd->rbd", Ks[rm], G, Ks[rm]),
                         np.einsum("rab,a->rb", Ks[rm], b)) for G, b in gbs]
                   for rm in rho_maxes}
            for s in sigmas:
                L220[s][i, j] = sum(ln_eff_stack(Gr, br, s)[0] for Gr, br in red0)
                for rm in rho_maxes:
                    L221[(s, rm)][i, j] = sum(ln_eff_stack(Gr, br, s) for Gr, br in red[rm])

    def lse(L, n):
        m = L.max()
        return m + math.log(np.exp(L - m).sum()) - math.log(n)

    out = {}
    for s in sigmas:
        z1 = lse(L220[s], nmf * naf)
        for rm in rho_maxes:
            L = L221[(s, rm)]
            z2 = lse(L, L.size)
            out[(s, rm)] = {"lnB_220": float(z1), "lnB_221": float(z2), "dlnB": float(z2 - z1)}
    L = L221[(SIGMA_A_DEFAULT, RHO_MAX_DEFAULT)] if (SIGMA_A_DEFAULT, RHO_MAX_DEFAULT) in out else None
    post = None
    if L is not None:
        w = np.exp(L - L.max()).sum(axis=(0, 1))
        rr, ri = grids[RHO_MAX_DEFAULT]
        post = {"rho_abs_mean": float((np.hypot(rr, ri) * w).sum() / w.sum())}
    return out, post


def _inject_2mode(seg, i0, rho, amp=A_PEAK, phi=0.7, Mf=None, af=None):
    Mf = Mf if Mf is not None else IMR["Mf_det"]
    af = af if af is not None else IMR["af"]
    f0, t0 = qnm(Mf, af, "220")
    f1, t1 = qnm(Mf, af, "221")
    t = np.arange(len(seg) - i0) / FS
    x = seg.copy()
    x[i0:] += amp * (np.exp(-t / t0) * np.cos(2 * math.pi * f0 * t)
                     + rho * np.exp(-t / t1) * np.cos(2 * math.pi * f1 * t + phi))
    return x


def offsource_fits(strains, gps, off_s, dt_s=0.0, rho=None, amp=A_PEAK):
    """Fits on a signal-free stretch `off_s` seconds from the merger, optionally with a synthetic
    ringdown injected. Used for the null distributions and the profile-shape template."""
    fits = []
    for d in DETECTORS:
        st, g0 = strains[d]
        j = int((gps - g0) * FS) + int(off_s * FS)
        if j - 40 * int(FS) < 0 or j + 4 * int(FS) > len(st):
            return None
        seg = st[j - 4 * int(FS): j + 4 * int(FS)].copy()
        nz = st[j - 40 * int(FS): j - 8 * int(FS)].copy()
        i0 = len(seg) // 2
        if rho is not None:
            seg = _inject_2mode(seg, i0, rho, amp)
        fits.append(RingdownFit(seg, FS, i0 + int(round(dt_s * FS)), NWIN, nz))
    return fits


def null_distribution(strains, gps, rho, offs, amp=A_PEAK):
    """Distribution of dlnB when the truth is known. rho=0.0 is THE relevant null (a loud 220 with no
    overtone); rho=None is signal-free; rho>0 measures detection power."""
    vals = []
    for o in offs:
        f = offsource_fits(strains, gps, o, rho=rho, amp=amp)
        if f is None:
            continue
        ev, _ = evidence(f)
        vals.append(ev[(SIGMA_A_DEFAULT, RHO_MAX_DEFAULT)]["dlnB"])
    a = np.array(vals)
    return {"n": int(len(a)), "mean": float(a.mean()), "sd": float(a.std(ddof=1)),
            "min": float(a.min()), "max": float(a.max()), "values": [float(x) for x in a]}


def dlnB_pinned(fits, Mf, af, rho_max=RHO_MAX_DEFAULT, sigma_A=SIGMA_A_DEFAULT):
    """dlnB with the remnant PINNED. The gap to the marginalized value measures how much of the
    overtone the single-mode model absorbs by simply moving (Mf, af)."""
    K = kmats(*rho_grid(rho_max))
    K0 = kmats(np.zeros(1), np.zeros(1))
    t0 = 0.0
    tot = np.zeros(len(K))
    for f in fits:
        G, b = gb(f, Mf, af)
        t0 += ln_eff_stack(np.einsum("rab,ac,rcd->rbd", K0, G, K0),
                           np.einsum("rab,a->rb", K0, b), sigma_A)[0]
        tot += ln_eff_stack(np.einsum("rab,ac,rcd->rbd", K, G, K),
                            np.einsum("rab,a->rb", K, b), sigma_A)
    m = tot.max()
    return float(m + math.log(np.exp(tot - m).sum()) - math.log(len(tot)) - t0)


def lvk_evidences(tarball=TGR_TARBALL):
    """LVK's own pyRing Kerr_220 / Kerr_221 log Bayes factors, averaged over sampler seeds."""
    import tarfile, re, collections
    t = tarfile.open(tarball)
    ev = collections.defaultdict(list)
    for n in t.getnames():
        m = re.search(r"Kerr_(220|221)_(\d+)M_SEED_\d+/Nested_sampler/Evidence\.txt$", n)
        if m:
            row = [float(x) for x in t.extractfile(n).read().decode().strip().split("\n")[1].split()]
            ev[(m.group(1), int(m.group(2)))].append(row)
    out = {}
    for (mode, M), rows in ev.items():
        a = np.array(rows)
        out.setdefault(M, {})[mode] = {"lnB": float(a[:, 2].mean()), "snr": float(a[:, 3].mean()),
                                       "n_seeds": int(len(rows))}
    return out


def main():
    pre = {}
    for det, rel in DETECTORS.items():
        seg, noise = load_detector(os.path.join(ROOT, rel))
        pre[det] = (seg, noise, find_peak(seg, FS))
    lvk = lvk_evidences() if os.path.exists(TGR_TARBALL) else {}

    f0, tau0 = qnm(IMR["Mf_det"], IMR["af"], "220")
    f1, tau1 = qnm(IMR["Mf_det"], IMR["af"], "221")
    out = {"sigma_A_default": SIGMA_A_DEFAULT, "rho_max_default": RHO_MAX_DEFAULT,
           "t_Mf_ms": T_M_MS, "A_peak": A_PEAK,
           "mode_structure": {"f220": f0, "tau220_ms": tau0 * 1e3, "f221": f1,
                              "tau221_ms": tau1 * 1e3, "df_hz": f0 - f1,
                              "ratio_decay_ms": 1 / (1 / tau1 - 1 / tau0) * 1e3},
           "feasibility": {}, "evidence": {}, "prior_sensitivity": {}, "lvk": {}}

    sigmas = tuple(sorted(set(SIGMA_A_SCAN) | {SIGMA_A_DEFAULT}))
    rhos = tuple(sorted(set(RHO_MAX_SCAN) | {RHO_MAX_DEFAULT}))
    for M in START_TIMES_M:
        dt = M * T_M_MS * 1e-3
        fits = [RingdownFit(pre[d][0], FS, pre[d][2] + int(round(dt * FS)), NWIN, pre[d][1])
                for d in DETECTORS]
        a220 = A_PEAK * math.exp(-dt / tau0)
        out["feasibility"][f"{M}M"] = {}
        for r0 in (1.0, 0.5):
            s0, s1, sp = snr_perp(fits[0], IMR["Mf_det"], IMR["af"], a220,
                                  r0 * A_PEAK * math.exp(-dt / tau1))
            out["feasibility"][f"{M}M"][f"ratio0_{r0}"] = {"snr220": s0, "snr221": s1, "snr_perp": sp}

        ev, post = evidence(fits, sigmas, rhos)
        d0 = ev[(SIGMA_A_DEFAULT, RHO_MAX_DEFAULT)]
        out["evidence"][f"{M}M"] = dict(d0, rho_posterior=post)
        out["prior_sensitivity"][f"{M}M"] = {f"sigA={s:.0e},rhomax={rm}": ev[(s, rm)]["dlnB"]
                                             for s in sigmas for rm in rhos}
        if M in lvk:
            out["lvk"][f"{M}M"] = {"dlnB": lvk[M]["221"]["lnB"] - lvk[M]["220"]["lnB"],
                                   "lnB_220": lvk[M]["220"]["lnB"], "snr_220": lvk[M]["220"]["snr"]}
        msg = f"{M:3d}M  dlnB(ours) = {d0['dlnB']:7.2f}   lnB_220 = {d0['lnB_220']:9.2f}"
        if f"{M}M" in out["lvk"]:
            msg += f"   dlnB(LVK) = {out['lvk'][f'{M}M']['dlnB']:7.2f}"
        print(msg)

    # ---- nulls, detection power, absorption, and the profile-shape discriminator ----
    import h5py
    strains = {}
    for d, rel in DETECTORS.items():
        with h5py.File(os.path.join(ROOT, rel), "r") as h:
            strains[d] = (np.asarray(h["strain/Strain"]), h["meta/GPSstart"][()])
    gps = 1420878141.22
    OFFS = (-300, -240, -180, -150, -120, -90, -60, -45, 60, 90, 120, 150, 200, 260)
    out["nulls"] = {
        "signal_free": null_distribution(strains, gps, None, OFFS),
        "pure_220": null_distribution(strains, gps, 0.0, OFFS),          # THE relevant null
        "overtone_rho1": null_distribution(strains, gps, 1.0, OFFS[:8]),  # detection power
    }
    obs0 = out["evidence"]["0M"]["dlnB"]
    n = out["nulls"]["pure_220"]
    out["nulls"]["z_vs_pure220_at_0M"] = float((obs0 - n["mean"]) / n["sd"])

    # how much does remnant freedom absorb? (pinned vs marginalized, on injections)
    out["absorption"] = {}
    for r in (0.5, 1.0, 2.0):
        f = offsource_fits(strains, gps, -150, rho=r)
        ev, _ = evidence(f)
        out["absorption"][f"rho{r}"] = {
            "pinned": dlnB_pinned(f, IMR["Mf_det"], IMR["af"]),
            "marginalized": ev[(SIGMA_A_DEFAULT, RHO_MAX_DEFAULT)]["dlnB"]}

    # THE discriminator: a genuine overtone's dlnB must COLLAPSE with start time
    out["shape_test"] = {}
    for label, r in (("genuine_rho1.5", 1.5), ("pure_220", 0.0)):
        prof = {}
        for M in START_TIMES_M:
            f = offsource_fits(strains, gps, -150, dt_s=M * T_M_MS * 1e-3, rho=r)
            ev, _ = evidence(f)
            prof[f"{M}M"] = ev[(SIGMA_A_DEFAULT, RHO_MAX_DEFAULT)]["dlnB"]
        out["shape_test"][label] = prof
    obs = {k: v["dlnB"] for k, v in out["evidence"].items()}
    out["shape_test"]["fall_0M_to_8M"] = {
        "observed": obs["0M"] - obs["8M"],
        "genuine_rho1.5": out["shape_test"]["genuine_rho1.5"]["0M"]
                          - out["shape_test"]["genuine_rho1.5"]["8M"]}

    path = os.path.join(ROOT, "results/e88_overtone_evidence_results.json")
    json.dump(out, open(path, "w"), indent=1)
    print("\nnulls:", {k: (round(v["mean"], 2), round(v["sd"], 2)) if isinstance(v, dict) else round(v, 2)
                       for k, v in out["nulls"].items()})
    print("shape fall 0M->8M:", {k: round(v, 2) for k, v in out["shape_test"]["fall_0M_to_8M"].items()})
    print("wrote", path)


if __name__ == "__main__":
    main()
