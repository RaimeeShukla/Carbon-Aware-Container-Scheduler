# Development Log

## 0.1 - Project Initialization

## 0.2 - Workload Model and Validation

## 0.3 - Baseline Scheduling Engine

## 0.4 — Docker-Based Workload Execution

## 0.5 — Carbon Data Provider Interface

### Objective
Establish a provider-independent interface for carbon-intensity data

### Implemented
- Immutable carbon-intensity data model
- Carbon data provider interface
- Deterministic synthetic carbon-intensity provider
- Support for India, France, and Germany
- Timestamp and intensity validation
- Unit tests for provider behavior

### Current Limitations
- Synthetic data doesn't represent actual grid conditions
- Historical data ingestion is not implemented
- Live API integration is not implemented
- Forecast-based scheduling is not implemented
- The scheduling engine does not yet consume carbon-intensity data

### Next Milestone
Implement historical carbon data ingestion and check live data integration