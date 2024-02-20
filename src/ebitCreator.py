from qiskit import QuantumCircuit, execute, Aer
from src.ebitCreator import create_entangled_pair, apply_alice_bob_operations, measure_and_get_results
import numpy as np


def create_entangled_pair():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    return qc

def apply_alice_bob_operations(qc, a_input, b_input):
    if a_input == 1:
        qc.ry(np.pi/4, 0)
    if b_input == 1:
        qc.ry(-np.pi/4, 1)
    return qc

def measure_and_get_results(qc, shots=1000):
    qc.measure([0, 1], [0, 1])
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=shots)
    result = job.result()
    counts = result.get_counts(qc)
    return counts
