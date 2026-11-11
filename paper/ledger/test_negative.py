#!/usr/bin/env python3
"""Negative tests (v7): the validator must reject a corrupted ledger.

Each test copies the ledger to a temporary directory, corrupts one thing and
runs make_figdata.py --check-only there. The test passes only if the validator
exits non-zero. Run after build_ledger.py:  python3 test_negative.py
"""
import csv, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = [f for f in os.listdir(HERE) if f.endswith((".csv", ".txt")) or f == "make_figdata.py"]

def run(mutate, label):
    d = tempfile.mkdtemp(prefix="ledger_neg_")
    try:
        for f in FILES:
            shutil.copy(os.path.join(HERE, f), d)
        mutate(d)
        r = subprocess.run([sys.executable, os.path.join(d, "make_figdata.py"), "--check-only"], capture_output=True, text=True)
        ok = r.returncode != 0
        print(("PASS " if ok else "FAIL ") + label + (" (rejected)" if ok else " (accepted: validator is too weak)"))
        return ok
    finally:
        shutil.rmtree(d, ignore_errors=True)

def edit(d, name, match, field, new):
    path = os.path.join(d, name)
    rows = list(csv.DictReader(open(path)))
    hit = 0
    for r in rows:
        if match(r):
            r[field] = new; hit += 1
    assert hit, "nothing matched in " + name
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

tests = [
 ("plotted coordinate changed (Hubbard 10x10 quantum time set to 1e8 h)",
  lambda d: edit(d, "figure_points.csv", lambda r: r["fig"] == "dumbbell" and r["point_id"] == "R-HUB-1010-s", "x", "1e8")),
 ("source value changed without regenerating the point (Ru runtime)",
  lambda d: edit(d, "resources.csv", lambda r: r["res_id"] == "R-RU-us3", "runtime_s", "8.2e8")),
 ("one-sided value written to an ordinary series (FeMoco-54 point marked as an upper bound)",
  lambda d: edit(d, "figure_points.csv", lambda r: r["fig"] == "femoco54" and r["point_id"] == "R-FEMO54-compact", "bound", "upper")),
 ("abstract-level record used in a figure",
  lambda d: edit(d, "resources.csv", lambda r: r["res_id"] == "R-XAS-circ", "locator_level", "abstract")),
 ("empty source version",
  lambda d: edit(d, "resources.csv", lambda r: r["res_id"] == "R-HUB-66-s", "source_version", "current version")),
 ("meaningless source version ('latest available') on a plotted row",
  lambda d: edit(d, "resources.csv", lambda r: r["res_id"] == "R-HUB-1010-s", "source_version", "latest available")),
 ("version carried from an earlier draft ('as read for v4') on a plotted row",
  lambda d: edit(d, "resources.csv", lambda r: r["res_id"] == "R-TFIM-ns4", "source_version", "arXiv:2211.07629 (as read for v4)")),
 ("unit changed from hours to seconds without changing the value (FeMoco classical reference)",
  lambda d: edit(d, "values.csv", lambda r: r["val_id"] == "C-FEMO76-ideal", "unit", "s")),
 ("Toffoli count placed in a T-count series",
  lambda d: edit(d, "resources.csv", lambda r: r["res_id"] == "R-P450-2022", "gate_type", "T")),
 ("dense-code row violating expected = one-shot/(1 - p_fail)",
  lambda d: edit(d, "resources.csv", lambda r: r["res_id"] == "R-FEMO76-DC-fastest", "one_shot_runtime_s", "5000")),
 ("class linked to a record that does not exist",
  lambda d: edit(d, "forward_classes.csv", lambda r: r["class_id"] == "9", "linked_resources", "R-XAS-v9")),
 ("subroutine count used in a plot of application counts",
  lambda d: edit(d, "resources.csv", lambda r: r["res_id"] == "R-SU3-KRY", "quantity_scope", "subroutine")),
 ("citation key from another topic (E32 citing the quantum-learning paper for Carleman linearization)",
  lambda d: edit(d, "entries.csv", lambda r: r["entry_id"] == "E32", "primary_sources", "hhl2009;montanaro2016;liu2021")),
 ("repository dataset record without a commit identifier",
  lambda d: edit(d, "resources.csv", lambda r: r["res_id"] == "R-CFD-PENUEL-Re1e8", "source_version", "github.com/isi-usc-edu/qsub")),
]
ok = all([run(m, lab) for lab, m in tests])
sys.exit(0 if ok else 1)
