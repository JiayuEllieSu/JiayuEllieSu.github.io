---
layout: single
title: "Circular Stop Optimization"
description: "Modeling the placement of a fixed number of stops along circular bus routes, with discrete optimization and travel-time calibration."
date: 2026-03-01
category: project
kind: "Mathematical and computational project"
materials: "Paper (PDF), source code, figures, and reproducibility scripts"
primary_label: "Read paper (PDF)"
primary_url: "https://github.com/JiayuEllieSu/circular-stop-optimization/blob/main/paper/Fixed_Budget_Stop_Design_on_Circular_Routes_Theory__Discrete_Benchmarks__and_Observational_Calibration.pdf"
secondary_label: "View code"
secondary_url: "https://github.com/JiayuEllieSu/circular-stop-optimization"
classes: wide
author_profile: true
---

{% include work-meta.html %}

**Circular Stop Optimization** is a project I developed to investigate how to place a fixed number of bus stops along a circular route. Stop placement creates a tradeoff: closely spaced stops reduce passenger walking distances, but additional stops also impose delays on riders already aboard. I was interested in how a mathematical model of optimal stop density could be converted into a practical set of individual stop locations.

## Approach

The project combines several parts:

- **Continuum optimization:** derive a spatial stop-density rule under a fixed stop budget, accounting for passenger access, through-rider delays, and directional service.
- **Discrete stop placement:** translate the density into feasible locations with spacing and siting constraints, then compare projection, phase selection, and local search.
- **Passenger reassignment:** evaluate candidate layouts after allowing passengers to change their boarding and alighting stops, travel direction, or choice to walk.
- **Timing calibration:** test estimates of interstop travel time using published shuttle observations, fitting on an earlier period and evaluating on a later one.

## Computational experiments

Across 48 synthetic configurations and 720 training fits, the mean excess travel cost of a single-phase density projection was **14.23 seconds per trip**. Phase selection reduced this to **1.64 seconds**, and two-stop-exchange refinement reduced it to **0.60 seconds**. A matched random-start search reached a similar result, **0.61 seconds**, helping distinguish the contributions of the continuum model and discrete refinement.

The separate observational analysis assesses travel-time prediction, **not** the effects of actually relocating bus stops. The stop-placement experiments use synthetic passenger demand and hypothetical constraints, so they are not a field validation of a proposed transit redesign.

## Paper and code

**[Read the paper (PDF)](https://github.com/JiayuEllieSu/circular-stop-optimization/blob/main/paper/Fixed_Budget_Stop_Design_on_Circular_Routes_Theory__Discrete_Benchmarks__and_Observational_Calibration.pdf)**

[View the GitHub repository](https://github.com/JiayuEllieSu/circular-stop-optimization) | [LaTeX manuscript](https://github.com/JiayuEllieSu/circular-stop-optimization/blob/main/paper/transit_final.tex) | [Figures and reproducibility scripts](https://github.com/JiayuEllieSu/circular-stop-optimization#readme)
