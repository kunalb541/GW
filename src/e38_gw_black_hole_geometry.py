#!/usr/bin/env python3
"""E38 - gravitational-wave black-hole posterior geometry.

Uses actual public GW posterior HDF5 samples when cached under data/chains/gw_posteriors
(ignored by git), and GWOSC event summaries for broader landmark-event context.
"""
from __future__ import annotations

import json
import math
import urllib.request
from pathlib import Path

import h5py
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
GW_CACHE = DATA / "chains" / "gw_posteriors"
RESULTS = ROOT / "results"

LANDMARKS = {
    "GW150914": "canonical_BBH",
    "GW170817": "BNS_standard_siren",
    "GW190521_074359": "high_mass_BBH",
    "GW190814": "asymmetric_mass_ratio",
}

PLANES = [
    ("mass_1_source", "mass_2_source"),
    ("chirp_mass_source", "mass_ratio"),
    ("mass_ratio", "chi_eff"),
    ("final_mass_source", "final_spin"),
    ("luminosity_distance", "cos_iota"),
    ("redshift", "total_mass_source"),
]


def psi_rho(x, y):
    C = np.cov(np.vstack([x, y]))
    vals, vecs = np.linalg.eigh(C)
    u = vecs[:, int(np.argmax(vals))]
    psi = math.degrees(math.atan2(u[1], u[0])) % 180.0
    rho = C[0, 1] / math.sqrt(C[0, 0] * C[1, 1])
    ratio = math.sqrt(vals.max() / vals.min()) if vals.min() > 0 else float("inf")
    return {
        "psi": round(float(psi), 2),
        "rho": round(float(rho), 3),
        "axis_ratio": round(float(ratio), 2),
    }


def find_posterior_dataset(h5):
    preferred = [
        "C01:Mixed/posterior_samples",
        "C01:IMRPhenomXPHM/posterior_samples",
    ]
    for key in preferred:
        if key in h5:
            return key
    found = []
    h5.visititems(lambda name, obj: found.append(name) if isinstance(obj, h5py.Dataset) and name.endswith("posterior_samples") else None)
    if not found:
        raise KeyError("no posterior_samples dataset found")
    return sorted(found)[0]


def read_event_chain(event, path):
    with h5py.File(path, "r") as h5:
        ds_name = find_posterior_dataset(h5)
        arr = h5[ds_name][()]
    names = set(arr.dtype.names or [])
    planes = {}
    for xname, yname in PLANES:
        if xname not in names or yname not in names:
            continue
        x = np.asarray(arr[xname], dtype=float)
        y = np.asarray(arr[yname], dtype=float)
        ok = np.isfinite(x) & np.isfinite(y)
        if ok.sum() < 100:
            continue
        g = psi_rho(x[ok], y[ok])
        g.update({
            "x_median": round(float(np.median(x[ok])), 4),
            "y_median": round(float(np.median(y[ok])), 4),
            "x_q16_q84": [round(float(q), 4) for q in np.quantile(x[ok], [0.16, 0.84])],
            "y_q16_q84": [round(float(q), 4) for q in np.quantile(y[ok], [0.16, 0.84])],
        })
        planes[f"{xname}__{yname}"] = g
    return {
        "event": event,
        "source": "posterior_hdf5",
        "path": str(path.relative_to(ROOT)),
        "posterior_dataset": ds_name,
        "n_samples": int(len(arr)),
        "planes": planes,
    }


def gwosc_catalog():
    url = "https://gwosc.org/eventapi/json/GWTC/"
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)["events"]


def fetch_summary(catalog, common_name):
    matches = [e for e in catalog.values() if e.get("commonName") == common_name]
    if not matches:
        return None
    # Prefer the highest version among matching releases.
    ev = sorted(matches, key=lambda e: (str(e.get("catalog.shortName")), int(e.get("version") or 0)))[-1]
    params = {}
    for p in [
        "mass_1_source", "mass_2_source", "chirp_mass_source", "total_mass_source",
        "final_mass_source", "final_spin", "chi_eff", "luminosity_distance", "redshift",
        "network_matched_filter_snr", "far", "p_astro",
    ]:
        if ev.get(p) is not None:
            params[p] = {
                "median": ev.get(p),
                "lower": ev.get(p + "_lower"),
                "upper": ev.get(p + "_upper"),
                "unit": ev.get(p + "_unit"),
            }
    return {
        "event": common_name,
        "class": LANDMARKS[common_name],
        "catalog": ev.get("catalog.shortName"),
        "version": ev.get("version"),
        "jsonurl": ev.get("jsonurl"),
        "summary_params": params,
    }


