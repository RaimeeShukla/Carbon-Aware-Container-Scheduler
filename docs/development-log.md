# Development Log

## 0.1 - Project Initialization

### Objective
To create a clean, reproducible project structure

## 0.2 - Workload Model and Validation

### Objective
Define a validated workload representation for the scheduler

## 0.3 - Baseline Scheduling Engine

### Objective
Implement a deterministic baseline scheduler for pending workloads

### Implemented
- FIFO workload queue
- Duplicate queued-workload protection
- Queue inspection and removal operations
- Scheduling based on FIFO ordering
- Earliest-start-time enforcement
- Deadline feasibility checks
- Deterministic scheduling using an injected timestamp
- Unit tests for queue and scheduler behavior

### Current Limitations
- Workloads are stored in memory
- Workload execution is not implemented
- Rejected workloads are not yet tracked in a persistent lifecycle
- Carbon intensity does not influence scheduling decisions
- The scheduler processes one workload per scheduling call

### Next
Implement workload execution using Docker