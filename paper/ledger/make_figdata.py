#!/usr/bin/env python3
"""Validate the ledger and generate everything the manuscript reads from it.

Reads the eight CSV tables written by build_ledger.py and writes, under
../figdata/ (or $LEDGER_OUT): pgfplots tables (*.dat), TeX snippets for
connectors, bars and labels (*_annot.tex), the numbers quoted in the text
(counts.tex) and the forward-class grid (forward_grid.tex).

Validation (any failure exits non-zero and writes nothing with --check-only):
  1. every plotted coordinate is recomputed here from the cited record field
     and named transformation, and must equal the stored coordinate;
  2. the cited record must have a table-, section- or primary-page-level
     locator in a pinned source version (abstract/secondary rows are refused);
  3. a point's bound kind must equal its source row's runtime bound, and a
     one-sided value may only be written to a series drawn with a limit marker;
  4. the source version must be a recognised immutable identifier (an arXiv
     identifier with its version number, or a journal reference);
  5. units: each transformation declares the unit it accepts and returns, and
     the result must be the unit of the axis it is plotted on; T-state and
     Toffoli counts are kept in separate series;
  6. rows of the dense-code table must satisfy its two internal relations;
  7. every linked entry/resource identifier must exist; counts must add up.
Usage:  python3 make_figdata.py [--check-only]
"""
import csv, math, os, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("LEDGER_OUT", os.path.join(HERE, "..", "figdata"))
CHECK_ONLY = "--check-only" in sys.argv

def read(name):
    with open(os.path.join(HERE, name)) as f:
        return list(csv.DictReader(f))

E, R, V, M, F, P, PAIRS = (read(n + ".csv") for n in ("entries", "resources", "values", "models", "forward_classes", "figure_points", "pairs"))
EI = {r["entry_id"]: r for r in E}
RI = {r["res_id"]: r for r in R}
VI = {r["val_id"]: r for r in V}
MP = {(m["model_id"], m["parameter"]): m["value"] for m in M}
TAB = {"entries": EI, "resources": RI, "values": VI}
fails, npass = [], 0
def check(cond, msg):
    global npass
    if cond:
        npass += 1
    else:
        fails.append(msg); print("FAIL " + msg)

TR = {"identity": lambda v: v, "s_to_h": lambda v: v / 3600.0, "y_to_h": lambda v: v * 8766.0,
      "d_to_month": lambda v: v / 30.44, "min_to_h": lambda v: v / 60.0, "d_to_h": lambda v: v * 24.0}
OKLVL = {"table", "section", "primary_page"}
# unit bookkeeping
TR_UNITS = {"s_to_h": ("s", "h"), "y_to_h": ("y", "h"), "d_to_month": ("d", "month"), "min_to_h": ("min", "h"), "d_to_h": ("d", "h")}
FIELD_UNIT = {"runtime_s": "s", "physical_qubits": "qubits", "logical_qubits": "qubits", "n_nc": "count",
              "st_volume_Mqh": "Mqh", "elapsed_days": "d", "n_nc/runtime_s": "count/s"}
AXIS_UNIT = {("timeline", "x"): {"month"}, ("dumbbell", "x"): {"h"}, ("hubbard", "y"): {"s"},
             ("femoco54", "x"): {"qubits"}, ("femoco54", "y"): {"h"}, ("femoco54vol", "y"): {"Mqh"},
             ("femoco76", "x"): {"qubits"}, ("femoco76", "y"): {"h"}, ("p450dc", "x"): {"qubits"}, ("p450dc", "y"): {"h"},
             ("dmrg", "y"): {"CPU-h", "core-h"}, ("rates", "x"): {"count/s"}, ("platform", "y"): {"s"},
             ("resmap", "x"): {"qubits"}, ("resmap", "y"): {"count"}, ("gauge", "x"): {"count"},
             ("sqd", "x"): {"samples"}, ("sqd", "y"): {"determinants", "per shot"}, ("funnel", "x"): {"candidates"}}
GATE_OF_SERIES = {("rates", "T"): "T", ("rates", "CCZ"): "Toffoli", ("resmap", "T_point"): "T",
                  ("resmap", "Toff_point"): "Toffoli", ("gauge", "lo"): "T", ("gauge", "hi"): "T"}
