# Development Log

## 0.1 - Project Initialization

### Objective
To create a clean, reproducible project structure

## 0.2 — Workload Model and Validation

### Objective
Define a validated workload representation for the scheduler

### Implemented
- Unique workload identifiers
- Command and resource requirements
- Submission and earliest-start timestamps
- Optional execution deadlines
- Optional allowed-region constraints
- Validation of resource values and scheduling timestamps
- Unit tests for valid and invalid workload definitions

### Design Decisions
- Scheduling timestamps must be timezone-aware
- UTC is used as the default submission timezone
- An empty allowed-region list means no explicit region restriction
- Deadlines must leave enough time for the estimated execution duration

### Next
Implement baseline scheduling engine