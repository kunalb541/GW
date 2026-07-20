#!/usr/bin/env python3
"""E89 - black-hole spin magnitude rises with mass across 265 events: a hierarchical-assembly signature,
with the estimator's own bias measured and subtracted.

THE PHYSICS. A comparable-mass BBH merger leaves a remnant with a_f ~ 0.69 almost independently of what
went in - one of GR's cleanest predictions. So black holes that are THEMSELVES merger remnants (second
generation) should carry a ~ 0.7, and if hierarchical assembly happens they will sit preferentially at
high mass. The signature is therefore a rising spin MAGNITUDE with mass.

WHY E42-E44 SAW NOTHING. Those batteries hunted the hierarchical channel in chi_eff and found no
requirement for it. That is exactly what is expected: dynamically assembled binaries have ISOTROPIC spin
orientations, so large spin magnitudes average to chi_eff ~ 0. chi_eff is structurally blind to this
population. The magnitude a_1 is not. E89 is E44's test done in the observable that can see the effect.

TWO TRAPS, BOTH OF WHICH THIS BATTERY FELL INTO FIRST:

 1. **An "informative events" cut is self-biasing.** Splitting on how far each posterior sits from its
    prior looks like the E85 lesson applied well, and gives a beautifully strengthened trend. It is
    circular: among HEAVY events, spin is well measured precisely WHEN IT IS LARGE, so the cut selects
    high spins by construction. Measured here: KS-from-prior rises monotonically with a_1 among the ten
    heaviest events. Cuts on informativeness are not used in the result.

 2. **The hierarchical fit is itself biased when measurement quality correlates with mass** - which it
    does (Spearman(ln m1, posterior concentration) = -0.52). Simulating a population with NO mass-spin
    correlation but the real per-event informativeness still returns slope b1 = +0.42 +/- 0.11 and
    dlnL = 6.0 +/- 2.3. So the naive "dlnL = 11.5 -> 4.8 sigma" is NOT a valid significance, and the
    slope must be bias-corrected. The tempting analytic argument - that a flat posterior contributes
    ln(integral of a normalized density) = 0 to every model and so cannot bias anything - is wrong,
    because NEAR-flat posteriors do not.

Significance is therefore quoted against two independent nulls, not against chi^2.

CHARACTERIZATION (no prereg; the trend was already visible in an earlier audit, so this is not a blind
test and is not scored as one). Seed 89."""
import os, sys, json, glob, math
import numpy as np
from scipy.stats import beta as BetaDist, ks_2samp, spearmanr
from scipy.optimize import minimize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e71_gwtc5_curved_law import pick_group

CATALOGS = (("GWTC-3", "data/chains/gw_posteriors"),
            ("O4a", "data/chains/gwtc4"),
            ("O4b", "data/chains/gwtc5"))
M_PIVOT = 30.0
N_SAMP = 600
SEED = 89
A_REMNANT = 0.69          # universal remnant spin of a comparable-mass BBH merger


def event_name(fp):
    b = os.path.basename(fp)
    return (b.split("-")[0].replace("_PE.h5", "").replace(".h5", "").replace(".hdf5", "")
            .split("_PEDataRelease")[0])


def load_events(root=ROOT, n_samp=N_SAMP, seed=SEED):
    """One entry per unique event: median source-frame m1 and a thinned a_1 posterior. The a_1 prior is
    uniform(0,1) (verified against the `priors` group in the release files), so the marginal posterior
    is proportional to the marginal likelihood and needs no reweighting in the population fit."""
    import h5py
    rng = np.random.default_rng(seed)
    out, seen = [], set()
    for lab, d in CATALOGS:
        for fp in sorted(glob.glob(os.path.join(root, d, "*.h5"))
                         + glob.glob(os.path.join(root, d, "*.hdf5"))):
            ev = event_name(fp)
            if ev in seen:
                continue
            try:
                with h5py.File(fp, "r") as h:
                    g = pick_group(h)
                    if g is None:
                        continue
                    ds = h[g]["posterior_samples"]
                    nm = ds.dtype.names
                    if not all(k in nm for k in ("a_1", "mass_1_source")):
                        continue
                    a1 = np.asarray(ds["a_1"], float)
                    m1 = np.asarray(ds["mass_1_source"], float)
                    fs_col = next((c for c in ("final_spin", "final_spin_non_evolved") if c in nm), None)
                    fs = np.asarray(ds[fs_col], float) if fs_col else None
            except Exception:
                continue
            ok = np.isfinite(a1) & np.isfinite(m1)
            if ok.sum() < 200:
                continue
            seen.add(ev)
            i = rng.integers(0, ok.sum(), min(n_samp, ok.sum()))
            rec = dict(ev=ev, cat=lab, m1=float(np.median(m1[ok])),
                       a=np.clip(a1[ok][i], 1e-4, 1 - 1e-4))
            if fs is not None and np.isfinite(fs[ok]).all():
                rec["fs_med"] = float(np.median(fs[ok]))
                rec["fs_corr"] = float(spearmanr(a1[ok], fs[ok])[0])
            out.append(rec)
    return out


