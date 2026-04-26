import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap

n = 8
line_edges = [(i, i + 1) for i in range(n - 1)]
coupling = CouplingMap(couplinglist=line_edges)

def build_ntt_n8():
    qc = QuantumCircuit(n)
    for stride in [1, 2, 4]:
        for i in range(0, n, stride * 2):
            for j in range(stride):
                u = i + j
                v = i + j + stride
                if u < n and v < n:
                    qc.h(u)
                    qc.cx(u, v)
                    qc.rz(0.25, v)
                    qc.cx(u, v)
                    qc.h(u)
    return qc

qc = build_ntt_n8()
pre_ops = qc.count_ops()

transpiled = transpile(
    qc,
    coupling_map=coupling,
    basis_gates=['cx', 'rz', 'h', 'x'],
    optimization_level=1,
    seed_transpiler=42
)
post_ops = transpiled.count_ops()

gates = ['cx', 'rz', 'h']
pre_counts  = [pre_ops.get(g, 0)  for g in gates]
post_counts = [post_ops.get(g, 0) for g in gates]

x = np.arange(len(gates))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 5))

bars_pre  = ax.bar(x - width / 2, pre_counts,  width, color='steelblue',  label='Pre-transpilation',  edgecolor='black', linewidth=0.7)
bars_post = ax.bar(x + width / 2, post_counts, width, color='darkorange', label='Post-transpilation', edgecolor='black', linewidth=0.7)

for bar in bars_pre:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
            str(int(bar.get_height())), ha='center', va='bottom', fontsize=10)

for bar in bars_post:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
            str(int(bar.get_height())), ha='center', va='bottom', fontsize=10)

ax.set_xlabel('Gate Type', fontsize=12)
ax.set_ylabel('Gate Count', fontsize=12)
ax.set_title('Figure 2: Gate Counts Before and After Transpilation (n=8 NTT)', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(['CX (CNOT)', 'RZ', 'H'], fontsize=11)
ax.legend(fontsize=10)
ax.set_ylim(0, max(post_counts) * 1.25)
ax.grid(axis='y', linestyle='--', alpha=0.5)

cx_overhead = round((post_ops.get('cx', 0) - pre_ops.get('cx', 0)) / pre_ops.get('cx', 1) * 100)
ax.annotate(
    f'+{cx_overhead}% CNOT overhead',
    xy=(x[0] + width / 2, post_ops.get('cx', 0)),
    xytext=(x[0] + width / 2 + 0.3, post_ops.get('cx', 0) + 1.5),
    arrowprops=dict(arrowstyle='->', color='red'),
    fontsize=10, color='red'
)

plt.tight_layout()
plt.savefig('results/figure2_gate_counts.png', dpi=150)
plt.show()
print("Figure saved to results/figure2_gate_counts.png")
