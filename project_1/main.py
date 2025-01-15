from matplotlib import pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import os


def random_number_quantum(n_bits: int, n_execution: int = 0):
    os.makedirs(name='Hist', exist_ok=True)
    simulator = AerSimulator()
    n: int = 0

    for _ in range(n_execution):
        i: int = 0
        number: str = ''
        n += 1

        while i < n_bits:
            qc = QuantumCircuit(1)
            qc.h(0)
            qc.measure_all()
            compiled_circuit = transpile(qc, simulator)
            result = simulator.run(compiled_circuit, shots=1024).result()
            counts = result.get_counts()
            number += str(max(counts, key=counts.get))
            i += 1

        plt.bar([0, 1], [number.count('0'), number.count('1')], color=['blue', 'red'])
        plt.title(f'Histogram of quantum numbers: {number} : {int(number, 2)}')
        plt.xlabel('quantum number')
        plt.ylabel('count')
        plt.savefig(f'Hist/quantum{n}.png')
        plt.close()

        print(f"binary number : {number};\n"
              f"base 10 number: {int(number, 2)}")


if __name__ == '__main__':
    print(random_number_quantum(n_bits=10, n_execution=10))