PIN = re.compile(r"arXiv:\d{4}\.\d{4,5}v\d+|PNAS|JACS|Science \d|Nature \d|Phys\. Rev|PRX|J\. Chem")
UNPINNED = ("as read for", "via ", "latest", "current version", "not re-read")
def close(a, b):
    return abs(a - b) <= 1e-9 * max(1.0, abs(a), abs(b))

# ---------------------------------------------------------------- 1-3: per-point validation
ncoord = 0
for p in P:
    pid = p["fig"] + "/" + p["point_id"]
    check(p["checks"] != "", pid + ": has a provenance check")
    for c in p["checks"].split(";"):
        ax, tb, rid, fld, trn = c.split(":")
        rec = TAB.get(tb, {}).get(rid)
        if rec is None:
            check(False, pid + ": source record %s/%s does not exist" % (tb, rid)); continue
        try:
            if "/" in fld:
                a, b = fld.split("/"); v = float(rec[a]) / float(rec[b])
            else:
                v = float(rec[fld])
        except (KeyError, ValueError):
            check(False, pid + ": field %s of %s is not a number" % (fld, rid)); continue
        check(close(TR[trn](v), float(p[ax])), "%s: %s=%s differs from %s.%s via %s (=%.6g)" % (pid, ax, p[ax], rid, fld, trn, TR[trn](v)))
        ncoord += 1
        if tb in ("resources", "values"):
            check(rec["locator_level"] in OKLVL, pid + ": source %s has locator level '%s'" % (rid, rec["locator_level"]))
            sv = rec["source_version"]
            check(bool(PIN.search(sv)) and not any(u in sv for u in UNPINNED), pid + ": source %s version '%s' is not a pinned identifier" % (rid, sv))
        unit = rec.get("unit") if tb == "values" else FIELD_UNIT.get(fld)
        if trn != "identity":
            check(unit == TR_UNITS[trn][0], pid + ": %s expects %s but %s.%s is in %s" % (trn, TR_UNITS[trn][0], rid, fld, unit))
            unit = TR_UNITS[trn][1]
        if (p["fig"], ax) in AXIS_UNIT:
            check(unit in AXIS_UNIT[(p["fig"], ax)], pid + ": axis %s of %s is in %s, but the value is in %s" % (ax, p["fig"], "/".join(sorted(AXIS_UNIT[(p["fig"], ax)])), unit))
        if tb == "resources" and (p["fig"], p["series"]) in GATE_OF_SERIES:
            check(rec["gate_type"] == GATE_OF_SERIES[(p["fig"], p["series"])], pid + ": series %s holds %s counts, record %s is in %s" % (p["series"], GATE_OF_SERIES[(p["fig"], p["series"])], rid, rec["gate_type"]))
        if tb == "resources" and fld == "runtime_s":
            check(p["bound"] == rec["runtime_bound"], pid + ": bound '%s' differs from source '%s'" % (p["bound"], rec["runtime_bound"]))
    check((p["bound"] in ("upper", "lower")) == p["series"].endswith(("_upper", "_lower")), pid + ": a one-sided value must be in a series drawn with a limit marker, and only there")

# ---------------------------------------------------------------- internal relations of the dense-code table
def num(x):
    try: return float(x)
    except ValueError: return None
for r in R:
    one, pf, rtv, pq, vol = (num(r[k]) for k in ("one_shot_runtime_s", "p_fail_logical", "runtime_s", "physical_qubits", "st_volume_Mqh"))
    if one is not None and pf is not None:
        check(abs(rtv - one / (1 - pf)) <= 0.02 * rtv, "%s: expected runtime %.4g s differs from one-shot/(1-p_fail) = %.4g s" % (r["res_id"], rtv, one / (1 - pf)))
        check(abs(vol - pq * rtv / 3600 / 1e6) <= 0.02 * vol, "%s: volume %.4g differs from qubits x runtime = %.4g" % (r["res_id"], vol, pq * rtv / 3600 / 1e6))

# ---------------------------------------------------------------- 4: links and counts
for r in F:
    for e in filter(None, r["linked_entries"].split(";")):
        check(e in EI, "class %s links missing entry %s" % (r["class_id"], e))
    for x in filter(None, r["linked_resources"].split(";")):
        check(x in RI, "class %s links missing resource %s" % (r["class_id"], x))
