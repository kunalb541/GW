#!/usr/bin/env python
"""Render the cosmo2 consolidated lab notebook to REPORT.pdf (reportlab).

Plain lab-notebook layout (not a paper). ASCII-safe notation throughout to avoid
missing-glyph boxes in the built-in fonts. Run:  python -m src.build_report_pdf
"""
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)

OUT = Path(__file__).resolve().parent.parent / "REPORT.pdf"
ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=14, spaceBefore=12, spaceAfter=4)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=11.5, spaceBefore=8, spaceAfter=2)
BODY = ParagraphStyle("Body", parent=ss["Normal"], fontSize=9.3, leading=12.6, spaceAfter=5)
SMALL = ParagraphStyle("Small", parent=ss["Normal"], fontSize=8.2, leading=10.5, textColor=colors.HexColor("#444"))
TITLE = ParagraphStyle("Title", parent=ss["Title"], fontSize=18, spaceAfter=2)


def b(label, text):
    return Paragraph(f"<b>{label}</b> {text}", BODY)


def tbl(data, widths):
    t = Table(data, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2d3d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8.2),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bbbbbb")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f4f7")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def main():
    s = []
    s.append(Paragraph("cosmo2 - Consolidated Lab Notebook", TITLE))
    s.append(Paragraph("Value/shape geometry of the expansion history (V2 of cosmo). "
                       "Kunal Bhatia - ORCID 0009-0007-4447-6325.", SMALL))
    s.append(Paragraph("Plain running record - not a paper. Per-battery detail in "
                       "REPORT_E1..E29.md. 41 tests pass; pre-registrations locked before runs "
                       "(E4 exploratory-then-formalized). Repo: kunalb541/cosmo2 (private).", SMALL))
    s.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#1f2d3d"), spaceBefore=6, spaceAfter=8))

    s.append(Paragraph("What this is", H1))
    s.append(Paragraph("V2 of <i>cosmo</i> (V1). V1 showed structure-growth probe "
        "disagreements carry a value/shape geometry organized by the lensing kernel in "
        "(Omega_m, sigma_8). cosmo2 carries the same machinery - value/shape (W2/Bures) "
        "decomposition + constraint-orientation angle psi + a first-principles kernel "
        "forecast - onto the EXPANSION HISTORY, then back to the growth sector to connect "
        "with V1.", BODY))

    s.append(Paragraph("Data (public; md5 in data/provenance.json)", H2))
    s.append(Paragraph("Cosmic chronometers H(z) (31 pts); Pantheon+/SH0ES (full STAT+SYS "
        "cov); DES-Y5 (Dovekie); DESI DR2 BAO compressed likelihood; DESI DR2 cobaya chains "
        "(Zenodo 16644577: base, w, w_wa, omegak_w_wa, mnu_w_wa x DESI+CMB +/- SN); Planck "
        "CMB-only base chain; SDSS DR16 full-shape f-sigma8 (LRG, QSO). Chains (1.3 GB) "
        "gitignored.", BODY))

    s.append(Paragraph("Running log of results", H1))

    s.append(b("Forecast (data-free, locked) - validated.",
        "Kernel-Fisher Level-A predicts each probe's degeneracy angle from redshift "
        "sampling + observable derivative alone. Measured vs predicted:"))
    s.append(tbl([["probe", "class", "forecast psi", "measured psi", "residual"],
                  ["cosmic chronometers", "direct-rate", "115.7", "115.0", "0.7"],
                  ["Pantheon+", "integrated-distance", "104.7", "101.7", "3.0"],
                  ["DES-Y5", "integrated-distance", "101.8", "101.6", "0.2"]],
                 [1.7*inch, 1.5*inch, 0.9*inch, 0.95*inch, 0.7*inch]))
    s.append(Spacer(1, 6))

    s.append(b("(q0,j0) is the weak plane.",
        "Chronometer-vs-SN orientation split only 13 deg (forecast ~11). Survives "
        "z-matching (kernel-driven, not coverage) and is basis-invariant. Cosmographic "
        "MEAN MLE diverges for wide-z probes (Taylor truncation) -> quantitative mean "
        "decomposition there is gated out."))

    s.append(b("(H0,r_d) - Outcome A (read as consistent-with, not a clean confirmation).",
        "DESI's standard-ruler degeneracy (H0*r_d fixed to 0.6%) sits 45.0 deg from the "
        "r_d-free axis in the scale-free (log) basis -- exactly at the locked >45 deg trigger "
        "(cleared only via a >45-1e-6 relaxation; 24.6 deg in physical units, below "
        "threshold). The orientations are constructed; the data-driven content is DESI's "
        "0.6% precision + chronometer H0=67.8, not the angle. So: consistent with the "
        "distance-redshift kernel organizing expansion orientations, not a clean transfer of "
        "V1's result. Data correction from the real Planck chain: CMB sits at psi=9.7 deg, "
        "rho(H0,r_d)=+0.69 (positive) - NOT the BAO ruler orientation the forecast assumed; "
        "(H0,r_d) has three orientations (BAO 135, r_d-free 90, CMB ~10), not two classes."))

    s.append(b("The SN-sample DEPENDENCE of the DESI evolving-DE preference is VALUE-dominated,",
        "shown two independent ways (cosmographic null + native chains; the latter "
        "cross-checked three non-independent ways on the same chains):"))
    for line in [
        "cosmographic LambdaCDM null: DESI vs Pantheon+ value fraction 96-100% across BAO "
        "z-cuts; conservative 3.6 sigma (6.8 full-sample is truncation-inflated by the "
        "high-z Lya point).",
        "native (w0,wa) chains: the three SN samples share orientation (spread 2.6 deg) and "
        "differ only in mean -> value fractions 90-100%. Reproduces published DR2 (w0,wa).",
        "per-sample significance: evolving-DE 3.0/3.8/4.3 sigma (Pantheon+/Union3/DES-Y5) "
        "vs LambdaCDM; the SN choice moves the result noticeably (descriptive scatter "
        "scale ~1.7-2.6 sigma depending on metric -- not a formal consistency test).",
        "slide test: adding any SN shifts the (w0,wa) mean 100% ALONG the DESI+CMB "
        "degeneracy (reorients <=5.8 deg) -> SNe add value along a fixed shape."]:
        s.append(Paragraph("&bull; " + line, ParagraphStyle("li", parent=BODY, leftIndent=12, spaceAfter=3)))

    s.append(b("Slide is universal across DE models (U).",
        "The 100%-along-degeneracy result holds in w0wa, +Omega_k, +sum-m_nu (DESI+CMB psi "
        "stable ~108-109 deg). Value-dominance is generic, not w0wa-specific."))
    s.append(b("Growth vs geometry (M).",
        "SDSS DR16 f-sigma8 is a mostly-distinct axis from the (D_M,D_H) geometry at low z "
        "(LRG |corr| 0.17-0.39) but couples at high z (QSO 0.64)."))
    s.append(b("Growth joins V1's lensing-amplitude class (L) - the bridge.",
        "Placing f-sigma8 in V1's (Omega_m,sigma_8) plane via the LambdaCDM growth model "
        "gives psi=172.5 deg, rho(Omega_m,sigma_8)=-0.70, gamma-robust -> RSD/f-sigma8 sits "
        "in V1's negative-correlation class with shear + CMB lensing."))
    s.append(b("The late-time tensions do NOT share a direction (F) - most discovery-shaped.",
        "In all 9 DESI+CMB+SN w0wa-family chains, moving along the evolving-DE direction "
        "drives H0 DOWN (dH0 in [-2.43,-0.65], away from SH0ES -> worsens H0) while "
        "sigma_8/S8 is untouched (|d-sigma8|<0.02). So H0 and DESI-DE are mutually "
        "frustrating (anti-aligned) and S8 is decoupled (orthogonal). No single lever "
        "resolves all three."))
    s.append(b("V1's two classes are one continuous psi(alpha) law (1L).",
        "Every (Omega_m,sigma_8) amplitude probe is placed by its Omega_m-exponent alpha in "
        "sigma_8*Omega_m^alpha via psi(alpha)=atan2(-(sigma_8/Omega_m)*alpha,1). Textbook "
        "exponents predict V1-measured orientations to <5 deg (shear 0.50->128 vs 126; CMB "
        "lensing 0.25->147 vs 152). Probes order on one curve: primary CMB (a=-0.27) -> "
        "growth (a=0.05) -> CMB lensing (a=0.21) -> shear (a=0.54). The two 'classes' are "
        "the a<0 and a>0 arcs of one continuum; growth fills the small-alpha end."))

    s.append(b("The value signal is NOT one BAO tracer (controversy check).",
        "Leave-one-tracer-out on DESI DR2 BAO: at full z-range only the high-z Lya bin "
        "moves the DESI-vs-Pantheon+ separation (47%, the E1 truncation effect); in the "
        "valid z<=1.5 range the 3.6 sigma value signal is DISTRIBUTED (max single removal "
        "11%) and the historical LRG z=0.51 bin does NOT drive it (-5%). Contrary to the "
        "'one anomalous bin' narrative."))
    s.append(b("The DESI dark-energy signal itself is SHAPE (evolution), not value.",
        "Decomposing (w0,wa) at the best-constrained pivot: the EoS value w_p is consistent "
        "with -1 (0.6-1.9 sigma) for all SN samples, while the evolution wa is the detection "
        "(3.0-3.9 sigma). 'Evolving dark energy' is literally a time-evolution (shape) "
        "statement. Layered with E1: the SN-sample DEPENDENCE is value (anchor), the SIGNAL "
        "is shape (evolution)."))
    s.append(b("The DESI-DE evidence is robust to curvature/neutrino mass (R).",
        "The 2D (w0,wa)-from-LambdaCDM distance changes <=14% when Omega_k or sum-m_nu is "
        "opened (Pantheon+ 3.0->2.6/2.9, DES-Y5 4.3->4.0/4.2) -> not a curvature/neutrino "
        "degeneracy."))

    s.append(Paragraph("All-instrument sweep (E14-E18) - real chains, all three sectors", H1))
    s.append(tbl([["sector / plane", "instruments (real chains)", "result"],
                  ["Dark energy (w0,wa)", "DESI DR2 x {Pantheon+,Union3,DES-Y5,Dovekie} x {CamSpec/plik} x {w0wa,+Ok,+mnu}; unimpeded grid",
                   "value-spread about a shared shape; cross-validated"],
                  ["S8 (Om,sigma8)", "Planck, ACT DR6 lensing, KiDS-1000, DES-Y3, DES-Y1 3x2pt",
                   "two-class shape (CMB +rho vs lensing -rho); shape-dominated"],
                  ["H0 (axis)", "Planck, DESI, chronometers, GW GWTC-3 (real 69.3+/-12.9), JWST CCHP, TDCOSMO, SH0ES",
                   "SH0ES-outlier: all 8 cluster at early value, SH0ES 4.85 sigma off"]],
                 [1.3*inch, 3.3*inch, 2.2*inch]))
    s.append(Spacer(1, 6))
    s.append(b("On JWST (asked repeatedly, answered definitively).",
        "The most comprehensive public chain database, unimpeded (10 models x 77 datasets), has "
        "ZERO JWST datasets. JWST's cosmology product is the CCHP H0 MEASUREMENT -- a prior on "
        "one number (encoded like SH0ES's H0.riess2020Mb), not a likelihood/chain. JWST IS used, "
        "as H0, three ways (E10 anchor, E13 chain prior, E16 map). Its only non-H0 cosmology "
        "(high-z galaxy sigma8) is model-dependent, not released as chains. GW likewise measures "
        "H0 only (no sigma8), so it lives on the H0 axis, not the S8 consensus."))
    s.append(b("Grid-wide sweep (E18).",
        "13 chains from unimpeded, uniform pipeline: 7 walcdm dark-energy chains cluster at "
        "psi~102-106 with CMB (SN choice moves w0 -0.68->-0.85 / wa -0.57->-1.01 ALONG the "
        "degeneracy = value-spread); 6 lcdm S8 chains hold the two-class split (CMB +rho psi~24-31, "
        "weak-lensing -rho psi~100-114). Caveat: Planck-lensing-alone S8=1.46 is a degeneracy "
        "artifact (orientation ok, value not)."))

    s.append(Paragraph("Bottom line", H1))
    s.append(Paragraph("The value/shape geometry extends from structure growth (V1) to the "
        "expansion history. The distance-redshift kernel sets expansion orientations much as "
        "the lensing kernel set them in (Omega_m,sigma_8) (Outcome A, read as consistent-with "
        "given the basis-dependence). The SN-SAMPLE DEPENDENCE of the DESI DR2 evolving-dark-"
        "energy preference is value-dominated - a displacement in where each SN sample sits "
        "along a shared degeneracy, not a reorientation - robustly across the available DE "
        "models and extensions; the SIGNAL ITSELF, decomposed at its best-constrained pivot, "
        "is an evolution (shape) detection with w consistent with -1 at the pivot. The "
        "late-time tensions (H0, S8, DESI-DE) are three distinct directions, not one late-time "
        "cause. And V1's two-class split is well described by a single continuous law in the "
        "Omega_m-weighting exponent (near-definitional in form), now including the growth rate. "
        "This is a reframing and independent re-verification of largely known results in a "
        "value/shape formalism - not a claim of new physics.", BODY))

    s.append(Paragraph("Honesty ledger (corrections, negatives, limits)", H1))
    for line in [
        "Cosmographic ABSOLUTE quantities are truncation-biased beyond z~1: a cosmographic "
        "H0*r_d inverse-ladder gave a spurious ~9 sigma BAO-vs-CMB offset (BAO+CMB actually "
        "agree) - NOT reported as a tension. Cosmographic claims restricted to orientations.",
        "Forecast correction: the real Planck chain put CMB outside the BAO ruler class.",
        "E5's psi(alpha) form is near-definitional; the content is the <5 deg match to "
        "textbook exponents and the cross-class unification, not the curve itself.",
        "E3 bug caught+fixed: omitting the D(0) growth normalization first flipped the sign.",
        "E4 was exploratory-then-formalized; a clean confirmatory run is deferred to future data.",
        "No new physics is claimed anywhere; orientation structure is LambdaCDM-consistent "
        "measurement geometry. No paper - this is a lab notebook."]:
        s.append(Paragraph("&bull; " + line, ParagraphStyle("li2", parent=BODY, leftIndent=12, spaceAfter=3)))

    s.append(Paragraph("Battery map", H1))
    s.append(tbl([["battery", "question", "outcome", "report"],
                  ["E1", "value/shape on expansion; DESI dissection", "value-dominated; (H0,r_d) A", "REPORT_E1"],
                  ["E2", "slide universality; growth vs geometry", "U ; M", "REPORT_E2"],
                  ["E3", "growth in V1 (Omega_m,sigma_8) plane", "L (lensing-amplitude)", "REPORT_E3"],
                  ["E4", "do H0/S8/DE share a direction?", "F (frustrated/decoupled)", "REPORT_E4"],
                  ["E5", "is the two-class split one psi(alpha) law?", "1L (single law)", "REPORT_E5"],
                  ["E6", "is the value signal one BAO tracer?", "M (z<=1.5: not one-point-driven)", "REPORT_E6"],
                  ["E7", "is the EoS signal value or shape?", "SH (shape/evolution)", "REPORT_E7"],
                  ["E8", "does Omega_k/m_nu absorb DE evidence?", "R (robust)", "REPORT_E8"],
                  ["E9", "DE evidence vs CMB likelihood?", "DES-Y5 robust (4%)", "REPORT_E9"],
                  ["E10", "JWST anchor: H0 tension SH0ES-specific?", "SO (SH0ES-outlier)", "REPORT_E10"],
                  ["E11", "provenance-audited probe atlas", "63 records, audit PASS", "atlas_probes.json"],
                  ["E12", "consensus geometry over real chains", "value-spread, shared shape", "REPORT_E12"],
                  ["E13", "JWST/SH0ES H0 prior on the chains", "JWST ok; SH0ES collapses", "REPORT_E13"],
                  ["E14", "S8 tension on real chains (Planck+KiDS)", "shape-dominated (5%)", "REPORT_E14"],
                  ["E15", "full real-chain (Om,s8) consensus", "2class-shape (4 chains)", "REPORT_E15"],
                  ["E16", "complete H0 map incl real GW", "SH0ES-outlier (8 instr.)", "REPORT_E16"],
                  ["E17", "value/shape over unimpeded grid", "DE cross-validated; no JWST", "REPORT_E17"],
                  ["E18", "grid-wide sweep (13 chains)", "DE value-spread; S8 2-class", "REPORT_E18"],
                  ["E19", "psi(alpha) a validated universal relation?", "VALIDATED (<7 deg, 4 surveys)", "REPORT_E19"],
                  ["E20", "blind Stage-IV orientation forecasts", "LOCKED (shear 128, S4 147)", "REPORT_E20"],
                  ["E21", "three tension directions in one chain", "distinct; refines E4", "REPORT_E21"],
                  ["E22", "bridge to formal tension statistics", "API wired; rate-limited", "REPORT_E22"],
                  ["E23", "coherent shape residual under DESI?", "no-residual (honest null)", "REPORT_E23"],
                  ["E24", "synthetic validation (ground truth)", "PASS; spurious-DE FP 0%", "REPORT_E24"],
                  ["E25", "three headline figures + errors", "figs generated", "REPORT_E25"],
                  ["E26", "chain-processing + basis invariance", "robust (psi 0.1 deg)", "REPORT_E26"],
                  ["E27", "forecast vs random null + Fisher", "~7 sigma vs random", "REPORT_E27"],
                  ["E28", "leave-one-SN; model-ladder direction", "stable; direction survives", "REPORT_E28"],
                  ["E29", "master adversarial robustness table", "8/9 PASS, 1 null", "REPORT_E29"]],
                 [0.55*inch, 2.7*inch, 1.85*inch, 0.95*inch]))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Reproduce: per-battery <font face='Courier'>python -m src.e&lt;n&gt;_*</font> "
        "(see each REPORT_E*.md); <font face='Courier'>pytest tests/ -q</font> (41 tests). "
        "Generated from REPORT.md by src/build_report_pdf.py.", SMALL))

    SimpleDocTemplate(str(OUT), pagesize=letter, topMargin=0.7*inch, bottomMargin=0.7*inch,
                      leftMargin=0.8*inch, rightMargin=0.8*inch,
                      title="cosmo2 lab notebook", author="Kunal Bhatia").build(s)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