def concentration(a):
    """Beta concentration implied by a posterior's mean and variance: ~2 means flat (uninformative)."""
    m, v = a.mean(), a.var()
    return float(min(max(0.05, m * (1 - m) / max(v, 1e-6) - 1), 300.0))


def ks_from_prior(a, rng):
    return float(ks_2samp(a, rng.uniform(0, 1, 4000)).statistic)


# ---------------- hierarchical population model ----------------
def nll(p, lm, A):
    """p(a | m) = Beta with mean sigmoid(b0 + b1 * ln(m/30)) and concentration exp(lk).
    With a uniform a_1 prior the per-event term is just the sample average of the population density."""
    b0, b1, lk = p
    k = math.exp(lk)
    if not (0.5 < k < 500):
        return 1e9
    mu = np.clip(1.0 / (1.0 + np.exp(-(b0 + b1 * lm))), 1e-3, 1 - 1e-3)
    v = BetaDist.pdf(A, (mu * k)[:, None], ((1 - mu) * k)[:, None]).mean(axis=1)
    if np.any(~np.isfinite(v)) or np.any(v <= 0):
        return 1e9
    return float(-np.log(v).sum())


def fit(lm, A):
    """Returns (b0, b1, conc, dlnL) where dlnL compares the free slope to slope = 0."""
    o = dict(maxiter=2000, fatol=1e-4)
    f1 = minimize(nll, [0.0, 0.0, math.log(5)], args=(lm, A), method="Nelder-Mead", options=o)
    f0 = minimize(lambda p, *a: nll(np.array([p[0], 0.0, p[1]]), *a), [0.0, math.log(5)],
                  args=(lm, A), method="Nelder-Mead", options=o)
    return float(f1.x[0]), float(f1.x[1]), float(math.exp(f1.x[2])), float(f0.fun - f1.fun)


def simulate_posterior(a_true, w, n_samp, rng, kappa_tight=60.0):
    """Posterior for a known truth at informativeness w in [0,1], as a MIXTURE of a concentrated
    component at the truth and the uniform prior.

    This shape matters and an earlier version of this battery got it wrong. Modelling the posterior as
    a Beta CENTRED on the truth with a low concentration makes a low true spin come out piled against
    a_1 = 0, which looks highly informative. Real uninformative posteriors do not do that -- they relax
    to the flat prior: heavy events with concentration <= 4 have median a_1 = 0.474 and KS = 0.14,
    i.e. they sit at the prior median 0.5. The wrong shape manufactured a spurious +0.42 slope bias
    and would have caused this battery to under-report its own result."""
    w = float(np.clip(w, 0.0, 1.0))
    n_t = int(round(w * n_samp))
    parts = []
    if n_t:
        parts.append(rng.beta(a_true * kappa_tight, (1 - a_true) * kappa_tight, n_t))
    if n_samp - n_t:
        parts.append(rng.uniform(0, 1, n_samp - n_t))
    return np.clip(np.concatenate(parts), 1e-4, 1 - 1e-4)


def null_forward(lm, w, n_trials, rng, mu0=0.23, k0=2.62, n_samp=N_SAMP):
    """NULL A. Draw true spins from a MASS-INDEPENDENT population, then give each event a posterior at
    its REAL informativeness w (calibrated per event from the KS distance to the uniform prior).
    Measures whatever bias the mass-informativeness confound induces in the estimator."""
    b1s, dls = [], []
    for _ in range(n_trials):
        sim = np.empty((len(lm), n_samp))
        for i in range(len(lm)):
            at = float(np.clip(rng.beta(mu0 * k0, (1 - mu0) * k0), 1e-3, 1 - 1e-3))
            sim[i] = simulate_posterior(at, w[i], n_samp, rng)
        _, b1, _, dl = fit(lm, sim)
        b1s.append(b1)
        dls.append(dl)
    return np.array(b1s), np.array(dls)


def null_permute(lm, A, kap, n_trials, rng, n_strata=8):
    """NULL B. Shuffle masses WITHIN concentration strata, keeping the real posteriors. Destroys any
    true mass-spin link while holding measurement quality fixed. Conservative: if better-measured spin
    is itself a consequence of higher spin, conditioning on concentration removes real signal too."""
    order = np.argsort(kap)
    strata = np.array_split(order, n_strata)
    b1s, dls = [], []
    for _ in range(n_trials):
        p = lm.copy()
        for s in strata:
            p[s] = lm[rng.permutation(s)]
        _, b1, _, dl = fit(p, A)
        b1s.append(b1)
        dls.append(dl)
    return np.array(b1s), np.array(dls)


