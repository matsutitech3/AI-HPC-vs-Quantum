#!/usr/bin/env python3
"""Authoritative source of the v7 evidence ledger.

Writes eight linked CSV tables next to this file:
  entries.csv, pairs.csv, resources.csv, values.csv, models.csv,
  forward_classes.csv, figure_points.csv, update_log.csv
Direct edits to the CSV files are overwritten by this script; edit here.
Run:  python3 build_ledger.py && python3 make_figdata.py

Missing-value codes
  not_reported   the source does not give the value
  not_extracted  the source may give it; we have not read it out (our gap)
  not_applicable the field has no meaning for this row
  not_estimated  no estimate exists in the source and we make none
Locator levels
  table / section / primary_page : read by us at that location in a pinned version
  abstract / secondary / table_unverified : NOT used in any figure or ratio
"""
import csv, math, os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
CUTOFF = date(2026, 11, 11)
NR, NX, NA, NE = "not_reported", "not_extracted", "not_applicable", "not_estimated"

def days(a, b=None):
    a = date.fromisoformat(a)
    b = CUTOFF if b is None else date.fromisoformat(b)
    return (b - a).days

def w(name, header, rows):
    with open(os.path.join(HERE, name), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(header)
        for r in rows:
            assert len(r) == len(header), (name, r[0], len(r), len(header))
            wr.writerow(r)

# ====================================================================== entries
EH = ["entry_id", "stratum", "comparison_level", "problem", "model_or_circuit",
      "observable", "quantum_side", "classical_method", "method_class",
      "training_signal", "match_metric_and_tolerance", "match_type",
      "timeline_eligible", "first_claim_date", "claim_date_precision",
      "first_response_date", "response_date_precision", "elapsed_days",
      "present_result", "quantum_time", "quantum_time_kind", "classical_time",
      "classical_time_kind", "primary_sources"]
EX = ["task_family", "instance_version", "boundaries", "tolerance", "failure_prob_meaning",
      "workload", "access_model", "claim_status", "classical_capability", "matched_result",
      "sub_records", "source_locator", "timeline_label", "last_checked"]

def tl(claim, cprec, resp=None, rprec=NA):
    d = days(claim, resp) if claim else NA
    return [claim or NA, cprec, resp or NA, rprec, d]
NT = [NA, NA, NA, NA, NA]

E = [
 ["E01","E1","task","Random circuit sampling, 53 q","Sycamore RCS circuits","XEB on samples","Google Sycamore","Tensor-network contraction","SC","none","XEB comparable to experiment","validation_benchmark_matched","yes", *tl("2019-10-23","exact","2021-11-04","exact"),"matched",NR,NR,NR,NR,"pan2022;hangleiter2026"],
 ["E02","E1","task","Gaussian boson sampling, Jiuzhang 2.0","144-mode Jiuzhang 2.0 datasets","Low-order marginals and cross-entropy of the samples (2021 response); the experiment's benchmark statistics (2023 response)","USTC Jiuzhang 2.0","Marginal-based mock-up samplers (2021); tensor-network GBS algorithm (2023)","SC","none","2021: total variation distance of marginals to the ideal distribution, mock-up sampler against experiment; 2023: benchmark statistics used by the experiment","validation_challenged","yes", *tl("2021-06-29","exact","2021-09-23","exact"),"challenged_2021_matched_2023",NR,NR,NR,NR,"zhong2021;villalonga2021;martinez2023;oh2024"],
 ["E03","E1","task","Kicked Ising 127 q, 20 steps","Heavy-hex kicked TFIM (ideal circuit)","Local magnetizations","IBM Eagle","BP tensor networks; sparse Pauli dynamics","SC","none","Within experimental error bars","observables_reproduced","yes", *tl("2023-06-14","exact","2023-06-26","exact"),"matched",NR,NR,"laptop core (minutes)","measured","tindall2024;begusic2023;begusic2024"],
 ["E04","E1","task","Spin-glass annealing dynamics 2D/3D","Ising spin-glass quench","Selected observables, subsets of lattices and times","D-Wave Advantage2","BP-TN; Jastrow-Feenberg t-VMC","SC;CV","TDVP","Error vs reference in subset of regimes","observables_reproduced_partial","yes", *tl("2024-03-01","exact","2025-03-07","exact"),"partly_matched",NR,NR,NR,NR,"king2025;tindall2025;mauron2025;kingreply"],
 ["E05","E1","task","2D TFIM Floquet prethermalization, 56 q","7x8 periodic Trotterized TFIM","Magnetization dynamics","Quantinuum H2","TN; NN; operator truncation","SC;AI","mixed","No converged method in hardest regime","open","yes", *tl("2025-03-26","exact"),"standing",NR,NR,NR,NR,"haghshenas2025"],
 ["E06","E1","task","OTOC(2), 65 q","Random-circuit echo protocol","OTOC(2) per data point","Google Willow","TN contraction; TNMC; TNBP","SC","none","No published match found","open","yes", *tl("2025-06-11","exact"),"standing","~2 h (experiments)","measured","3.2 y per data point (Frontier)","estimated","google2025otoc;googleblog2025;bermejo2026"],
 ["E07","E1","task","Operator Loschmidt echo, 56 q","Disordered heavy-hex dynamics","OLE over full regime","IBM Heron + Algorithmiq","Three classical groups; monoprop","SC","none","Classical predictions mutually inconsistent","open","yes", *tl("2025-11-30","month_lower_bound"),"standing",NR,NR,NR,NR,"barron2026;ibmalgo2026"],
 ["E08","E4","decision","Rydberg spin-liquid diagnostics","Analog Rydberg array protocol","Renyi TEE (not measured)","Harvard simulator","Time-dependent VMC","CV","TDVP","n/a","not_applicable","no", *NT,"complementary_inference",NA,NA,NR,NR,"mauron2025tee;brydges2019"],
 ["E09","E1","workflow","Fe-S clusters by SQD","LUCJ sampling + classical diagonalization","Ground-state energy vs subspace size","IBM Heron + Fugaku","Selected CI; recovery; single-layer UCJ energy evaluation; ML selectors; GPU DMRG","SC;AI","variational/supervised","Determinants at 0.1 Ha error (ideal QSCI vs HCI)","no_advantage_claimed","no", *NT,"no_advantage_claimed",NR,NR,"<1 min laptop ([4Fe-4S] single-layer energy); 12.6 h one DGX B200 (CAS(54,36) DMRG)","measured","shirakawa2025;belagali2026;reinholdt2025;bonilla2026;legeza2026"],
 ["E10","E2","task","FeMoco 76-orbital model","Li et al. 76o113e active space","Ground-state energy, 1 kcal/mol","FTQC estimates (THC; spectrum amplification; dense code)","UDMRG + UCCSDTQ","SC","none","Empirical +-0.31 (consensus) / +-1.25 (conservative) kcal/mol","not_applicable","no", *NT,"classical_feasibility_ranking_unresolved","5.26 h expected (dense code, 1.17M physical)","modeled","22.9 h ideal Frontier; 2.77e6 core-h campaign","ideal/measured","zhai2026;low2025sa;lee2021thc;low2026dense"],
 ["E11","E3","theory","Generic ground-state chemistry","Ab initio and model Hamiltonians","Empirical cost scaling","QPE hypothesis","Classical heuristics","SC",NA,"n/a","not_applicable","no", *NT,"theory",NA,NA,NA,NA,"lee2023"],
 ["E12","E4","decision","Main-group thermochemistry","Skala XC functional","W4-17; GMTKN55 WTMAD-2","none","Learned functional","AI","supervised","WTMAD-2 3.89 (v1.0) / 2.72 (v1.1) kcal/mol","not_applicable","no", *NT,"no_quantum_comparator",NA,NA,NR,NR,"luise2025;skala10;skala11"],
 ["E13","E4","decision","Solid-electrolyte discovery","ML+DFT+MD screen of 32.6e6 candidates","Synthesis; structure; ionic conductivity","none","ML + DFT + MD on ~1000 cloud VMs","AI","supervised","18 candidates; NaxLi3-xYCl6 synthesized and characterized","not_applicable","no", *NT,"validated_classical_result",NA,NA,"<80 h screening wall time","measured","chen2024"],
 ["E14","E4","decision","Crystal stability at scale","GNoME","DFT hull stability","none","Graph networks + DFT active learning","AI","supervised","2.2e6 stable vs prior; ~381k on updated hull","not_applicable","no", *NT,"no_quantum_comparator",NA,NA,NR,NR,"merchant2023"],
 ["E15","E1","task","Lattice protein folding","Tetrahedral-lattice MJ Hamiltonian","Model energy; RMSD vs experiment","VQE on IBM devices","Exhaustive search/Gurobi on same Hamiltonian","SC","none","RMSD 1.781 (quantum best) vs 1.879 A (classical model optimum)","objectives_differ","no", *NT,"not_a_computational_tie",NR,NR,NR,NR,"robert2021;doga2024;zhang2026"],
 ["E16","E1","workflow","KRAS inhibitor generation","QCBM prior + LSTM","Generative benchmark metrics","IBM device","Classical generative priors","AI","supervised","Modest benchmark gain","not_applicable","no", *NT,"quantum_contribution_unisolated",NR,NR,NR,NR,"kras2025;uoft2025"],
 ["E17","E4","task","Spin-glass ground states","EA spin glasses","Residual energy","Simulated QA (emulation)","Variational neural annealing","AI","variational","Beats SA/SQA over studied sizes","not_applicable","no", *NT,"no_hardware_comparator",NA,NA,NR,NR,"hibat2021"],
 ["E18","E1","task","Approximate optimization, 2D spin glass","QAC-encoded QUBOs","Time-to-epsilon scaling","D-Wave + QAC","PT-ICM; simulated bifurcation","SC","none","Scaling exponent at gap >=1%","contested","yes", *tl("2024-01-14","exact","2025-05-28","exact"),"contested",NR,NR,NR,NR,"munoz2025;pawlowski2026"],
 ["E19","E4","task","MIS on 1e6-node graphs (control)","Sparse random regular graphs","Set size; runtime","none","GNN vs greedy","AI;SC","unsupervised","Greedy larger sets, 1e4x faster","not_applicable","no", *NT,"control",NA,NA,NR,NR,"angelini2022;schuetz2023"],
 ["E20","E3","theory","Recommendation, PCA, low-rank SDP","Low-rank linear algebra","Asymptotic complexity","Quantum linear algebra","Dequantized sampling","SC",NA,"n/a","not_applicable","no", *NT,"theory",NA,NA,NA,NA,"tang2021;tang2023;liu2021"],
 ["E21","E3","theory","Ground-state properties within a phase","Gapped local Hamiltonians","Sample/time complexity","QC simulation target","Classical ML on classical shadows","AI","supervised","n/a","not_applicable","no", *NT,"theory",NA,NA,NA,NA,"huang2022;huang2022exp"],
 ["E22","E4","decision","Nuclear ground states A<=20","Pionless EFT and cited interactions","Energies, radii, moments","Few-nucleon demos","Hidden-nucleon NQS","AI","variational","n/a","not_applicable","no", *NT,"no_matched_comparator",NA,NA,NR,NR,"lovato2022;gnech2024;lovato2026"],
 # ---- added in v6
 ["E23","E1","task","Heavy-hex Floquet magnetization, up to 74 q","Prethermal Floquet dynamics on Heron","Magnetization dynamics","IBM Heron + QESEM mitigation","Tensor networks; sparse Pauli-path (GPU, Fugaku)","SC","none","TN not converged; Pauli-path truncation-dependent (authors)","open","yes", *tl("2026-07-27","exact"),"standing",NR,NR,NR,NR,"leviatan2026"],
 ["E24","E1","task","Doped Clifford sampling, 70 q (original)","Open-boundary brickwork, 70 layers, 468 T","Amplitudes of published bitstrings; log-XEB","IBM Heron (spacetime codes)","Temporal-boundary tensor-network contraction","SC","none","log-XEB 0.350 [0.298, 0.403], compatible with reported fidelity bound","validation_benchmark_matched","yes", *tl("2026-07-28","exact","2026-08-13","exact"),"matched",NR,NR,"37.3 min on 256 H100 GPUs (2051 amplitude batches)","measured","martiel2026;manabe2026"],
 ["E25","E1","task","Doped Clifford sampling, 64 q (revised)","Depth-73 Clifford + 314 T, 76 physical qubits, cyclic connectivity","Sampling with fidelity lower bound 0.349 (95%)","IBM Heron (spacetime codes)","none found","SC","none","No published classical response found","open","yes", *tl("2026-09-01","exact_v2_posting"),"standing",NR,NR,NR,NR,"martiel2026"],
 ["E26","E1","task","Driven Bose-Hubbard sampling, 64 sites / 20 atoms","Driven chains and two-leg ladders, thermalized phase","Output samples; correlations to 14th order","USTC ultracold-atom quantum gas microscope","Tensor networks (authors' comparison)","SC","none","Authors: sampling rate 1e3x a supercomputer; Bayesian tests of phase","open","yes", *tl("2026-04-11","exact"),"standing",NR,NR,NR,NR,"zheng2026"],
 ["E27","E1","task","Maximum independent set, Rydberg array, up to 289 q","Unit-disk (Union-Jack-like) graphs","Probability of exact solution vs depth; scaling","Harvard Rydberg array","Exact and heuristic solvers; relaxed simulated annealing","SC","none","Quasi-planar instances solved to optimality at thousands of nodes in minutes","contested","yes", *tl("2022-02-18","exact","2023-07-18","exact"),"contested",NR,NR,"minutes on commodity hardware (thousands of nodes)","measured","ebadi2022;andrist2023"],
 ["E28","E1","workflow","Embedded protein-ligand electronic structure","EWF embedding + TrimSQD fragment solver; 11,608 and 12,635 atoms","Fragment energies vs DMRG/CCSD; binding energies","Two IBM Heron r2, up to 94 q","SCI (DICE), DMRG, CCSD on fragments","SC","none","TrimSQD 0.10-2.3 mHa above DMRG on named fragments; SCI better on one","no_advantage_claimed","no", *NT,"no_advantage_claimed","239 QPU-h (21,006 circuits)","measured","4.45e6 Fugaku node-h + GPU systems","measured","merz2026"],
 ["E29","E4","task","Direct neural solvers: frustrated and doped lattice models","J1-J2 Heisenberg 10x10 (J2=0.5); doped 2D Hubbard with t'","Variational energy; stripe order","none","Transformer neural quantum states","AI","variational","E/N = -0.497634(1) (J1-J2), below DMRG -0.495530","not_applicable","no", *NT,"no_matched_comparator",NA,NA,"4 days on 20 A100 GPUs (J1-J2)","measured","rende2024;gu2026"],
 ["E30","E4","task","Direct neural solvers: molecular excited states","Ab initio molecules; transition-metal model (per sources)","Excited-state energies and transition observables","none","Neural-network variational Monte Carlo","AI","variational","n/a","not_applicable","no", *NT,"no_matched_comparator",NA,NA,NX,NX,"pfau2024;schatzle2026"],
 ["E31","E3","theory","Query-model limit on unstructured quantum speedups","T-query quantum algorithms, decision problems, uniform inputs","Acceptance probability within eps on all but delta of inputs","Any T-query quantum algorithm","Deterministic classical queries to influential variables","SC",NA,"(4T)^8 eps^-14 delta^-8 classical queries","not_applicable","no", *NT,"theory_claimed_proof",NA,NA,NA,NA,"turturean2026;aa2014;bdst2026"],
 # ---- added in v7
 ["E32","E3","theory","Engineering PDEs by quantum linear-system and differential-equation solvers","Discretized elliptic and parabolic PDEs (FEM, finite differences); Carleman-linearized nonlinear flow","A functional of the solution at accuracy eps","HHL/QSVT linear solvers; quantum ODE solvers; Carleman linearization","Preconditioned Krylov and multigrid solvers; explicit time stepping; Monte Carlo","SC",NA,"Complexity in size, condition number, accuracy, dimension and nonlinearity","not_applicable","no", *NT,"theory",NA,NA,NA,NA,"hhl2009;aaronson2015;montanaro2016;linden2022;liu2021c;lewis2024;an2025"],
 ["E33","E2","task","Drag force and incompressible flow by quantum lattice-Boltzmann solvers","Flow past a sphere and related benchmarks; Carleman-embedded lattice Boltzmann equation","Drag force or another scalar of the flow","Fault-tolerant resource estimates by three groups","Explicit classical CFD (cost O(Re^3) for resolved turbulence, per penuel2025)","SC","none","Logical qubits x T gates; scaling with Reynolds number","not_applicable","no", *NT,"two_estimates_find_no_practical_advantage_one_reports_a_crossover_at_2^80_grid_points",NR,"modeled",NR,"scaling_law","penuel2025;jennings2025;zhuang2025;scherer2017"],
 ["E34","E1","task","Gaussian boson sampling, Jiuzhang (2020)","100-mode experiment of 2020 (dataset 1 of villalonga2021)","Low-order marginals and cross-entropy of the samples","USTC Jiuzhang","Marginal-based mock-up samplers; classically sampleable squashed-state model","SC","none","Total variation distance of marginals to the ideal distribution; Bayesian and heavy-output tests against an alternative classical model","validation_challenged","yes", *tl("2020-12-03","exact","2021-09-23","exact"),"challenged_not_matched",NR,NR,NR,NR,"zhong2020;villalonga2021;martinez2023"],
 ["E35","E1","task","Gaussian boson sampling, Borealis","Borealis datasets M16 to M288","Experiment-specific benchmark statistics","Xanadu Borealis","Tensor-network GBS algorithm","SC","none","Benchmark statistics used by the experiment","validation_benchmark_matched","yes", *tl("2022-06-01","exact","2023-06-06","exact"),"matched",NR,NR,NR,NR,"madsen2022;oh2024"],
 ["E36","E1","task","Gaussian boson sampling, Jiuzhang 3.0","144-mode Jiuzhang 3.0 dataset (high)","Experiment-specific benchmark statistics","USTC Jiuzhang 3.0","Tensor-network GBS algorithm","SC","none","Benchmark statistics used by the experiment","validation_benchmark_matched","yes", *tl("2023-04-24","exact","2023-06-06","exact"),"matched",NR,NR,NR,NR,"deng2023;oh2024"],
]
# extra (tuple and status) fields; unlisted fields default to not_extracted
XD = {k: NX for k in EX}
X = {
 "E01": dict(task_family="capability-sampling", instance_version="Sycamore 53 q, 20 cycles", claim_status="answered_validation", classical_capability="measured_run", matched_result="validation_benchmark", access_model="circuit description", timeline_label="Google Sycamore RCS, 53 q (2019)"),
 "E02": dict(task_family="capability-sampling", instance_version="arXiv:2106.15534v1 (29 Jun 2021); first response arXiv:2109.11525v1 (23 Sep 2021); later response arXiv:2306.03709v2", tolerance="2021: mock-up sampler closer than the experiment to the ideal marginals in total variation distance for the datasets tested; 2023: classical sampler better than the experiment on its benchmark statistics", claim_status="challenged_then_answered_validation", classical_capability="measured_run", matched_result="validation_challenge", source_locator="villalonga2021 v1: Table I, main result (total variation distance of marginals); oh2024 v2: largest-scale section; martinez2023: abstract (the quantum model explains Jiuzhang 2.0 better than the squashed-state alternative)", timeline_label="USTC Jiuzhang 2.0 GBS (2021)"),
 "E34": dict(task_family="capability-sampling", instance_version="Science 370, 1460 (3 Dec 2020); first response arXiv:2109.11525v1 (23 Sep 2021)", tolerance="mock-up sampler closer than the experiment to the ideal marginals in total variation distance; full high-click probabilities not evaluated", claim_status="validation_challenged", classical_capability="measured_run", matched_result="validation_challenge", source_locator="villalonga2021 v1: Table I lists dataset 1 as the 100-mode experiment (mean click number 41.04); martinez2023: abstract (a classical explanation of Jiuzhang 1.0 is not ruled out)", timeline_label="USTC Jiuzhang GBS, 100 modes (2020)"),
 "E35": dict(task_family="capability-sampling", instance_version="Nature 606, 75 (1 Jun 2022); response arXiv:2306.03709v2", claim_status="answered_validation", classical_capability="measured_run", matched_result="validation_benchmark", source_locator="oh2024 v2: dataset table (M16, M72, M216, M288) and largest-scale section", timeline_label="Xanadu Borealis GBS (2022)"),
 "E36": dict(task_family="capability-sampling", instance_version="arXiv:2304.12240v1 (24 Apr 2023); response arXiv:2306.03709v2", claim_status="answered_validation", classical_capability="measured_run", matched_result="validation_benchmark", source_locator="oh2024 v2: largest-scale section (Jiuzhang 3.0, high, M=144)", timeline_label="USTC Jiuzhang 3.0 GBS (2023)"),
 "E03": dict(task_family="coherent-dynamics", instance_version="127 q heavy-hex, ideal circuit", claim_status="answered_observables", classical_capability="measured_run", matched_result="observables_reproduced", timeline_label="IBM Eagle kicked Ising, 127 q (2023)"),
 "E04": dict(task_family="coherent-dynamics", instance_version="arXiv:2403.00910v1 (1 Mar 2024); Science 388, 199", claim_status="partly_answered", classical_capability="measured_run", matched_result="partial", timeline_label="D-Wave annealing dynamics (v1, 2024)"),
 "E05": dict(task_family="coherent-dynamics", instance_version="56 q, 7x8 periodic", boundaries="periodic", claim_status="standing", classical_capability="none_recorded", matched_result="open", timeline_label="Quantinuum H2 magnetism, 56 q (2025)"),
 "E06": dict(task_family="coherent-dynamics", instance_version="65 of 105 q", tolerance="not_extracted", workload="quantum: all experiments (about 2 h); classical: one data point (3.2 y est.); not one workload basis", access_model="circuit description", claim_status="standing", classical_capability="none_recorded", matched_result="open", timeline_label="Google OTOC(2), 65 q (2025)"),
 "E07": dict(task_family="coherent-dynamics", claim_status="standing", classical_capability="none_recorded", matched_result="open", timeline_label="IBM--Algorithmiq OLE, 56 q (2025)"),
 "E08": dict(task_family="analog-simulation", claim_status="no_claim", classical_capability="measured_run", matched_result="none"),
 "E09": dict(task_family="iron-sulfur-chemistry", instance_version="[2Fe-2S] (30e,20o); [4Fe-4S] CAS(54,36)", claim_status="no_claim", classical_capability="measured_run", matched_result="scoped_classical_single_layer_energy", sub_records="a: single-layer circuit-energy evaluation (classical, polynomial); b: ideal QSCI compactness vs HCI; c: hardware SQD product subspaces; d: full closed-loop workflow; e: GPU DMRG on CAS(54,36), instance match to c not extracted"),
 "E10": dict(task_family="femoco", instance_version="Li et al. 76o113e", boundaries="not_applicable", tolerance="1 kcal/mol on the model ground-state energy", failure_prob_meaning="classical: empirical extrapolation range, no probability; quantum: logical failure per shot tabulated (0.070 at minimum volume), spectral-hit probability not reported", workload="one energy per candidate state; the scientific question ranks spin isomers", access_model="second-quantized Hamiltonian; quantum side assumes a supplied initial state", source_locator="zhai2026 cost section; low2026dense Sec. VI.B and Table XXVII", claim_status="no_claim", classical_capability="extrapolated_estimate", matched_result="none"),
 "E11": dict(task_family="generic-chemistry", claim_status="theory", classical_capability="none_recorded", matched_result="none"),
 "E12": dict(task_family="thermochemistry", claim_status="no_claim", classical_capability="validated_benchmark", matched_result="none"),
 "E13": dict(task_family="materials-discovery", claim_status="no_claim", classical_capability="validated_experiment", matched_result="none"),
 "E14": dict(task_family="materials-discovery", claim_status="no_claim", classical_capability="validated_benchmark", matched_result="none"),
 "E15": dict(task_family="protein-structure", claim_status="no_claim", classical_capability="measured_run", matched_result="objectives_differ", sub_records="a: 2021-2024 lattice comparisons; b: 2026 binding-site study (own protocol)"),
 "E16": dict(task_family="molecular-generation", claim_status="no_claim", classical_capability="measured_run", matched_result="none"),
 "E17": dict(task_family="optimization", claim_status="no_claim", classical_capability="measured_run", matched_result="none"),
 "E18": dict(task_family="optimization", claim_status="contested", classical_capability="measured_run", matched_result="contested", timeline_label="D-Wave QAC optimization (v1, 2024)"),
 "E19": dict(task_family="optimization", claim_status="no_claim", classical_capability="measured_run", matched_result="none"),
 "E20": dict(task_family="qml-classical-data", access_model="l2-norm sampling access", claim_status="theory", classical_capability="theorem", matched_result="none"),
 "E21": dict(task_family="learning-quantum-systems", claim_status="theory", classical_capability="theorem", matched_result="none", sub_records="a: classical learnability after data access (huang2022); b: sample-complexity separation with quantum memory (huang2022exp)"),
 "E22": dict(task_family="nuclear", claim_status="no_claim", classical_capability="measured_run", matched_result="none"),
 "E23": dict(task_family="coherent-dynamics", instance_version="arXiv:2607.24937v1; heavy-hex ladders, up to 74 q", tolerance="absolute magnetization precision 0.02 (unbiased estimator) and 0.005 (extrapolated estimator), Fig. 1 caption", workload="magnetization per Floquet cycle", access_model="circuit description", claim_status="standing", classical_capability="none_recorded", matched_result="open", source_locator="v1 PDF: abstract, Sec. I, Fig. 1, Apps. B-D (validation hierarchy)", timeline_label="IBM Heron Floquet, 74 q (v1, 2026)"),
 "E24": dict(task_family="capability-sampling", instance_version="arXiv:2607.25941v1 (original instance: 70 q, 70 layers, 468 T)", boundaries="open", tolerance="log-XEB 0.350 with 95% interval [0.298, 0.403]", failure_prob_meaning="95% interval on the estimator", workload="2051 amplitude batches for the published bitstrings", access_model="circuit description and published bitstrings", claim_status="answered_validation", classical_capability="measured_run", matched_result="validation_benchmark", source_locator="arXiv listings; arXiv:2608.13110 abstract page (v2, 29 Oct 2026)", timeline_label="IBM doped Clifford, 70 q (v1, 2026)"),
 "E25": dict(task_family="capability-sampling", instance_version="arXiv:2607.25941v3 (revised instance: 64 q, depth 73, 314 T, 76 physical; v2 posted 1 Sep 2026)", boundaries="periodic (cycle graph)", tolerance="fidelity lower bound 0.349", failure_prob_meaning="95% confidence on the bound", workload="sampling with post-selection on syndromes", access_model="circuit description", claim_status="standing", classical_capability="none_recorded", matched_result="open", source_locator="v3 PDF: abstract and main text (periodic boundaries replace the open chain of v1)", timeline_label="IBM doped Clifford, 64 q (v2, 2026)"),
 "E26": dict(task_family="capability-sampling", instance_version="arXiv:2210.08556v2 (11 Apr 2026); PRX 16, 021057: chains and two-leg ladders, up to 64 sites and 20 atoms", workload="output samples and correlations to 14th order", claim_status="standing", classical_capability="none_recorded", matched_result="open", sub_records="history: v1 (16 Oct 2022), another title, a 32-site chain, computational power stated as comparable to the fastest supercomputer; not an advantage claim under the eligibility rule", source_locator="abstract pages of v1 and v2; arXiv listing", timeline_label="USTC ultracold atoms, 64 sites (v2, 2026)"),
 "E27": dict(task_family="optimization", instance_version="Science 376, 1209", claim_status="contested", classical_capability="measured_run", matched_result="contested", source_locator="abstracts; arXiv listing dates", timeline_label="Harvard Rydberg MIS, 289 atoms (2022)"),
 "E28": dict(task_family="iron-sulfur-chemistry;binding", instance_version="arXiv:2605.01138", workload="21,006 circuits; 3.0e9 measurement outcomes", claim_status="no_claim", classical_capability="measured_run", matched_result="none", source_locator="Secs. IV-VII; Tables II, IX-XII"),
 "E29": dict(task_family="lattice-models", instance_version="arXiv:2310.05715v2; arXiv:2507.02644v2", boundaries="not stated in retrieved text (J1-J2 benchmark)", claim_status="no_claim", classical_capability="measured_run", matched_result="none", source_locator="rende2024 Table I and Results; gu2026 abstract"),
 "E30": dict(task_family="excited-states", claim_status="no_claim", classical_capability="measured_run", matched_result="none", source_locator="not re-read; cited as context"),
 "E32": dict(task_family="linear-systems-pde", instance_version="published versions as cited", boundaries="not_applicable", tolerance="eps on a linear functional of the solution", failure_prob_meaning="per source", workload="one functional per solve", access_model="sparse-matrix oracle or block encoding; state-preparation oracle for the right-hand side", claim_status="theory", classical_capability="theorem", matched_result="none", source_locator="montanaro2016: Table I of arXiv:1512.05903v2 (PDF text layer); other sources: abstracts"),
 "E33": dict(task_family="fluids", instance_version="arXiv:2406.06323v3; PRX Quantum 7, 033060; arXiv:2509.08807v1; arXiv:1505.06552v2", tolerance="per source", workload="one scalar (drag force)", access_model="geometry and boundary data encoded in block encodings", claim_status="no_claim", classical_capability="scaling_law", matched_result="none", source_locator="abstract pages (11 Nov 2026)"),
 "E31": dict(task_family="query-complexity", instance_version="repository commit 2a6ceae (6 Nov 2026); Lean 4.33.0", tolerance="eps on acceptance probability", failure_prob_meaning="delta = fraction of exceptional inputs", access_model="query access to input bits", claim_status="theory", classical_capability="theorem_claimed_machine_checked_core", matched_result="none", source_locator="paper Secs. 1.1-1.3; Conjecture.lean"),
}
rows = []
for r in E:
    d = dict(XD); d.update(X.get(r[0], {})); d["last_checked"] = "2026-11-11"
    if r[12] != "yes" and d["timeline_label"] == NX: d["timeline_label"] = NA
    rows.append(r + [d[k] for k in EX])
E = rows
EHX = EH + EX
w("entries.csv", EHX, E)

# ====================================================================== resources
RH = ["res_id", "target", "model", "source", "source_version", "source_locator", "locator_level",
      "gate_type", "n_nc", "n_nc_kind", "n_nc_scope", "logical_qubits", "lq_convention",
      "physical_qubits", "runtime_s", "runtime_bound", "runtime_scope", "st_volume_Mqh",
      "schedule_assumptions", "coverage", "unvalidated_or_omitted", "extraction_gap",
      "one_shot_runtime_s", "p_fail_logical", "artifact_type", "retrieved", "provenance_status", "quantity_scope"]
R = []
def res(rid, target, model, source, ver, loc, lvl, gate=NR, n=NR, nk=NR, ns=NR, lq=NR, lqc=NR,
        pq=NR, rt=NR, rb="point", rs=NR, vol=NR, sched=NR, cov="partial", unv="", gap="", one=NA, pf=NA):
    art, ret = ART[source.split(";")[0]] if lvl not in ("secondary",) else ("secondary citation", "2026-11-09")
    prov = {"table": "primary_text", "section": "primary_text", "dataset": "primary_dataset", "abstract": "source_reported_aggregate", "secondary": "secondary", "table_unverified": "secondary"}[lvl]
    if nk in ("range_lo", "range_hi") and lvl == "abstract": prov = "source_reported_aggregate_unreconciled" if rid.startswith("R-CFD-PENUEL") else prov
    qs = "subroutine" if rs == "subroutine_only" else ("per_preparation" if "per preparation" in str(ns) else "application_or_execution")
    R.append([rid, target, model, source, ver, loc, lvl, gate, n, nk, ns, lq, lqc, pq, rt, rb, rs, vol, sched, cov, unv, gap, one, pf, art, ret, prov, qs])
# artifact actually read for each source, and the day it was retrieved (JST)
ART = {"beverland2022": ("PDF text layer", "2026-11-11"), "yoshioka2024": ("arXiv HTML", "2026-11-10"),
       "fomichev2025": ("PDF text layer", "2026-11-11"), "lee2021thc": ("PDF text layer", "2026-11-11"),
       "low2026dense": ("PDF text layer", "2026-11-11"), "low2025sa": ("PDF text layer", "2026-11-11"),
       "berry2024": ("PDF text layer", "2026-11-11"), "goings2022": ("published HTML (PMC)", "2026-11-09"),
       "lamm2026": ("arXiv HTML", "2026-11-09"), "osorio2025": ("PDF text layer", "2026-11-11"),
       "draper2026": ("PDF text layer", "2026-11-11"), "google2025otoc": ("PDF text layer", "2026-11-11"), "qsub": ("repository file at a pinned commit (web view)", "2026-11-11"), "scherer2017": ("PDF text layer", "2026-11-11"),
       "penuel2025": ("PDF text layer", "2026-11-11"), "zhuang2025": ("PDF text layer", "2026-11-11"),
       "jennings2025": ("PDF text layer (abstract and introduction)", "2026-11-11"),
       "googleblog2025": ("web page", "2026-11-09"), "zhai2026": ("arXiv HTML", "2026-11-10"),
       "manabe2026": ("abstract page", "2026-11-11"), "legeza2026": ("arXiv HTML", "2026-11-10"),
       "rende2024": ("arXiv HTML", "2026-11-10"), "reinholdt2025": ("PDF text layer", "2026-11-11"),
       "chen2024": ("published article", "2026-11-09"), "merz2026": ("PDF", "2026-11-10")}

BV = ("beverland2022", "arXiv:2211.07629v1", "Tables I and IV; App. F", "table")
for rid, rt, pq, sch in [("ns4", 0.56, 682020, "ns gates, p=1e-4, 199 factories"), ("ns3", 1.1, 8.2e6, "ns gates, p=1e-3, 242 factories"),
                         ("us4", 840, 6.8e5, "us gates, p=1e-4, 199 factories"), ("us3", 1740, 3.0e6, "us gates, p=1e-3, 199 factories")]:
    res("R-TFIM-" + rid, "2D TFIM dynamics", "100 spins, 10 4th-order Trotter steps", *BV, "T", 2.4e6, "point", "per_execution", 230, "compiled", pq, rt, "point", "per_execution", sched=sch, unv="repetitions for sampling/estimation; current classical baseline")
for rid, rt, pq, sch in [("ns4", 2.63e6, 1.9e6, "ns gates, p=1e-4"), ("ns3", 5.26e6, 6.9e6, "ns gates, p=1e-3"),
                         ("us4", 4.1e9, 1.6e6, "us gates, p=1e-4"), ("us3", 8.2e9, 6.4e6, "us gates, p=1e-3")]:
    res("R-RU-" + rid, "Ru CO2-fixation catalyst", "Beverland catalyst model", *BV, "T", 5.4e11, "point", "per_execution", 2740, "compiled", pq, rt, "point", "per_execution", sched=sch, unv="state preparation/overlap; classical baseline")
res("R-RSA", "RSA-2048 (reference)", "Beverland RSA", *BV, "T", 1.5e10, "point", "per_execution", 25481, "compiled", NR, 6.48e4, "point", "per_execution", sched="ns gates, p=1e-4", unv="reference only")

YO = ("yoshioka2024", "arXiv:2210.14109v3", "Supplementary Table S12", "table")
for rid, tgt, mdl, lq, pq, rt, sch in [
    ("R-HUB-66-s", "2D Fermi-Hubbard ground energy", "6x6 cylinder, U/t=4, half filling, eps=0.01 total", 72, 4.29e5, 1.23e4, "(1,1) single factory, d=23, p=1e-3"),
    ("R-HUB-66-p", "2D Fermi-Hubbard ground energy", "6x6 cylinder, U/t=4, half filling, eps=0.01 total", 72, 3.40e6, 1.59e3, "(16,16) parallel schedule, d=21, p=1e-3"),
    ("R-HUB-1010-s", "2D Fermi-Hubbard ground energy", "10x10 cylinder, U/t=4, half filling, eps=0.01 total", 200, 8.86e5, 1.05e5, "(1,1) single factory, d=25, p=1e-3"),
    ("R-HUB-1010-p", "2D Fermi-Hubbard ground energy", "10x10 cylinder, U/t=4, half filling, eps=0.01 total", 200, 5.42e6, 1.46e4, "(16,16) parallel schedule, p=1e-3"),
    ("R-HEIS-1010-s", "2D J1-J2 Heisenberg ground energy", "10x10 cylinder, J2/J1=0.5, eps=0.01 total", 100, 5.12e5, 5.64e4, "(1,1) single factory, d=23, p=1e-3"),
    ("R-HEIS-1010-p", "2D J1-J2 Heisenberg ground energy", "10x10 cylinder, J2/J1=0.5, eps=0.01 total", 100, 4.35e6, 4.32e3, "(16,16) parallel schedule, p=1e-3")]:
    res(rid, tgt, mdl, *YO, lq=lq, lqc="system qubits", pq=pq, rt=rt, rb="point", rs="modelled QPE schedule", sched=sch,
        unv="adiabatic preparation assumed cheap; classical baseline is 4-core DMRG; sign-free QMC not costed (Hubbard)")

XA = ("fomichev2025", "arXiv:2506.15784v3")
XUNV = "initial-state fidelity of the D=1e4 sum of Slaters; perturbative spectral-error model at target size; MHz logical clock; classical baseline is a rough RAS estimate"
res("R-XAS-circ", "X-ray absorption, Li4Mn2O", "CAS(22e,18o), longest circuit", *XA, "Table 1, row N=18; Introduction", "table", "Toffoli", 3.54e8, "point", "longest_circuit", 100, "minimum workspace incl. preparation ancillas, excl. factories", NR, 108.0, "point", "longest circuit: 1.08e8 logical cycles (source) at 1 MHz", sched="active-volume architecture, 350 logical qubits, 1 MHz logical clock; active volume 1.89e10", cov="complete_logical", unv=XUNV)
res("R-XAS-alg", "X-ray absorption, Li4Mn2O", "CAS(22e,18o), full sampled spectrum (S=2500 shots)", *XA, "Table 1, row N=18", "table", "Toffoli", 5.20e11, "point", "total_algorithm", 100, "minimum workspace incl. preparation ancillas, excl. factories", NR, NE, "point", "total over all circuits", sched="S=2500 shot budget; D=1e4 determinants; active volume 2.76e13", cov="complete_logical", unv=XUNV)
res("R-XAS-av", "X-ray absorption, Li4Mn2O", "CAS(22e,18o), active-volume implementation", *XA, "Introduction (active-volume paragraph)", "section", "Toffoli", 5.20e11, "point", "total_algorithm", 350, "active-volume architecture (workspace + memory)", NR, 1.58e5, "point", "total algorithm: 1.58e11 logical cycles (source) at 1 MHz; source: less than two days", sched="active-volume architecture, 1 MHz logical clock", cov="complete_logical", unv=XUNV)
XA2 = ("fomichev2025", "arXiv:2506.15784v2")
SUP = "superseded by v3 (5 Nov 2026); kept as history"
res("R-XAS-circ-v2", "X-ray absorption, Li4Mn2O", "CAS(22e,18o), longest circuit (v2)", *XA2, "Table I, row N=18; Introduction", "table", "Toffoli", 3.11e8, "point", "longest_circuit", 100, "minimum workspace incl. preparation ancillas, excl. factories", NR, 56.0, "point", "longest circuit: 5.6e7 logical cycles at 1 MHz (derived)", sched=SUP, cov="complete_logical", unv=XUNV)
res("R-XAS-alg-v2", "X-ray absorption, Li4Mn2O", "CAS(22e,18o), full sampled spectrum (v2)", *XA2, "Table I, row N=18", "table", "Toffoli", 4.58e11, "point", "total_algorithm", 100, "minimum workspace incl. preparation ancillas, excl. factories", NR, NE, "point", "total over all circuits", sched=SUP, cov="complete_logical", unv=XUNV)
res("R-XAS-av-v2", "X-ray absorption, Li4Mn2O", "CAS(22e,18o), active-volume implementation (v2)", *XA2, "Introduction; Sec. V; Fig. 10", "section", "Toffoli", 4.58e11, "point", "total_algorithm", 350, "active-volume architecture (workspace + memory)", NR, 8.1e4, "point", "total algorithm: 8.1e10 logical cycles at 1 MHz (source: less than a day)", sched=SUP, cov="complete_logical", unv=XUNV)

LEE = ("lee2021thc", "arXiv:2011.03494v3; PRX Quantum 2, 030305")
res("R-FEMO76-THC", "FeMoco ground energy", "76o113e (Li model), THC, M=450", *LEE, "Table V, row M=450", "table", "Toffoli", 3.2e10, "point", "per_run", 2196, "compiled", NR, NE, "point", "per_run", sched="no physical layout given for this model in the source", unv="initial-state overlap; repetitions")
res("R-FEMO54-THC-lee", "FeMoco-54 phase estimation", "54 orbitals (Reiher model), THC, M=350", *LEE, "Table IV, row M=350", "table", "Toffoli", 5.3e9, "point", "per_run", 2142, "compiled", NR, NE, "point", "per_run", sched="see R-FEMO54-THC-layout for the surface-code layout", unv="initial-state overlap; repetitions")
res("R-FEMO54-THC-layout", "FeMoco-54 phase estimation", "54 orbitals (Reiher model), THC, surface-code layout", *LEE, "Sec. IV C and Fig. 10", "section", "Toffoli", 6.7e9, "point", "per_run (layout count: 483,000 inner loops x 13,880 Toffoli)", 1908, "surface-code patches of the Fig. 10 floorplan", 4e6, 2.59e5, "point", "per_run: 3 days of Toffoli production at 25 kHz (abstract: under four days)", sched="p=1e-3, 1 us cycle, 10 us reaction, four CCZ factories, distance 31", unv="initial-state overlap; repetitions")
res("R-FEMO76-SA-count", "FeMoco ground energy", "76o113e (Li et al.), DFTHC + BLISS + spectrum amplification", "low2025sa", "arXiv:2502.15882v1", "Table I", "table", "Toffoli", 9.99e8, "point", "per_run", 1459, "as tabulated by the source", unv="initial-state overlap; repetitions", gap="no physical layout with this count")
res("R-FEMO54-SA-count", "FeMoco ground energy", "54o54e (Reiher et al.), DFTHC + BLISS + spectrum amplification", "low2025sa", "arXiv:2502.15882v1", "Table I", "table", "Toffoli", 3.41e8, "point", "per_run", 1137, "as tabulated by the source", unv="initial-state overlap; repetitions", gap="no physical layout with this count")
res("R-FEMO76-SA-sched", "FeMoco ground energy", "76o113e, spectrum amplification", "low2025sa;zhai2026", "via zhai2026", "schedule as cited in zhai2026", "secondary", "Toffoli", pq=4.5e6, rt=30960, rs="per_attempt", sched="four CCZ factories", unv="overlap; repetitions", gap="still second-hand: a reviewer locates this schedule in the article of record (PRX 15, 041016, Sec. V, p. 041016-15); the journal page did not permit text extraction on 11 Nov 2026")
res("R-FEMO-BERRY", "FeMoco ground energy incl. preparation", "Hamiltonian of the single-shot THC estimate the source compares with (ratio 2.3; consistent with the 76-orbital Li model at 3.2e10)", "berry2024", "arXiv:2409.11748v1", "abstract; Sec. I", "section", "Toffoli", 7.3e10, "point", "total_protocol", rt=NE, rs="2 or 3 QPE iterations from a matrix-product state of bond dimension 4000 (extrapolated overlap squared about 0.9), with symmetry shifting", sched="overlap extrapolation; candidate search excluded", unv="candidate search; extrapolation validity", gap="logical-qubit count and tables not extracted")
DC = ("low2026dense", "arXiv:2605.30455v1")
T27 = "App. F, Table XXVII (PDF text layer; each row passes volume = qubits x expected runtime and expected = one-shot/(1 - p_fail))"
for rid, mdl, pq, rt, rb, vol, sch in [
    ("DF", "prior art", 5.9e6, 5.18e6, "point", 8500, "double factorization"),
    ("THC", "prior art", 3.9e6, 2.59e5, "point", 280, "THC"),
    ("DFTHC", "prior art", 3.2e6, 1.08e4, "point", 8.6, "DFTHC + SA, layout of THC")]:
    res("R-FEMO54-" + rid, "FeMoco-54 phase estimation", "54o54e, 1 mHa (" + mdl + ")", *DC, "Fig. 1 table", "table", pq=pq, rt=rt, rb=rb, rs="runtime as tabulated for prior work", vol=vol, sched=sch + "; p=1e-3, 1 us cycle, 10 us reaction", unv="initial-state overlap")
RSX = "expected accepted runtime = one-shot runtime/(1 - p_fail), as defined in Sec. VI.B"
DCS = "dense planar surface code, p=1e-3, 1 us cycle, 10 us reaction"
# (id, target, model label, qubits/1e3, expected h, volume 1e6 qubit-h, one-shot h, p_fail, Toffoli/1e9, note)
for rid, tgt, mdl, pqk, rth, vol, osh, pf, tof, note in [
    ("R-FEMO54-DC-minq", "FeMoco-54 phase estimation", "54o54e, minimum qubits", 77.27, 11300, 873, 1290, 0.885, 18.9, ""),
    ("R-FEMO54-compact", "FeMoco-54 phase estimation", "54o54e, within-a-month row ('compact')", 88.84, 671, 59.6, 351, 0.477, 5.47, ""),
    ("R-FEMO54-balanced", "FeMoco-54 phase estimation", "54o54e, within-a-day row ('balanced')", 196.2, 22.8, 4.47, 15.5, 0.318, 1.39, ""),
    ("R-FEMO54-efficient", "FeMoco-54 phase estimation", "54o54e, minimum volume ('efficient')", 1149, 1.13, 1.30, 1.05, 0.071, 0.455, ""),
    ("R-FEMO54-fast", "FeMoco-54 phase estimation", "54o54e, fastest tabulated row ('fast')", 2002, 0.794, 1.59, 0.745, 0.061, 0.371, ""),
    ("R-FEMO76-DC-minq", "FeMoco ground energy", "76o113e, minimum qubits", 104.7, 42200, 4420, 6040, 0.857, 84.0, ""),
    ("R-FEMO76-DC-low", "FeMoco ground energy", "76o113e, within-a-month row", 166.9, 716, 120, 529, 0.262, 14.9, ""),
    ("R-FEMO76-DC-day", "FeMoco ground energy", "76o113e, within-a-day row", 444.0, 23.9, 10.6, 21.2, 0.111, 3.09, ""),
    ("R-FEMO76-DC-minvol", "FeMoco ground energy", "76o113e, minimum volume", 1170, 5.26, 6.16, 4.89, 0.070, 1.81, ""),
    ("R-FEMO76-DC-fast", "FeMoco ground energy", "76o113e, selected fast row (2.543 M qubits)", 2543, 2.64, 6.71, 2.38, 0.099, 1.10, ""),
    ("R-FEMO76-DC-fastest", "FeMoco ground energy", "76o113e, fastest tabulated row", 2692, 2.50, 6.73, 2.36, 0.058, 1.08, ""),
    ("R-P450-DC-minq", "P450 Cpd I (model X)", "Cpd1X 58o63e, minimum qubits", 81.13, 10800, 879, 1500, 0.862, 21.6, ""),
    ("R-P450-DC-month", "P450 Cpd I (model X)", "Cpd1X 58o63e, within-a-month row", 96.64, 658, 63.6, 450, 0.316, 7.01, ""),
    ("R-P450-DC-day", "P450 Cpd I (model X)", "Cpd1X 58o63e, within-a-day row", 223.3, 22.6, 5.04, 17.4, 0.229, 2.08, ""),
    ("R-P450-DC-minvol", "P450 Cpd I (model X)", "Cpd1X 58o63e, minimum volume", 1029, 1.88, 1.93, 1.69, 0.098, 0.702, ""),
    ("R-P450-DC-fast", "P450 Cpd I (model X)", "Cpd1X 58o63e, fastest tabulated row", 2181, 1.11, 2.41, 1.07, 0.034, 0.534, ""),
    ("R-RU56-DC-minq", "Ru catalyst XVIII (56o64e)", "XVIII 56o64e, minimum qubits", 75.91, 3200, 243, 351, 0.890, 5.55, "different active space from the Beverland catalyst model"),
    ("R-RU56-DC-minvol", "Ru catalyst XVIII (56o64e)", "XVIII 56o64e, minimum volume", 877.8, 0.693, 0.609, 0.620, 0.106, 0.263, "different active space from the Beverland catalyst model"),
    ("R-RU56-DC-fast", "Ru catalyst XVIII (56o64e)", "XVIII 56o64e, fastest tabulated row", 1567, 0.463, 0.726, 0.444, 0.042, 0.225, "different active space from the Beverland catalyst model")]:
    res(rid, tgt, mdl, *DC, T27, "table", "Toffoli", (tof * 1e9 if tof != NX else NX), ("point" if tof != NX else NX), "per_run (column Toffolis: total incl. rotation and state-preparation parts)", NX, "not constructed: the source tabulates compute, hot-storage and cold-storage regions separately", pqk * 1e3, rth * 3600, "point", RSX, vol,
        DCS + ("; " + note if note else ""), unv="initial-state overlap; spectral-hit repetitions; success criterion; architecture mapping",
        gap=("one-shot, failure-probability and Toffoli columns of this row not re-read" if tof == NX else ""),
        one=(osh * 3600 if osh != NX else NX), pf=pf)
res("R-P450-2022", "P450 Cpd I (model X)", "58 orbitals, THC", "goings2022", "PNAS (PMC9499570)", "Table 2 and text", "table", "Toffoli", 7.8e9, "point", "per_run", NR, NR, 4624440, 2.63e5, "point", "per_run", sched="p=1e-3, four factories", unv="overlap; spin-gap target")
res("R-P450-2022-p5", "P450 Cpd I (model X)", "58 orbitals, THC", "goings2022", "PNAS (PMC9499570)", "text", "section", "Toffoli", 7.8e9, "point", "per_run", NR, NR, 5e5, 9.0e4, "point", "per_run", sched="p=1e-5", unv="overlap; spin-gap target")
res("R-P450-FULL", "P450 Cpd I ~500-orbital model", "~500 orbitals", "goings2022", "PNAS (PMC9499570)", "text", "section", "Toffoli", 1.5e12, "point", "per_run", 9000, "compiled", rt=NE, rs="per_run", unv="overlap; feasibility")
LM = ("lamm2026", "arXiv:2603.29091v3")
GU = "state preparation; observable estimation; truncation convergence"
res("R-SU3-KN", "Real-time SU(3), fiducial shear viscosity", "10^3 lattice, electric basis, Trotter", *LM, "Table 5 (Kan-Nam type)", "table", "T", 6.5e48, "point", "evolution_only", 1e5, "approximate (per carena2022)", rt=NE, rs="evolution_only", sched="synthesis precision 1e-8", cov="scenario", unv=GU)
res("R-SU3-LCU", "Real-time SU(3), fiducial", "electric-basis LCU", *LM, "Table 5", "table", "T", 1e11, "range_lo", "evolution_only", rt=NE, rs="evolution_only", cov="scenario", unv=GU)
res("R-SU3-LCU-hi", "Real-time SU(3), fiducial", "electric-basis LCU", *LM, "Table 5", "table", "T", 1e14, "range_hi", "evolution_only", rt=NE, rs="evolution_only", cov="scenario", unv=GU)
res("R-SU3-S72-L", "Real-time SU(3), fiducial", "Sigma(72x3) discrete subgroup", *LM, "Table 5", "table_unverified", "T", 3.5e12, "point", "evolution_only", rt=NE, rs="evolution_only", cov="scenario", unv=GU + "; subgroup approximation", gap="secondary summary of R-SU3-S72-O, which we read in the primary; not an independent estimate")
res("R-SU3-S72-O", "Real-time SU(3), fiducial shear viscosity", "Sigma(72x3) discrete subgroup, Kogut-Susskind Hamiltonian", "osorio2025", "arXiv:2511.17437v1", "Sec. IX (resource estimate); encoding section", "section", "T", 3.5e12, "point", "evolution_only", 2.7e4, "data registers only: 9 qubits per link register, 3 links per site, 10^3 sites; ancillas not extracted", rt=NE, rs="evolution_only", cov="scenario", unv=GU + "; subgroup approximation", gap="ancilla width not extracted")
res("R-SU3-S72-OI", "Real-time SU(3), fiducial shear viscosity", "Sigma(72x3) discrete subgroup, improved Hamiltonian", "osorio2025", "arXiv:2511.17437v1", "Sec. IX (resource estimate)", "section", "T", 7.1e12, "point", "evolution_only", 2.7e4, "data registers only, as above", rt=NE, rs="evolution_only", cov="scenario", unv=GU + "; subgroup approximation", gap="ancilla width not extracted")
res("R-SU3-BE-B6", "SU(3) plaquette block encoding", "truncation B=6", "draper2026", "arXiv:2608.17115v1", "Tables 5 and 6", "table", "T", 1.2e5, "approx", "subroutine: one plaquette oracle U_p including PREP and its inverse", NR, "lattice register 10 L^3 plus proposal ancillas (Table 6); not a total width", rt=NE, rs="subroutine_only", cov="scenario", unv="normalization, evolution time, routing (about 1e2 L^3 per the source), state preparation, observable and shots", gap="not an application count")
res("R-SU3-BE-B9", "SU(3) plaquette block encoding", "truncation B=9", "draper2026", "arXiv:2608.17115v1", "Tables 5 and 6", "table", "T", 1.2e6, "approx", "subroutine: one plaquette oracle U_p including PREP and its inverse", NR, "lattice register 12 L^3 plus proposal ancillas (Table 6); not a total width", rt=NE, rs="subroutine_only", cov="scenario", unv="as above", gap="not an application count")
res("R-SU3-KRY", "Real-time SU(3), fiducial", "large-Nc / Krylov truncations", "lamm2026;ciavarella2025", "arXiv:2603.29091v3", "Table 5", "table", "T", 1e9, "range_lo", "evolution_only", rt=NE, rs="evolution_only", cov="scenario", unv="aggressive truncation; continuum control not established")
res("R-SU3-KRY-hi", "Real-time SU(3), fiducial", "large-Nc / Krylov truncations", "lamm2026;ciavarella2025", "arXiv:2603.29091v3", "Table 5", "table", "T", 1e12, "range_hi", "evolution_only", rt=NE, rs="evolution_only", cov="scenario", unv="as above")
res("R-SU3-DRAPER", "Non-Abelian LGT block encoding", "per plaquette oracle", "draper2026", "as read for v4", "abstract", "abstract", "T", 1e5, "range_lo", "subroutine", lqc="12L^3+O(1e3)", rt=NE, rs="subroutine", cov="scenario", unv="subroutine only", gap="full text not read")
LSG = "source-reported aggregate (abstract and introduction). The public per-instance files (R-CFD-PENUEL-Re*) give products from 5.3e21 to 7.9e40; the selection rule and tolerance behind the published range are not documented. The source authors have not been contacted (author decision, 11 Nov 2026)"
res("R-QLSA-EM", "EM scattering cross section of a 2D target (FEM)", "N=332,020,680 unknowns, accuracy 0.01, HHL-type solver with oracles", "scherer2017", "arXiv:1505.06552v2; Quantum Inf. Process. 16, 60", "Table II (depths); abstract (widths)", "table", "elementary gates (circuit depth)", 1.8e29, "point", "circuit depth incl. oracles (3.30e25 without); T-depth 8.2e28 (1.28e25 without); measurements 2.8e27 (8.23e21 without)", 1e8, "circuit width incl. oracles (340 without), from the abstract", rt=NE, rs="logical circuit only", unv="physical-level cost; classical baseline is a big-O comparison", gap="width column of Table II not extracted")
res("R-CFD-PENUEL-lo", "Drag force, flow past a sphere", "Carleman-linearized lattice Boltzmann, lowest Reynolds number studied", "penuel2025", "arXiv:2406.06323v3", "abstract", "abstract", "logical qubits x T gates", 1e21, "range_lo", "product over the whole algorithm", rt=NE, rs="logical resources only", unv="block-encoding constants; time-step restriction of explicit evolution", gap=LSG)
res("R-CFD-PENUEL-hi", "Drag force, flow past a sphere", "Carleman-linearized lattice Boltzmann, highest Reynolds number studied", "penuel2025", "arXiv:2406.06323v3", "abstract", "abstract", "logical qubits x T gates", 1e39, "range_hi", "product over the whole algorithm", rt=NE, rs="logical resources only", unv="as above", gap=LSG)
QS = ("qsub", "github.com/isi-usc-edu/qsub, commit cc8d3ce00c0b1ac73c0fd15bc1ea46caf42c19fc")
res("R-CFD-PENUEL-Re1e1", "Drag force, flow past a sphere, Re=1e1", "Carleman-linearized lattice Boltzmann, structured encoding", *QS, "QRE/CFD/2025-06/CFD_sphere_structured_logRe_10.json, logical-abstract", "dataset", "T", 9.328557736283274e+17, "point", "per instance as stored (t_count)", 5679, "num_qubits as stored", rt=NE, rs="logical resources only", unv="initial-state calls, some lower-level T gates and inlet/outlet boundary conditions are not costed by the source", gap="tolerance appears only in a task string (0.05); timestamp is a template field")
res("R-CFD-PENUEL-Re1e2", "Drag force, flow past a sphere, Re=1e2", "Carleman-linearized lattice Boltzmann, structured encoding", *QS, "QRE/CFD/2025-06/CFD_sphere_structured_logRe_100.json, logical-abstract", "dataset", "T", 4.980942352172372e+19, "point", "per instance as stored (t_count)", 57791, "num_qubits as stored", rt=NE, rs="logical resources only", unv="initial-state calls, some lower-level T gates and inlet/outlet boundary conditions are not costed by the source", gap="tolerance appears only in a task string (0.05); timestamp is a template field")
res("R-CFD-PENUEL-Re1e3", "Drag force, flow past a sphere, Re=1e3", "Carleman-linearized lattice Boltzmann, structured encoding", *QS, "QRE/CFD/2025-06/CFD_sphere_structured_logRe_1000.json, logical-abstract", "dataset", "T", 3.1333332196494777e+21, "point", "per instance as stored (t_count)", 629387, "num_qubits as stored", rt=NE, rs="logical resources only", unv="initial-state calls, some lower-level T gates and inlet/outlet boundary conditions are not costed by the source", gap="tolerance appears only in a task string (0.05); timestamp is a template field")
res("R-CFD-PENUEL-Re1e4", "Drag force, flow past a sphere, Re=1e4", "Carleman-linearized lattice Boltzmann, structured encoding", *QS, "QRE/CFD/2025-06/CFD_sphere_structured_logRe_10000.json, logical-abstract", "dataset", "T", 1.8637968777079765e+23, "point", "per instance as stored (t_count)", 6858591, "num_qubits as stored", rt=NE, rs="logical resources only", unv="initial-state calls, some lower-level T gates and inlet/outlet boundary conditions are not costed by the source", gap="tolerance appears only in a task string (0.05); timestamp is a template field")
res("R-CFD-PENUEL-Re1e5", "Drag force, flow past a sphere, Re=1e5", "Carleman-linearized lattice Boltzmann, structured encoding", *QS, "QRE/CFD/2025-06/CFD_sphere_structured_logRe_100000.json, logical-abstract", "dataset", "T", 9.531670418463518e+24, "point", "per instance as stored (t_count)", 74292561, "num_qubits as stored", rt=NE, rs="logical resources only", unv="initial-state calls, some lower-level T gates and inlet/outlet boundary conditions are not costed by the source", gap="tolerance appears only in a task string (0.05); timestamp is a template field")
res("R-CFD-PENUEL-Re1e6", "Drag force, flow past a sphere, Re=1e6", "Carleman-linearized lattice Boltzmann, structured encoding", *QS, "QRE/CFD/2025-06/CFD_sphere_structured_logRe_1000000.json, logical-abstract", "dataset", "T", 4.617209900690028e+26, "point", "per instance as stored (t_count)", 800059756, "num_qubits as stored", rt=NE, rs="logical resources only", unv="initial-state calls, some lower-level T gates and inlet/outlet boundary conditions are not costed by the source", gap="tolerance appears only in a task string (0.05); timestamp is a template field")
res("R-CFD-PENUEL-Re1e7", "Drag force, flow past a sphere, Re=1e7", "Carleman-linearized lattice Boltzmann, structured encoding", *QS, "QRE/CFD/2025-06/CFD_sphere_structured_logRe_10000000.json, logical-abstract", "dataset", "T", 2.0714809615313216e+28, "point", "per instance as stored (t_count)", 8000587876, "num_qubits as stored", rt=NE, rs="logical resources only", unv="initial-state calls, some lower-level T gates and inlet/outlet boundary conditions are not costed by the source", gap="tolerance appears only in a task string (0.05); timestamp is a template field")
res("R-CFD-PENUEL-Re1e8", "Drag force, flow past a sphere, Re=1e8", "Carleman-linearized lattice Boltzmann, structured encoding", *QS, "QRE/CFD/2025-06/CFD_sphere_structured_logRe_100000000.json, logical-abstract", "dataset", "T", 9.224349527801268e+29, "point", "per instance as stored (t_count)", 85720153832, "num_qubits as stored", rt=NE, rs="logical resources only", unv="initial-state calls, some lower-level T gates and inlet/outlet boundary conditions are not costed by the source", gap="tolerance appears only in a task string (0.05); timestamp is a template field")
res("R-CFD-ZHUANG", "Navier-Stokes on a 2^80-point mesh (linear system of dimension 2^82)", "spectral input/output, synthesized circuit, refined error correction", "zhuang2025", "arXiv:2509.08807v1", "Appendix F, Eqs. F12-F34", "section", "Toffoli", 9.41e7, "point", "per preparation and solve (Eq. F20); arbitrary rotations are a separate count, 3.94e8", 181, "logical algorithm width (Eq. F12)", 8.71e6, 3.68e6, "point", "1,000 preparations for compressed-sensing tomography of the output (Eqs. F26, F30)", sched="distance 25; physical error 5e-4; 1 us cycle; 28,301 queries; factories 8.16e6 of 8.71e6 physical qubits", unv="spectrally compact input, intermediate states and output; condition number at most 550; classical baseline materializes the full system", gap="rotation synthesis cost is the source's; no T-count conversion made")
for _r in R:
    if _r[0].endswith("-v2"):
        _r[-2], _r[-1] = "PDF via fetch tool", "2026-11-10"
w("resources.csv", RH, R)
RI = {r[0]: dict(zip(RH, r)) for r in R}

# ====================================================================== values
VH = ["val_id", "quantity", "value", "unit", "kind", "bound", "scope_or_machine", "source", "source_version", "locator", "locator_level", "note", "artifact_type", "retrieved"]
V = []
def val(vid, q, v, unit, kind, src, ver, loc, lvl="table", bound="point", scope="", note=""):
    art, ret = ART[src.split(";")[0]]
    V.append([vid, q, v, unit, kind, bound, scope, src, ver, loc, lvl, note, art, ret])
val("C-OTOC-q", "OTOC(2), experimental data collection time per circuit", 2.1, "h", "measured", "google2025otoc", "arXiv:2506.10191v1", "main text beside Fig. 4(c)", "section", scope="Willow, 65 qubits; 7,560 s; data collection only")
val("C-OTOC-c", "OTOC(2), classical time per circuit", 3.2, "y", "estimated", "google2025otoc", "arXiv:2506.10191v1", "main text beside Fig. 4(c)", "section", scope="tensor-network contraction on Frontier, cost model; the source states a factor of about 13,000 (3.2 y / 2.1 h = 13,358)")
Y3 = "arXiv:2210.14109v3"
DM = "single AMD EPYC 7702 CPU, 4 cores (ITensor); time to a state with E-E0<=0.01, E0 extrapolated"
S1 = {0.0: [(6, 6, 2.3), (8, 8, 1.1e2), (10, 10, 3.7e4), (12, 12, 9.6e5)],
      0.5: [(6, 6, 2.9), (8, 8, 1.9e2), (10, 10, 7.9e4), (12, 12, 1.3e6)]}
S2 = {1.0: [(4, 4, 8.8), (4, 8, 4.1e2), (4, 16, 4.8e3)],
      4.0: [(4, 4, 3.6e1), (4, 8, 1.5e3), (6, 6, 2.2e5), (8, 8, 1.5e9), (10, 10, 7.1e9), (4, 16, 1.2e4)],
      8.0: [(4, 4, 1.6e2), (4, 8, 2.0e3), (6, 6, 7.4e3), (8, 8, 9.4e4), (10, 10, 3.7e8), (4, 16, 9.9e3)]}
for j, pts in S1.items():
    for lx, ly, t in pts:
        val(f"C-S1-J{j:g}-{lx}x{ly}", f"DMRG time, J1-J2 Heisenberg {lx}x{ly} cylinder, J2/J1={j:g}", t, "s", "estimated", "yoshioka2024", Y3, "Supplementary Table S1", scope=DM, note=f"sites={lx*ly}")
for u, pts in S2.items():
    for lx, ly, t in pts:
        val(f"C-S2-U{u:g}-{lx}x{ly}", f"DMRG time, Hubbard {lx}x{ly} cylinder, U/t={u:g}, half filling", t, "s", "estimated", "yoshioka2024", Y3, "Supplementary Table S2", scope=DM, note=f"sites={lx*ly}")
ZC = ("zhai2026", "arXiv:2601.04621v2", "section 'Cost of classical methods and quantum advantage'", "section")
val("C-FEMO76-ideal", "FeMoco-76: two variational UDMRG sweeps at D=393,000, idealized wall time (calculation not performed)", 22.9, "h", "ideal", *ZC, scope="FLOP estimate at 1.102 exaFLOPS with ideal scaling; candidate construction and ranking not included")
val("C-FEMO76-ideal-coreh", "FeMoco-76: the same two sweeps in CPU core-hours, from the D^3.05 law", 4.08e9, "core-h", "extrapolated", *ZC, scope="largest bond dimension actually run: 18,000")
val("C-FEMO76-uccsdtq", "FeMoco-76: full-space UCCSDTQ estimate, idealized wall time", 21.0, "s", "ideal", *ZC, scope="same FLOP basis; the source calls its classical cost estimates upper bounds that omit practical implementation factors")
val("C-FEMO76-campaign", "FeMoco-76 UDMRG campaign", 2768994, "core-h", "measured", "zhai2026", "arXiv:2601.04621v2", "cost table", "table")
val("C-FEMO76-sweep", "FeMoco-76 UDMRG one sweep, D=18000", 317440, "core-h", "measured", "zhai2026", "arXiv:2601.04621v2", "cost table", "table", note="M=18000")
GO = ("goings2022", "PNAS (PMC9499570)", "Table 1")
val("C-P450-G1500", "P450 model G DMRG, M=1500", 1800, "CPU-h", "measured", *GO, note="M=1500")
val("C-P450-X1500", "P450 model X DMRG, M=1500", 4570, "CPU-h", "estimated", *GO, note="M=1500")
val("C-P450-X3000", "P450 model X DMRG, M=3000", 36564, "CPU-h", "estimated", *GO, note="M=3000")
val("C-P450-wall", "P450 model X DMRG wall time, M=3000", 720, "h", "estimated", *GO, scope="about one month, source estimate")
XV = ("fomichev2025", "arXiv:2506.15784v3")
val("C-XAS-RAS-1000", "Classical RAS estimate, 1000 states, CAS(22e,18o)", 32, "d", "estimated", *XV, "Sec. 5", "section", scope="0.76 h x 1000 states; source (v3): likely an optimistic estimate on the classical side; v2 added that the cost may be closer to 100 days")
val("C-XAS-RAS-gs", "Classical RAS estimate, ground state, CAS(22e,18o)", 0.76, "h", "estimated", *XV, "Sec. 5", "section")
PN = ("penuel2025", "arXiv:2406.06323v3", "Table 3")
WS = "ANSYS steady RANS on one workstation (Intel Xeon W-11855M, 96 GB); mesh generation plus solver run; the source uses these runtimes as its utility threshold"
for re_, mesh, run in [(3, 0.1, 1), (4, 8 / 60, 1), (5, 20 / 60, 3), (6, 4, 3), (7, 5, 5)]:
    val("C-CFD-RANS-Re1e%d" % re_, "Drag on a sphere, classical reference, Re=1e%d" % re_, round(mesh + run, 2), "h", "measured", *PN, scope=WS, note="mesh %.2f h + run %d h; Re=1e8 exceeded the workstation memory" % (mesh, run))
val("C-CFD-ZHUANG-classical", "Navier-Stokes, 2^80-point grid, classical time", 130, "y", "estimated", "zhuang2025", "arXiv:2509.08807v1", "main text", "section", scope="banded Cholesky operation count >= 7.13e27 FLOPs on the full 2^82-dimensional system divided by 1.74e18 FLOP/s (Eqs. F37, F38); the source states a 1100x speedup; conjugate gradients > 9.96e29 FLOPs (Eq. F36), about 18,000 years; neither model uses the spectral compactness assumed on the quantum side")
val("C-DC-TN", "Doped Clifford 70 q, tensor-network amplitudes", 37.3, "min", "measured", "manabe2026", "arXiv:2608.13110 (v1 13 Aug 2026; abstract page of v2, 29 Oct 2026)", "abstract", "abstract", scope="32 nodes x 8 H100 GPUs; 2051 amplitude batches")
val("C-FE4S4-DMRG", "Fe4S4 CAS(54,36) DMRG, D_SU(2)=12288", 12.6, "h", "measured", "legeza2026", "arXiv:2603.28648v1", "numerical benchmark section", "section", scope="one DGX B200 node; E=-327.24466 Ha")
val("C-NQS-J1J2", "Transformer NQS, J1-J2 10x10, J2/J1=0.5", 96, "h", "measured", "rende2024", "arXiv:2310.05715v2", "Results; Table I", "table", scope="20 A100 GPUs; E/N=-0.497634(1)")
RE = ("reinholdt2025", "arXiv:2501.07231v5; J. Chem. Theory Comput. 21, 6811", "Sec. 4 text; Fig. S2", "section")
val("V-QSCI-dets", "[2Fe-2S] ideal QSCI determinants at 0.1 Ha", 50551, "determinants", "copied", *RE)
val("V-HCI-dets", "[2Fe-2S] HCI determinants at 0.1 Ha", 4260, "determinants", "copied", *RE)
val("V-N2-rate-1e3", "N2 CAS(10e,12o) new determinants per shot at 1e3 shots", 0.1, "per shot", "copied", *RE, note="shots=1e3")
val("V-N2-rate-1e9", "N2 CAS(10e,12o) new determinants per shot at 1e9 shots", 5e-4, "per shot", "copied", *RE, note="shots=1e9")
val("V-QSCI-samples", "Samples for micro-hartree precision (source estimate)", 4e14, "samples", "estimated", *RE)
for i, (lab, n) in enumerate([("Generated (AI)", 32.6e6), ("Predicted stable (ML)", 5e5), ("Functional filter (ML)", 800), ("DFT + ML-MD (HPC)", 150), ("Practicality filter", 23), ("Predicted new candidates", 18)], 1):
    val(f"V-FUNNEL-{i}", "Electrolyte funnel: " + lab, n, "candidates", "copied", "chen2024", "JACS 146, 20009", "screening workflow", "section", note="stage=%d" % i)
MZ = ("merz2026", "arXiv:2605.01138v2")
val("V-MERZ-qpu", "Embedded protein-ligand: QPU time", 239, "h", "measured", *MZ, "Table XI", scope="161 h ibm_cleveland + 78 h ibm_kobe")
val("V-MERZ-circuits", "Embedded protein-ligand: circuits", 21006, "circuits", "measured", *MZ, "Secs. I and VII", "section")
val("V-MERZ-fugaku", "Embedded protein-ligand: Fugaku node-hours (calcs A, B, E)", 4450769, "node-h", "measured", *MZ, "Table XI", scope="369,315 + 308,528 + 3,772,926")
w("values.csv", VH, V)
VI = {r[0]: dict(zip(VH, r)) for r in V}

# ====================================================================== models (formula figures and scenarios)
MH = ["model_id", "parameter", "value", "unit", "note"]
MD = [
 ["rep", "delta_total", 0.01, "", "total failure budget of the repetition scenario"],
 ["rep", "split", "equal", "", "delta_hit = delta_low = delta_total/2 in the split-budget column; delta_hit = delta_total when downward outliers have zero budget"],
 ["rep", "p_scenario", 0.5, "", "hypothetical hit probability per accepted execution"],
 ["rep", "record", "R-FEMO76-DC-minvol", "", "one accepted execution costs the expected accepted runtime of this row"],
 ["breakeven", "t_C", 1e-8, "s", "illustrative classical oracle evaluation"],
 ["breakeven", "P_ref", 1e6, "cores", "reference point for annotations"],
 ["breakeven", "t_react", 1e-5, "s", "reaction time (low2026dense)"],
 ["readout", "b", 32, "bits", ""], ["readout", "n", 1000, "qubits", ""],
 ["readout", "t_shot_slow", 1e-3, "s", ""], ["readout", "t_shot_fast", 1e-6, "s", ""],
 ["readout", "B_mem", 1e12, "bits/s", ""], ["readout", "N_example", 1e9, "values", ""],
 ["aa", "T", 1e3, "queries", "illustration of the simulation bound"],
 ["aa", "eps", 0.1, "", ""], ["aa", "delta", 0.1, "", ""],
 ["dmrg_plan", "anchor", "C-P450-X3000", "", "M^3 planning curve anchored at this value"],
 ["cores", "fugaku", 7.63e6, "cores", "ideal conversion only"],
]
w("models.csv", MH, MD)
MP = {(m[0], m[1]): m[2] for m in MD}

# ====================================================================== forward classes
FH = ["class_id", "name", "task_family", "present_status", "status_qualifier", "resource_maturity",
      "unvalidated_assumptions", "linked_entries", "linked_resources",
      "trigger_toward_classical", "trigger_toward_quantum", "trigger_resource_estimate"]
SQ, TH, CT, NC, CC, MS, CP = "standing_claim", "theory", "contested", "not_compared", "classical_capability", "matched_scoped", "capability"
F = [
 [1,"OTOC(2) scrambling, 2D","coherent-dynamics",SQ,"conditional","none","mitigation and timing basis","E06","","Converged classical reproduction of the stated observable, depth and precision at 65 q","Validated accuracy and full cost at larger scale","FT compilation of the observable"],
 [2,"Disordered operator Loschmidt echo","coherent-dynamics",SQ,"conditional","none","heuristic rescaling argument","E07","","Majorana/Pauli propagation converged over the full regime","Bounded-error estimator costed for the same regime","FT compilation"],
 [3,"Floquet prethermal 2D magnetism (H2 and Heron instances)","coherent-dynamics",SQ,"conditional; two separate instances","none","validation at selected cycles only","E05;E23","","Converged TN/NQS/Pauli-path result in the hardest regime of either instance","Validation across the hard regime, with mitigation overhead costed","FT compilation"],
 [4,"2D TFIM dynamics, 100 spins, 10 Trotter steps","coherent-dynamics",NC,"","partial","repetitions; preparation","E03","R-TFIM-ns4","Converged classical result for the stated time, initial state and observable","Costed sampling and observable estimation below classical","Repetitions and preparation costed"],
 [5,"Coherent 3D spin-glass quenches","coherent-dynamics",CT,"analog scope","none","","E04","","Stable long-time t-VMC or 3D BP-TN at claimed scales","Observables beyond classical coverage at matched error","Gate-model compilation (one deployment comparison)"],
 [6,"2D frustrated J1-J2 Heisenberg, 10x10 cylinder","lattice-models",NC,"baseline is 4-core DMRG","partial","adiabatic preparation","E29","R-HEIS-1010-s;R-HEIS-1010-p","NQS, PEPS or GPU DMRG on the same cylinder at eps=0.01 total with measured cost","Validated adiabatic preparation at 10x10","Preparation gap scaling"],
 [7,"2D Fermi-Hubbard ground energy, half filling","lattice-models",NC,"best classical baseline unresolved","partial","adiabatic preparation","","R-HUB-66-s;R-HUB-1010-s;R-HUB-1010-p","Sign-free QMC or parallel DMRG at eps=0.01 total on the same cylinder with measured time below the modelled schedule","Quantum estimate below the best measured classical cost at matched tolerance","Preparation cost"],
 [8,"Strongly correlated materials","lattice-models",NC,"","none","","","","Downfolded classical solution at decision accuracy","Multi-orbital estimate with downfolding error and decision tolerance","Multi-orbital estimate"],
 [9,"Core-level XAS (Li-excess cathode cluster)","spectroscopy",NC,"resource-estimated candidate","complete","initial-state fidelity; spectral-error model; clock rate; classical baseline","","R-XAS-circ;R-XAS-alg;R-XAS-av","Classical spectrum at decision accuracy from the best available method","Validated preparation and error model with cost below that classical spectrum","Physical-level compilation"],
 [10,"FeMoco precision and other cofactor models","femoco",NC,"","partial","initial-state overlap; repetitions","E10","R-FEMO76-THC;R-FEMO76-DC-minvol;R-FEMO76-DC-fast;R-FEMO76-DC-fastest;R-FEMO76-DC-low;R-FEMO54-efficient;R-FEMO54-THC-lee","Classical estimate at matched confidence for larger models","Measured overlap and complete protocol cost","Model-specific counts for larger cofactor models"],
 [11,"P450 Cpd I spin gaps","p450",NC,"","partial","overlap; two spin-state costs","","R-P450-2022;R-P450-DC-minvol;R-P450-DC-fast","Classical spin gap converged at a stated tolerance","Quantum cost for both spin states with error cancellation at that tolerance","Preparation overlap, success criterion and both spin states mapped to an architecture"],
 [12,"Ru CO2-fixation catalysts","ru-catalyst",NC,"older model and 2026 56-orbital model are different active spaces","partial","overlap","","R-RU-ns4;R-RU56-DC-fast","Classical multireference result at target accuracy","Model-specific modern count with protocol","Modern count for the Beverland model"],
 [13,"Transition-metal ML labels","thermochemistry",NC,"","none","","E12","","Classical labels adequate for downstream decisions","Demonstrated incremental value of more accurate labels against the downstream error budget","Label cost per decision"],
 [14,"Enzyme active-site energetics","enzymes",NC,"","none","","E30","","Embedding + classical or neural solver adequate for a named cluster and observable","Solver error dominating a validated budget","Embedded-cluster estimates"],
 [15,"Learning from quantum data","learning-quantum-systems",TH,"quantum-side sample-complexity separation","not_applicable","","E21","","Classical access model shown equivalent for targeted observables","Task-specific demonstrations at scale","Copies, memory and access restrictions"],
 [16,"Real-time SU(3) gauge theory","gauge",NC,"","scenario","preparation; measurement; truncation","","R-SU3-KRY;R-SU3-LCU;R-SU3-KN","Classical real-time method for a controlled physical observable","Controlled-truncation estimate with preparation and measurement costed","Single formulation, full observable"],
 [17,"Sampling capability benchmarks (RCS, GBS, doped Clifford, analog atoms)","capability-sampling",CP,"outside application ranking","not_applicable","","E01;E02;E24;E25;E26;E34;E35;E36","","n/a","n/a","n/a"],
 [18,"SQD, single-layer LUCJ circuit-energy objective","iron-sulfur-chemistry",MS,"sampled-subspace workflow as a whole: not compared","not_applicable","","E09;E28","","n/a","Sampler ablation: QPU samples beat classical selectors under a common selection, recovery and diagonalization procedure","n/a"],
 [19,"FeMoco-76 model energy","femoco",CC,"classical feasibility, extrapolation-dependent; operational ranking unresolved","not_applicable","","E10","","n/a","n/a (a failed classical estimate would reopen the comparison)","n/a"],
 [20,"P450 ~500-orbital model","p450",NC,"","partial","overlap; feasibility","","R-P450-FULL","Embedding solves the decision","A gap or decision target with a complete comparison","Modern count"],
 [21,"Generic ground-state chemistry","generic-chemistry",NC,"","none","","E11","","n/a","Representative instance family, fixed accuracy, with empirical or proven exponential classical scaling","n/a"],
 [22,"Main-group thermochemistry","thermochemistry",CC,"named benchmarks; no quantum comparator","not_applicable","","E12","","n/a","Validated-domain failure with decision consequence (a solver need, not yet a quantum result)","n/a"],
 [23,"Rydberg topological diagnostics","analog-simulation",NC,"","none","","E08","","n/a","A matched computational task (a measured TEE alone improves experimental access)","Measurement cost at 288 atoms"],
 [24,"High-throughput materials discovery","materials-discovery",CC,"experimentally validated workflow; no quantum comparator","not_applicable","","E13;E14","","n/a","Decision-critical electronic-structure bottleneck identified and resolved","Bottleneck-specific estimate"],
 [25,"Binding free energies, MD","binding",CC,"mature practice; one unmatched hybrid workflow record","not_applicable","","E28","","n/a","Quantum subproblem dominating the error budget, shown by ablation","Subproblem estimate"],
 [26,"Property learning within a phase","learning-quantum-systems",TH,"classical-side guarantee within theorem scope; data acquisition separate","not_applicable","","E21","","n/a","Labels unobtainable classically","n/a"],
 [27,"Protein structure prediction (proteome scale)","protein-structure",CC,"fragment studies are a separate record","not_applicable","","E15","","n/a","Fragment gain under identical ensemble-selection and cost rules (a separate record)","n/a"],
 [28,"Generative molecular design","molecular-generation",NC,"","none","","E16","","Matched ablation shows no gain","Matched ablation, including downstream selection and experimental budget, shows gain","n/a"],
 [29,"Unstructured search (exact optimization model)","query-complexity",TH,"conditional model result; query-model limit","scenario","oracle equivalence; partitionability","E31","","n/a","t_Q <~ 10 us with Q >> 1 within a stated latency envelope, or a structured speedup","Oracle-specific estimate"],
 [30,"Approximate optimization by annealing (D-Wave QAC; Rydberg MIS)","optimization",CT,"family-specific","none","","E18;E27","","Classical portfolio matches scaling on the defined family","Scaling separation vs the full classical portfolio with stated runtime accounting","n/a"],
 [31,"QML on classical data","qml-classical-data",NC,"constructed separations exist","none","","E20","","n/a","Practical separation on a stated workload and access model","n/a"],
 [32,"Nuclear ground states (A<=20)","nuclear",CC,"cited interactions and precision; no quantum comparator identified","not_applicable","","E22","","n/a","A quantum comparator within scope at matched precision","n/a"],
 [33,"Euclidean lattice QCD, zero density","gauge",CC,"mature practice; no demonstrated practical matched quantum advantage","none","","","","n/a","Quantum-assisted sampling improving autocorrelation and full observable cost against modern HMC at relevant lattice spacing","n/a"],
 [34,"CFD (full field / selected outputs)","fluids",CC,"full field: no costed quantum workflow; selected outputs: published estimates in class 38","scenario","information model of the output","E33","","n/a","Selected-observable workload with demonstrated value and an end-to-end cost below explicit classical CFD","Selected-output estimate at an engineering Reynolds number"],
 [35,"Weather/climate (forecasts / statistics)","fluids",CC,"per named forecast, statistic or component; no matched quantum workflow","none","","","","n/a","A named component with a costed quantum advantage","Component estimate"],
 [36,"Doped 2D Fermi-Hubbard (sign-problem instances)","lattice-models",NC,"new record; not a reversal of class 7","none","","E29","","NQS, PEPS, constrained-path or embedding result at stated density, U/t, t' and tolerance with measured cost","Costed QPE estimate for the same instance and tolerance","Doped-lattice estimate with preparation"],
 [37,"Quantum-enhanced MCMC sampling","optimization",NC,"conditional candidate","none","","","","Classical nonlocal updates matching time per independent sample","Lower time per statistically independent sample including proposal generation and noise","Proposal circuit cost on a named instance family"],
 [38,"Sparse linear solves and time stepping for engineering PDEs (FEM, CFD)","linear-systems-pde",TH,"at most polynomial speedup in fixed dimension; two of three end-to-end estimates find no practical advantage","partial","block-encoding and preconditioner cost; condition number at scale; input model; clock rate","E32;E33","R-QLSA-EM;R-CFD-PENUEL-lo;R-CFD-PENUEL-hi;R-CFD-PENUEL-Re1e1;R-CFD-PENUEL-Re1e8;R-CFD-ZHUANG","n/a (classical practice is the incumbent)","A high-dimensional or quantum-native linear problem with a scalar output, an efficient block encoding and an end-to-end cost below tuned multigrid or Monte Carlo","Constant-factor estimate at industrial condition numbers (1e5 to 1e6) with input and readout included"],
]
w("forward_classes.csv", FH, F)

# ====================================================================== figure points
PH = ["fig", "series", "point_id", "x", "y", "kind", "bound", "checks", "label", "anchor"]
P = []
TR = {"identity": lambda v: v, "s_to_h": lambda v: v / 3600.0, "y_to_h": lambda v: v * 8766.0,
      "d_to_month": lambda v: v / 30.44, "min_to_h": lambda v: v / 60.0, "d_to_h": lambda v: v * 24.0}
def get(table, rid, field):
    src = {"resources": RI, "values": VI, "entries": {e[0]: dict(zip(EHX, e)) for e in E}}[table]
    return float(src[rid][field])
def p(fig, series, pid, kind, checks, x=None, y=None, bound="point", label="", anchor="west"):
    """checks: list of (axis, table, id, field, transform); the axis value is computed here from the record."""
    c = {"x": x, "y": y}
    for ax, tb, rid, fld, trn in checks:
        if "/" in fld:
            a, b = fld.split("/"); v = get(tb, rid, a) / get(tb, rid, b)
        else:
            v = get(tb, rid, fld)
        c[ax] = TR[trn](v)
    P.append([fig, series, pid, c["x"], c["y"], kind, bound,
              ";".join(":".join(k) for k in checks), label, anchor])

# Fig timeline: x = elapsed months
order = ["E01", "E35", "E36", "E24", "E34", "E02", "E03", "E04", "E18", "E27", "E05", "E06", "E07", "E26", "E23", "E25"]
ser = {"E01": "validation", "E35": "validation", "E36": "validation", "E34": "challenged", "E02": "challenged", "E24": "validation", "E03": "observables", "E04": "partial",
       "E18": "contested", "E27": "contested", "E05": "open", "E06": "open", "E07": "open", "E23": "open", "E25": "open", "E26": "open"}
for i, eid in enumerate(order, 1):
    p("timeline", ser[eid], eid, "elapsed", [("x", "entries", eid, "elapsed_days", "d_to_month")], y=i)
TL_ORDER = order

# Fig dumbbell (hours)
for row, rs, rp, cv, cl in [(1, "R-HUB-66-s", "R-HUB-66-p", "C-S2-U4-6x6", "61\\,h"),
                            (2, "R-HUB-1010-s", "R-HUB-1010-p", "C-S2-U4-10x10", "$\\sim$225\\,y"),
                            (3, "R-HEIS-1010-s", "R-HEIS-1010-p", "C-S1-J0.5-10x10", "22\\,h")]:
    p("dumbbell", "q_est", rs, "modelled_schedule", [("x", "resources", rs, "runtime_s", "s_to_h")], y=row)
    p("dumbbell", "q_par", rp, "modelled_schedule_parallel", [("x", "resources", rp, "runtime_s", "s_to_h")], y=row)
    p("dumbbell", "c_est", cv, "estimated_4core_dmrg", [("x", "values", cv, "value", "s_to_h")], y=row, label=cl, anchor="south")
p("dumbbell", "q_est", "R-FEMO76-DC-minvol", "expected_runtime", [("x", "resources", "R-FEMO76-DC-minvol", "runtime_s", "s_to_h")], y=4, label="5.3\\,h", anchor="north")
p("dumbbell", "q_par", "R-FEMO76-DC-fastest", "expected_runtime", [("x", "resources", "R-FEMO76-DC-fastest", "runtime_s", "s_to_h")], y=4)
p("dumbbell", "c_est", "C-FEMO76-ideal", "ideal_not_run", [("x", "values", "C-FEMO76-ideal", "value", "identity")], y=4, label="22.9\\,h", anchor="south")
p("dumbbell", "q_est", "R-P450-2022", "per_run", [("x", "resources", "R-P450-2022", "runtime_s", "s_to_h")], y=5, label="2022: 25--73\\,h", anchor="north")
p("dumbbell", "q_est", "R-P450-2022-p5", "per_run", [("x", "resources", "R-P450-2022-p5", "runtime_s", "s_to_h")], y=5)
p("dumbbell", "q_par", "R-P450-DC-minvol", "expected_runtime", [("x", "resources", "R-P450-DC-minvol", "runtime_s", "s_to_h")], y=5, label="2026: 1.1--1.9\\,h", anchor="south")
p("dumbbell", "q_par", "R-P450-DC-fast", "expected_runtime", [("x", "resources", "R-P450-DC-fast", "runtime_s", "s_to_h")], y=5)
p("dumbbell", "c_est", "C-P450-wall", "estimated_in_source", [("x", "values", "C-P450-wall", "value", "identity")], y=5, label="$\\sim$1 month", anchor="south")

# Fig hubbard: DMRG time vs sites, and source QPE schedules
for u, pts in S2.items():
    for lx, ly, t in pts:
        s = f"strip_U{u:g}" if lx != ly else f"U{u:g}"
        p("hubbard", s, f"U{u:g}-{lx}x{ly}", "estimated_dmrg_4core", [("y", "values", f"C-S2-U{u:g}-{lx}x{ly}", "value", "identity")], x=lx * ly)
for rid, n in [("R-HUB-66-s", 36), ("R-HUB-1010-s", 100)]:
    p("hubbard", "qpe_s", rid, "modelled_schedule", [("y", "resources", rid, "runtime_s", "identity")], x=n)
for rid, n in [("R-HUB-66-p", 36), ("R-HUB-1010-p", 100)]:
    p("hubbard", "qpe_p", rid, "modelled_schedule_parallel", [("y", "resources", rid, "runtime_s", "identity")], x=n)

# Fig femoco54 frontier and volumes
for vi, rid in enumerate(["DF", "THC", "DFTHC", "compact", "balanced", "efficient", "fast"], 1):
    k = "R-FEMO54-" + rid
    s = "prior" if rid in ("DF", "THC", "DFTHC") else "dense"
    p("femoco54", s, k, "expected", [("x", "resources", k, "physical_qubits", "identity"), ("y", "resources", k, "runtime_s", "s_to_h")], bound=RI[k]["runtime_bound"])
    p("femoco54vol", s, k, "copied", [("y", "resources", k, "st_volume_Mqh", "identity")], x=vi, label=rid)
# FeMoco-76 and P450 dense-code frontiers (Table XXVII)
for fig, ids in [("femoco76", ["R-FEMO76-DC-minq", "R-FEMO76-DC-low", "R-FEMO76-DC-day", "R-FEMO76-DC-minvol", "R-FEMO76-DC-fast", "R-FEMO76-DC-fastest"]),
                 ("p450dc", ["R-P450-DC-minq", "R-P450-DC-month", "R-P450-DC-day", "R-P450-DC-minvol", "R-P450-DC-fast"])]:
    for k in ids:
        p(fig, "dense", k, "expected", [("x", "resources", k, "physical_qubits", "identity"), ("y", "resources", k, "runtime_s", "s_to_h")])
p("p450dc", "prior", "R-P450-2022", "per_run", [("x", "resources", "R-P450-2022", "physical_qubits", "identity"), ("y", "resources", "R-P450-2022", "runtime_s", "s_to_h")])
p("p450dc", "prior", "R-P450-2022-p5", "per_run", [("x", "resources", "R-P450-2022-p5", "physical_qubits", "identity"), ("y", "resources", "R-P450-2022-p5", "runtime_s", "s_to_h")])

# Fig dmrg (P450 planning)
for vid, s in [("C-P450-G1500", "measured_G"), ("C-P450-X1500", "estimated_X"), ("C-P450-X3000", "estimated_X"), ("C-FEMO76-sweep", "femoco_sweep")]:
    M = float(VI[vid]["note"].split("=")[1])
    p("dmrg", s, vid, VI[vid]["kind"], [("y", "values", vid, "value", "identity")], x=M)

# Fig rates: effective rate N/T
for i, rid in enumerate(["R-TFIM-ns4", "R-TFIM-ns3", "R-RU-ns4", "R-RU-ns3", "R-TFIM-us4", "R-RU-us4"], 1):
    p("rates", "T", rid, "effective_rate", [("x", "resources", rid, "n_nc/runtime_s", "identity")], y=i)
for i, rid in enumerate(["R-P450-2022", "R-FEMO54-THC-layout"], 7):
    p("rates", "CCZ", rid, "effective_rate", [("x", "resources", rid, "n_nc/runtime_s", "identity")], y=i)

# Fig platform: runtime per execution by scenario
for j, sc in enumerate(["us3", "us4", "ns3", "ns4"], 1):
    for tgt in ("TFIM", "RU"):
        k = f"R-{tgt}-{sc}"
        p("platform", tgt, k, "per_execution", [("y", "resources", k, "runtime_s", "identity")], x=j)

# Fig resource map: logical qubits vs non-Clifford count (only table/section-level rows with a compiled width)
for rid, s, lab, anc in [("R-TFIM-ns4", "T_point", "2D TFIM dynamics, per execution", "west"), ("R-RU-ns4", "T_point", "Ru CO$_2$ catalyst", "north"),
                         ("R-RSA", "T_point", "RSA-2048", "west"), ("R-XAS-circ", "Toff_point", "XAS, longest circuit (min.\\ workspace)", "west"),
                         ("R-FEMO54-THC-lee", "Toff_point", "FeMoco-54 (Reiher), THC", "north west"),
                         ("R-FEMO76-THC", "Toff_point", "FeMoco-76 (Li), THC", "west"), ("R-P450-FULL", "Toff_point", "P450 $\\sim$500-orbital model", "south east")]:
    p("resmap", s, rid, RI[rid]["n_nc_scope"], [("x", "resources", rid, "logical_qubits", "identity"), ("y", "resources", rid, "n_nc", "identity")], label=lab, anchor=anc)

# Fig gauge: ranges per formulation (table-level rows only)
for i, (name, lo, hi) in enumerate([("Kan-Nam electric Trotter", "R-SU3-KN", "R-SU3-KN"), ("Electric-basis LCU", "R-SU3-LCU", "R-SU3-LCU-hi"),
                                    ("Large-Nc / Krylov truncations", "R-SU3-KRY", "R-SU3-KRY-hi")], 1):
    p("gauge", "lo", lo + "-lo", "range_lo", [("x", "resources", lo, "n_nc", "identity")], y=i, label=name)
    p("gauge", "hi", hi + "-hi", "range_hi", [("x", "resources", hi, "n_nc", "identity")], y=i, label=name)

# Fig sqd and funnel
p("sqd", "dets", "V-QSCI-dets", "copied", [("y", "values", "V-QSCI-dets", "value", "identity")], x=1, label="QSCI")
p("sqd", "dets", "V-HCI-dets", "copied", [("y", "values", "V-HCI-dets", "value", "identity")], x=2, label="HCI")
p("sqd", "rate", "V-N2-rate-1e3", "copied", [("y", "values", "V-N2-rate-1e3", "value", "identity")], x=1e3)
p("sqd", "rate", "V-N2-rate-1e9", "copied", [("y", "values", "V-N2-rate-1e9", "value", "identity")], x=1e9)
p("sqd", "samples", "V-QSCI-samples", "estimated", [("x", "values", "V-QSCI-samples", "value", "identity")], y=1)
for i in range(1, 7):
    p("funnel", "new" if i == 6 else "screen", f"V-FUNNEL-{i}", "copied", [("x", "values", f"V-FUNNEL-{i}", "value", "identity")], y=i)
w("figure_points.csv", PH, P)
with open(os.path.join(HERE, "timeline_order.txt"), "w") as f:
    f.write("\n".join(TL_ORDER) + "\n")

# ====================================================================== comparison pairs (benchmark tuples of the headline comparisons)
QH = ["pair_id", "pair", "instance", "boundaries", "model_or_approximation", "observable", "tolerance_and_meaning",
      "failure_probability_meaning", "workload", "access_and_state_model", "quantum_records", "classical_records", "what_is_missing"]
Q = [
 ["P-HUB", "Fermi-Hubbard 10x10 (and 6x6)", "half filling, U/t=4, nearest-neighbour hopping", "cylinder; the source's text and one caption disagree on the periodic direction", "single-band Hubbard model", "ground-state energy", "0.01 in total energy (source units); classical time is for a variational state at that accuracy", NR, "one energy", "Hamiltonian given; adiabatic state preparation assumed cheap", "R-HUB-66-s;R-HUB-66-p;R-HUB-1010-s;R-HUB-1010-p", "C-S2-U4-6x6;C-S2-U4-10x10", "sign-free QMC cost; parallel or GPU DMRG time; preparation cost"],
 ["P-HEIS", "J1-J2 Heisenberg 10x10", "J2/J1=0.5", "cylinder (as above)", "spin-1/2 J1-J2 model", "ground-state energy", "0.01 in total energy; classical time is for a variational state", NR, "one energy", "Hamiltonian given; adiabatic preparation assumed cheap", "R-HEIS-1010-s;R-HEIS-1010-p", "C-S1-J0.5-10x10;C-NQS-J1J2", "classical time on a current machine; neural-state result on the same cylinder"],
 ["P-FEMO", "FeMoco, 76-orbital model", "Li et al. active space, 76 orbitals, 113 electrons", NA, "active-space Hamiltonian; not the enzyme", "ground-state energy (scientific question: ranking of spin isomers)", "1 kcal/mol; classical: empirical extrapolation range (0.31 consensus, 1.25 conservative); quantum: phase-estimation precision", "quantum: logical failure 0.070 per shot at minimum volume, spectral-hit probability not reported; classical: none", "one energy per candidate state", "quantum side starts from a supplied initial state", "R-FEMO76-DC-minvol;R-FEMO76-DC-fastest;R-FEMO76-THC", "C-FEMO76-campaign;C-FEMO76-ideal;C-FEMO76-uccsdtq", "measured overlap; candidate search on both sides; classical run at D near 393,000"],
 ["P-P450", "Cytochrome P450 compound I, model X", "58 orbitals, 63 electrons", NA, "active-space Hamiltonian", "single total energy (scientific target: a spin-state gap)", "chemical accuracy on one energy", "quantum: logical failure 0.098 per shot at minimum volume; classical: none", "at least two spin states for a gap", "supplied initial state", "R-P450-2022;R-P450-DC-minvol;R-P450-DC-fast", "C-P450-X3000;C-P450-wall", "both spin states at a stated tolerance on either side; a classical gap converged in bond dimension"],
 ["P-XAS", "X-ray absorption, Li4Mn2O cluster", "active space of 22 electrons in 18 orbitals", NA, "active-space Hamiltonian; randomized second-order product formula", "absorption spectrum", "Lorentzian broadening eta=0.05 Ha; spectral error by the source's perturbative analysis", NX, "2500 shots over 200 time points", "initial state: sum of 1e4 Slater determinants", "R-XAS-circ;R-XAS-alg;R-XAS-av", "C-XAS-RAS-1000;C-XAS-RAS-gs", "validated initial state; classical spectrum for this cluster; a machine with the assumed clock"],
 ["P-OTOC", "OTOC(2), 65 qubits", "Willow processor, 65 of 105 qubits", NX, "random-circuit echo protocol", "second-order out-of-time-order correlator", NX, NX, "quantum: all experiments (about 2 h); classical: one data point (3.2 y est.)", "circuit description", "C-OTOC-q", "C-OTOC-c", "a common workload basis; tolerance; a converged classical method"],
 ["P-DC", "Doped Clifford sampling (two instances)", "v1: 70 q, 70 layers, 468 T; v2/v3: 64 q, depth 73, 314 T", "v1 open chain; v2/v3 cycle graph", "Clifford brickwork doped with T gates, encoded in spacetime codes", "amplitudes of published bitstrings and log-XEB (v1); samples with a fidelity certificate (v3)", "v1: log-XEB 0.350 [0.298, 0.403]; v3: fidelity lower bound 0.349", "95% interval or confidence", "v1: 2051 amplitude batches", "circuit description and published bitstrings", NA, "C-DC-TN", "a classical response to the periodic instance; fresh samples from either distribution"],
]
for _q in Q:
    if _q[0] == "P-OTOC":
        _q[6] = "signal-to-noise ratio of the measured correlator against exact simulation at up to 40 qubits (3.9 for the off-diagonal correlator); at 65 qubits accuracy is estimated from an empirical error model"
        _q[7] = "none stated as a probability: error bars come from an empirical error model"
    if _q[0] in ("P-HUB", "P-HEIS") and _q[7] == "not_reported":
        _q[7] = NX
w("pairs.csv", QH, Q)

# ====================================================================== update log
UH = ["date_jst", "source", "check", "result", "version_inspected", "issue"]
U = [
 ["2026-11-09","microsoft.github.io/skala","Skala 1.0/1.1 WTMAD-2","3.89 / 2.72","model cards",""],
 ["2026-11-09","arXiv:2506.15784","XAS gate unit","v2: T gates; current version: Toffoli gates per circuit","v2 abstract; current PDF abstract","SUPERSEDED on 10 and 11 Nov: the v2 PDF states Toffoli; the abstract page of v2 stated T gates"],
 ["2026-11-09","arXiv:2210.14109 v3","Hubbard setting","Half filling; eps total energy; QPE <1e5 s at 10x10 single factory; DMRG Table S2","v3","SUPERSEDED on 10 Nov by the Table S12 schedules"],
 ["2026-11-09","arXiv:2605.30455","FeMoco-54 frontier","36x space, 6.6x space-time vs SA; table values; P450 Cpd1X target listed","v1","SUPERSEDED on 11 Nov by the Table XXVII rows read from the PDF"],
 ["2026-11-09","arXiv:2511.02125","Helios pairing paper metadata","Granet et al., v3","v3",""],
 ["2026-11-09","arXiv:2607.25998","OLE primary","Barron et al.","v1",""],
 ["2026-11-09","arXiv:2603.29091","Gauge estimates","Table of fiducial SU(3) estimates","v3","subgroup value 3.5e12 not re-read; removed from figures in v6"],
 ["2026-11-09","PMC9499570","P450 DMRG costs","Model X costs estimated; model G measured","published",""],
 ["2026-11-09","research.google blog","OTOC(2) timing","~2 h experiments; 3.2 y per data point; 13,000x","blog","no calibration/readout statement; workload bases differ"],
 ["2026-11-09","pnnl.gov; arXiv:2401.04070","Electrolyte validation","JACS 146, 20009 (2024); synthesis and conductivity","published",""],
 ["2026-11-09","arXiv:2609.12146","FeMoco-76 SA count","1459 logical qubits, 9.99e8 Toffoli per PE run (citing Low et al.)","v1","secondary tabulation; excluded from figures in v6"],
 ["2026-11-09","arXiv:2409.11748","FeMoco candidate-refinement protocol","7.3e10 Toffoli total","v1 abstract","abstract-level; excluded from figures and ratios"],
 ["2026-11-10","arXiv:2210.14109","Lattice QPE schedules","Table S12: single-factory 1.23e4 s (Hubbard 6x6), 1.05e5 s (Hubbard 10x10), 5.64e4 s (Heisenberg 10x10); (16,16) schedules 1.59e3, 1.46e4, 4.32e3 s","v3 HTML","supersedes the rounded <1e5 s statement used in v5"],
 ["2026-11-10","arXiv:2210.14109","Lattice DMRG baselines","Tables S1, S2: single AMD EPYC 7702, 4 cores; time to a state within 0.01 of extrapolated E0; cylinders; Heisenberg 10x10 J2=0.5: 7.9e4 s","v3 HTML","text and Fig. S1 caption disagree on which direction is periodic"],
 ["2026-11-10","arXiv:2506.15784","XAS resources","Table I N=18: 3.11e8 Toffoli longest circuit, 4.58e11 algorithm; 100 logical qubits minimum; 350 active-volume; 8.1e10 cycles; D=1e4; S=2500; RAS ~32 d for 1000 states","v2 (20 Aug 2025)","SUPERSEDED on 11 Nov by v3. The note written here on 10 Nov, that the v2 abstract states Toffoli, was wrong for the abstract web page (T gates) and right for the PDF"],
 ["2026-11-10","arXiv:2605.30455","Dense-code compilations","Fig. 1 table (FeMoco-54); Table XXVII rows for FeMoco-54, FeMoco-76, Cpd1X 58o63e, XVIII 56o64e","v1","SUPERSEDED on 11 Nov: the 2.692 M-qubit FeMoco-76 row was dropped because a merged cell failed the volume check"],
 ["2026-11-10","arXiv:2401.07184","QAC first posting","v1 14 January 2024","arXiv listing","v5 used 12 January, inferred from the identifier"],
 ["2026-11-10","arXiv:2607.24937","Heron Floquet","up to 74 q; TN not converged; Pauli-path truncation-dependent; RIKEN co-authors","v1 abstract",""],
 ["2026-11-10","arXiv:2607.25941","Doped Clifford versions","v1 28 Jul 2026; v2 1 Sep 2026; v3 2 Sep 2026 (64 q, depth 73, 314 T, 76 physical)","arXiv listing; v3 abstract","Note added not read"],
 ["2026-11-10","arXiv:2608.13110","Doped Clifford classical response","37.3 min, 32 nodes x 8 H100, 2051 amplitude batches; 10.6 min is a projection","v1 (13 Aug 2026) abstract","later version not read"],
 ["2026-11-10","arXiv:2210.08556","Ultracold-atom sampling","64 sites, 20 atoms; sampling-rate claim; Bayesian tests","listing and abstract","SUPERSEDED on 11 Nov: the request for v1 returned the current abstract, and the claim was dated from v1"],
 ["2026-11-10","arXiv:2202.09372; arXiv:2307.09442","Rydberg MIS pair","18 Feb 2022; 18 Jul 2023","arXiv listings and abstracts",""],
 ["2026-11-10","arXiv:2605.01138","Embedded protein-ligand workflow","239 QPU-h; 21,006 circuits; 4.45e6 Fugaku node-h; no advantage claimed; no sampler ablation","PDF","abstract text garbled in extraction"],
 ["2026-11-10","arXiv:2603.28648","GPU DMRG Fe4S4","E=-327.24466 Ha at D_SU(2)=12288; 12.6 h on one DGX B200 node","v1 HTML","instance match to the SQD experiment not established"],
 ["2026-11-10","arXiv:2310.05715","Transformer NQS J1-J2","E/N=-0.497634(1); 20 A100 GPUs, 4 days; DMRG -0.495530","v2 HTML","boundary conditions not stated in retrieved text"],
 ["2026-11-10","arXiv:2507.02644","NQS doped Hubbard","abstract only","v2 listing","no numbers extracted"],
 ["2026-11-11","arXiv:2506.15784","XAS resources, version 3","Table 1 N=18: 3.54e8 Toffoli (active volume 1.89e10) longest circuit; 5.20e11 Toffoli (2.76e13) algorithm; 100 logical qubits minimum; 350 active-volume; 1.08e8 and 1.58e11 logical cycles; less than two days at MHz","v3 (5 Nov 2026), PDF text layer","classical RAS estimate not re-read in v3"],
 ["2026-11-11","arXiv:2605.30455","Dense-code Table XXVII","Full blocks for FeMoco-54, FeMoco-76, Cpd1X 58o63e; selected rows for XVIII 56o64e; columns qubits, volume, expected and one-shot runtime, p_fail, Toffoli; Sec. VI.B defines expected runtime","v1, PDF text layer","first row of the XVIII 56o64e block not re-read"],
 ["2026-11-11","arXiv:2210.08556","Ultracold-atom versions","v1 16 Oct 2022: another title, 32-site chain, power comparable to the fastest supercomputer; v2 11 Apr 2026: 64 sites, 20 atoms, three orders of magnitude; PRX 16, 021057","abstract pages of v1 and v2",""],
 ["2026-11-11","arXiv:2403.00910; 2503.05693; 2505.22514","First-posting dates","1 Mar 2024; 7 Mar 2025; 28 May 2025","arXiv listings","Tindall et al. now Science 392, 868 (2026)"],
 ["2026-11-11","arXiv:2607.24937","Heron Floquet validation","Unbiased and extrapolated estimators agree over their common window; cross-platform checks at selected cycles on two trapped-ion systems; thermodynamic-limit statement is an extrapolation","v1, PDF text layer",""],
 ["2026-11-11","arXiv:2607.25941","Doped Clifford revision","v3 text: periodic boundary conditions eliminate the low-width contraction path used in the classical response; framework unchanged","v3, PDF text layer",""],
 ["2026-11-11","arXiv:2608.13110","Doped Clifford classical response","v2 posted 29 Oct 2026; abstract figures unchanged (37.3 min; 32 nodes x 8 H100; log-XEB 0.35034 [0.29763, 0.40305])","abstract page of v2",""],
 ["2026-11-11","arXiv:2605.01138","Embedded protein-ligand workflow","v2 5 Sep 2026: 21,006 circuits, over 239 hours, up to 94 qubits","abstract page of v2",""],
 ["2026-11-11","arXiv:2211.07629","Beverland et al. tables","Table I: 230/2740/25481 logical qubits, 2.4e6/5.4e11/1.5e10 T; Table IV runtimes and physical qubits for four qubit scenarios","v1, PDF text layer","pins the rows carried as (as read for v4)"],
 ["2026-11-11","arXiv:2011.03494","THC FeMoco tables","Table IV (Reiher, 54 orbitals, M=350): 5.3e9 Toffoli, 2142 logical qubits; Table V (Li, 76 orbitals, M=450): 3.2e10 Toffoli, 2196 logical qubits; layout (Reiher only): 4e6 physical qubits, 6.7e9 Toffoli in 3 days at 25 kHz","v3, PDF text layer","CORRECTION: versions 4 to 6 attributed the Reiher numbers to the 76-orbital model"],
 ["2026-11-11","arXiv:2501.07231","QSCI limits","4,260 vs 50,551 determinants at 0.1 Ha; 0.1 and 0.0005 determinants per sample at 1e3 and 1e9 samples; 4e14 samples for micro-hartree precision","v5, PDF text layer","pins the rows carried as (as read for v4/v5)"],
 ["2026-11-11","arXiv:1505.06552; 1512.05903; 2004.06516; 2011.03185; 2307.09593; 2211.05246; 2406.06323; 2509.08807; 2502.20908; 2606.01067; 2303.13012","Linear solvers and CFD","Complexity limits and end-to-end estimates as cited in Section 4.5","abstract pages and search results","SUPERSEDED later on 11 Nov (v7.1) for 1505.06552, 1512.05903, 2406.06323 and 2509.08807, which were read in the PDF"],
 ["2026-11-11","arXiv:2406.06323","Drag estimate: instances and classical reference","Sphere at Re=1e1 to 1e8 and three ship hulls; classical reference is steady RANS on one workstation: 1.1 h (Re=1e3) to 10 h (Re=1e7) with meshing, Re=1e8 out of memory (Table 3); estimates are stated as lower bounds; inlet/outlet conditions not included","v3, PDF text layer (browser)","v7.1; the product range 1e21 to 1e39 remains an abstract-level value"],
 ["2026-11-11","arXiv:2509.08807","Navier-Stokes crossover","2^80 grid; 8.71e6 physical qubits at error 5e-4; 42.6 days; classical 130 years; stated speedup 1100x; output by state tomography of a spectrally compact state","v1, PDF text layer (browser)","v7.1"],
 ["2026-11-11","arXiv:1505.06552","EM scattering resource table","Table II, N=332,020,680: depth 1.8e29 with oracles and 3.30e25 without; T-depth 8.2e28 and 1.28e25; measurements 2.8e27 and 8.23e21","v2, PDF text layer (browser)","v7.1"],
 ["2026-11-11","arXiv:1512.05903","FEM complexity table","Table I, optimal preconditioning: classical (|u|_2/eps)^(d/2), quantum ||u||_1/eps, up to logarithms","v2, PDF text layer (browser)","v7.1"],
 ["2026-11-11","arXiv:2502.15882","Spectrum amplification counts","Table I: FeMoco-54 1137 qubits, 3.41e8 Toffoli; FeMoco-76 1459 qubits, 9.99e8 Toffoli; prior THC 2142/5.3e9 and 2196/3.2e10; symmetry-compressed THC 1512/4.3e9 for the 76-orbital model","v1, PDF text layer (browser)","v7.1; replaces the second-hand record; confirms the v7 correction of the THC attribution"],
 ["2026-11-11","arXiv:2409.11748","FeMoco candidate refinement","7.3e10 Toffoli; 2 or 3 QPE iterations; bond dimension 4000; overlap squared about 0.9 (extrapolated); 2.3 times the single-shot THC estimate","v1, PDF text layer (browser)","v7.1"],
 ["2026-11-11","arXiv:2605.30455","Dense code: Ru minimum-qubit row; Fig. 1 table","XVIII-56o64e row 1: 75.91k qubits, 3200 h expected, 351 h per shot, p_fail 0.890, 5.55e9 Toffoli (3.20 + 1.69 + 0.65 by part); Fig. 1 table agrees with the four FeMoco-54 rows of the ledger","v1, PDF text layer (browser)","v7.1; closes the row marked not re-read"],
 ["2026-11-11","arXiv:2506.15784","XAS classical estimate","Sec. 5: 0.76 h x 1000 states, about 32 days; called likely optimistic on the classical side; accepted in Quantum on 23 Sep 2026","v3, PDF text layer (browser)","v7.1; the estimate is now pinned to v3"],
 ["2026-11-11","arXiv:2306.03709","Gaussian boson sampling: datasets covered","Borealis (M16, M72, M216, M288), Jiuzhang 2.0 and Jiuzhang 3.0","v2, PDF text layer (browser)","v7.1; the classical result covers these datasets, so entry 2 is a family record. CORRECTION: versions up to 7 dated this entry from the 2020 Jiuzhang experiment, which the paired classical result does not simulate; the claim date is now that of Jiuzhang 2.0 (arXiv:2106.15534v1, 29 Jun 2021)"],
 ["2026-11-11","arXiv:2506.10191","OTOC timing basis","Fig. 4c: estimated time to compute the correlator of a single circuit on Frontier by tensor-network contraction","v1, PDF text layer (browser)","v7.1; the classical basis is one circuit; the 2 h quantum figure is still known from the blog only"],
 ["2026-11-11","arXiv:2506.10191","OTOC timing","Main text beside Fig. 4(c): 3.2 years on Frontier is about 13,000 times the data collection time of 2.1 hours per circuit","v1, PDF text layer (browser)","v8 CORRECTION: version 7.1 said the quantum figure was known from the vendor post only and covered a set of experiments"],
 ["2026-11-11","github.com/isi-usc-edu/qsub","Drag estimate: per-instance records","All eight structured sphere files opened at commit cc8d3ce: products 5.3e21 (Re=10) to 7.9e40 (Re=1e8); task string 0.05 failure tolerance; least-squares slope 2.745 against the published 2.68","repository web view","v8; UNRESOLVED against the published range 1e21 to 1e39; source authors not contacted (author decision)"],
 ["2026-11-11","arXiv:2509.08807","Navier-Stokes Appendix F","F12 181 logical qubits; F15 28,301 queries; F20 9.41e7 Toffoli and 3.94e8 rotations; F24 distance 25; F26 1,000 samples; F30 3.68e6 s; F31 226,250 and F33 8.16e6 physical qubits; F36-F38 classical operation counts and rate","v1, PDF text layer (browser)","v8; 130 years is the banded-Cholesky model"],
 ["2026-11-11","arXiv:2511.17437; 2608.17115","Gauge counts","Osorio: 3.5e12 T (Kogut-Susskind), 7.1e12 T (improved), 9-qubit register. Draper Table 5: U_p 1.2e5 (B=6), 1.2e6 (B=9) T; Table 6 register terms","v1 of each, PDF text layer (browser)","v8 CORRECTION: data width 27,000, not 24,000"],
 ["2026-11-11","arXiv:2512.03758; 2502.11239; 2502.20908; 2606.01067","Solver studies","Jennings Eqs. 181-186 and Re^0.287; Tu: error 1e-5, 10 ns logical cycle, no input/output cost; Lapworth: 879/8,348 against 249/41,181; Goldfriend Table 2 and factor 2 in outer iterations","PDF text layer (browser)","v8"],
 ["2026-11-11","arXiv:2109.11525; 2207.10058; 2304.12240; Nature 606, 75","Boson sampling by experiment","Villalonga v1 (23 Sep 2021) covers the 2020 100-mode data and Jiuzhang 2.0; Martinez-Cifuentes v1 20 Jul 2022 (abstract); Jiuzhang 3.0 posted 24 Apr 2023; Borealis published 1 Jun 2022","PDF text layer (v1) and listing pages","v8 CORRECTION: entry 2 split into four records; Jiuzhang 2.0 first response is 86 days, not 707"],
 ["2026-11-11","doi:10.1103/pb2g-j9cw","Spectral amplification, article of record","Open-access page loads (title: ...by Spectral Amplification); FeMoco paragraph present; text extraction refused","journal page (browser)","NOT READ: schedule row stays second-hand"],
 ["2026-11-10","github.com/physical-superintelligence/aaronson-ambainis","Claimed proof of the Aaronson-Ambainis conjecture","statement file matches Conjecture 1.7; simulation bound (4T)^8 eps^-14 delta^-8 in paper Sec. 1.3","commit 2a6ceae","Lean proof not rebuilt by us; no peer review"],
]
w("update_log.csv", UH, U)
print("wrote", len(E), "entries,", len(R), "resources,", len(V), "values,", len(F), "classes,", len(P), "figure points,", len(U), "log rows")
