# Development Log

## 0.1 - Project Initialization

### Objective
To create a clean, reproducible project structure

## 0.2 - Workload Model and Validation

### Objective
Define a validated workload representation for the scheduler

## 0.3 - Baseline Scheduling Engine

## 0.4 — Docker-Based Workload Execution

### Objective
Execute scheduled workloads in isolated, resource-limited containers

### Implemented
- Docker SDK integration
- Structured execution results
- CPU and memory limits
- Container execution and exit-code handling
- Standard output and error log collection
- Basic container security restrictions
- Container cleanup after execution
- Mock-based unit tests
- Manual Docker smoke test

### Current Limitations
- Workload scheduling and execution are not yet connected by a persistent orchestration loop
- Only a single configured container image is supported
- The CPU benchmark does not measure actual electricity consumption
- Execution targets are not yet separated by region

### Next 
Implement carbon-data provider interface