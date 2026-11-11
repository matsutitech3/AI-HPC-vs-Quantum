# Ledger changes, v7.1 -> v8 (11 November 2026)

Counts: 36 entries (was 33), 76 resource records (65), 59 values, 38 classes, 123 figure points (120),
56 log rows (49); 1,312 validation checks (1,039); 14 negative tests (11).

| Record | v7.1 | v8 | Source locator |
|---|---|---|---|
| E02 | Jiuzhang 2.0/3.0/Borealis merged, 707 d | Jiuzhang 2.0 only: challenged at 86 d, matched 2023 | arXiv:2109.11525v1; arXiv:2306.03709v2 |
| E34, E35, E36 | absent | Jiuzhang 2020 (294 d, challenged); Borealis (370 d); Jiuzhang 3.0 (43 d) | as above; Nature 606, 75; arXiv:2304.12240 |
| E32 primary_sources | liu2021 | liu2021c | key correction |
| C-OTOC-q / C-OTOC-c | 2.0 h (vendor post) / 3.2 y | 2.1 h per circuit / 3.2 y per circuit | arXiv:2506.10191v1, text beside Fig. 4(c) |
| R-CFD-ZHUANG | no counts | 181 LQ; 9.41e7 Toffoli per preparation; 3.94e8 rotations; 1,000 preparations | arXiv:2509.08807v1, App. F |
| R-CFD-PENUEL-Re1e1..1e8 | absent | eight per-instance records, 5.3e21 to 7.9e40 in product | qsub commit cc8d3ce |
| R-SU3-S72-O / -OI | 1e12 T (abstract), 24,000 LQ | 3.5e12 and 7.1e12 T, 27,000 data qubits | arXiv:2511.17437v1, Sec. IX |
| R-SU3-BE-B6 / -B9 | absent | 1.2e5 and 1.2e6 T per plaquette oracle (subroutine) | arXiv:2608.17115v1, Tables 5-6 |
| R-FEMO76-SA-sched | 3.10e4 s | 30,960 s; still second-hand | article of record not read |
| resources.csv | 26 columns | 28: provenance_status, quantity_scope | new fields |

# Ledger changes, v7 -> v7.1 (11 November 2026)

Counts: 33 entries, 65 resource records (was 64), 59 values (53), 38 classes, 120 figure points,
49 log rows (39); 1039 validation checks (1037); 11 negative tests.

| Record | v7 | v7.1 | Source locator |
|---|---|---|---|
| E02 claim date | 3 Dec 2020 (915 d to answer) | 29 Jun 2021 (707 d) | arXiv:2306.03709v2 simulates Jiuzhang 2.0, Jiuzhang 3.0 and Borealis, not the 2020 experiment; Jiuzhang 2.0 is arXiv:2106.15534v1 |
| R-FEMO76-SA-count | second-hand | 1459 qubits, 9.99e8 Toffoli, read in the primary | arXiv:2502.15882v1, Table I |
| R-FEMO54-SA-count | absent | 1137 qubits, 3.41e8 Toffoli | same |
| R-FEMO-BERRY | abstract | section level; 2 or 3 QPE rounds, 2.3x the single-shot THC count | arXiv:2409.11748v1, Sec. I |
| R-QLSA-EM | depth 1e29 (abstract) | depth 1.8e29 (3.30e25 without oracles); T-depth 8.2e28 | arXiv:1505.06552v2, Table II |
| R-CFD-ZHUANG | abstract | section level; classical 130 y, stated speedup 1100 | arXiv:2509.08807v1 |
| R-RU56-DC-minq | one-shot, p_fail, Toffoli not read | 351 h, 0.890, 5.55e9 | arXiv:2605.30455v1, Table XXVII |
| C-XAS-RAS-* | read in v2 | pinned to v3 | arXiv:2506.15784v3, Sec. 5 |
| C-CFD-RANS-Re1e3..1e7 | absent | 1.1 h to 10 h on one workstation | arXiv:2406.06323v3, Table 3 |
| C-CFD-ZHUANG-classical | absent | 130 y | arXiv:2509.08807v1 |

# Ledger changes, v6 -> v7 (11 November 2026)

