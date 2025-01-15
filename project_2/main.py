from matplotlib import pyplot as plt
from qiskit import QuantumCircuit, transpile, ClassicalRegister
from random import uniform
import numpy as np
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector


def quantum_teleportation() -> QuantumCircuit:
    qc = QuantumCircuit(3)

    #  Random value for A
    theta = uniform(a=0, b=np.pi)
    phi = uniform(a=0, b=2 * np.pi)
    qc.ry(theta=theta, qubit=0)
    qc.rz(phi=phi, qubit=0)

    #  State of Bell between B and C
    qc.h(qubit=1)
    qc.cx(control_qubit=1, target_qubit=2)

    #  Intricate A with B
    qc.cx(control_qubit=0, target_qubit=1)
    qc.h(qubit=0)

    qc.draw(output='mpl')
    plt.show()

    return qc


def hinton_schema(qc: QuantumCircuit):
    statevector = Statevector.from_instruction(qc)
    print(f'State vector initial: {statevector}')
    statevector.draw(output='hinton')
    plt.show()


def simulation_and_result(qc: QuantumCircuit):
    qc.add_register(ClassicalRegister(3, 'E'))

    qc.measure(qubit=0, cbit=0)
    qc.measure(qubit=1, cbit=1)

    qc.x(2).c_if(qc.clbits[1], val=1)
    qc.z(2).c_if(qc.clbits[0], val=1)
    qc.measure(qubit=2, cbit=2)

    qc.draw(output='mpl')
    plt.show()

    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    result = simulator.run(compiled_circuit, shots=1024).result()
    counts = result.get_counts()
    print(f'counts: {counts}')
    plot_histogram(counts).show()


if __name__ == '__main__':
    qc = quantum_teleportation()
    hinton_schema(qc)
    simulation_and_result(qc)