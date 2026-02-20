# A depth QV circuit is successful if it has mean heavy-output probability > 2/3 with confidence level > 0.977 (corresponding to z_value = 2), and at least 100 trials have been ran.

# vai ir vienādi, uz 3-niekiem

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import random_unitary
from qiskit.quantum_info import Statevector
from qiskit import transpile


def random_circuit(N, seed=None) -> QuantumCircuit:
    '''
    Generates a random quantum circuit with N qubits and depth N. 
    Each layer consists of random 2-qubit gates applied to random pairs of qubits.
    '''

    rng = np.random.default_rng(seed)
    qc = QuantumCircuit(N, N)
    
    for _ in range(N): 
        perm = rng.permutation(N) 

        for i in range(0, N - 1, 2):
            q1, q2 = perm[i], perm[i+1]

            U = random_unitary(4, seed=rng.integers(1e6))
            qc.append(U, [q1, q2])
    
    qc.measure(range(N), range(N))
    return qc


def heavy_set_ideal(qc_with_meas) -> set:
    '''
    Returns the set of bitstrings with probability greater than the median, 
    based on the statevector of the circuit without measurements.
    '''

    # remove measurement instructions, since statevector does not support
    qc_no_meas = qc_with_meas.remove_final_measurements(inplace=False)
    
    # get the full statevector amplitudes
    amplitudes = Statevector.from_instruction(qc_no_meas).data

    # convert amplitudes to probabilities
    probabilities = []
    for amp in amplitudes: probabilities.append(abs(amp) ** 2)

    # find the median probability value
    median_value = np.median(probabilities)

    # create the set of bitstrings with probability greater than the median
    heavy_set = set()
    n_qubits = qc_with_meas.num_qubits
    for i, prob in enumerate(probabilities):
        if prob > median_value:
            bitstring = format(i, 'b')
            while len(bitstring) < n_qubits: bitstring = '0' + bitstring
            heavy_set.add(bitstring)

    return heavy_set


def hop_from_counts(counts_dict, heavy_set):
    ''' 
    Returns the heavy output probability based on the counts dictionary and the heavy set. 
    '''

    shots = sum(counts_dict.values())

    heavy_hits = 0

    # count how many measurments are in the heavy set
    for bitstring, count in counts_dict.items():
        if bitstring in heavy_set: heavy_hits += count

    return heavy_hits / shots


def quantum_volume(N, k, n, backend, subset=None, seed=0):

    """
    N: logical qubits (should match len(subset) if subset provided)
    k: number of random circuits (trials)
    n: shots per circuit
    backend: target backend (AerSimulator or real backend)
    subset: list of physical qubit indices, length N
    """

    if len(subset) != N:
        raise ValueError("len(subset) must equal N")

    # build all circuits
    circuits = [random_circuit(N, seed=seed+i) for i in range(k)]

    # transpile all circuits

    transpile_kwargs = dict(
        backend=backend,
        optimization_level=0,
        layout_method="trivial",
        routing_method="basic",
        seed_transpiler=seed,
        initial_layout=subset,
    )

    transpiled = transpile(circuits, **transpile_kwargs)

    # run all circuits in a single job
    result = backend.run(transpiled, shots=n).result()

    individual_hops, cumulative_hops = [], []

    for i in range (k):
        heavy_set = heavy_set_ideal(transpiled[i])
        counts_dict = result.get_counts(i)
        hop = hop_from_counts(counts_dict, heavy_set)
        
        individual_hops.append(hop)
        cumulative_hops.append(float(np.mean(individual_hops)))

    return {
        "individual_hops": individual_hops,
        "cumulative_hops": cumulative_hops, 
    }
