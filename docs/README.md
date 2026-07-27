# Documentation index

This repository keeps two kinds of documentation: **reference** documents describing the released work,
and a **working record** of how the result was built and stress-tested. The working record is kept public
deliberately — the project's integrity story includes the mistakes it caught in itself — but it is not
required reading, and it is separated here so a reader can find the reference material quickly.

## Reference

Start here if you want to read, reproduce, or evaluate the result.

| document | what it is |
|---|---|
| [EXTERNAL_READER_PACKET.md](EXTERNAL_READER_PACKET.md) | The reader's guide: thesis in one paragraph, strongest and weakest claims, and a reproduction checklist. |
| [REFEREE_READINESS.md](REFEREE_READINESS.md) | The honest summary a referee should read first, including what is *not* claimed. Its headline table is generated from the artifacts. |
| [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md) | Every data source pinned with record numbers, DOIs and licence terms; the citation and acknowledgment obligations. |
| [CITATION_VERIFICATION.md](CITATION_VERIFICATION.md) | Every literature claim in the manuscript, verified against the source. Records two references removed as unsupported and one description corrected. |
| [LITERATURE.md](LITERATURE.md) | Related work, the gap, and why the result is novel. |
| [WORKFLOW.md](WORKFLOW.md) | The locked-preregistration battery cycle and the analysis conventions used throughout. |
| [TESTING.md](TESTING.md) | How to run the data-free contract test suite. |
| [SCOPE.md](SCOPE.md) | What this project does and does not attempt. |

## Working record

Kept for transparency. These are process documents — planning, review rounds, and dated lab notes — not
statements of the released result. Where they quote numbers, those numbers may predate later corrections;
the manuscript and the committed artifacts are authoritative.

| document | what it is |
|---|---|
| [PLAN_EXPANSION.md](PLAN_EXPANSION.md) | Proposal for expanding the program into further papers; awaiting go/no-go. |
| [HANDOFF_ADVERSARIAL_REVIEW.md](HANDOFF_ADVERSARIAL_REVIEW.md) | A brief written to be attacked: what changed across review rounds and where the paper is most likely to break. |
| [HANDOFF.md](HANDOFF.md) | State-of-the-repo handoff between working sessions. |
| [ROADMAP.md](ROADMAP.md) · [PAPER_PLAN.md](PAPER_PLAN.md) · [PAPER_DIRECTION.md](PAPER_DIRECTION.md) | Planning and direction notes. |
| [NOVELTY.md](NOVELTY.md) | Working novelty scan (superseded by CITATION_VERIFICATION.md for the final claims). |
| [REBUTTAL_TO_AUDIT.md](REBUTTAL_TO_AUDIT.md) · [CODEX_RESPONSE_TO_REBUTTAL.md](CODEX_RESPONSE_TO_REBUTTAL.md) | Transcript of an internal adversarial review exchange. |
| [GATE_A_FIRST_MEASUREMENT.md](GATE_A_FIRST_MEASUREMENT.md) · [GATE_B](GATE_B_FIRST_MEASUREMENT.md) · [GATE_C](GATE_C_FIRST_MEASUREMENT.md) · [GATE_DE](GATE_DE_FIRST_MEASUREMENT.md) | Dated lab notes for the submission-gate measurements. Several carry banners noting that their prose numbers were later superseded by regenerated artifacts; they are kept unedited as a record. |

## A note on the numbers

Every result number in the manuscript is emitted from a committed machine-readable artifact by
`src/build_paper_numbers.py`, and the reader-facing tables in the reference documents above are emitted by
`src/build_doc_numbers.py`. The generators are regression-guarded but are not proof of correctness — they
faithfully propagate whatever the artifacts contain. Where you want assurance, check the artifact under
`results/`, not only the document.
