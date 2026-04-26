from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap

n = 8
line_edges = [(i, i + 1) for i in range(n - 1)]
coupling = CouplingMap(couplinglist=line_edges)

def build_stage(n, stride):
    qc = QuantumCircuit(n)
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

stages = [1, 2, 4]
total_pre_cx  = 0
total_post_cx = 0

print(f"{'Stage':<8} {'Stride':<8} {'Pre-CX':<10} {'Post-CX':<10} {'Overhead':<10} {'Depth'}")
print("-" * 58)

for idx, stride in enumerate(stages):
    qc = build_stage(n, stride)
    pre_cx = qc.count_ops().get('cx', 0)

    transpiled = transpile(
        qc,
        coupling_map=coupling,
        basis_gates=['cx', 'rz', 'h', 'x'],
        optimization_level=1,
        seed_transpiler=42
    )

    post_cx = transpiled.count_ops().get('cx', 0)
    depth   = transpiled.depth()
    overhead = round((post_cx - pre_cx) / pre_cx * 100) if pre_cx > 0 else 0

    total_pre_cx  += pre_cx
    total_post_cx += post_cx

    print(f"{idx + 1:<8} {stride:<8} {pre_cx:<10} {post_cx:<10} {overhead:+}%{'':<7} {depth}")

print("-" * 58)
total_overhead = round((total_post_cx - total_pre_cx) / total_pre_cx * 100)
print(f"{'TOTAL':<8} {'':<8} {total_pre_cx:<10} {total_post_cx:<10} {total_overhead:+}%")
