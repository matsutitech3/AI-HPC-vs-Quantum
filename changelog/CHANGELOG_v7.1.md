# Changes, v7 -> v7.1 (11 November 2026)

48 pages (was 47). No change to the structure, the abstract or the conclusions.

## Corrections

1. **Gaussian boson sampling (entry 2, Fig. 2).** Versions up to 7 paired the December 2020
   Jiuzhang claim with the classical algorithm of Oh et al. and reported 30 months (915 days).
   The full text of Oh et al. (arXiv:2306.03709v2) simulates Jiuzhang 2.0, Jiuzhang 3.0 and
   Borealis, not the 2020 experiment. The entry is now dated from Jiuzhang 2.0
   (arXiv:2106.15534v1, 29 June 2021): 707 days, 23.2 months. The range of answered claims is
   now "12 days to 24 months" (was "30 months"). Counts by outcome are unchanged.
2. **Section 4.1.** "None of the ten values" -> "None of the plotted values" (the figure has
   one-sided cases).
3. **Section 4.4.** The X-ray estimate is the only end-to-end costing *among the chemistry and
   materials estimates*; v7 said "in our set", which conflicted with Table 3.
4. **X-ray classical estimate.** "32 days, possibly 100" -> "about 32 days, which the source
   calls likely optimistic on the classical side". The 100-day remark is in version 2 of the
   source and was not re-checked in version 3.
5. **PDF metadata.** Title and author are now set.
6. **Bibliography.** One secondary source (bench2026) removed: the value it supplied is now
   read in the primary. One source added (zhong2021). 150 entries, all cited.

## Information retrieved through the browser extension (PDF text layers on arxiv.org)

| Source | What was read | Effect |
|---|---|---|
| Penuel et al., arXiv:2406.06323v3 | Tables 1-3: sphere at Re 10 to 1e8, three ship hulls; classical reference is steady RANS on one workstation, 1.1 h to 10 h with meshing, out of memory at Re 1e8; estimates stated as lower bounds | Table 3, Section 4.5, Table 10; five classical values added |
| Zhuang et al., arXiv:2509.08807v1 | 130 years classical, stated speedup 1100; output by tomography | "over a century" replaced by the stated figure |
| Scherer et al., arXiv:1505.06552v2 | Table II: depth 1.8e29 / 3.30e25, T-depth 8.2e28 / 1.28e25 | exact values replace orders of magnitude |
| Montanaro and Pallister, arXiv:1512.05903v2 | Table I: classical eps^(-d/2), quantum eps^(-1) with optimal preconditioning | one sentence added to the theory paragraph |
| Low et al., arXiv:2502.15882v1 | Table I: 1459 qubits / 9.99e8 Toffoli (FeMoco-76); 1137 / 3.41e8 (FeMoco-54) | second-hand record replaced; one record added; confirms the THC attribution corrected in v7 |
| Berry et al., arXiv:2409.11748v1 | 7.3e10 Toffoli = 2 or 3 phase-estimation rounds, 2.3x the single-shot THC count | record raised from abstract to section level |
| Low et al. (dense code), arXiv:2605.30455v1 | Ru block, first row: 351 h per shot, p_fail 0.890, 5.55e9 Toffoli; Fig. 1 table | closes the row marked "not re-read"; Fig. 1 agrees with the four FeMoco-54 rows |
| Fomichev et al., arXiv:2506.15784v3 | Sec. 5: 0.76 h x 1000 states, about 32 days | classical estimate pinned to v3 |
| Oh et al., arXiv:2306.03709v2 | datasets simulated | correction 1 |
| Google OTOC paper, arXiv:2506.10191v1 | Fig. 4c: classical estimate is for one circuit | workload basis of the classical figure resolved |
| Jennings et al., arXiv:2512.03758 | abstract and introduction | no new numbers |

## Checks

Ledger: 1039 checks pass (1037), 11 negative tests pass. Build: no undefined references or
citations, no overfull boxes. The arXiv package compiles in a clean directory.

## Still not done

- The product range 1e21 to 1e39 for the drag estimate is an abstract-level value; the source
  plots the per-instance values and they were not digitized. Gate counts for the Navier-Stokes
  estimate were not extracted.
- Lapworth and Sunderhauf, Goldfriend et al. and Tu et al. are at abstract level.
- The spectrum-amplification schedule (8.6 h, 4.5 M physical qubits) is still second-hand.
- The two-hour quantum figure for the OTOC experiment is known from the vendor post only.
- Two gauge-theory values and one block-encoding count remain unverified; tolerance and
  access-model fields are still missing for most device entries.
- Whether any classical result reproduces the 2020 Jiuzhang data was not searched.
