#!/usr/bin/env python3
"""E71 - GWTC-5 (O4b) out-of-sample REPEAT of the E65 curved chirp-mass law + E40 tangent law.
Prereg E71 (locked BEFORE any GWTC-5 file was opened; commit d19a7a8). Third disjoint catalog after
GWTC-1/2.1/3 (E40/E65 train) and GWTC-4/O4a (E67). Scoring machinery is byte-identical to E67; the
ONLY changes are the declared structural adapter (data dir, GWTC-5 filename parse) and a pre-committed
O4b/O4a disjointness assertion + a GWTC-4 D3 baseline. Seed 71 (no RNG).

Structural note (prereg 'structural adapter' clause): GWTC-5.0 O4b PE files carry NO 'Mixed' combined
group (only per-waveform analyses: IMRPhenomXPHM-SpinTaylor / IMRPhenomXPNR / NRSur7dq4 / SEOBNRv5PHM).
The locked E67 rule 'Mixed if present, else the single largest available analysis' therefore selects the
largest-sample waveform analysis per event -- deterministic, declared, and recorded per event."""
import os, sys, json, glob, math, time
import numpy as np
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e65_pn_fisher_rotation import ang_of, adiff

GW5 = os.path.join(ROOT, "data/chains/gwtc5")
E67_RESULTS = os.path.join(ROOT, "results/e67_gwtc4_curved_law_results.json")

# ---------- core scoring: COPIED VERBATIM FROM src/e67_gwtc4_curved_law.py (no edits) ----------
def pick_group(h):
    """locked preference: Mixed group (largest posterior_samples if several), else largest analysis."""
    cands = [k for k in h.keys() if isinstance(h[k], h5py.Group) and "posterior_samples" in h[k]]
    mixed = [k for k in cands if "mixed" in k.lower()]
    pool = mixed if mixed else cands
    if not pool: return None
    return max(pool, key=lambda k: len(h[k]["posterior_samples"]))

def psi_axr_rho(m1, m2):
    X = np.column_stack([m1, m2]); X = X - X.mean(0)
    C = X.T @ X / len(X)
    w, V = np.linalg.eigh(C)
    psi = ang_of(V[:, 1])
    axr = math.sqrt(max(w[1], 1e-30) / max(w[0], 1e-30))
    rho = C[0, 1] / math.sqrt(C[0, 0] * C[1, 1])
    return psi, axr, rho

def tangent_angles(m1m, m2m):
    M = m1m + m2m
    g_c = np.array([0.6 / m1m - 0.2 / M, 0.6 / m2m - 0.2 / M])   # grad ln Mc
    psi_t = ang_of(np.array([-g_c[1], g_c[0]]))                   # constant-Mc tangent
    return psi_t, 135.0                                           # constant-Mtot tangent

def curve_psi(mc_src, qs):
    qs = np.clip(qs[np.isfinite(qs)], 0.02, 1.0)
    m1 = mc_src * (1 + qs) ** 0.2 * qs ** -0.6
    m2 = qs * m1
    P = np.column_stack([m1, m2]); P = P - P.mean(0)
    _, V = np.linalg.eigh(P.T @ P / len(P))
    return ang_of(V[:, 1])

def load_event(fp):
    for attempt in range(4):                                      # errno-60 stall retry
        try:
            with h5py.File(fp, "r") as h:
                g = pick_group(h)
                if g is None: return None, "no posterior group"
                ds = h[g]["posterior_samples"]
                need = ["mass_1_source", "mass_2_source", "mass_ratio", "chirp_mass_source"]
                if any(n not in ds.dtype.names for n in need): return None, f"missing cols in {g}"
                m1 = np.asarray(ds["mass_1_source"], float); m2 = np.asarray(ds["mass_2_source"], float)
                q = np.asarray(ds["mass_ratio"], float); mc = float(np.median(ds["chirp_mass_source"]))
            ok = np.isfinite(m1) & np.isfinite(m2)
            return dict(m1=m1[ok], m2=m2[ok], q=q, mc=mc, group=g), None
        except (TimeoutError, OSError) as e:
            if attempt == 3: return None, f"read error: {e}"
            time.sleep(3 * (attempt + 1))
