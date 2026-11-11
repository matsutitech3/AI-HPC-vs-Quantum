# Evidence ledger for "AI+HPC versus Quantum Computing on the Same Scientific Problems" (v8.2)

## Build

    python3 build_ledger.py     # writes the eight CSV tables and timeline_order.txt
    python3 make_figdata.py     # validates, then writes ../figdata/*
    python3 test_negative.py    # fourteen corruptions the validator must reject
    cd .. && pdflatex main && pdflatex main && pdflatex main

Tested with Python 3.13 (standard library only) and TeX Live 2023 (pdflatex, pgfplots 1.18,
tcolorbox, natbib). `make_figdata.py --check-only` validates without writing. Set `LEDGER_OUT`
to write the generated files somewhere other than `../figdata`.

`build_ledger.py` is the authoritative source. The CSV files are its output: a direct edit to a
CSV file is overwritten by the next run, and is rejected by `make_figdata.py` if it makes a
plotted coordinate disagree with its source record.

## Tables

| File | One row per | Key fields |
|---|---|---|
| `entries.csv` | evidence entry (E01-E33) | match type, dates with precision flags, elapsed days, comparison-record fields (instance and version, boundaries, tolerance, failure-probability meaning, workload, access model), three status fields |
| `pairs.csv` | headline comparison that is a problem class, not an entry | the same comparison-record fields, linked quantum and classical records, what is missing |
| `resources.csv` | Hamiltonian x algorithm x layout x schedule | source version, locator, locator level, artifact read, retrieval day, gate type, count and scope, width and convention, physical qubits, expected runtime, one-shot runtime, logical failure probability, volume, coverage, unvalidated assumptions, extraction gap |
| `values.csv` | classical time or other scalar fact | value, unit, kind, machine or criterion, version, locator, artifact, retrieval day |
| `models.csv` | parameter of a formula figure or scenario | value, unit |
| `forward_classes.csv` | problem class (1-38) | present status, coverage, linked entries and resources, three triggers |
| `figure_points.csv` | plotted point | figure, series, coordinates, bound kind, and the record field and transformation each coordinate is computed from |
| `update_log.csv` | source check | date, version inspected, issue; superseded checks are kept and marked |

## Codes

Missing values: `not_reported` (the source does not give it), `not_extracted` (we have not read
it out), `not_applicable`, `not_estimated`.

Locator levels: `table`, `section`, `primary_page` (read by us at that place in an identified
version; may be plotted); `abstract`, `secondary`, `table_unverified` (never plotted).

Coverage of a resource record: `complete_logical`, `partial`, `scenario`.

`classical_capability` in `entries.csv` is the validation-basis field: `measured_run`,
`validated_benchmark`, `validated_experiment`, `extrapolated_estimate`, `scaling_law`,
`theorem`, `theorem_claimed_machine_checked_core`, `none_recorded`.

## What the validator checks

1. Every plotted coordinate is recomputed from its cited record and transformation.
2. A plotted record must be read at table, section or primary-page level.
3. A plotted record's `source_version` must be an arXiv identifier with a version number or a
   journal reference. Strings such as "latest", "current version", "as read for v4" or "via ..."
   are rejected.
4. Units: each transformation declares the unit it accepts and returns; the result must be the
   unit of the axis. T-state and Toffoli counts cannot be written to the same series.
5. A point's bound kind must equal its source row's, and a one-sided value may be written only
   to a series whose name ends in `_upper` or `_lower` (drawn with a limit marker).
6. Rows of the dense-code table (those with a one-shot runtime and a failure probability) must
   satisfy volume = qubits x expected runtime and expected = one-shot/(1 - p_fail), within 2%.
7. Links between tables, status vocabularies and the coverage-aggregation rule.

The validator establishes that figures agree with tables and that tables are internally
consistent. It does not establish that a value was read correctly from its source. Version
identity is taken from the artifact read (the stamp on the PDF or the listing of the page),
because a request for an older version of a web page can return the current one.
