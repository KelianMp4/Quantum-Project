from matplotlib import pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import os


def random_number_quantum(n_bits: int) -> int:

    """
    Generate a random integer using a quantum simulator.

    A quantum circuit with a single qubit applies a Hadamard gate,
    measures the qubit, and uses the most frequent result from 1024
    shots to build a binary number of length `n_bits`.

    Args:
        n_bits (int): Number of bits for the random number.

    Returns:
        int: Random integer generated from the binary number.
    """
    simulator = AerSimulator()
    binary_number: str = ''

    for _ in range(n_bits):
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.measure_all()
        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit, shots=1024).result()
        counts = result.get_counts()
        binary_number += str(max(counts, key=counts.get))

    number: int = int(binary_number, 2)
    return number


def create_histogram(binary_number: str, iteration: int):
    """
    Create and save a histogram of the counts of '0' and '1' in a binary string.

    Args:
        binary_number (str): Binary string to analyze.
        iteration (int): Iteration number used for naming the output file.

    Saves:
        A PNG file of the histogram in the 'histogram' directory.
    """
    counts = [binary_number.count('0'), binary_number.count('1')]
    plt.bar([0, 1], counts, color=['blue', 'red'])
    plt.title(f'Histogram of {binary_number}')
    plt.xlabel('Quantum number')
    plt.ylabel('Count')
    os.makedirs('histogram', exist_ok=True)
    plt.savefig(f'histogram/{iteration}.png')
    plt.close()


def create_global_histogram(global_count: dict):
    """
    Create and save a histogram of the global counts of '0' and '1'.

    Args:
        global_count (dict): Dictionary with keys '0' and '1' representing
                             the global counts of each quantum outcome.

    Saves:
        A PNG file of the histogram as 'histogram/global_histogram.png'.
    """
    plt.bar([0, 1], [global_count['0'], global_count['1']], color=['blue', 'red'])
    plt.title(f'Histogram of global count')
    plt.xlabel('Quantum number')
    plt.ylabel('Count')
    plt.savefig(f'histogram/global_histogram.png')
    plt.close()


def main():
    """
    Execute the quantum random number generation process and visualize results.

    Prompts the user for the number of iterations and bits, generates random
    binary numbers using a quantum simulator, creates individual histograms
    for each binary number, and generates a global histogram of '0' and '1' counts.

    Steps:
        1. Input the number of iterations and bits.
        2. Generate random numbers and save histograms for each iteration.
        3. Accumulate counts of '0' and '1' across iterations.
        4. Create and save a global histogram.

    """
    global_count: dict = {'0': 0, '1': 0}

    while True:
        try:
            n_iterations = int(input('Number of iterations: '))
            n_bits = int(input('Number of bits: '))
            if n_iterations > 0 and n_bits > 0:
                break
            else:
                print("Both values must be greater than 0. Please try again.")
        except ValueError:
            print("Invalid input. Please enter integers greater than 0.")

    for j in range(n_iterations):
        number = random_number_quantum(n_bits)
        binary = bin(number)[2:]
        print(f'random binary number: {binary};\n'
              f'random decimal number: {number}\n')
        create_histogram(binary, j)

        global_count['0'] += binary.count('0')
        global_count['1'] += binary.count('1')

    create_global_histogram(global_count)


if __name__ == '__main__':
    main()
