from qiskit import QuantumCircuit, Aer, execute
from qiskit.extensions import UnitaryGate

import numpy as np
import math

def simulate_chsh_game(a_input, b_input, mode='quantum', shots=1000, ruleset='default'):
    outcomes = {"wins": 0, "losses": 0}

    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)

    # Alice's operation based on x
    if a_input == 0:
        # Apply ^U0 (Identity operation, so do nothing)
        pass
    elif a_input == 1:
        # Apply ^Uπ/4
        qc.ry(math.pi/4, 0)

    # Bob's operation based on y
    if b_input == 0:
        # Apply ^Uπ/8
        qc.ry(math.pi/8, 1)
    elif b_input == 1:
        # Apply ^U-π/8
        qc.ry(-math.pi/8, 1)
    


    # Apply strategies based on inputs
    if mode == 'quantum':
        if a_input == 1:
            qc.ry(np.pi/4, 0)
        if b_input == 1:
            qc.ry(-np.pi/4, 1)

    # Measure the qubits
    qc.measure([0, 1], [0, 1])

    # Execute the circuit
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=shots)
    result = job.result()
    counts = result.get_counts(qc)

    # Determine win/loss based on a predefined condition
    for outcome in counts:
        # Assuming a win condition for demonstration. Adjust according to your game's rules.
        if outcome == "11":
            outcomes["wins"] += counts[outcome]
        else:
            outcomes["losses"] += counts[outcome]

    # Calculate win rate
    win_rate = (outcomes["wins"] / shots) * 100

    return {
        "total_shots": shots,
        "outcome_counts": counts,
        "wins": outcomes["wins"],
        "losses": outcomes["losses"],
        "win_rate": win_rate
    }

# Example usage
a_input = 1
b_input = 0
mode = 'quantum'
shots = 1000
game_results = simulate_chsh_game(a_input, b_input, mode, shots)
print(game_results)