Counts: 33 entries (was 31), 64 resource records (50), 53 values (51), 38 classes (37),
120 figure points, 39 log rows; 1037 validation checks (636); 11 negative tests (6).

## Corrections of values

| Record | v6 | v7 | Source locator |
|---|---|---|---|
| E26 claim date | 16 Oct 2022 (1,486 d open) | 11 Apr 2026 (214 d open) | arXiv:2210.08556: v1 has another title and a 32-site chain; the 64-site claim is v2 |
| R-XAS-circ | 3.11e8 Toffoli, 56 s | 3.54e8 Toffoli, 108 s (1.08e8 cycles) | arXiv:2506.15784v3, Table 1 (N=18), Introduction |
| R-XAS-alg / R-XAS-av | 4.58e11 Toffoli, 8.1e4 s | 5.20e11 Toffoli, 1.58e5 s (1.58e11 cycles) | same; v2 rows kept as R-XAS-*-v2 |
| R-FEMO76-THC | 2142 logical qubits, 5.3e9 Toffoli, 4e6 physical, 4 days | 2196 logical qubits, 3.2e10 Toffoli, no layout | arXiv:2011.03494v3, Table V. The v6 numbers are Table IV, the 54-orbital model; now R-FEMO54-THC-lee and R-FEMO54-THC-layout |
| R-FEMO76-DC-fast | "minimum runtime", 2.64 h | "selected fast row"; R-FEMO76-DC-fastest added: 2.50 h at 2.692 M | arXiv:2605.30455v1, Table XXVII |
| R-FEMO54-compact / -balanced | upper limits (1 month, 1 day) | tabulated 671 h and 22.8 h | same table |
| R-TFIM-ns3, -us4, -us3 | physical qubits not reported | 8.2e6, 6.8e5, 3.0e6 | arXiv:2211.07629v1, Table IV |
| E04, E18 date flags | approximate | exact (1 Mar 2024, 7 Mar 2025; 28 May 2025) | arXiv listings |
| C-FEMO76-ideal | "variational UDMRG, idealized Frontier wall time" | "two variational sweeps at D=393,000, calculation not performed"; C-FEMO76-ideal-coreh (4.08e9 core-h) and C-FEMO76-uccsdtq (21.0 s) added | arXiv:2601.04621v2, cost section |

## New fields and records

- `resources.csv`: `one_shot_runtime_s`, `p_fail_logical`, `artifact_type`, `retrieved`.
  Toffoli totals filled for the dense-code rows; logical width deliberately not constructed.
- `values.csv`: `artifact_type`, `retrieved`.
- `pairs.csv` (new): comparison records for seven headline pairs.
- Dense-code rows added: within-a-day and within-a-month rows for FeMoco-76 and P450, minimum-volume row for the Ru model.
- Entries E32 (theory: PDEs by quantum linear and differential-equation solvers) and E33 (resource estimates for drag force); class 38; abstract-level records R-QLSA-EM, R-CFD-PENUEL-lo/-hi, R-CFD-ZHUANG.
- Comparison-record fields filled for E04, E06, E10, E21, E23-E26.
- `update_log.csv`: superseded checks are kept and marked; 14 checks of 11 November added.

## Version identity

All plotted rows now carry an arXiv identifier with a version number or a journal reference.
The rows carried as "as read for v4" (Beverland et al., Lee et al., Reinholdt et al.) were
re-read from the PDFs on 11 November. That re-read found the THC error above.

## Validator

New checks: version-identifier syntax; units of every transformation against the axis; gate
type of each series; one-sided values only in limit series; the two internal relations of the
dense-code table. New negative tests: "latest available"; "as read for v4"; unit changed from
hours to seconds; Toffoli record in a T series; inconsistent dense-code row; upper bound in an
ordinary series.

## Figures

- Time comparison: OTOC(2) removed from the common axis; five modelled cases remain.
- Repetition scenario: one attempt is one accepted execution (5.26 h expected, from a 4.89 h
  shot at p_fail 0.070); columns for an unsplit and an equally split failure budget.
- Hubbard: strips are separate series and are not joined to square lattices.
- FeMoco-76 panel: the THC point (a different Hamiltonian) and the classical line removed.
- Resource map: cumulative XAS count removed; both FeMoco THC records shown.
- Gauge figure: chemistry reference row removed.
