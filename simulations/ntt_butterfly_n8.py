from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap

n = 8
qc = QuantumCircuit(n)

def ntt_butterfly_stage(circuit, qubits, stride):
    for i in range(0, len(qubits), stride * 2):
        for j in range(stride):
            u = qubits[i + j]
            v = qubits[i + j + stride]
            circuit.h(u)
            circuit.cx(u, v)
            circuit.rz(0.25, v)
            circuit.cx(u, v)
            circuit.h(u)

stages = [1, 2, 4]
for s in stages:
    ntt_butterfly_stage(qc, list(range(n)), s)

pre_cx = qc.count_ops().get('cx', 0)
pre_rz = qc.count_ops().get('rz', 0)
pre_h  = qc.count_ops().get('h', 0)

line_edges = [(i, i + 1) for i in range(n - 1)]
coupling = CouplingMap(couplinglist=line_edges)

transpiled = transpile(
    qc,
    coupling_map=coupling,
    basis_gates=['cx', 'rz', 'h', 'x'],
    optimization_level=1,
    seed_transpiler=42
)

post_cx = transpiled.count_ops().get('cx', 0)
post_rz = transpiled.count_ops().get('rz', 0)
post_h  = transpiled.count_ops().get('h', 0)

overhead = round((post_cx - pre_cx) / pre_cx * 100)

print(f"Pre-transpilation  : CX={pre_cx}, RZ={pre_rz}, H={pre_h}")
print(f"Post-transpilation : CX={post_cx}, RZ={post_rz}, H={post_h}")
print(f"CNOT Overhead      : +{overhead}%")
