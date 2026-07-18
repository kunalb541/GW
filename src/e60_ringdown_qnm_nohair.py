#!/usr/bin/env python3
"""E60 - model-independent ringdown no-hair test: measured 220 QNM frequency (damped-sinusoid,
no Kerr assumption) vs the Kerr prediction from the INSPIRAL remnant (independent data).
f_DS (rin DS_1mode) vs f_Kerr(Mf,af) from imr inspiral via the Berti et al. (l,m,n)=(2,2,0) fit.
Prereg E60. Seed 60 (random pairing of the two independent posteriors)."""
import os, re, json, math, zipfile, tempfile
import numpy as np
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RIN = os.path.join(ROOT, "data/chains/tgr/IGWN-GWTC3-TGR-v2-rin.zip")
IMR = os.path.join(ROOT, "data/chains/tgr/IGWN-GWTC3-TGR-v1-imr.zip")
zr = zipfile.ZipFile(RIN); zi = zipfile.ZipFile(IMR)
rng = np.random.default_rng(60)
F0 = 32312.0  # c^3/(2 pi G Msun) in Hz  -> f_220[Hz] = omega_hat_R * F0 / (M_det/Msun)
# Berti et al. 2006 fit, (l,m,n)=(2,2,0):
def kerr_f_tau(Mdet, a):
    a = np.clip(a, 0, 0.998)
    wR = 1.5251 - 1.1568 * (1 - a)**0.1292            # omega_R * M (dimensionless)
    Q = 0.7000 + 1.4187 * (1 - a)**(-0.4990)
    f = wR * F0 / Mdet                                 # Hz
    tau = Q / (math.pi * f)                             # s  (tau = 2Q/omega_R = Q/(pi f))
    return f, tau

def read_ds(member):
    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as t: t.write(zr.read(member)); tp = t.name
    try:
        with h5py.File(tp, "r") as h:
            fnd = []; h.visititems(lambda n, o: fnd.append(n) if isinstance(o, h5py.Dataset) and n.endswith("posterior_samples") else None)
            ds = h[fnd[0]]; return np.asarray(ds["f_t_0"], float), np.asarray(ds["tau_t_0"], float)
    finally: os.remove(tp)

def read_imr_inspiral(member):
    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as t: t.write(zi.read(member)); tp = t.name
    try:
        with h5py.File(tp, "r") as h:
            ins = h["primary/posterior_samples/inspiral"]
            names = set(ins.dtype.names or [])
            if not {"final_mass", "final_spin"} <= names: return None, None
            return np.asarray(ins["final_mass"], float), np.asarray(ins["final_spin"], float)
    finally: os.remove(tp)

def numid(e):
    m = re.search(r"(\d{6})", e); return m.group(1) if m else e
dsm = {numid(os.path.basename(x).split("_pyring_")[0].replace("rin_", "")): x
       for x in zr.namelist() if "DS_1mode" in x and x.endswith(".h5")}
imrm = {numid(os.path.basename(x).replace("imr_", "").replace("_posterior_samples.h5", "")): x
        for x in zi.namelist() if x.endswith("_posterior_samples.h5")}
common = sorted(set(dsm) & set(imrm))

rows = []
for cid in common:
    fD, tauD = read_ds(dsm[cid])
    Mf, af = read_imr_inspiral(imrm[cid])
    if Mf is None: continue
    okD = np.isfinite(fD); okI = np.isfinite(Mf) & np.isfinite(af)
    fD = fD[okD]; Mf, af = Mf[okI], af[okI]
    if min(fD.size, Mf.size) < 200: continue
    fK, tauK = kerr_f_tau(Mf, af)
    N = min(fD.size, fK.size)
    fd = rng.permutation(fD)[:N]; fk = rng.permutation(fK)[:N]
    dfrac = (fd - fk) / fk                              # fractional frequency deviation (DS vs Kerr)
    med = float(np.median(dfrac)); z = float(np.mean(dfrac) / (np.std(dfrac) + 1e-30))
    p_consistent = float((np.abs(dfrac - 0) < np.abs(dfrac).std() * 2).mean())  # rough
    rows.append({"event": cid, "f_DS_med": round(float(np.median(fD)), 1), "f_Kerr_med": round(float(np.median(fK)), 1),
                 "delta_f_frac_med": round(med, 3), "z_from_Kerr": round(z, 2)})

n = len(rows)
zs = np.array([r["z_from_Kerr"] for r in rows])
big = [r for r in rows if abs(r["z_from_Kerr"]) > 2.0]
# coherence of the deviation (systematic vs scatter)
n_pos = sum(1 for r in rows if r["delta_f_frac_med"] > 0)
coherent = (n_pos / n > 0.8 or n_pos / n < 0.2)
comb_z = float(np.sum(zs) / math.sqrt(n))
D1 = len(big) == 0          # no event's measured QNM freq deviates from Kerr at >2sigma
D2 = abs(comb_z) < 2.0      # no coherent population deviation

print(f"events (DS ringdown vs inspiral-remnant Kerr prediction, independent): {n}")
print(f"{'event':10s} {'f_DS':>7} {'f_Kerr':>7} {'df/f':>7} {'z':>6}")
for r in sorted(rows, key=lambda r: -abs(r["z_from_Kerr"])):
    print(f"{r['event']:10s} {r['f_DS_med']:7.1f} {r['f_Kerr_med']:7.1f} {r['delta_f_frac_med']:7.3f} {r['z_from_Kerr']:6.2f}")
print(f"\nmedian |z| from Kerr: {np.median(np.abs(zs)):.2f}; events >2sigma: {len(big)} {[r['event'] for r in big]}")
print(f"deviation coherence: df/f>0 in {n_pos}/{n}; combined z = {comb_z:.2f}sigma")
print(f"\nD1 (no event QNM freq deviates from Kerr >2sigma): {'PASS' if D1 else 'FAIL'}")
print(f"D2 (no coherent population deviation, |comb z|<2): {'PASS' if D2 else 'FAIL'} ({comb_z:.2f})")

json.dump({"prereg": "preregs/E60_ringdown_qnm_nohair_prereg.md", "n_events": n,
           "median_abs_z": round(float(np.median(np.abs(zs))), 2), "n_gt_2sigma": len(big),
           "events_gt_2sigma": [r["event"] for r in big], "combined_z": round(comb_z, 2),
           "deviation_frac_pos": round(n_pos / n, 2), "coherent": bool(coherent),
           "D1_no_event_violation": bool(D1), "D2_no_population_deviation": bool(D2),
           "method": "DS_1mode measured 220 freq (no Kerr assumption) vs Berti Kerr f_220(Mf,af) from imr inspiral (independent data); detector frame",
           "per_event": sorted(rows, key=lambda r: -abs(r["z_from_Kerr"]))},
          open(os.path.join(ROOT, "results/e60_ringdown_qnm_nohair_results.json"), "w"), indent=2)
print("\nwrote results/e60_ringdown_qnm_nohair_results.json")
