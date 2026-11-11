# Monthly update procedure

The survey is revised about once a month. An update is a release: it gets a version number, a change
log and a tag. The steps below keep the paper, the ledger and the web page consistent.

## 1. Search

For each entry and each forward class in `paper/ledger/entries.csv` and `forward_classes.csv`:

- new versions of the sources already cited (arXiv version bumps, journal publication);
- new classical responses to an open or contested device claim;
- new device claims that meet the eligibility rule of Fig. 2;
- new or revised fault-tolerant resource estimates for a listed target;
- new AI or tensor-network results on a listed problem.

Record every search in the update log (`log` rows in `build_ledger.py`), including searches that
found nothing.

## 2. Read before entering

A value enters a figure only after it has been read in the primary source, with version, table,
equation or page recorded. A value known from an abstract or at second hand is entered with that
status and stays out of figures and ratios. Never carry a value forward from an earlier draft
without re-pinning its source version.

## 3. Edit the ledger, not the figures

Change `paper/ledger/build_ledger.py`, then run:

```bash
cd paper/ledger
python3 build_ledger.py && python3 make_figdata.py && python3 test_negative.py
```

All checks must pass. Counts, intervals and figure coordinates in the paper are macros generated
into `paper/figdata/`; do not type them into the text.

## 4. Edit the text

Edit `paper/parts/*.tex` and `paper/figs/*.tex`. Set the version and date in `parts/p0_pre.tex`.
Figures identify series by marker shape, line style, hatching or a label, never by a colour name.

## 5. Build and check

```bash
cd paper && ./build.sh
```

No undefined references or citations, no overfull boxes, every bibliography entry cited. Read the
changed pages in the PDF.

## 6. Release

1. Write `changelog/CHANGELOG_vN.md`: corrections first, then additions, then what is still open.
2. Add a row to `CHANGELOG.md` and update the version in `README.md` and `CITATION.cff`.
3. Copy the PDF to `docs/paper/ai_vs_qc_survey_vN.pdf` and to `docs/paper/ai_vs_qc_survey_latest.pdf`.
4. Update the version block and the history table in `docs/index.html`.
5. Commit, tag `vN`, push.

## Open items carried from version 8.2

- The spectral-amplification schedule (8.6 h, 4.5 M qubits) is still a second-hand value; read it in
  PRX 15, 041016, Section V.
- The drag study's published range (1e21 to 1e39) is not reconciled with its public per-instance
  files (up to 7.9e40). Its authors have not been contacted.
- Immediate future work: a compressed classical baseline for the Navier-Stokes crossover claim
  (Section 7.2 of the paper).
- Failure allocation is missing for the two lattice-model pairs and the spectroscopy pair.
