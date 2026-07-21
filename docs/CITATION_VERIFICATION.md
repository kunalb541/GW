# CITATION VERIFICATION — every literature sentence in the narrowed manuscript (2026-07-21)

Scope: only references that support claims in `paper/manuscript.tex` as narrowed by the submission-gate
audit. Verification is at **full text** (ar5iv / journal HTML) except where marked. Convention inherited
from [NOVELTY.md](NOVELTY.md): nothing enters the manuscript on trust.

## Summary of actions taken

| # | citation | manuscript claim | verification | status | action |
|---|---|---|---|---|---|
| 1 | Suzuki et al. 2026 (arXiv:2605.03576) | GW250114 ringdown: overtone detected at 99.9%, no Kerr deviation | **full text** | verified, **needed narrowing** | narrowed — see §1 |
| 2 | Hannam et al. 2013 (ApJL 766 L14) | posterior lies along near-constant-$\mathcal{M}_c$ contours | **full text** | **verified** (verbatim) | promoted to the novelty sentence |
| 3 | Ohme et al. 2013 (PRD 88, 042002) | closest PCA neighbour | **full text** | **verified** | now cited (was uncited) |
| 4 | Fairhurst et al. 2023 (`simple-pe`) | metric ellipse = the local/linear approximation | **full text** | **verified** | now cited (was uncited) |
| 5 | Baird et al. 2013 (PRD 87, 024035) | constant-$\mathcal{M}_c$ stops describing the degeneracy at high mass | abstract + NOVELTY.md | verified for the caveat | now cited as a limitation |
| 6 | Cutler & Flanagan 1994; Poisson & Will 1995 | $\mathcal{M}_c$ is the best-measured mass combination | textbook, identity verified | verified | kept |
| 7 | Transtrum et al. 2015 | stiff/sloppy direction structure | identity verified | verified | kept |
| 8 | Hastie & Stuetzle 1989 | **their self-consistency DEFINITION, used as a testable property (E97)** | **full text** | **verified; claim upgraded** | now load-bearing — see §7 |
| 9 | Amari 2016 (Fisher–Rao) | "the content of Fisher–Rao information geometry" | — | **REMOVED** | ornamental; we compute no Fisher–Rao quantity |
| 10 | Backus & Gilbert 1968 | resolved/unresolved directions | — | **REMOVED** | ornamental; was already uncited in the body |
| 11 | Bernstein–von Mises | *(was: the tangent error is the error of the asymptotic Gaussian limit)* | — | **CLAIM WITHDRAWN, no citation needed** | §3 now claims only the elementary fact — see §8 |

**Reading order note.** Rows 8 and 11 changed status *after* this table was first written, in response to
an external review. The table above is current; §7 and §8 give the detail. Nothing below contradicts it.

---

## 1. Suzuki et al. 2026 — narrowed

**Manuscript said:** "published ringdown spectroscopy detects the overtone at $99.9\%$ confidence and finds
no deviation from the Kerr prediction, **confirming the no-hair theorem at record signal-to-noise**."

**Full text says:** the analysis is *"Ringdown Analysis of GW250114 with Orthonormal Modes"* (Suzuki,
Kubota, Morisaki, Motohashi, Watarai). The 99.9% is specific to their **orthonormal-mode** treatment, with
"the inferred significance increasing from 82.5% to 99.9%" relative to nonorthogonal analyses. On Kerr
consistency they report *"no significant deviation, consistent with previous analyses."*

**Why this needed narrowing.** (i) The 99.9% is not a generic result for the event; it is what the
orthonormal basis yields, and the same paper reports 82.5% without it. Quoting the higher number without
that context misrepresents the strength of the evidence. (ii) "No significant deviation" is a null result;
"confirming the no-hair theorem" is a positive claim the paper does not make. **Both corrected.**

**Placement (2026-07-21).** The GW250114 material now sits in Appendix~C rather than the body: it
supports none of the paper's claims and the ringdown results are other groups' work. The narrowing above
still applies to how it is quoted there --- the 99.9% figure is given with its orthonormal-basis context
and the 82.5% nonorthogonal value beside it, and the Kerr result is described as the null it is reported
to be.

