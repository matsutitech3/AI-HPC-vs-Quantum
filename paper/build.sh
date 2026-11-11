#!/bin/bash
# assemble (flattening figs/*.tex into one file) and compile; run from v7/
set -e
python3 - <<'PY'
import re
parts=["p0_pre","p1_intro","p2_compare","p3_devices","p4_ft","p5_ai","p6_cross","p7_opps","p8_end","pA_app","pE_ledger","pZ_bib"]
s="".join(open(f"parts/{p}.tex").read() for p in parts)
s=re.sub(r"\\input\{(figs/[A-Za-z0-9_]+\.tex)\}", lambda m: open(m.group(1)).read().rstrip("\n"), s)
assert "\\input{figs/" not in s
open("main.tex","w").write(s)
PY
for i in 1 2 3; do timeout 280 pdflatex -interaction=nonstopmode -halt-on-error main.tex > build$i.log 2>&1 || { echo "pdflatex pass $i failed"; grep -E "^!|^l\.[0-9]+" build$i.log | head -12; exit 1; }; done
grep -E "Output written" build3.log
grep -E "LaTeX Warning: (Reference|Citation)|multiply defined|undefined" build3.log | sort | uniq -c | head -30
echo "overfull: $(grep -c Overfull build3.log || true)"
