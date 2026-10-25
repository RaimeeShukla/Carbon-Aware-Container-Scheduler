# Carbon Aware Container Scheduler

A container scheduling system that incorporates carbon intensity and forecast information into workload execution decisions

## Problem Statement

Conventional workload scheduling often prioritizes resource availability without explicitly considering the carbon intensity of electricity at the time and location of execution

This project explores how carbon-aware scheduling can reduce estimated operational emissions while respecting workload deadlines and execution constraints

## Objectives

- Implement a baseline container workload scheduler
- Integrate carbon intensity observations and forecasts
- Evaluate carbon-aware scheduling policies
- Explore deadline-aware workload time shifting
- Execute workloads using Docker and Kubernetes
- Monitor scheduling behavior with Prometheus and Grafana
- Evaluate the system using reproducible experiments

## Technology Stack

- Python
- Git and GitHub
- Docker
- Kubernetes and Kind
- Carbon Aware SDK
- Prometheus
- Grafana