**Related, and deliberately not cited:** Dey et al. (arXiv:2605.18595) also analyse GW250114 and report
that their Full-sky analysis samples extrinsic parameters *"jointly with remnant mass, spin, mode
amplitudes, and phases"* and that *"mode amplitude ratios remain consistent across approaches."* Verified
at full text during the E88 work. It supports no claim in the narrowed manuscript — the ringdown material
is not part of this paper — so it is not cited here. Recorded so the verification is not repeated.

## 2. Hannam et al. 2013 — verified verbatim, and it establishes the gap

Full text (ar5iv) contains, in the neutron-star-binaries section: *"The component masses consistent with the
signal lie roughly along a line of constant chirp mass."* Figure 2's caption confirms chirp mass is labelled
on the confidence regions. So the qualitative "banana along constant-$\mathcal{M}_c$" claim is **verified at
full text**, not merely assumed.

Equally important for the novelty sentence: the paper contains **no quantitative statement about the
orientation or principal axis** of the mass posterior. It is the closest visual neighbour and it stops short
of the measurement this manuscript makes. NOVELTY.md previously flagged the figure content as UNVERIFIED;
that flag is now cleared.

## 3. Ohme et al. 2013 — the closest PCA neighbour, and it is a different object

Full text: the PCA is applied to *"the PN coefficients themselves as free parameters rather than the
original physical parameters"* — i.e. to phase-expansion coefficients, **not** to $(m_1,m_2)$ posterior
samples. It predicts no per-event posterior orientation, and performs no catalog validation: the study is
theoretical, at a single fiducial system and SNR 20. This is precisely the distinction the novelty sentence
needs, so the paper is now cited there rather than left unused in the bibliography.

## 4. Fairhurst et al. 2023 (`simple-pe`) — verified, with a coordinate caveat

Full text confirms a Gaussian/metric approximation producing elliptical confidence regions, built by
assuming *"that the match varies quadratically with the difference in parameters"* — an explicitly local
expansion about a peak. The authors themselves note it breaks down and that they *"observe curved contours
rather than perfect ellipses."*

**Caveat now respected in the manuscript:** their metric is computed in $(\mathcal{M}, \eta)$ and spin
coordinates, **not** in $(m_1,m_2)$. So the manuscript says the ellipse is the same *local, linear* class of
approximation as our tangent, and does not claim the two are the same object in the same coordinates.

## 5. Baird et al. 2013 — cited as a limitation, not as support

Per NOVELTY.md (identity verified; correct attribution is **Baird**, not "Brown"), this paper concerns the
mass–**spin** degeneracy and explicitly caveats that at higher masses the degeneracy is not so clearly
characterised by constant chirp mass. That is a genuine bound on where a constant-$\mathcal{M}_c$
construction should be expected to work, so it is cited in the limitations rather than as support.

## 6. Removed as ornamental

The audit required that Fisher–Rao / Čencov / Bernstein–von Mises language be dropped unless such a quantity
is actually computed. It is not. **Amari 2016** was cited only to assert that the viewpoint "is the content
of Fisher–Rao information geometry", and **Backus & Gilbert 1968** was already uncited in the body after the
rewrite. Both removed from the bibliography.

## Outstanding and resolved items

- Cutler & Flanagan 1994 and Poisson & Will 1995 are used only for the textbook statement that
  $\mathcal{M}_c$ is the best-measured mass combination. Identity verified; not re-read at full text, since
  no specific numerical or figure content is claimed from them.
## 7. Hastie & Stuetzle 1989 — status changed, now load-bearing

- **STATUS CHANGED (external review).** This entry previously said "no specific
  claim is drawn from their contents". That is no longer true: since E97 the manuscript uses their
  **definition** of a principal curve by self-consistency, $f(t)=\mathbb{E}[X\mid t_f(X)=t]$, as a
  testable property, and reports a measurement against it. The definition was checked against the paper
  (Hastie & Stuetzle, *JASA* **84**, 502, 1989; self-consistency is their defining property, not a
  derived one). The citation now carries a specific, load-bearing claim and must be verified as such.
