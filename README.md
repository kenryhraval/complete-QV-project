# Complete QV Project

## `1_Extract_Calibration.ipynb` 
- extracts calibration data from IBM Quantum backends and stores it locally (uses environment `runtime.txt`)
- stores snapshots under: `calibrations/<backend_name>/<timestamp>.json`
- this notebook only needs to be run when updating calibration data


## `2_Run_Experiment.ipynb` 
- runs Quantum Volume experiments using classical simulation with GPU acceleration (uses environment `gpu.txt`)
- uses the GPU environment with: `qiskit-aer-gpu`, CUDA-enabled Aer simulation
- enumerates connected qubit subsets of three from the device coupling graph and calculates QV for each


## `3_Analyze_Results.ipynb` 
- 



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

