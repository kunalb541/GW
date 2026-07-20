#!/usr/bin/env python3
"""E91 - reproducible deterministic submission gates for the curved chirp-mass law.

This is the executable provenance layer for Gates A/C/D. It writes one event-level CSV plus a JSON
summary. GWTC-3 preferred-group rows are read from the existing E65/E40 derived artifacts because the
raw GWTC-3 HDF5 chains are not present in this workspace; O4a/O4b are recomputed from local HDF5 files.
Seed 91 (used only for the deterministic shuffled-q baseline).
"""
import csv
import glob
import json
import math
import os
import sys
import time
from collections import Counter, defaultdict

import h5py
import numpy as np
from scipy.stats import spearmanr, wilcoxon

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e65_pn_fisher_rotation import adiff, ang_of
from src.e71_gwtc5_curved_law import curve_psi, pick_group, tangent_angles

SEED = 91
CATALOGS = {
    "O4a": os.path.join(ROOT, "data/chains/gwtc4"),
    "O4b": os.path.join(ROOT, "data/chains/gwtc5"),
}
RESULT_JSON = os.path.join(ROOT, "results/e91_curve_submission_gates_results.json")
RESULT_CSV = os.path.join(ROOT, "results/e91_curve_submission_gates_events.csv")


def signed_adiff(a, b):
    return float((a - b + 90.0) % 180.0 - 90.0)


def psi_axr_rho(m1, m2):
    x = np.column_stack([m1, m2])
    x = x - x.mean(0)
    c = x.T @ x / len(x)
    w, v = np.linalg.eigh(c)
    psi = ang_of(v[:, 1])
    axr = math.sqrt(max(w[1], 1e-30) / max(w[0], 1e-30))
    rho = c[0, 1] / math.sqrt(c[0, 0] * c[1, 1])
    return float(psi), float(axr), float(rho)


def event_name(fp):
    return os.path.basename(fp).replace("-combined_PEDataRelease.hdf5", "").replace(".hdf5", "")


def posterior_groups(h):
    return [k for k in h.keys() if isinstance(h[k], h5py.Group) and "posterior_samples" in h[k]]


def open_h5_retry(fp, attempts=4):
    last = None
    for i in range(attempts):
        try:
            return h5py.File(fp, "r")
        except (TimeoutError, OSError) as exc:
            last = exc
            time.sleep(2 * (i + 1))
    raise last


def aligned_samples(ds, frame="source"):
    if frame == "source":
        m1_col, m2_col, mc_col = "mass_1_source", "mass_2_source", "chirp_mass_source"
    elif frame == "detector":
        m1_col, m2_col, mc_col = "mass_1_detector", "mass_2_detector", "chirp_mass"
        if m1_col not in ds.dtype.names or m2_col not in ds.dtype.names:
            # Public O4 files used here omit component detector-frame masses. Redshift is a common
            # sample-wise scale, so detector-frame orientation equals source-frame orientation when
            # only source component masses are available; leave this explicitly flagged upstream.
            m1_col, m2_col = "mass_1_source", "mass_2_source"
    else:
        raise ValueError(frame)
    need = [m1_col, m2_col, "mass_ratio", mc_col]
    if any(c not in ds.dtype.names for c in need):
        missing = [c for c in need if c not in ds.dtype.names]
        raise KeyError(f"missing columns: {missing}")
    m1 = np.asarray(ds[m1_col], float)
    m2 = np.asarray(ds[m2_col], float)
    q = np.asarray(ds["mass_ratio"], float)
    mc = np.asarray(ds[mc_col], float)
    ok = np.isfinite(m1) & np.isfinite(m2) & np.isfinite(q) & np.isfinite(mc)
    return m1[ok], m2[ok], q[ok], mc[ok]


def score_samples(catalog, event, group, m1, m2, q, mc_samples, target=None, frame="source"):
    psi_m, axr, rho = psi_axr_rho(m1, m2)
    m1m, m2m = float(np.median(m1)), float(np.median(m2))
    psi_t, psi_tot = tangent_angles(m1m, m2m)
    mc = float(np.median(mc_samples))
    psi_c = curve_psi(mc, q)
    q05, q95 = np.quantile(q, [0.05, 0.95])
    row = {
        "catalog": catalog,
        "event": event,
        "group": group,
        "target_group": target or group,
        "frame": frame,
        "n_samples": int(len(q)),
        "m1": m1m,
        "m2": m2m,
        "mc": mc,
        "q_median": float(np.median(q)),
        "q05": float(q05),
        "q95": float(q95),
        "q_range_05_95": float(q95 - q05),
        "axr": axr,
        "rho": rho,
        "psi_meas": psi_m,
        "psi_curve": psi_c,
        "psi_tangent": psi_t,
        "psi_total": psi_tot,
        "err_curve": adiff(psi_c, psi_m),
        "err_tangent": adiff(psi_t, psi_m),
        "err_total": adiff(psi_tot, psi_m),
        "signed_curve_minus_meas": signed_adiff(psi_c, psi_m),
        "source": "raw_hdf5",
    }
    return row


