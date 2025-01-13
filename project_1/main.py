from matplotlib import pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import os


def random_number_quantum(long: int, iteration: int) -> str:
    i: int = 0
    number: str = ''
    simulator = AerSimulator()

    while i < long:
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.measure_all()
        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit, shots=1024).result()
        counts = result.get_counts()
        number += str(max(counts, key=counts.get))
        i += 1

    plt.bar([0, 1], [number.count('0'), number.count('1')], color=['blue', 'red'])
    plt.title(f'Histogram of quantum numbers: {number}')
    plt.xlabel('quantum number')
    plt.ylabel('count')
    plt.savefig(f'Hist/quantum{iteration}.png')
    plt.close()

    return (f"binary number : {number};\n"
            f"base 10 number: {int(number, 2)}")


if __name__ == '__main__':
    os.makedirs('Hist', exist_ok=True)
    for iteration in range(10):
        print(random_number_quantum(10, iteration))