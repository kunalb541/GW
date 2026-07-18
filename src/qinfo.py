#!/usr/bin/env python3
"""qinfo - quantum-information toolbox for value/shape probe posteriors.

Foundation (verified numerically in E62): for a probe posterior covariance C,
    rho = C / Tr(C)
is a valid density matrix (PSD, unit trace), and the value/shape Bures 'shape' term equals
1/4 the quantum Fisher metric on these states. So the QI toolbox applies to cosmology Fisher
matrices, with value/shape as one entry.

IMPORTANT distinction:
- QUANTUM measures (qrelent/qfidelity/qhelstrom/qchernoff/purity/vn_entropy) act on rho=C/TrC:
  they capture SHAPE (covariance orientation/concentration) distinguishability ONLY -- they IGNORE
  the mean. Use for parametrization-invariant probe-geometry comparison and per-probe figures of merit.
- CLASSICAL Gaussian measures (gauss_kl/gauss_bhattacharyya/gauss_chernoff) use (mu, C): they include
  the MEAN (value) term and are the physically-relevant model/probe discrimination (e.g. LCDM vs w0wa).
"""
import numpy as np
from numpy.linalg import eigh, slogdet, inv, det

# ---------- density matrix + spectral helpers ----------
def density(C):
    C = np.asarray(C, float); return C / np.trace(C)

def _spec(rho):
    w, V = eigh(rho); w = np.clip(w, 0, None); return w, V

def _fpow(rho, p):
    w, V = _spec(rho); return (V * np.where(w > 1e-15, w**p, 0.0)) @ V.T

def _flog(rho):
    w, V = _spec(rho); lw = np.where(w > 1e-15, np.log(w), 0.0); return (V * lw) @ V.T

# ---------- QUANTUM measures on rho = C/Tr(C) (shape-only) ----------
def purity(rho):            # Tr(rho^2) in [1/d, 1]; 1 = pure (rank-1, fully anisotropic)
    w, _ = _spec(rho); return float(np.sum(w**2))

def vn_entropy(rho):        # -Tr(rho ln rho); 0 = pure, ln(d) = maximally mixed (isotropic)
    w, _ = _spec(rho); w = w[w > 1e-15]; return float(-np.sum(w * np.log(w)))

def qrelent(rho, sigma):    # Umegaki S(rho||sigma) = Tr[rho(ln rho - ln sigma)] >= 0
    val = float(np.trace(rho @ (_flog(rho) - _flog(sigma))).real)
    return max(val, 0.0)

def qfidelity(rho, sigma):  # Uhlmann F = (Tr sqrt(sqrt(rho) sigma sqrt(rho)))^2 in [0,1]
    sr = _fpow(rho, 0.5); inner = sr @ sigma @ sr
    w, _ = _spec(inner); return float(np.sum(np.sqrt(np.clip(w, 0, None)))**2)

def qhelstrom_perr(rho, sigma, p=0.5):   # min error prob distinguishing rho vs sigma (priors p,1-p)
    A = p * rho - (1 - p) * sigma
    w, _ = eigh(A); return float(0.5 * (1 - np.sum(np.abs(w))))

def qchernoff(rho, sigma, ns=201):       # xi = -ln min_s Tr(rho^s sigma^(1-s)); optimal error EXPONENT
    ss = np.linspace(0, 1, ns)
    Q = [float(np.trace(_fpow(rho, s) @ _fpow(sigma, 1 - s)).real) for s in ss]
    Q = np.clip(Q, 1e-300, None); i = int(np.argmin(Q))
    return float(-np.log(Q[i])), float(ss[i])

# ---------- CLASSICAL Gaussian measures on (mu, C) (value + shape) ----------
def gauss_kl(mu1, C1, mu2, C2):          # KL(N1 || N2)
    mu1 = np.asarray(mu1, float); mu2 = np.asarray(mu2, float)
    k = len(mu1); C2i = inv(C2); dmu = mu2 - mu1
    s1, ld1 = slogdet(C1); s2, ld2 = slogdet(C2)
    return float(0.5 * ((ld2 - ld1) - k + np.trace(C2i @ C1) + dmu @ C2i @ dmu))

def gauss_bhattacharyya(mu1, C1, mu2, C2):   # D_B; error ~ exp(-D_B); = 1/8 Mahalanobis^2 if C1=C2
    mu1 = np.asarray(mu1, float); mu2 = np.asarray(mu2, float)
    Cb = 0.5 * (C1 + C2); dmu = mu2 - mu1
    s, ldb = slogdet(Cb); s1, ld1 = slogdet(C1); s2, ld2 = slogdet(C2)
    return float(0.125 * dmu @ inv(Cb) @ dmu + 0.5 * (ldb - 0.5 * (ld1 + ld2)))

def gauss_chernoff(mu1, C1, mu2, C2, ns=201):    # xi = -ln min_s exp(-K(s)); optimal error exponent
    mu1 = np.asarray(mu1, float); mu2 = np.asarray(mu2, float); dmu = mu2 - mu1
    s1, ld1 = slogdet(C1); s2, ld2 = slogdet(C2)
    def K(s):
        Cs = s * C1 + (1 - s) * C2; ss, lds = slogdet(Cs)
        return 0.5 * s * (1 - s) * dmu @ inv(Cs) @ dmu + 0.5 * (lds - (s * ld1 + (1 - s) * ld2))
    ss = np.linspace(1e-3, 1 - 1e-3, ns); vals = [K(s) for s in ss]
    i = int(np.argmax(vals)); return float(vals[i]), float(ss[i])   # xi = max_s K(s)