def load_raw_group_rows(catalog, data_dir, all_groups=False):
    rows, dropped = [], {}
    for fp in sorted(glob.glob(os.path.join(data_dir, "GW*.hdf5"))):
        ev = event_name(fp)
        try:
            with open_h5_retry(fp) as h:
                preferred = pick_group(h)
                groups = posterior_groups(h) if all_groups else [preferred]
                for g in groups:
                    if g is None:
                        continue
                    ds = h[g]["posterior_samples"]
                    m1, m2, q, mc = aligned_samples(ds, "source")
                    row = score_samples(catalog, ev, g, m1, m2, q, mc)
                    row["is_preferred_group"] = bool(g == preferred)
                    rows.append(row)
        except Exception as exc:
            dropped[ev] = str(exc)
    return rows, dropped


def load_gwtc3_derived_rows():
    path = os.path.join(ROOT, "results/e65_pn_fisher_rotation_results.json")
    if not os.path.exists(path):
        return [], {"GWTC-3": "missing results/e65_pn_fisher_rotation_results.json"}
    rows = []
    for r in json.load(open(path))["per_event"]:
        rows.append({
            "catalog": "GWTC-3",
            "event": r["event"],
            "group": "derived:E65-picked",
            "target_group": "derived:E65-picked",
            "frame": "source",
            "n_samples": "",
            "m1": r["m1"],
            "m2": r["m2"],
            "mc": "",
            "q_median": "",
            "q05": "",
            "q95": "",
            "q_range_05_95": "",
            "axr": r["axr"],
            "rho": "",
            "psi_meas": r["psi_meas"],
            "psi_curve": r["psi_curve"],
            "psi_tangent": r["psi_chirp"],
            "psi_total": r.get("psi_total", 135.0),
            "err_curve": r["err_curve"],
            "err_tangent": r["err_chirp"],
            "err_total": adiff(r["psi_total"], r["psi_meas"]),
            "signed_curve_minus_meas": signed_adiff(r["psi_curve"], r["psi_meas"]),
            "source": "derived_e65_no_raw_gwtc3_hdf5",
        })
    return rows, {}


def load_curve_result_rows(catalog, path, source):
    if not os.path.exists(path):
        return [], {catalog: f"missing {path}"}
    rows = []
    for r in json.load(open(path))["per_event"]:
        rows.append({
            "catalog": catalog,
            "event": r["event"],
            "group": r.get("group", "derived:preferred"),
            "target_group": r.get("group", "derived:preferred"),
            "frame": "source",
            "n_samples": "",
            "m1": r["m1"],
            "m2": r["m2"],
            "mc": "",
            "q_median": "",
            "q05": "",
            "q95": "",
            "q_range_05_95": "",
            "axr": r["axr"],
            "rho": r.get("rho", ""),
            "psi_meas": r["psi_meas"],
            "psi_curve": r["psi_curve"],
            "psi_tangent": r["psi_tangent"],
            "psi_total": r.get("psi_total", 135.0),
            "err_curve": r["err_curve"],
            "err_tangent": r["err_tangent"],
            "err_total": r["err_total"],
            "signed_curve_minus_meas": signed_adiff(r["psi_curve"], r["psi_meas"]),
            "source": source,
        })
    return rows, {}


def baseline_summary(preferred_rows):
    out = {}
    rng = np.random.default_rng(SEED)
    for cat in sorted({r["catalog"] for r in preferred_rows}):
        rows = [r for r in preferred_rows if r["catalog"] == cat]
        elong = [r for r in rows if float(r["axr"]) >= 3.0]
        out[cat] = {
            "n_all": len(rows),
            "n_elong": len(elong),
            "median_curve_elong": median_key(elong, "err_curve"),
            "median_tangent_elong": median_key(elong, "err_tangent"),
            "median_total_elong": median_key(elong, "err_total"),
        }
        raw = [r for r in elong if r["source"] == "raw_hdf5"]
        if raw:
            # Recompute pooled/shuffled q baselines from cached per-event rows by reopening source files.
            q_by_event = {}
            mc_by_event = {}
            for r in raw:
                fp = os.path.join(CATALOGS[cat], f"{r['event']}-combined_PEDataRelease.hdf5")
                with open_h5_retry(fp) as h:
                    ds = h[r["group"]]["posterior_samples"]
                    _, _, q, mc = aligned_samples(ds, "source")
                q_by_event[r["event"]] = q
                mc_by_event[r["event"]] = float(np.median(mc))
            pooled = np.concatenate(list(q_by_event.values()))
            shuffled_events = list(q_by_event)
            shuffled_q = dict(zip(shuffled_events, rng.permutation(shuffled_events)))
            pooled_err, shuffled_err = [], []
            for r in raw:
                pooled_err.append(adiff(curve_psi(mc_by_event[r["event"]], pooled), r["psi_meas"]))
                shuffled_err.append(adiff(curve_psi(mc_by_event[r["event"]], q_by_event[shuffled_q[r["event"]]]), r["psi_meas"]))
            out[cat]["median_pooled_q_elong"] = float(np.median(pooled_err))
            out[cat]["median_single_shuffle_q_elong"] = float(np.median(shuffled_err))
        else:
            out[cat]["raw_q_baselines"] = "not available from derived-only rows"
    return out