def classify_support(summaries, chains):
    supported = []
    disfavored = []
    open_items = []

    if len(chains) >= 2:
        supported.append("Actual GW posterior chains can be reduced to the same value/shape geometry objects used in the cosmology atlas.")

    gw190814 = next((c for c in chains if c["event"] == "GW190814"), None)
    if gw190814:
        mr = gw190814["planes"].get("mass_1_source__mass_2_source", {})
        qchi = gw190814["planes"].get("mass_ratio__chi_eff", {})
        supported.append(
            "GW190814 is geometrically sharp and asymmetric: its mass plane has "
            f"rho={mr.get('rho')} and axis_ratio={mr.get('axis_ratio')}, while mass-ratio/spin has "
            f"rho={qchi.get('rho')}."
        )

    gw190521 = next((c for c in chains if c["event"] == "GW190521_074359"), None)
    if gw190521:
        fm = gw190521["planes"].get("final_mass_source__final_spin", {})
        supported.append(
            "GW190521_074359 provides a high-mass BBH geometry anchor, including final-mass/final-spin "
            f"rho={fm.get('rho')} and axis_ratio={fm.get('axis_ratio')}."
        )

    disfavored.append("The idea that all compact-binary events have interchangeable posterior geometry.")
    disfavored.append("A first-pass claim of quantum-gravity or no-hair violation; E38 is an observational-geometry test, not a GR-deviation fit.")
    open_items.append("Extend to more posterior HDF5 files from GWOSC/Zenodo and run event-family clustering.")
    open_items.append("For actual GR tests, ingest LVK inspiral-merger-ringdown, ringdown, dispersion, polarization, or parameterized-deviation products.")
    open_items.append("For cosmological gravity, use standard-siren distance-redshift likelihoods rather than BBH mass/spin geometry.")
    return supported, disfavored, open_items


def main():
    chains = []
    for path in sorted(GW_CACHE.glob("*_PE.h5")):
        event = path.name[:-6]
        chains.append(read_event_chain(event, path))

    catalog = gwosc_catalog()
    summaries = [fetch_summary(catalog, name) for name in LANDMARKS]
    summaries = [s for s in summaries if s is not None]

    supported, disfavored, open_items = classify_support(summaries, chains)

    out = {
        "prereg": "preregs/E38_gw_black_hole_geometry_prereg.md",
        "question": "Can real GW event posteriors be explored with the value/shape geometry framework?",
        "data_sources": {
            "gwosc_catalog": "https://gwosc.org/eventapi/json/GWTC/",
            "cached_hdf5": [c["path"] for c in chains],
            "n_cached_hdf5": len(chains),
            "note": "Raw HDF5 posterior files are ignored by git; only derived geometry is committed.",
        },
        "landmark_summaries": summaries,
        "posterior_chain_geometry": chains,
        "supported": supported,
        "disfavored": disfavored,
        "open": open_items,
        "bottom_line": (
            "Supported: real GW posterior samples can be mapped into the same geometry language, "
            "and landmark events occupy visibly different black-hole geometry regimes. Not supported: "
            "any claim of quantum-gravity or GR violation from this first geometry pass."
        ),
    }
    path = RESULTS / "e38_gw_black_hole_geometry_results.json"
    path.write_text(json.dumps(out, indent=2))

    print("E38 GW black-hole posterior geometry\n")
    print(f"  landmark summaries: {len(summaries)}")
    print(f"  actual posterior chains read: {len(chains)}")
    for c in chains:
        print(f"  {c['event']}: n={c['n_samples']} planes={len(c['planes'])} [{c['posterior_dataset']}]")
        for pname, g in c["planes"].items():
            print(f"    {pname}: psi={g['psi']:.1f} rho={g['rho']:+.3f} axis_ratio={g['axis_ratio']:.1f}")
    print("\n  SUPPORTED:")
    for s in supported:
        print(f"  - {s}")
    print("\n  DISFAVORED:")
    for s in disfavored:
        print(f"  - {s}")
    print("\n  OPEN:")
    for s in open_items:
        print(f"  - {s}")
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
