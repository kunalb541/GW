# E68 lab notebook - the nanohertz GWB across four PTAs: pure degeneracy-sliding, and gamma marches with time span

Prereg: preregs/E68_pta_gwb_anatomy_prereg.md (locked + pushed before analysis). First application
of the value/shape machinery to the nanohertz GW band. Real public chains, all validated against
their publications before use:

| probe | chain | log10A@1/yr | gamma | rho(A,gam) | psi |
|---|---|---|---|---|---|
| NANOGrav 15yr (HD) | fig-1 release, nano15_hd_chain_long | -14.20+/-0.14 | 3.25+/-0.36 | -0.91 | 110 |
| EPTA DR2full (HD)  | Zenodo 8091568 hd_pl | -14.56+/-0.21 | 4.21+/-0.42 | -0.94 | 116 |
| PPTA DR3 (CRN)     | github PPTA-DR3 pl_nocorr_freegam_DE440 | -14.51+/-0.16 | 3.87+/-0.37 | -0.85 | 111 |
| EPTA DR2new (HD, robustness) | Zenodo 8091568 | -13.98+/-0.24 | 2.79+/-0.62 | -0.95 | 111 |

(NANOGrav's own tarball [Zenodo 8423265] contains timing data only - the GWB chain lives in the
fig-1 data release linked from github nanograv/15yr_stochastic_analysis. CPTA DR1: no public GWB
chain [Zenodo 13828113 = single-pulsar noise plots only]; excluded per prereg.)

## D1 - mutual consistency: all pairs agree

NANOGrav-EPTAfull 1.80 sigma; NANOGrav-PPTA 1.50; EPTA-PPTA 1.03. Every pair Gaussian-faithful
(E48 sliced-W ratio 0.98-1.01) and value-dominated at fixed orientation (vf_orientation-only
0.91-0.99, delta-rho <= 0.09). No pair reaches the 2-sigma flag.

## D2 - the headline: inter-PTA differences are PURE degeneracy-sliding

The constraint GEOMETRY is universal (rho -0.85..-0.95, psi 110-116 deg - one measurement kernel,
like the cosmology probes' kernel classes), and the pairwise mean offsets lie
**94.6-99.9% along the common A-gamma degeneracy axis** (mean 0.98; locked threshold 2/3):

- NANOGrav | EPTAfull: 0.999
- NANOGrav | PPTA: 0.994
- EPTAfull | PPTA: 0.946

Classification (locked): degeneracy-sliding. Everything the PTAs currently disagree about lives in
the direction a common power-law fit slides when the same spectrum is read over different bands.
The prereg caveat is now the interesting part: this signature cannot distinguish "band/convention
artifact" from "the true spectrum is not a power law" - a bend/turnover produces exactly this.

## D3 - gamma = 13/3 (SMBHB circular): NANOGrav alone carries the exclusion

z-scores: NANOGrav +3.03; EPTA-full +0.29; PPTA +1.25 (1 of 3 PTAs above 2). The "PTA data
disfavor the circular-GWB prediction" narrative currently rests on a single experiment - the same
anatomy as the H0 tension's SH0ES dependence (E52). No combined number is fabricated (E58 lesson).

## POST-HOC (exploratory, labelled): gamma is strictly monotonic in observing span

| span | dataset | gamma |
|---|---|---|
| 10.3 yr | EPTA DR2new | 2.79 |
| 16.0 yr | NANOGrav 15yr | 3.25 |
| 18.0 yr | PPTA DR3 | 3.87 |
| 24.7 yr | EPTA DR2full | 4.21 |

Perfectly ordered, including EPTA's INTERNAL split (DR2new vs DR2full: same telescopes, 1.89 sigma
apart, offset also along the degeneracy) - so the ordering is not a telescope effect. Longer span =
more low-frequency leverage = steeper fitted slope: the coherent signature of a spectrum that
FLATTENS at high frequency relative to a single power law (or a span-correlated systematic, e.g.
unmodeled red-noise absorption). Statistics are honest-weak (4 datasets, 2 dependent; p ~ 1/24
one-sided if independent). This is the E68 successor prediction, now on record: **in IPTA DR3 /
NANOGrav 20yr-class data, the fitted gamma of longer-span subsets should sit systematically above
shorter-span subsets of the same array** - preregisterable the day those chains are public.

## Reading

The four PTA measurements are one consistent object: a universal constraint geometry, offsets
confined to the degeneracy direction, and a gamma that marches with time span. Under the
value/shape anatomy there is no evidence of genuine inter-experiment disagreement (contrast: the
cosmology S8/H0 network) - but also no support yet for the gamma=13/3 exclusion narrative beyond
NANOGrav. The discriminating observable is the span-ordering, which points at spectral curvature -
testable out-of-sample with the next data releases.

## Verification

4 contract tests (self-pair null; degeneracy projection exact 1/0; rho/psi conventions;
pure-mean-shift classification). Headlines independently re-derived (np.corrcoef/np.cov path):
NG gam 3.248 / A -14.195 / rho -0.905 / z 3.03; EPTAf 4.191 / -14.536 / -0.943; NG-EPTAf sig 1.801.
All probe values match publications (NG15: -14.19+0.15-0.14, 3.2+/-0.6; EPTA DR2new 2.71; PPTA
3.87+/-0.36).

Code: src/e68_pta_gwb_anatomy.py. Numbers: results/e68_pta_gwb_anatomy_results.json.
Data: data/chains/pta/ (gitignored; Zenodo 8091568, PPTA-DR3 github, NANOGrav fig-1 release).
