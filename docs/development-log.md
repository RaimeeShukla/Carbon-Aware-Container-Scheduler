# Development Log

## 0.1 - Project Initialization

## 0.2 - Workload Model and Validation

## 0.3 - Baseline Scheduling Engine

## 0.4 — Docker-Based Workload Execution

## 0.5 — Carbon Data Provider Interface

## 0.6 — Historical Carbon Data Integration

### Objective

Load and query historical carbon-intensity observations from CSV

### Implemented

* Historical CSV provider
* Required-column validation
* Region validation
* Timezone normalization to UTC
* Non-negative intensity validation through the carbon data model
* Duplicate observation detection
* Exact timestamp lookup
* Missing-observation error handling
* Test fixtures for India, France, and Germany

### Current Limitations

* No verified real-world historical dataset is added yet
* Lookup requires an exact timestamp match
* Forecast retrieval is not implemented
* The scheduling engine does not yet consume carbon data

### Next

Verify suitable external carbon data sources and integrate the chosen live or historical data provider