strata = Counter(r["stratum"] for r in E)
tl = Counter(p["series"] for p in P if p["fig"] == "timeline")
pres = Counter(r["present_status"] for r in F)
mat = Counter(r["resource_maturity"] for r in F)
check(sum(tl.values()) == sum(1 for r in E if r["timeline_eligible"] == "yes"), "timeline points = eligible entries")
# contract checks added in v8
for p_ in P:
    for c_ in p_["checks"].split(";"):
        f_ = c_.split(":")
        if len(f_) > 2 and f_[1] == "resources" and f_[2] in RI:
            check(RI[f_[2]]["quantity_scope"] != "subroutine", p_["point_id"] + ": subroutine count used in a plot of application counts")
for r_ in R:
    check(not ("data registers only" in r_["lq_convention"] and "total" in r_["lq_convention"].split(";")[0]), r_["res_id"] + ": data-only width labelled total")
    check(r_["provenance_status"] != "primary_dataset" or "commit" in r_["source_version"], r_["res_id"] + ": dataset record without a repository commit")
KEY_TOPIC = {"liu2021": {"qml-classical-data", "quantum-data"}, "liu2021c": {"linear-systems-pde", "fluids"}}
for r_ in E:
    for k_ in r_["primary_sources"].split(";"):
        if k_ in KEY_TOPIC:
            check(r_["task_family"] in KEY_TOPIC[k_], r_["entry_id"] + ": cites %s, whose topic does not match task family %s" % (k_, r_["task_family"]))
check(sum(strata.values()) == len(E), "strata partition the entries")
XS = ["standing_claim", "theory", "contested", "not_compared", "classical_capability", "matched_scoped", "capability"]
YS = ["complete", "partial", "scenario", "none", "not_applicable"]
check(all(r["present_status"] in XS and r["resource_maturity"] in YS for r in F), "forward statuses use the defined vocabulary")
for r in F:  # maturity aggregation rule: a class is no more mature than the least mature linked record
    lv = [RI[x]["coverage"] for x in filter(None, r["linked_resources"].split(";")) if x in RI]
    if lv and r["resource_maturity"] in ("complete", "partial"):
        check("scenario" not in lv, "class %s is %s but links a scenario record" % (r["class_id"], r["resource_maturity"]))
    if r["resource_maturity"] == "complete":
        check(all(x.startswith("complete") for x in lv), "class %s complete only if all linked records are" % r["class_id"])

if fails:
    print("FAILED %d of %d checks" % (len(fails), npass + len(fails))); sys.exit(1)
print("PASS %d checks (%d plotted coordinates recomputed from %d records)" % (npass, ncoord, len(R) + len(V) + len(E)))
if CHECK_ONLY:
    sys.exit(0)
os.makedirs(OUT, exist_ok=True)
for _f in os.listdir(OUT):  # remove stale generated files
    if _f.endswith((".dat", ".tex")):
        os.remove(os.path.join(OUT, _f))
def out(name):
    return open(os.path.join(OUT, name), "w")

# ---------------------------------------------------------------- pgfplots tables
groups = defaultdict(list)
for p in P:
    groups[(p["fig"], p["series"])].append(p)
for (fig, ser), pts in groups.items():
    with out(f"{fig}_{ser}.dat") as f:
        f.write("x y\n")
        for p in pts:
            f.write(f'{float(p["x"]):.6g} {float(p["y"]):.6g}\n')
def labels(fig, extra=""):
    with out(fig + "_labels.tex") as f:
        f.write("% generated by ledger/make_figdata.py\n")
        for p in P:
            if p["fig"] == fig and p["label"]:
                f.write("\\node[font=\\scriptsize, inner sep=5pt, anchor=%s%s] at (axis cs:%.6g,%.6g) {%s};\n" % (p["anchor"], extra, float(p["x"]), float(p["y"]), p["label"]))
for fig in ("dumbbell", "resmap"):
    labels(fig)
PX = {(p["fig"], p["point_id"]): p for p in P}
def px(fig, pid, ax="x"):
    return float(PX[(fig, pid)][ax])

# ---------------------------------------------------------------- formatting helpers
def sci(v, d=1):
    e = int(math.floor(math.log10(abs(v)))); m = v / 10 ** e
    ms = f"{m:.{d}f}"
    if float(ms) >= 10: ms = f"{m/10:.{d}f}"; e += 1
    return f"${ms}\\times10^{{{e}}}$" if float(ms) != 1 else f"$10^{{{e}}}$"
def grp(n):
    return f"{int(round(n)):,}".replace(",", "{,}")
WORDS = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()
def rt(rid): return float(RI[rid]["runtime_s"])
def vv(vid): return float(VI[vid]["value"])
mac = {}

