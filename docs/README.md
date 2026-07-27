# Documentation index

Reference documentation for the released work. The project's internal working record — planning notes,
adversarial-review rounds, and dated lab notes — is kept out of the public tree; the manuscript and the
committed artifacts under `results/` are the authoritative record of the result.

| document | what it is |
|---|---|
| [EXTERNAL_READER_PACKET.md](EXTERNAL_READER_PACKET.md) | The reader's guide: thesis in one paragraph, strongest and weakest claims, and a reproduction checklist. |
| [REFEREE_READINESS.md](REFEREE_READINESS.md) | The honest summary a referee should read first, including what is *not* claimed. Its headline table is generated from the artifacts. |
| [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md) | Every data source pinned with record numbers, DOIs and licence terms; the citation and acknowledgment obligations. |
| [CITATION_VERIFICATION.md](CITATION_VERIFICATION.md) | Every literature claim in the manuscript, verified against the source. Records two references removed as unsupported and one description corrected. |
| [LITERATURE.md](LITERATURE.md) | Related work, the gap, and why the result is novel. |
| [NOVELTY.md](NOVELTY.md) | The novelty scan underlying the citation decisions above. |
| [WORKFLOW.md](WORKFLOW.md) | The locked-preregistration battery cycle and the analysis conventions used throughout. |
| [TESTING.md](TESTING.md) | How to run the data-free contract test suite. |
| [SCOPE.md](SCOPE.md) | What this project does and does not attempt. |

## A note on the numbers

Every result number in the manuscript is emitted from a committed machine-readable artifact by
`src/build_paper_numbers.py`, and the reader-facing tables in the reference documents above are emitted by
`src/build_doc_numbers.py`. The generators are regression-guarded but are not proof of correctness — they
faithfully propagate whatever the artifacts contain. Where you want assurance, check the artifact under
`results/`, not only the document.