def cross_family_rows():
    rows, dropped = [], {}
    directions = [("C00:IMRPhenomXPHM-SpinTaylor", "C00:SEOBNRv5PHM"), ("C00:SEOBNRv5PHM", "C00:IMRPhenomXPHM-SpinTaylor")]
    for cat, data_dir in CATALOGS.items():
        for fp in sorted(glob.glob(os.path.join(data_dir, "GW*.hdf5"))):
            ev = event_name(fp)
            try:
                with open_h5_retry(fp) as h:
                    for src, tgt in directions:
                        if src not in h or tgt not in h:
                            continue
                        sds, tds = h[src]["posterior_samples"], h[tgt]["posterior_samples"]
                        sm1, sm2, sq, smc = aligned_samples(sds, "source")
                        tm1, tm2, tq, tmc = aligned_samples(tds, "source")
                        tpsi, taxr, _ = psi_axr_rho(tm1, tm2)
                        spsi, saxr, _ = psi_axr_rho(sm1, sm2)
                        if saxr < 3.0 or taxr < 3.0:
                            continue
                        tm1m, tm2m = float(np.median(tm1)), float(np.median(tm2))
                        ttan, _ = tangent_angles(tm1m, tm2m)
                        pred = curve_psi(float(np.median(smc)), sq)
                        rows.append({
                            "catalog": cat,
                            "event": ev,
                            "source_group": src,
                            "target_group": tgt,
                            "source_axr": saxr,
                            "target_axr": taxr,
                            "source_target_axis_disagreement": adiff(spsi, tpsi),
                            "err_curve_cross": adiff(pred, tpsi),
                            "err_tangent_target": adiff(ttan, tpsi),
                        })
            except Exception as exc:
                dropped[f"{cat}:{ev}"] = str(exc)
    return rows, dropped


def waveform_family_summary(all_group_rows):
    out = {}
    for (cat, group), rows in groupby(all_group_rows, "catalog", "group").items():
        elong = [r for r in rows if r["axr"] >= 3.0]
        if len(elong) >= 5:
            out[f"{cat}|{group}"] = {
                "catalog": cat,
                "group": group,
                "n_elong": len(elong),
                "median_curve": median_key(elong, "err_curve"),
                "median_tangent": median_key(elong, "err_tangent"),
            }
    return out


def frame_coordinate_summary(preferred_rows):
    # Detector component masses are absent from the local O4 public files; log-source coordinates are still
    # directly reproducible and the detector-frame limitation is recorded.
    log_rows = []
    for cat, data_dir in CATALOGS.items():
        for r in [x for x in preferred_rows if x["catalog"] == cat and x["source"] == "raw_hdf5"]:
            fp = os.path.join(data_dir, f"{r['event']}-combined_PEDataRelease.hdf5")
            with open_h5_retry(fp) as h:
                ds = h[r["group"]]["posterior_samples"]
                m1, m2, q, mc = aligned_samples(ds, "source")
            log_rows.append(score_samples(cat, r["event"], r["group"], np.log(m1), np.log(m2), q, np.log(mc), frame="log_source"))
    src_elong = [r for r in preferred_rows if r["source"] == "raw_hdf5" and r["axr"] >= 3.0]
    log_elong = [r for r in log_rows if r["axr"] >= 3.0]
    bands = [(1.0, 1.5), (1.5, 2.0), (2.0, 3.0), (3.0, 5.0), (5.0, float("inf"))]
    return {
        "source_m1_m2": {"n_elong": len(src_elong), "median_curve_elong": median_key(src_elong, "err_curve"), "median_axr": median_key(src_elong, "axr")},
        "log_source_m1_m2": {"n_elong": len(log_elong), "median_curve_elong": median_key(log_elong, "err_curve"), "median_axr": median_key(log_elong, "axr")},
        "detector_frame": "not recomputed: local O4 files lack mass_1_detector/mass_2_detector columns",
        "axr_bands_source": [
            {"lo": lo, "hi": hi, "n": len(xs), "median_curve": median_key(xs, "err_curve")}
            for lo, hi in bands
            for xs in [[r for r in preferred_rows if r["source"] == "raw_hdf5" and lo <= r["axr"] < hi]]
        ],
    }