# ---------------------------------------------------------------- repetition scenario (FeMoco-76)
# One attempt = one logically accepted execution. Its expected duration is the
# source's retry-adjusted runtime; p is the hit probability conditional on acceptance.
dtot, pscen = float(MP[("rep", "delta_total")]), float(MP[("rep", "p_scenario")])
rrec = RI[MP[("rep", "record")]]
t1 = float(rrec["runtime_s"]) / 3600.0
tshot, pfl = float(rrec["one_shot_runtime_s"]) / 3600.0, float(rrec["p_fail_logical"])
def Rn(pp, d):
    return math.ceil(math.log(d) / math.log(1 - pp) - 1e-12)
Rzero = lambda pp: Rn(pp, dtot)        # downward outliers given zero budget
Rsplit = lambda pp: Rn(pp, dtot / 2)   # budget split equally between misses and low outliers
with out("rep_curves.dat") as f:
    f.write("p fixed split herald\n")
    for i in range(5, 96):
        pp = i / 100
        f.write(f"{pp:.2f} {Rzero(pp)*t1:.4g} {Rsplit(pp)*t1:.4g} {t1/pp:.4g}\n")
with out("rep_annot.tex") as f:
    f.write("\\draw[black!35, dashed] (axis cs:0.05,%g) -- (axis cs:0.95,%g) node[pos=0.97, below, anchor=north east, font=\\scriptsize]{one accepted execution, %.2f\\,h expected};\n" % (t1, t1, t1))
mac.update(femoT=f"{t1:.2f}", femoShot=f"{tshot:.2f}", femoPfail=f"{pfl:.3f}",
           repAttempts=Rzero(pscen), repHours=f"{Rzero(pscen)*t1:.1f}", repHit=f"{1-(1-pscen)**Rzero(pscen):.3f}",
           repAttemptsSplit=Rsplit(pscen), repHoursSplit=f"{Rsplit(pscen)*t1:.1f}", repQlow=sci(dtot / 2 / Rsplit(pscen), 2),
           repHerald=f"{t1/pscen:.1f}",
           femoFastT=f"{rt('R-FEMO76-DC-fastest')/3600:.2f}", femoSelT=f"{rt('R-FEMO76-DC-fast')/3600:.2f}",
           femoLowDays=f"{rt('R-FEMO76-DC-low')/86400:.0f}", femoClassIdeal=f"{vv('C-FEMO76-ideal'):g}",
           femoClassCoreH=sci(vv("C-FEMO76-ideal-coreh"), 2), femoUcc=f"{vv('C-FEMO76-uccsdtq'):g}")
reprows = "".join(f"{pp:.2f} & {Rzero(pp)} & {Rzero(pp)*t1:.1f} & {Rsplit(pp)} & {Rsplit(pp)*t1:.1f}\\\\\n" for pp in (0.9, 0.8, 0.6, 0.5, 0.25, 0.1, 0.05))

# ---------------------------------------------------------------- output-rate scenario
b, n = float(MP[("readout", "b")]), float(MP[("readout", "n")])
ts, tf, bm = float(MP[("readout", "t_shot_slow")]), float(MP[("readout", "t_shot_fast")]), float(MP[("readout", "B_mem")])
with out("readout_curves.dat") as f:
    f.write("N q_ms q_us c_node\n")
    for k in range(60, 215, 5):
        N = 10 ** (k / 10)
        f.write(f"{N:.4g} {N*b*ts/n:.4g} {N*b*tf/n:.4g} {N*b/bm:.4g}\n")
Nex = float(MP[("readout", "N_example")])
mac.update(outQ=sci(Nex * b * ts / n), outC=f"{Nex*b/bm:g}", outRatio=sci(bm * ts / n, 0))

# ---------------------------------------------------------------- break-even model
tC, Pref = float(MP[("breakeven", "t_C")]), float(MP[("breakeven", "P_ref")])
def tstar(P_, tQ, d=2, Q=1):
    return (P_ * tQ / (Q ** (1 / d) * tC)) ** (d / (d - 1)) * tC / P_
with out("breakeven_curves.dat") as f:
    f.write("P d2ms d2hundred d2ten d3ms d4ms\n")
    for k in range(0, 71, 5):
        P_ = 10 ** (k / 10)
        f.write(f"{P_:.4g} {tstar(P_,1e-3):.4g} {tstar(P_,1e-4):.4g} {tstar(P_,1e-5):.4g} {tstar(P_,1e-3,3):.4g} {tstar(P_,1e-3,4):.4g}\n")
