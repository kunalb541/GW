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
| 8 | Hastie & Stuetzle 1989 | principal curve vs linear PCA (chord vs tangent) | identity verified | verified | kept |
| 9 | Amari 2016 (Fisher–Rao) | "the content of Fisher–Rao information geometry" | — | **REMOVED** | ornamental; we compute no Fisher–Rao quantity |
| 10 | Backus & Gilbert 1968 | resolved/unresolved directions | — | **REMOVED** | ornamental; was already uncited in the body |

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

## Outstanding

- Cutler & Flanagan 1994 and Poisson & Will 1995 are used only for the textbook statement that
  $\mathcal{M}_c$ is the best-measured mass combination. Identity verified; not re-read at full text, since
  no specific numerical or figure content is claimed from them.
- Transtrum et al. 2015 and Hastie & Stuetzle 1989 support conceptual framing (sloppy directions; principal
  curve vs linear PCA). Identity verified; no specific claim is drawn from their contents.
- §6 (coherence) and §8–9 (information anatomy, GW250114) were reviewed for citation integrity only. Their
  prose predates the gate work and has not been re-audited for claim strength.