def groupby(rows, *keys):
    out = defaultdict(list)
    for r in rows:
        out[tuple(r[k] for k in keys)].append(r)
    return out


def median_key(rows, key):
    vals = [float(r[key]) for r in rows if r.get(key) not in ("", None)]
    return None if not vals else float(np.median(vals))


def write_csv(rows):
    fields = ["catalog", "event", "group", "target_group", "frame", "source", "n_samples", "m1", "m2", "mc",
              "q_median", "q05", "q95", "q_range_05_95", "axr", "rho", "psi_meas", "psi_curve",
              "psi_tangent", "psi_total", "err_curve", "err_tangent", "err_total", "signed_curve_minus_meas"]
    with open(RESULT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def main():
    recompute_raw = os.environ.get("E91_RECOMPUTE_RAW") == "1"
    full_waveforms = os.environ.get("E91_FULL_WAVEFORMS") == "1"
    run_cross = os.environ.get("E91_CROSS_FAMILY") == "1"
    preferred, dropped = load_gwtc3_derived_rows()
    all_group_rows = []
    if recompute_raw:
        for cat, data_dir in CATALOGS.items():
            rows, dr = load_raw_group_rows(cat, data_dir, all_groups=False)
            preferred.extend(rows)
            dropped.update({f"{cat}:{k}": v for k, v in dr.items()})
            if full_waveforms:
                fam_rows, fam_dr = load_raw_group_rows(cat, data_dir, all_groups=True)
                all_group_rows.extend(fam_rows)
                dropped.update({f"family:{cat}:{k}": v for k, v in fam_dr.items()})
    else:
        for cat, path in [
            ("O4a", os.path.join(ROOT, "results/e67_gwtc4_curved_law_results.json")),
            ("O4b", os.path.join(ROOT, "results/e71_gwtc5_curved_law_results.json")),
        ]:
            rows, dr = load_curve_result_rows(cat, path, f"derived:{os.path.basename(path)}")
            preferred.extend(rows)
            dropped.update(dr)

    cross, cross_dropped = (cross_family_rows() if run_cross else ([], {"cross_family": "skipped; set E91_CROSS_FAMILY=1"}))
    dropped.update({f"cross:{k}": v for k, v in cross_dropped.items()})
    write_csv(preferred)

    by_cat = baseline_summary(preferred)
    summary = {
        "battery": "E91 curve submission gates",
        "seed": SEED,
        "inputs": {
            "GWTC-3": "results/e65_pn_fisher_rotation_results.json (derived; raw HDF5 absent)",
            "O4a": "results/e67_gwtc4_curved_law_results.json by default; set E91_RECOMPUTE_RAW=1 for HDF5",
            "O4b": "results/e71_gwtc5_curved_law_results.json by default; set E91_RECOMPUTE_RAW=1 for HDF5",
        },
        "dropped": dropped,
        "preferred_group_counts": dict(Counter(f"{r['catalog']}|{r['group']}" for r in preferred)),
        "gate_A_baselines": by_cat,
        "gate_A_cross_family": {
            "n": len(cross),
            "median_axis_disagreement": median_key(cross, "source_target_axis_disagreement"),
            "median_curve_cross": median_key(cross, "err_curve_cross"),
            "median_tangent_target": median_key(cross, "err_tangent_target"),
            "by_direction": {
                f"{k[0]}|{k[1]}|{k[2]}": {
                    "n": len(v),
                    "median_axis_disagreement": median_key(v, "source_target_axis_disagreement"),
                    "median_curve_cross": median_key(v, "err_curve_cross"),
                    "median_tangent_target": median_key(v, "err_tangent_target"),
                }
                for k, v in groupby(cross, "catalog", "source_group", "target_group").items()
            },
            "events": cross,
        },
        "gate_C_frame_coordinate": frame_coordinate_summary(preferred),
        "gate_D_waveform_families": (
            waveform_family_summary(all_group_rows)
            if full_waveforms
            else {"status": "skipped by default for speed; rerun with E91_FULL_WAVEFORMS=1"}
        ),
        "gate_D_prereg_public_record": {
            "E71": "publicly separated prereg/result commits per docs/GATE_DE_FIRST_MEASUREMENT.md",
            "E67": "prereg and result enter this repo in same bulk-port commit; private-parent attestation only",
        },
        "event_csv": "results/e91_curve_submission_gates_events.csv",
    }
    json.dump(summary, open(RESULT_JSON, "w"), indent=2)
    print(f"wrote {RESULT_JSON}")
    print(f"wrote {RESULT_CSV}")
    print(f"preferred rows: {len(preferred)}; cross-family rows: {len(cross)}")


if __name__ == "__main__":
    main()