be = [tstar(Pref, 1e-3), tstar(Pref, 1e-4), tstar(Pref, 1e-5), tstar(Pref, 1e-3, 3), tstar(Pref, 1e-3, 4)]
with out("breakeven_annot.tex") as f:
    for v, col, lab, anc in [(be[0], "qcF", f"{be[0]/3.156e7:.1f} y", "east"), (be[1], "qcF!70", f"{be[1]/86400:.1f} d", "west"),
                             (be[2], "qcF!45", f"{be[2]/3600:.1f} h", "west"), (be[4], "black!60", f"{be[4]:.1f} s", "north")]:
        f.write("\\node[circle, fill=%s, inner sep=1.5pt] at (axis cs:%g,%g) {};\n\\node[font=\\scriptsize, anchor=%s, inner sep=5pt] at (axis cs:%g,%g) {%s};\n" % (col, Pref, v, anc, Pref, v, lab))
mac.update(beSms=sci(be[0], 0), beYms=f"{be[0]/3.156e7:.1f}", beShundred=sci(be[1], 0), beDhundred=f"{be[1]/86400:.1f}",
           beSten=sci(be[2], 0), beHten=f"{be[2]/3600:.1f}", beCubic=f"{be[3]:.0f}", beQuartic=f"{be[4]:.1f}")

# ---------------------------------------------------------------- DMRG planning curve
anc = MP[("dmrg_plan", "anchor")]
a_v, a_M = vv(anc), float(VI[anc]["note"].split("=")[1])
with out("dmrg_plan.dat") as f:
    f.write("M cpuh\n")
    for k in range(0, 14):
        Mv = a_M * 10 ** (k / 10)
        f.write(f"{Mv:.5g} {a_v*(Mv/a_M)**3:.5g}\n")
fug = float(MP[("cores", "fugaku")])
mac.update(planCoreH=sci(a_v * (12000 / a_M) ** 3), planMemTB=f"{348*(12000/a_M)**2/1000:.1f}")
with out("dmrg_annot.tex") as f:
    f.write("\\draw[black!40, dashed] (axis cs:1000,%g) -- (axis cs:30000,%g) node[pos=0.03, above, anchor=south west, font=\\scriptsize, black!60]{allocation equivalent: all Fugaku cores for one hour (not a runtime)};\n" % (fug, fug))

# ---------------------------------------------------------------- connectors, bars, lines
with out("dumbbell_annot.tex") as f:
    for row, a, c in [(1, "R-HUB-66-s", "C-S2-U4-6x6"), (2, "R-HUB-1010-s", "C-S2-U4-10x10"), (3, "R-HEIS-1010-s", "C-S1-J0.5-10x10"), (5, "R-P450-DC-fast", "C-P450-wall")]:
        f.write("\\draw[black!20, line width=1.4pt] (axis cs:%.5g,%d) -- (axis cs:%.5g,%d);\n" % (px("dumbbell", a), row, px("dumbbell", c), row))
    q5 = px("dumbbell", "R-FEMO76-DC-minvol")
    f.write("\\draw[qcU!60, line width=1.4pt] (axis cs:%.5g,4) -- (axis cs:%.5g,4);\n" % (q5, Rsplit(pscen) * t1))
with out("dumbbell_q_scen.dat") as f:
    f.write("x y\n%.5g 4\n%.5g 4\n" % (Rzero(pscen) * t1, Rsplit(pscen) * t1))
with out("gauge_annot.tex") as f:
    rows = defaultdict(dict)
    for p in P:
        if p["fig"] == "gauge": rows[int(float(p["y"]))][p["series"]] = p
    for y, d in sorted(rows.items()):
        if "ref" in d:
            x = float(d["ref"]["x"]); f.write("\\node[font=\\scriptsize, anchor=west, qcF, inner sep=5pt] at (axis cs:%g,%d) {%s Toffoli (different unit)};\n" % (x, y, sci(x)))
            continue
        lo, hi = float(d["lo"]["x"]), float(d["hi"]["x"])
        if hi > lo:
            f.write("\\draw[black!60, line width=4pt] (axis cs:%g,%d) -- (axis cs:%g,%d);\n" % (lo, y, hi, y))
            f.write("\\node[font=\\scriptsize, anchor=west, inner sep=5pt] at (axis cs:%g,%d) {%s--%s T};\n" % (hi, y, sci(lo, 0), sci(hi, 0)))
        else:
            f.write("\\node[font=\\scriptsize, anchor=east, inner sep=5pt] at (axis cs:%g,%d) {%s T, $\\sim10^5$ LQ};\n" % (lo, y, sci(lo)))
