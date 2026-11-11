# AI+HPC versus Quantum Computing on the Same Scientific Problems

**Matched Tasks, Complete Costs and Conditional Opportunities** — a living survey with an evidence ledger.

Satoshi Matsuoka, RIKEN Center for Computational Science (R-CCS)

| | |
|---|---|
| Current version | **8.2** (11 November 2026), 50 pages |
| Read it | [`docs/paper/ai_vs_qc_survey_latest.pdf`](docs/paper/ai_vs_qc_survey_latest.pdf) |
| Web page | enabled from the `docs/` folder of this repository (GitHub Pages) |
| Update cycle | about once a month; every release is tagged and logged in [`CHANGELOG.md`](CHANGELOG.md) |

## What this is

The survey asks whether advances in AI and high-performance computing remove the need for quantum
computers in science, and answers by comparing the two on the *same* problem: one instance, one
observable, one accuracy, and the complete cost on each side. It tracks device claims and the classical
responses to them, fault-tolerant resource estimates, AI methods used as solvers, and the conditions
under which a quantum advantage would be real.

Every number that appears in a figure or a ratio is held in a machine-readable **evidence ledger**
and recomputed by a validator before each release. Values known only from an abstract or at second
hand are marked and kept out of figures.

## Repository layout

| Path | Contents |
|---|---|
| `docs/` | The web page and the released PDFs (served by GitHub Pages) |
| `paper/main.tex` | Flattened LaTeX source of the current version |
| `paper/parts/`, `paper/figs/` | Section and figure sources; `paper/build.sh` assembles and compiles them |
| `paper/figdata/` | Figure data and macros **generated** from the ledger; do not edit by hand |
| `paper/ledger/` | Eight CSV tables, the builder, the validator and the negative tests |
| `changelog/` | One change log per version |
| `UPDATING.md` | The procedure for a monthly update |

## Reproducing the figures and the PDF

```bash
cd paper/ledger
python3 build_ledger.py      # writes the eight CSV tables
python3 make_figdata.py      # validates them and writes ../figdata
python3 test_negative.py     # 14 corruptions the validator must reject
cd .. && ./build.sh          # assembles main.tex and runs pdflatex three times
```

Python 3 with the standard library is enough for the ledger. The paper needs a TeX Live installation
with `pgfplots` and `tcolorbox`.

## Corrections and contributions

This document is meant to be corrected. If a value, a date or a characterization of a source is wrong,
please open an issue that names the source, its version, and the table, equation or page where the
correct value is found. A correction that comes with a locator can be checked and merged quickly.
New classical or quantum results on a problem already in the ledger are equally welcome.

## Status of the text

This is a preprint under continuous revision and has not been peer reviewed. The paper states how AI
models were used in its preparation; the author is accountable for its content.

## How to cite

See [`CITATION.cff`](CITATION.cff). Please cite the version you used.
