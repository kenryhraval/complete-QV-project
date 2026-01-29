# Complete QV Project

## `extract-calibration-data.ipynb` 
- extracts calibration data from IBM Quantum backends and stores it locally (uses environment `runtime.txt`)
- stores snapshots under: `calibrations/<backend_name>/<timestamp>.json`
- this notebook only needs to be run when updating calibration data


## `run-experiment.ipynb` 
- runs Quantum Volume experiments using classical simulation with GPU acceleration (uses environment `gpu.txt`)
- uses the GPU environment with: `qiskit-aer-gpu`, CUDA-enabled Aer simulation


## TODO / Future Work

### Qubit Subset Selection
- Enumerate **connected qubit subsets** from the device coupling graph
- Rank candidate subsets by:
  - connectivity
  - estimated two-qubit error rates
- Avoid brute-force enumeration for large devices via:
  - heuristic search
  - graph-based pruning strategies

### Quantum Volume Automation
- Automate **QV frontier detection**:
  - determine the maximum passing subset size `m`
- Cache and reuse results across runs to reduce recomputation

### Comparative Analysis
- Compare QV results across:
  - different calibration snapshots (temporal variation)
  - different IBM Quantum backends (  
    e.g. Fez vs Marrakesh vs Torino)

### Visualization
- Plot **HOP distributions** per subset size
- Plot **confidence vs subset size**
- Visualize QV frontier across devices and calibrations


## Quantum Volume Methodology

Quantum Volume (QV) is evaluated following the standard definition:

- Circuits are **square**, with
  - width = depth = number of qubits `m`
- For each `m`, multiple random QV circuits are generated and executed
- A run is considered successful if **both** conditions are met:
  - Mean heavy-output probability $HOP > 2/3$
  - Statistical confidence $≥ 97\%$

Experiments are performed for increasing subset sizes `m`.  
The reported Quantum Volume is defined as $QV = 2^m$