with out("femoco_annot.tex") as f:
    a, c = float(RI["R-FEMO54-compact"]["physical_qubits"]), float(RI["R-FEMO54-DFTHC"]["physical_qubits"])
    f.write("\\draw[{Latex[length=2mm]}-{Latex[length=2mm]}, black!50] (axis cs:%g,2.2) -- node[below, font=\\scriptsize]{%.0f$\\times$ fewer qubits} (axis cs:%g,2.2);\n" % (a, c / a, c))
with out("sqd_annot.tex") as f:
    s = vv("V-QSCI-samples")
    f.write("\\draw[qcU, line width=0.9pt] (axis cs:%g,1e-6) -- (axis cs:%g,1);\n" % (s, s))
    f.write("\\node[font=\\scriptsize, anchor=north east, align=right, qcUd] at (axis cs:%g,0.5) {%s samples for\\\\ $\\mu$Ha precision\\\\ (Reinholdt et al.)};\n" % (s * 0.75, sci(s, 0)))
    r1, r2 = vv("V-N2-rate-1e3"), vv("V-N2-rate-1e9")
    with out("sqd_interp.dat") as g:
        g.write("x y\n1e3 %g\n1e9 %g\n" % (r1, r2))

# ---------------------------------------------------------------- timeline labels
order = [l.strip() for l in open(os.path.join(HERE, "timeline_order.txt")) if l.strip()]
with out("timeline_axis.tex") as f:
    f.write("\\pgfplotsset{timelineaxis/.style={ytick={1,...,%d}, ymin=0.4, ymax=%.1f, yticklabels={%s}}}\n" % (
        len(order), len(order) + 0.6, ", ".join("{" + EI[e]["timeline_label"] + "}" for e in order)))