- **Bernstein–von Mises — USED WITHOUT A CITATION (external review).** Section 3 argues that a Gaussian
  posterior's principal axis *is* the local tangent, so the tangent error measures the error of the
  asymptotic Gaussian limit. That invokes the Bernstein–von Mises theorem by content while citing nothing.
  Either a standard reference must be added or the sentence must be rephrased to claim only the
  elementary geometric fact (a Gaussian's principal axis is its covariance eigenvector), which is what the
  argument actually needs. **Open.**
- Transtrum et al. 2015 supports the stiff/sloppy concept only; E98 measured that our own data does not
  support the hyperribbon geometry, and the manuscript says so.
- §6 (coherence) and §8–9 (information anatomy, GW250114) were originally reviewed for **citation
  integrity only**. A **claim-discipline pass** has since been done (2026-07-21, prose only, no new
  compute), and three things changed:
  1. §6's outlier-atlas null now states its own weakness — it is a null on $n=32$ events, so it bounds a
     large physical dependence rather than excluding one. It previously read as a clean "no physical axis
     survives" with no power statement.
  2. §6's `3σ` was a hand-typed literal in a paper where every other result number is generated; it is now
     the `\ExpNaiveSigma` macro, and the surviving atlas correlate carries its ρ and FDR q.
  3. §8 said the anatomy is "a map of what each detection measured". It is a forward-model computation, so
     it now says what the model *implies* each detection measured. The disclaimer that followed was already
     correct; the sentence it followed was not.

  §9 (GW250114) needed no change: it is labelled Context, its ringdown numbers are attributed to other
  groups, and our own retracted analysis is disclosed in it.


## Makinen et al. 2026 — added 2026-07-21, and a caution about how it reached us

`arXiv:2606.23838`, *The Degeneracy Distillery* (Makinen, Bartlett, Jeffrey, Wandelt). **Verified at the
arXiv abstract page**: title, author list, submission date and abstract content all confirmed.

It was suggested by an external LLM review as work that "attacks the same $\mathcal{M}_c$/$q$ problem
... so the posterior comes out round instead of stretched into the usual chirp-mass banana." **That
characterisation is wrong.** The paper is a general method: it detects degenerate parameter combinations
from the Fisher information and searches for symbolic coordinate transformations that flatten it, with
neural posterior estimation as a downstream beneficiary. It is not about gravitational-wave parameter
estimation and does not concern the chirp-mass/mass-ratio degeneracy specifically.

The citation was still worth adding — reparameterising a degeneracy away is a genuine complement to
characterising it in place — but it is cited for what it does, not for what the review said it does.
Recorded here because the failure mode is instructive: the reference existed and the identifier was
correct, so a citation check that stops at "does this paper exist?" would have passed it through with a
false description attached.

## Data and software citations (added 2026-07-21)

The manuscript previously had **no acknowledgments section and no data citation at all**, which is a
licence-compliance defect, not a stylistic one: GWOSC data are CC-BY and carry attribution obligations.
Now added, with verification status:

| citation | claim | status |
|---|---|---|
| GWOSC O3 data paper, ApJS **267**, 29 (2023) | source of the GWTC-2.1/3 data | **verified at gwosc.org/acknowledgement** |
| GWOSC O4a data paper, ApJ **1004**, 2329 (2026) | source of the O4a data | **verified at gwosc.org/acknowledgement**; was MISSING — we used O4a data while citing only O3 |
| GWOSC O4b data paper, arXiv:2605.27090 | source of the O4b data | **verified at gwosc.org/acknowledgement**; was MISSING |
| GWTC-2.1, PRD **109**, 022001 (2024), arXiv:2108.01045 | training-catalog posteriors | identity verified |
| GWTC-3, PRX **13**, 041039 (2023), arXiv:2111.03606 | training-catalog posteriors | identity verified |
| GWTC-4.0 / O4a | out-of-sample catalog 1 | **cited by Zenodo record only — catalog paper UNVERIFIED**, see DATA_AVAILABILITY.md |
| GWTC-5.0 / O4b | out-of-sample catalog 2 | **cited by Zenodo record only — catalog paper UNVERIFIED**, see DATA_AVAILABILITY.md |
| NumPy, Nature **585**, 357 (2020) | software | identity verified |
| SciPy, Nat. Methods **17**, 261 (2020) | software | identity verified |
| Matplotlib, CiSE **9**, 90 (2007) | software | identity verified |

A test (`tests/test_paper_numbers.py::test_every_bibitem_is_cited_and_every_citation_defined`) now fails
if any bibliography entry is uncited or any citation undefined, so an ornamental reference cannot
re-enter the way Amari 2016 and Backus & Gilbert 1968 did.
