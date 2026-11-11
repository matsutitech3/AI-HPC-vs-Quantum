# Changes, v7.1 -> v8 (11 November 2026)

50 pages (was 48). Response to the fifth-round review; author decisions of 11 November applied.
The structure is unchanged. The abstract and the engineering conclusion change, hence the new number.

## Author decisions applied

1. Engineering conclusion: the empirical finding plus one sentence labelled as the authors' assessment.
   "Candidates only for ..." and "should be regarded as components of quantum simulation and not as
   accelerators" are removed (abstract, Example 4, Sections 4.5, 7.2).
2. The authors of the drag study have not been contacted. The discrepancy is recorded as unresolved
   in Section 4.5, in Limitations, and in the ledger (resources and update log).
3. The compressed classical Navier-Stokes baseline is written into Section 7.2 as immediate future
   work, with two further tests that need only public data. It is not run in this paper.
4. Boson sampling is split into four records, with a new response type "validation statistic challenged".

## Corrections

- OTOC (Section 3.3, entry 6, values, pair record): 2.1 hours of data collection per circuit against
  3.2 years per circuit, both from the primary paper. The workload-mismatch argument is withdrawn.
- Timeline (Fig. 2): 16 rows (was 13). Jiuzhang 2020: challenged at 294 days. Jiuzhang 2.0: challenged
  at 86 days (v7.1 plotted 707), matched in 2023. Borealis: matched at 370 days. Jiuzhang 3.0: matched
  at 43 days. Counts: 4 matched, 2 challenged, 1 observables, 1 partial, 2 contested, 6 open.
- Section 4.5 is organized by four kinds of evidence. "A genuine exponential separation", "the full
  pipeline is costed", "far beyond any field ... an engineer inspects", "the only estimate that
  reports a crossover" and "quantum preconditioning does not recover it" are removed.
- Table 3 is renamed and rebuilt: seven studies, one result and one missing element each.
- Navier-Stokes: 181 logical qubits, 9.41e7 Toffoli and 3.94e8 rotations per preparation, 1,000
  preparations, distance 25; the 130 years is a banded-Cholesky operation count for the full system.
- Drag: the published range is kept; the eight public per-instance records (all opened by us at
  commit cc8d3ce) are entered separately; their product reaches 7.9e40.
- Gauge theory: 3.5e12 and 7.1e12 T gates for two Hamiltonians read in the primary; data width 27,000
  (was 24,000); two plaquette-oracle records with subroutine scope; sign-problem sentence narrowed.
- Section 6.4: the break-even model is an illustration of sensitivity, not a forecast for PDE solvers.
- Section 5.1, Section 3 (standing claims), Section 7 table, FeMoco sentence: categorical statements
  replaced by conditional ones. "No neural network was needed" appears once.
- Ledger: E32 cites liu2021c; two new resource fields (provenance status, quantity scope); three
  artifact identities (arXiv version, journal reference, repository commit); OTOC pair contract filled;
  "not_reported" replaced by "not_extracted" where the source was not inspected.
- Bibliography: 156 entries, all cited; the spectral-amplification entry now carries the title of the
  article of record.
- Readability: first-use glosses for condition number, block encoding and sign problem; shorter
  frontier caption (details moved to Appendix D); dumbbell axis relabelled; timeline caption reading.

## Checks

Ledger: 36 entries, 76 resources, 59 values, 38 classes, 123 figure points, 56 log rows.
1,312 checks pass (1,039). 14 negative tests pass (11): three new ones cover a subroutine count in an
application plot, a citation key from another topic, and a dataset record without a commit.
Build: no undefined references or citations, no overfull boxes. Package compiles in a clean directory.

## Not done

- Spectral-amplification schedule (8.6 h, 4.5 M qubits): still second-hand. The article of record
  loads but our tools could not extract its text.
- Failure allocation for the two lattice-model pairs and the spectroscopy pair is not extracted.
- The validation mechanism of the Quantinuum magnetism claim was not re-read in the primary; the new
  sentence on standing claims describes it generically.
- Martinez-Cifuentes et al. and Anand et al. are cited from their abstracts.
- Glosses for active space, readout, and logical versus physical qubits remain in the glossary only.
- No sensitivity sweep of the Tu et al. model; no new numerical experiment.