# ---------------------------------------------------------------- numbers quoted in the text
q = lambda k: float(RI[k]["physical_qubits"])
hub10, hub6, heis = vv("C-S2-U4-10x10"), vv("C-S2-U4-6x6"), vv("C-S1-J0.5-10x10")
ru = [rt("R-RU-" + s) for s in ("ns4", "ns3", "us4", "us3")]
aaT, aae, aad = (float(MP[("aa", k)]) for k in ("T", "eps", "delta"))
mac.update(
    nEntries=len(E), nEone=strata["E1"], nEtwo=strata["E2"], nEthree=strata["E3"], nEfour=strata["E4"],
    nTimeline=sum(tl.values()), nTLvalidation=tl["validation"], nTLobservables=tl["observables"],
    nTLpartial=tl["partial"], nTLcontested=tl["contested"], nTLopen=tl["open"], nTLchallenged=tl["challenged"],
    nClasses=len(F), nFstanding=pres["standing_claim"], nFtheory=pres["theory"], nFcontested=pres["contested"],
    nFnotcompared=pres["not_compared"], nFclasscap=pres["classical_capability"], nFmatched=pres["matched_scoped"],
    nFcapability=pres["capability"], nMcomplete=mat["complete"], nMpartial=mat["partial"], nMscenario=mat["scenario"],
    nMnone=mat["none"], nMna=mat["not_applicable"], nResources=len(R), nValues=len(V), nPoints=len(P), nCoords=ncoord, nChecks=npass,
    ratioHubTen=sci(hub10 / rt("R-HUB-1010-s")), ratioHubTenPar=sci(hub10 / rt("R-HUB-1010-p")),
    ratioHubSix=f"{hub6/rt('R-HUB-66-s'):.0f}", ratioHeis=f"{heis/rt('R-HEIS-1010-s'):.1f}", ratioHeisPar=f"{heis/rt('R-HEIS-1010-p'):.0f}",
    hubTenCoreH=sci(hub10 * 4 / 3600), hubTenFugakuH=f"{hub10*4/3600/fug:.1f}", heisCoreH=f"{heis*4/3600:.0f}",
    hubTenQh=f"{rt('R-HUB-1010-s')/3600:.0f}", hubTenParQh=f"{rt('R-HUB-1010-p')/3600:.1f}", heisQh=f"{rt('R-HEIS-1010-s')/3600:.1f}", heisCh=f"{heis/3600:.0f}",
    parQubitLo=f"{q('R-HUB-1010-p')/q('R-HUB-1010-s'):.0f}", parQubitHi=f"{q('R-HEIS-1010-p')/q('R-HEIS-1010-s'):.1f}",
    ruSpread=grp(round(max(ru) / min(ru), -1)), ruSpreadFixed=grp(round(rt("R-RU-us4") / rt("R-RU-ns4"), -1)),
    xasHours=f"{rt('R-XAS-av')/3600:.1f}", xasCircuits=grp(round(float(RI['R-XAS-alg']['n_nc']) / float(RI['R-XAS-circ']['n_nc']), -1)),
    xasCircS=f"{rt('R-XAS-circ'):.0f}", xasHoursOld=f"{rt('R-XAS-av-v2')/3600:.1f}",
    xasCircOld=sci(float(RI["R-XAS-circ-v2"]["n_nc"]), 2), xasAlgOld=sci(float(RI["R-XAS-alg-v2"]["n_nc"]), 2),
    xasGateRatio=f"{float(RI['R-XAS-alg']['n_nc'])/float(RI['R-XAS-alg-v2']['n_nc']):.2f}", xasCycleRatio=f"{rt('R-XAS-av')/rt('R-XAS-av-v2'):.2f}",
    xasCirc=sci(float(RI["R-XAS-circ"]["n_nc"]), 2), xasAlg=sci(float(RI["R-XAS-alg"]["n_nc"]), 2),
    femoSpace=f"{q('R-FEMO54-DFTHC')/q('R-FEMO54-compact'):.0f}",
    femoVol=f"{float(RI['R-FEMO54-DFTHC']['st_volume_Mqh'])/float(RI['R-FEMO54-efficient']['st_volume_Mqh']):.1f}",
    femoSevMinvolQ=f"{q('R-FEMO76-DC-minvol')/1e6:.2f}", femoSevFastQ=f"{q('R-FEMO76-DC-fastest')/1e6:.2f}", femoSevSelQ=f"{q('R-FEMO76-DC-fast')/1e6:.2f}", femoSevLowQ=grp(q('R-FEMO76-DC-low')),
    femoTofMinvol=sci(float(RI["R-FEMO76-DC-minvol"]["n_nc"]), 2), femoTofFast=sci(float(RI["R-FEMO76-DC-fastest"]["n_nc"]), 2),
    femoTofMinq=sci(float(RI["R-FEMO76-DC-minq"]["n_nc"]), 2), femoMinqH=grp(rt("R-FEMO76-DC-minq") / 3600), femoMinqShot=grp(float(RI["R-FEMO76-DC-minq"]["one_shot_runtime_s"]) / 3600),
    femoMinqPfail=RI["R-FEMO76-DC-minq"]["p_fail_logical"], femoLowPfail=RI["R-FEMO76-DC-low"]["p_fail_logical"],
    pfTofMinvol=sci(float(RI["R-P450-DC-minvol"]["n_nc"]), 2), pfTofFast=sci(float(RI["R-P450-DC-fast"]["n_nc"]), 2),
    thrHeis=f"{heis/rt('R-HEIS-1010-s'):.2f}", thrHeisPar=f"{heis/rt('R-HEIS-1010-p'):.1f}", nPairs=len(PAIRS), nLog=len(read("update_log.csv")),
    pfSpeed=f"{rt('R-P450-2022')/rt('R-P450-DC-minvol'):.0f}", pfQubits=f"{q('R-P450-2022')/q('R-P450-DC-minvol'):.1f}",
    pfMinvolH=f"{rt('R-P450-DC-minvol')/3600:.2f}", pfFastH=f"{rt('R-P450-DC-fast')/3600:.2f}", pfMinqDays=f"{rt('R-P450-DC-minq')/86400:.0f}",
    aaBound=sci(((4 * aaT) ** 8) * aae ** -14 * aad ** -8),
    merzQpu=grp(vv("V-MERZ-qpu")), merzCircuits=grp(vv("V-MERZ-circuits")), merzNodeH=sci(vv("V-MERZ-fugaku"), 2),
    dcMin=f"{vv('C-DC-TN'):g}", feDmrgH=f"{vv('C-FE4S4-DMRG'):g}",
    rateTFIM=sci(float(RI["R-TFIM-ns4"]["n_nc"]) / rt("R-TFIM-ns4"), 2),
)
for k in ("TLchallenged", "Timeline", "TLvalidation", "TLobservables", "TLpartial", "TLcontested", "TLopen", "Mpartial", "Mcomplete", "Fstanding"):
    mac["w" + k] = WORDS[mac["n" + k]]
