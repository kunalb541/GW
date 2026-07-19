#!/usr/bin/env python3
"""E83 - a from-scratch strain pipeline (numpy/scipy only) + GW250114 chirp/ringdown validation.
CAPABILITY + CONSISTENCY CHECK (not a precision Bayesian ringdown). Establishes strain-level analysis for
the program: download GWOSC strain, whiten with an off-source PSD, recover the chirp (instantaneous
frequency) and the ringdown (dominant frequency + damping time), and cross-check against the E74 Kerr QNM
prediction (from the PE remnant + Berti-Cardoso-Will fits). This unlocks the strain-level tests (data-driven
frequency geometry, ringdown-geometry bridge, and -- with systematic controls -- the exotic-echo class).
Seed 83. Data: data/strain/ (gitignored; GWOSC O4b_4KHZ_R1). GW250114 GPS ~ 1420878141.22."""
import os, sys, json, math
import numpy as np
from scipy.signal import welch, butter, filtfilt, hilbert

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STRAIN = os.path.join(ROOT, "data/strain/H-H1_GW250114_4KHZ.hdf5")
FS = 4096.0

# ---------- reusable pipeline ----------
def whiten(seg, fs, psd_freq, psd):
    N = len(seg); S = np.fft.rfft(seg * np.hanning(N)); f = np.fft.rfftfreq(N, 1 / fs)
    asd = np.interp(f, psd_freq, np.sqrt(psd))
    return np.fft.irfft(S / asd, n=N)

def bandpass(x, fs, lo, hi):
    b, a = butter(4, [lo, hi], btype="band", fs=fs); return filtfilt(b, a, x)

def inst_frequency(x, fs):
    return np.gradient(np.unwrap(np.angle(hilbert(x)))) * fs / (2 * math.pi)

def ringdown_fit(x, fs, n_ms=25, n_env=60):
    """dominant QNM frequency (FFT peak) + damping time (log-envelope slope) of a post-peak segment."""
    rd = x[:int(n_ms * 1e-3 * fs)]; t = np.arange(len(rd)) / fs
    F = np.abs(np.fft.rfft(rd * np.hanning(len(rd)))); ff = np.fft.rfftfreq(len(rd), 1 / fs)
    fdom = float(ff[np.argmax(F)])
    env = np.abs(hilbert(rd)); ok = env > 0
    tau = float(-1.0 / np.polyfit(t[ok][:n_env], np.log(env[ok][:n_env]), 1)[0])
    return fdom, tau

# ---------- GW250114 validation ----------
def main():
    import h5py
    if not os.path.exists(STRAIN):
        print(f"strain not found: {STRAIN}\nfetch: curl -sL -o {STRAIN} \\\n"
              "  https://gwosc.org/archive/data/O4b_4KHZ_R1/1420820480/"
              "H-H1_GWOSC_O4b_4KHZ_R1-1420877824-4096.hdf5"); return
    with h5py.File(STRAIN, "r") as h:
        strain = np.asarray(h["strain/Strain"]); gps0 = h["meta/GPSstart"][()]
    im = int((1420878141.22 - gps0) * FS)
    clean = strain[im - 40 * int(FS): im - 8 * int(FS)]
    fpsd, Pxx = welch(clean, fs=FS, nperseg=int(4 * FS))
    seg = strain[im - 4 * int(FS): im + 4 * int(FS)].copy(); N = len(seg)
    wb = bandpass(whiten(seg, FS, fpsd, Pxx), FS, 30, 400)
    t = (np.arange(N) - N // 2) / FS
    ipk = np.argmax(np.abs(wb) * (np.abs(t) < 0.1)); peak_sigma = float(np.abs(wb)[ipk])

    finst = inst_frequency(wb, FS)
    chirp = {f"{int(dt*1e3):+d}ms": round(float(np.median(finst[ipk + int(dt*FS) - 20: ipk + int(dt*FS) + 20])), 1)
             for dt in (-0.02, -0.01, -0.005, 0.0, 0.005)}
    fdom, tau = ringdown_fit(wb[ipk:], FS)

    E74 = {"f220_Hz": 248.9, "tau220_ms": 4.10}
    df = abs(fdom - E74["f220_Hz"]) / E74["f220_Hz"]; dtau = abs(tau * 1e3 - E74["tau220_ms"]) / E74["tau220_ms"]
    consistent = df < 0.1 and dtau < 0.3

    print(f"GW250114 H1: peak {peak_sigma:.0f} sigma (loudest event to date)")
    print(f"chirp f_inst rising through merger: {chirp}")
    print(f"ringdown: f_dom = {fdom:.0f} Hz (E74 Kerr {E74['f220_Hz']}), tau = {tau*1e3:.1f} ms (E74 {E74['tau220_ms']})")
    print(f"  fractional: df={df*100:.1f}%  dtau={dtau*100:.0f}%  -> "
          f"{'CONSISTENT with E74 Kerr prediction' if consistent else 'INCONSISTENT'}")
    print("  (crude single-detector, single-mode, peak-start fit: a consistency check, not a precision QNM)")

    json.dump({"battery": "E83 strain pipeline + GW250114 validation (capability/consistency)",
               "event": "GW250114_082203", "peak_sigma_whitened": peak_sigma,
               "chirp_f_inst_Hz": chirp, "ringdown_fdom_Hz": fdom, "ringdown_tau_ms": tau * 1e3,
               "E74_kerr_prediction": E74, "frac_freq_diff": df, "frac_tau_diff": dtau,
               "consistent_with_E74": bool(consistent),
               "note": "from-scratch numpy/scipy pipeline (no gwpy). Establishes strain-level analysis; the "
                       "single-mode point-estimate has few-% bias vs a proper Bayesian multi-mode ringdown. "
                       "Successor: Bayesian ringdown + the data-driven frequency-geometry test (E73 successor); "
                       "exotic-echo/DM-rotation tests only AFTER pipeline validation on more events + controls."},
              open(os.path.join(ROOT, "results/e83_strain_ringdown_results.json"), "w"), indent=2)
    print("\nwrote results/e83_strain_ringdown_results.json")

if __name__ == "__main__":
    main()
