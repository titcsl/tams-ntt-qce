# TAMS-NTT: Fault-Tolerant NTT Resource Analysis for ML-KEM

> Companion code for **"Architectural Area-Time Trade-offs for Fault-Tolerant NTT: A Congestion-Aware Resource Analysis for ML-KEM"**  
> Ishan Teredesai, Ayush Raj Sahay, Sanskar Chavan, Tushar Rahangadle  
> Yeshwantrao Chavan College of Engineering, Nagpur, India  
> IEEE QCE 2025

---

## Overview

This repository contains the Qiskit simulation code validating the routing overhead analysis presented in the paper. Specifically, it implements the `n=8` NTT butterfly circuit and transpiles it onto a line-connectivity graph approximating the IBM Heavy-Hex subgraph topology, confirming the 43% CNOT overhead reported in Section IV.

---

## Repository Structure

```
tams-ntt-qce/
├── simulation/
│   ├── ntt_butterfly_n8.py        # n=8 NTT butterfly circuit + Heavy-Hex transpilation
│   ├── routing_overhead.py        # Per-stage SWAP depth analysis (Eq. 3 in paper)
│   └── gate_count_plot.py         # Reproduces Figure 2 (pre vs post transpilation)
├── montgomery/
│   └── t_gate_budget.py           # T-gate decomposition for 12-bit Montgomery multiplier
├── results/
│   ├── gate_counts_n8.csv         # Raw gate count data (Table I in paper)
│   └── sensitivity_data.csv       # Sensitivity analysis data (Figure 5 in paper)
├── requirements.txt
└── README.md
```

---

## Reproducing Key Results

### 1. n=8 NTT Butterfly Simulation (Section IV)

Validates the 43% CNOT routing overhead on Heavy-Hex line topology.

```bash
python simulation/ntt_butterfly_n8.py
```

Expected output:
```
Pre-transpilation  : CX=14, RZ=7, H=7
Post-transpilation : CX=20, RZ=7, H=7
CNOT Overhead      : +43%
```

### 2. T-gate Budget Verification (Section V)

Reproduces the full 1320 T-gate breakdown for the 12-bit Montgomery multiplier.

```bash
python montgomery/t_gate_budget.py
```

Expected output:
```
Partial product additions : 528
Montgomery reduction      : 92
CSA tree (4 levels)       : 96
Carry propagation (KS)    : 44
Final carry ripple         : 8
Output MUX (12-bit)       : 48
Bennett uncomputation      : 156
m'q correction             : 348
─────────────────────────────
TOTAL T_mul                : 1320 ✓
```

### 3. Routing Overhead Plot (Figure 2)

```bash
python simulation/gate_count_plot.py
```

---

## Installation

```bash
git clone https://github.com/yourusername/tams-ntt-qce.git
cd tams-ntt-qce
pip install -r requirements.txt
```

### Requirements

```
qiskit>=1.0.0
qiskit-aer>=0.14.0
numpy>=1.26.0
matplotlib>=3.8.0
```

---

## Key Results Summary

| Metric | Baseline | TAMS | Improvement |
|---|---|---|---|
| Physical Qubits | ~5.40M | 3.51M ±8% | ~35–40% |
| T-Factory Utilization | <40% | 95–99% | 2.4× ↑ |
| Routing Overhead | 2.4× | 1.6× | 33% ↓ |
| Ancilla (peak) | 100% data | 12.5% data | 8× ↓ |

---

## Citation

If you use this code in your work, please cite:

```bibtex
@inproceedings{teredesai2025tams,
  title     = {Architectural Area-Time Trade-offs for Fault-Tolerant {NTT}:
               A Congestion-Aware Resource Analysis for {ML-KEM}},
  author    = {Teredesai, Ishan and Sahay, Ayush Raj and
               Chavan, Sanskar and Rahangadle, Tushar},
  booktitle = {Proceedings of the IEEE International Conference on
               Quantum Computing and Engineering (QCE)},
  year      = {2025},
  note      = {Yeshwantrao Chavan College of Engineering, Nagpur, India}
}
```

---

## Contact

For questions regarding the code or paper, reach out at `{ishan, sanskar, tushar, ayush}@aqcnr.co.in`

---

## License

MIT License. See `LICENSE` for details.
