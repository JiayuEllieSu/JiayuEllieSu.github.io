---
layout: single
title: "HistoRange: Histology-Guided Modeling of Anisotropic Diffusion and Effective Signaling Range in Spatial Transcriptomics"
description: "A computational framework using histology-derived anisotropic transport to study spatial ligand-receptor signaling and estimate effective signaling ranges."
date: 2026-10-29
status: "2026 research project · Manuscript in progress"
classes: wide
author_profile: true
---

**HistoRange** is a computational research project studying how tissue architecture influences cell-cell signaling in spatial transcriptomics. It uses registered hematoxylin-and-eosin (H&E) histology to construct a spatially varying, direction-dependent transport model, then analyzes associations between predicted ligand exposure and receptor responses.

The central question is whether the **geometry of tissue** can help explain not just where signaling interactions are associated with a response, but also the spatial scale over which secreted signals appear to act.

## Mathematical and computational approach

The framework separates **interaction detection** from **effective-range estimation** so that it does not automatically assign a meaningful physical range to every fitted interaction.

1. **Histology and geometry:** extract tissue structure and local orientations from H&E images, defining an anisotropic transport tensor while respecting tissue boundaries and holes.
2. **Transport modeling:** propagate ligand source fields through a screened diffusion equation with no-flux boundary conditions, using finite-element numerical methods.
3. **Spatial association testing:** evaluate whether predicted exposure is associated with receptor response using covariance-aware generalized least squares and bootstrap-based inference.
4. **Effective-range estimation:** estimate a characteristic transport length for supported secreted interactions, with simulation-calibrated uncertainty and boundary-aware reporting.
5. **Robustness and specificity:** evaluate the contribution of matched histology and the stability of inferred ranges separately from the primary detection results.

One model component takes the form

$$
-\nabla\cdot\bigl(A(x)\nabla u(x)\bigr) + \ell^{-2}u(x) = q(x),
$$

where $$A(x)$$ represents local anisotropic tissue transport, $$q(x)$$ is a ligand source field, and $$\ell$$ is a candidate signaling-length scale.

## Why this interested me

Biological tissue is not a homogeneous medium. Cells, fibers, boundaries, and morphological structures can make communication depend on **direction as well as distance**. HistoRange brings together partial differential equations, numerical linear algebra, spatial statistics, and computational biology to investigate that relationship.

The implementation includes Python modules for histology processing, mesh construction, finite-element transport, spatial inference, range estimation, and synthetic validation experiments.

**[Explore the HistoRange code and documentation on GitHub](https://github.com/JiayuEllieSu/HistoRange)**
