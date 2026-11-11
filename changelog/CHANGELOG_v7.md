# Changes from version 6 to version 7 (11 November 2026)

Version 7 is a full rewrite of the text into an eight-section narrative (22 pages) with five
appendices (23 pages), 47 pages in all. It implements the response to the fourth-round review
and the author's decisions of 11 November.

## Author decisions applied

1. Sources fetched through the Chrome extension: XAS version 3 and the dense-code PDF read from
   their text layers; six further sources re-read the same way.
2. The Aaronson-Ambainis result is out of the abstract and out of the conclusion's chain of
   evidence. It remains as a boxed paragraph in Section 5.4 and in Appendix D.6.
3. Subtitle: "Matched Tasks, Complete Costs and Conditional Opportunities".
4. Full reorganization (not the two-part compromise): Why comparisons disagree; How to compare
   the same answer; What device experiments show; Where fault-tolerant estimates stand; How AI
   changes the classical side; What determines a crossover; Opportunities and the evidence each
   needs; Limitations and conclusion. Case cards are replaced by prose answering five questions.
5. Competing interests: the author had no technical role in the studies named.
6. New Section 4.5, "Linear systems and fluid dynamics: a negative case", with a fourth opening
   example, a row in the summary table, entries E32 and E33, class 38, and a sentence in the
   abstract and the conclusion.

## Corrections confirmed against sources on 11 November

- XAS: version 3 (5 Nov 2026) is the record: 3.54e8 and 5.20e11 Toffoli; 1.08e8 and 1.58e11
  logical cycles; 43.9 h at 1 MHz (v6: 22.5 h). Version 2 values kept as history.
- Dense-code Table XXVII read in full: FeMoco-76 fastest row is 2.50 h at 2.692 M qubits
  (1.08e9 Toffoli); minimum volume 5.26 h expected = 4.89 h shot / (1 - 0.070), 1.81e9 Toffoli;
  P450 1.88 h (7.02e8) and 1.11 h (5.34e8). The P450, Ru and FeMoco-54 "fastest" rows are the
  last rows of their blocks. Sec. VI.B defines expected runtime.
- Ultracold atoms: v1 (16 Oct 2022) is a 32-site chain under another title, "comparable to the
  fastest supercomputer"; the 64-site claim is v2 (11 Apr 2026). Open interval 214 days.
- NEW, found while re-pinning sources: the THC numbers attributed to the 76-orbital FeMoco model
  in versions 4 to 6 (2,142 logical qubits, 5.3e9 Toffoli, 4 M physical qubits, 4 days) belong
  to the 54-orbital model. The 76-orbital model needs 2,196 logical qubits and 3.2e10 Toffoli,
  and the source gives no physical layout for it.
- FeMoco classical cost: three records (measured campaign; modelled two sweeps at D near 393,000,
  not performed; candidate construction not costed) plus the source's 21.0 s idealized figure.
- Heisenberg: thresholds 1.40 and 18.3 replace "reverses" and "parity".
- Heron Floquet: validation hierarchy read from the PDF and stated.
- Doped Clifford: v3 text states that periodic boundaries remove the contraction path.
- Dates: King 1 Mar 2024, Tindall 7 Mar 2025, Pawlowski 28 May 2025 confirmed exact. Merz pinned
  to v2; Manabe v2 (29 Oct 2026) noted.

## Models

- QPE: the product formula of v6 is replaced by the good-event lower bound with a divided
  tolerance (a + b <= eps) and a divided failure budget. One attempt is one accepted execution.
  At p = 0.5: 7 executions (36.8 h expected) with no low-outlier budget, 8 (42.1 h) with an
  equal split, q_low <= 6.25e-4.
- Classical cost: general bookkeeping with a per-instance solve term.
- Output: stated as a reconstruction cost that grows with field size; no tomography theorem.

## Figures and tables

Seven figures in the main text (timeline, four explanations, time comparison, Hubbard,
chemistry frontier, electrolyte funnel, repetition scenario); ten in the appendices. One
twelve-row summary table; two tables for the linear-solver case; one table of six
opportunities. Glossary, completeness table and comparison-pair table are new.

## Not done

- Per-generation boson-sampling records; the workload basis of the OTOC timing; a matrix of
  lattice, quench time and observable for the annealing claim.
- Comparison-record fields for most device entries (counts in Appendix E).
- All linear-solver and CFD numbers are at abstract level and enter no figure.
- The XAS classical estimate was not re-read in version 3. The first row of the Ru block of the
  dense-code table was not re-read. The Lean proof was not rebuilt.
