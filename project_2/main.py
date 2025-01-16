from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import random_unitary
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from matplotlib import pyplot as plt
from qiskit.result import marginal_counts


def quantum_teleportation_circuit() -> QuantumCircuit:
    """
        Creates a quantum teleportation circuit with a random unitary transformation.
        The circuit entangles two qubits, teleports the state of a third qubit (data_q)
        to Bob's qubit (bob_q), and applies the inverse of the unitary transformation to verify teleportation.

        Returns:
            QuantumCircuit: The constructed quantum teleportation circuit.
    """
    U = random_unitary(2)
    U_gate = U.to_instruction()
    U_digger = U.adjoint().to_instruction()

    data_q = QuantumRegister(1, 'data_q')
    alice_q = QuantumRegister(1, 'Alice_q')
    bob_q = QuantumRegister(1, 'Bob_q')
    alice_c1 = ClassicalRegister(1, 'Alice_c1')
    alice_c2 = ClassicalRegister(1, 'Alice_c2')
    bob_c = ClassicalRegister(1, 'Bob_c')

    qc = QuantumCircuit(data_q, alice_q, bob_q, alice_c1, alice_c2, bob_c)

    qc.h(alice_q)
    qc.cx(alice_q, bob_q)
    qc.barrier()
    qc.append(U_gate, data_q)
    qc.barrier()
    qc.cx(data_q, alice_q)
    qc.h(data_q)
    qc.measure(data_q, alice_c1)
    qc.measure(alice_q, alice_c2)
    qc.barrier()
    qc.x(bob_q).c_if(alice_c2, 1)
    qc.z(bob_q).c_if(alice_c1, 1)
    qc.barrier()
    qc.append(U_digger, bob_q)

    qc.measure(bob_q, bob_c)

    qc.draw(output='mpl')
    plt.show()
    return qc


def mesure(qc: QuantumCircuit) -> dict | str:
    """
        Simulates the quantum circuit and measures the third qubit to verify the final state.
        The results are marginalized to focus on the third qubit, representing the teleported state.
        If the count for '0' is 1024, the teleportation is deemed successful.

        Args:
            qc (QuantumCircuit): The quantum circuit to simulate.

        Returns:
            dict: A dictionary containing the measurement results for the third qubit.
    """
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit)
    result = job.result()
    counts = result.get_counts()

    marginal_results = marginal_counts(counts, indices=[2])
    plot_histogram(marginal_results)
    plt.show()

    if marginal_results.get('0', 0) == 1024:
        print('Teleportation complete.')
        return marginal_results
    else:
        return 'Teleportation failed.'




if __name__ == '__main__':
    qc = quantum_teleportation_circuit()
    marginal_results = mesure(qc)
    print(marginal_results)