# ---------- end verbatim block ----------

# ---------- structural adapter: GWTC-5 filename -> event name; O4b/O4a disjointness ----------
def event_name(fp):
    """GWTC-5 files are '<EVENT>-combined_PEDataRelease.hdf5' (IGWN prefix stripped at fetch)."""
    return os.path.basename(fp).replace("-combined_PEDataRelease.hdf5", "").replace(".hdf5", "")

def yymmdd(ev):
    """GWYYMMDD_HHMMSS -> int YYMMDD (for the O4a-cutoff disjointness check)."""
    d = ev[2:8]
    return int(d) if d.isdigit() else -1

O4A_END = 240116   # O4a last event 2024-01-16; O4b started 2024-04-10. E71 events must post-date this.

def main():
    rows, dropped = [], {}
    files = sorted(glob.glob(os.path.join(GW5, "GW*.hdf5")))
    print(f"O4b event files: {len(files)}")
    for fp in files:
        name = event_name(fp)
        ev, err = load_event(fp)
        if ev is None:
            dropped[name] = err; continue
        m1m, m2m = float(np.median(ev["m1"])), float(np.median(ev["m2"]))
        psi_m, axr, rho = psi_axr_rho(ev["m1"], ev["m2"])
        psi_t, psi_tot = tangent_angles(m1m, m2m)
        psi_c = curve_psi(ev["mc"], ev["q"])
        rows.append(dict(event=name, group=ev["group"], m1=round(m1m, 2), m2=round(m2m, 2),
                         axr=round(axr, 2), rho=round(rho, 3),
                         psi_meas=round(psi_m, 2), psi_tangent=round(psi_t, 2),
                         psi_curve=round(psi_c, 2),
                         err_curve=round(adiff(psi_c, psi_m), 2),
                         err_tangent=round(adiff(psi_t, psi_m), 2),
                         err_total=round(adiff(psi_tot, psi_m), 2)))
    print(f"scored {len(rows)} events; dropped {len(dropped)}: {dropped}")

    # ---- pre-committed disjointness from O4a (prereg honesty commitment) ----
    e71_events = {r["event"] for r in rows}
    dates = [yymmdd(r["event"]) for r in rows if yymmdd(r["event"]) > 0]
    min_date, max_date = (min(dates), max(dates)) if dates else (None, None)
    all_after_o4a = bool(dates) and all(d > O4A_END for d in dates)
    o4a_overlap = set()
    if os.path.exists(E67_RESULTS):
        e67 = json.load(open(E67_RESULTS))
        o4a_events = {r["event"] for r in e67.get("per_event", [])}
        o4a_overlap = e71_events & o4a_events
    print(f"disjointness: O4b date range {min_date}-{max_date}; all post-O4a(>{O4A_END})={all_after_o4a}; "
          f"name-overlap with E67/O4a set = {len(o4a_overlap)} {sorted(o4a_overlap) if o4a_overlap else ''}")

    # waveform-group usage (transparency: no Mixed group exists in GWTC-5)
    from collections import Counter
    grp_counts = Counter(r["group"] for r in rows)

    elong = [r for r in rows if r["axr"] >= 3]
    d1_med = float(np.median([r["err_curve"] for r in elong])) if elong else float("nan")
    D1 = bool(elong) and d1_med < 2.0
    d2_curve = float(np.median([r["err_curve"] for r in rows]))
    d2_tan = float(np.median([r["err_tangent"] for r in rows]))
    D2 = d2_curve < d2_tan
    # D3 descriptive: E40 replication
    wins = sum(1 for r in rows if r["err_tangent"] < r["err_total"])
    from scipy.stats import spearmanr
    sp = spearmanr([r["axr"] for r in rows], [r["err_tangent"] for r in rows])

    print(f"\nD1 (ON-RECORD E65/E67 prediction): elongated (axr>=3, n={len(elong)}) "
          f"median |dpsi_curve| = {d1_med:.2f} deg (< 2 required) -> {'PASS' if D1 else 'FAIL'}")
    print(f"D2: all events (n={len(rows)}): curve {d2_curve:.2f} vs tangent {d2_tan:.2f} deg "
          f"-> {'PASS' if D2 else 'FAIL'}")
    print(f"D3 (E40 replication, descriptive): median |dpsi_tangent| = {d2_tan:.2f} deg "
          f"(GWTC-3: 7.49; GWTC-4: 9.36); chirp-vs-total wins {wins}/{len(rows)} = "
          f"{wins/len(rows)*100:.0f}% (GWTC-3: 81%; GWTC-4: 86%); "
          f"Spearman(err, axr) = {sp.statistic:.2f} (GWTC-3: -0.42; GWTC-4: -0.40)")
    print(f"\nwaveform groups picked (no Mixed in GWTC-5): {dict(grp_counts)}")

    print(f"\n  elongated events (axr>=3), sorted by axr:")
    print(f"  {'event':22s} {'m1':>6s} {'m2':>6s} {'axr':>5s} {'meas':>7s} {'curve':>7s} {'tan':>7s} {'e_crv':>6s} {'e_tan':>6s}")
    for r in sorted(elong, key=lambda r: -r["axr"]):
        print(f"  {r['event']:22s} {r['m1']:6.1f} {r['m2']:6.1f} {r['axr']:5.1f} {r['psi_meas']:7.2f} "
              f"{r['psi_curve']:7.2f} {r['psi_tangent']:7.2f} {r['err_curve']:6.2f} {r['err_tangent']:6.2f}")

    # descriptive E72 seed: largest curve residuals overall (labelled post-hoc, not a decision)
    top_resid = sorted(rows, key=lambda r: -r["err_curve"])[:10]
    print(f"\n  [descriptive/post-hoc; E72 seed] 10 largest |dpsi_curve| residuals:")
    for r in top_resid:
        print(f"  {r['event']:22s} axr={r['axr']:5.1f} m1={r['m1']:6.1f} m2={r['m2']:6.1f} "
              f"q~{r['m2']/r['m1']:.2f} e_curve={r['err_curve']:6.2f}")

    json.dump({"prereg": "preregs/E71_gwtc5_curved_law_prereg.md",
               "catalog": "GWTC-5.0 / O4b (Zenodo 20276106 + 20348006)",
               "n_scored": len(rows), "dropped": dropped,
               "disjointness_O4a": {"min_yymmdd": min_date, "max_yymmdd": max_date,
                                    "all_post_O4a_cutoff_240116": all_after_o4a,
                                    "name_overlap_with_E67": sorted(o4a_overlap)},
               "waveform_groups_picked": dict(grp_counts),
               "D1": {"n_elong": len(elong), "median_err_curve_elong": d1_med, "pass": bool(D1)},
               "D2": {"median_err_curve_all": d2_curve, "median_err_tangent_all": d2_tan, "pass": bool(D2)},
               "D3": {"tangent_median": d2_tan, "chirp_wins": wins, "n": len(rows),
                      "spearman_err_axr": float(sp.statistic), "p": float(sp.pvalue),
                      "baselines": {"gwtc3": [7.49, 0.81, -0.42], "gwtc4": [9.36, 0.86, -0.40]}},
               "e72_seed_top_residuals": [r["event"] for r in top_resid],
               "per_event": rows},
              open(os.path.join(ROOT, "results/e71_gwtc5_curved_law_results.json"), "w"), indent=2)
    print("\nwrote results/e71_gwtc5_curved_law_results.json")

if __name__ == "__main__":
    main()