with out("counts.tex") as f:
    f.write("% generated by ledger/make_figdata.py -- do not edit\n")
    for k, v in mac.items():
        f.write(f"\\newcommand{{\\{k}}}{{{v}}}\n")
    for r in E:
        if r["elapsed_days"] != "not_applicable":
            f.write("\\expandafter\\newcommand\\csname eld%s\\endcsname{%s}\n" % (r["entry_id"], grp(float(r["elapsed_days"]))))
    f.write("\\newcommand{\\eld}[1]{\\csname eld#1\\endcsname}\n")
    f.write("\\newcommand{\\reptablerows}{%\n" + reprows + "}\n")

# ---------------------------------------------------------------- source-check table
def esc(t):
    for a_, b_ in [("\\", "/"), ("&", "\\&"), ("%", "\\%"), ("$", "\\$"), ("#", "\\#"), ("_", "\\_"), ("~", "$\\sim$"), ("^", "\\^{}"), ("<", "$<$"), (">", "$>$")]:
        t = t.replace(a_, b_)
    return t
with out("update_table.tex") as f:
    for u in read("update_log.csv"):
        vi = esc(u["version_inspected"]) + ("; " + esc(u["issue"]) if u["issue"] else "")
        f.write("%s & %s & %s & %s & %s\\\\\n" % (u["date_jst"][5:], esc(u["source"]).replace("/", "/\\allowbreak ").replace(".", ".\\allowbreak "), esc(u["check"]), esc(u["result"]), vi))

# ---------------------------------------------------------------- tuple completeness and pairs
TF = [("instance_version", "instance and version"), ("boundaries", "boundaries"), ("tolerance", "tolerance and its meaning"),
      ("failure_prob_meaning", "failure-probability meaning"), ("workload", "workload"), ("access_model", "access model"),
      ("source_locator", "source locator")]
E12 = [r for r in E if r["stratum"] in ("E1", "E2")]
comprows = ""
for k, lab in TF:
    miss = sum(1 for r in E12 if r[k] in ("not_extracted", ""))
    comprows += "%s & %d & %d\\\\\n" % (lab, len(E12) - miss, miss)
def texify(t):
    for a_, b_ in [("not_reported", "not reported"), ("not_extracted", "not extracted"), ("not_applicable", "---"), ("&", "\\&"), ("%", "\\%"), ("_", "\\_"), ("^", "\\^{}"), ("~", "$\\sim$")]:
        t = t.replace(a_, b_)
    return t
with out("pairs_table.tex") as f:
    for r in PAIRS:
        f.write(" & ".join(texify(r[k]) for k in ("pair", "instance", "tolerance_and_meaning", "failure_probability_meaning", "workload", "what_is_missing")) + "\\\\\n")
with out("counts_extra.tex") as f:
    f.write("\\newcommand{\\nEoneEtwo}{%d}\n" % len(E12))
    f.write("\\newcommand{\\completenessrows}{%\n" + comprows + "}\n")

# ---------------------------------------------------------------- forward grid cells
cells = defaultdict(list)
for r in F:
    cells[(r["present_status"], r["resource_maturity"])].append(r["class_id"])
CW, CH = 2.2, 1.05
with out("forward_grid.tex") as f:
    f.write("% generated by ledger/make_figdata.py\n")
    for (x, y), ids in cells.items():
        i, j = XS.index(x), YS.index(y)
        f.write(f"\\node[gridcell] at ({i*CW+CW/2:.3f},{-j*CH-CH/2:.3f}) {{{', '.join(ids)}}};\n")
# pgf's coordinate parser does not accept exponents written with a plus sign
import re
for _f in os.listdir(OUT):
    if _f.endswith(("_annot.tex", "_labels.tex")):
        _p = os.path.join(OUT, _f); _t = open(_p).read()
        _t = re.sub(r"(\d)e\+0*(\d+)", r"\1e\2", _t); _t = re.sub(r"(\d)e-0(\d)", r"\1e-\2", _t)
        open(_p, "w").write(_t)
print("wrote figure data and %d macros to %s" % (len(mac), os.path.normpath(OUT)))