def main(n_trials=150):
    rng = np.random.default_rng(SEED)
    evs = load_events()
    lm = np.array([math.log(e["m1"] / M_PIVOT) for e in evs])
    A = np.array([e["a"] for e in evs])
    kap = np.array([concentration(e["a"]) for e in evs])
    m1 = np.array([e["m1"] for e in evs])
    a_med = np.array([float(np.median(e["a"])) for e in evs])

    out = {"n_events": len(evs), "m_pivot": M_PIVOT,
           "by_catalog": {c: int(sum(e["cat"] == c for e in evs)) for c, _ in CATALOGS}}

    # descriptive trend + the cross-run coherence check
    out["spearman_all"] = dict(zip(("rho", "p"), [float(x) for x in spearmanr(m1, a_med)]))
    out["per_catalog"] = {}
    for c, _ in CATALOGS:
        s = np.array([e["cat"] == c for e in evs])
        r, p = spearmanr(m1[s], a_med[s])
        out["per_catalog"][c] = {"n": int(s.sum()), "rho": float(r), "p": float(p)}

    # the confound, stated explicitly
    out["confound"] = {"spearman_lnm1_concentration": float(spearmanr(lm, kap)[0])}

    # the self-biasing cut, documented so it is never reused as a result
    heavy = np.argsort(-m1)[:10]
    ksv = np.array([ks_from_prior(evs[i]["a"], rng) for i in heavy])
    out["informativeness_cut_is_circular"] = {
        "spearman_a1_vs_ks_among_10_heaviest": float(spearmanr(a_med[heavy], ksv)[0])}

    # remnant-spin leak test
    fsm = np.array([e.get("fs_med", np.nan) for e in evs])
    ok = np.isfinite(fsm)
    out["remnant_leak_test"] = {}
    for lo, hi, lab in ((0, 15, "0-15"), (15, 35, "15-35"), (35, 60, "35-60"), (60, 1e9, ">60")):
        s = ok & (m1 >= lo) & (m1 < hi)
        if s.sum() < 3:
            continue
        out["remnant_leak_test"][lab] = {
            "n": int(s.sum()), "median_a1": float(np.median(a_med[s])),
            "median_final_spin": float(np.median(fsm[s])),
            "gap": float(np.median(a_med[s]) - np.median(fsm[s])),
            "median_per_event_corr": float(np.median([evs[i]["fs_corr"] for i in np.where(s)[0]
                                                      if "fs_corr" in evs[i]]))}

    # the measurement
    b0, b1, conc, dl = fit(lm, A)
    out["fit"] = {"b0": b0, "b1": b1, "concentration": conc, "dlnL": dl}

    # per-event informativeness w, calibrated from the KS distance to the uniform prior
    w = np.array([ks_from_prior(e["a"], rng) for e in evs])
    out["informativeness"] = {"w_median": float(np.median(w)),
                              "spearman_lnm1_w": float(spearmanr(lm, w)[0])}
    nb, nd = null_forward(lm, w, n_trials, rng)
    pb, pd = null_permute(lm, A, kap, n_trials, rng)
    out["null_forward"] = {"b1_mean": float(nb.mean()), "b1_sd": float(nb.std(ddof=1)),
                           "b1_max": float(nb.max()), "dlnL_mean": float(nd.mean()),
                           "dlnL_sd": float(nd.std(ddof=1)), "dlnL_max": float(nd.max()),
                           "p_b1": float((nb >= b1).mean()), "p_dlnL": float((nd >= dl).mean()),
                           "n_trials": int(n_trials)}
    out["null_permute"] = {"b1_mean": float(pb.mean()), "b1_sd": float(pb.std(ddof=1)),
                           "b1_max": float(pb.max()), "dlnL_mean": float(pd.mean()),
                           "dlnL_sd": float(pd.std(ddof=1)), "dlnL_max": float(pd.max()),
                           "p_b1": float((pb >= b1).mean()), "p_dlnL": float((pd >= dl).mean()),
                           "n_trials": int(n_trials)}

    b1_corr = b1 - float(nb.mean())          # subtract the measured estimator bias
    out["bias_corrected"] = {"b1": b1_corr, "bias_subtracted": float(nb.mean()),
                             "population_mean_a1": {
                                 str(m): float(1 / (1 + math.exp(-(b0 + b1_corr * math.log(m / M_PIVOT)))))
                                 for m in (8, 15, 30, 60, 100)}}
    out["naive_population_mean_a1"] = {
        str(m): float(1 / (1 + math.exp(-(b0 + b1 * math.log(m / M_PIVOT))))) for m in (8, 15, 30, 60, 100)}
    out["a_remnant_reference"] = A_REMNANT

    path = os.path.join(ROOT, "results/e89_mass_spin_hierarchical_results.json")
    json.dump(out, open(path, "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("n_events", "spearman_all", "per_catalog", "confound",
                                          "fit", "null_forward", "null_permute", "bias_corrected")},
                     indent=1))
    print("wrote", path)


if __name__ == "__main__":
    main()
