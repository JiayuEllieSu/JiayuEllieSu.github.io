---
layout: single
title: "Noncommutative Shear Flows and Chaotic Advection"
description: "Exploring material stretching and passive-tracer transport through area-preserving shear maps."
date: 2026-11-18
category: project
kind: "Computational physics project"
materials: "Python simulation, numerical results, figures, and project poster"
primary_label: "View source code"
primary_url: "https://github.com/JiayuEllieSu/noncommutative-shear-flows"
secondary_label: "View poster (PDF)"
secondary_url: "https://github.com/JiayuEllieSu/noncommutative-shear-flows/blob/main/poster.pdf"
classes: wide
author_profile: true
---

{% include work-meta.html %}

This project grew out of my fluid mechanics course at Phillips Academy. I wanted to understand how a fluid can stretch and rearrange material even when the flow is incompressible, and why alternating simple shears can behave very differently from repeating one shear.

## Mathematical model

I model passive tracers with two linear shear maps,

\[
A=\begin{pmatrix}1&1\\0&1\end{pmatrix},
\qquad
B=\begin{pmatrix}1&0\\1&1\end{pmatrix}.
\]

Both have determinant one, so they preserve area. But their order matters: \(AB\ne BA\). I compare three repeated protocols: shearing in one direction, alternating shears, and shears of opposite sign. The particles are tracked on a periodic two-dimensional domain.

The key distinction is that noncommutativity alone does not guarantee exponential stretching. For an area-preserving two-shear matrix with shear-strength product \(ab\), exponential growth occurs when \(|2+ab|>2\); the boundary and intermediate regimes have different behavior.

## Numerical experiments

Using Python and NumPy, I compare maximum singular-value stretching, tracer trajectories, and the variance of particle counts across spatial bins. The alternating protocol has a largest Lyapunov exponent of approximately \(0.9624\) per cycle, compared with zero asymptotic exponential growth for the single-direction shear protocol.

In the saved simulation, at cycle 10, the maximum stretch is approximately **15,127** for alternating shears and **20.05** for repeated single-direction shears. At cycle 6, the coarse count variances are **0.0665** (alternating), **8.7274** (single direction), and **19.3206** (opposite-sign shears), against a uniform-sampling reference of approximately **0.0639**.

These measurements distinguish geometric stretching from coarse-grained spatial redistribution. The model illustrates *chaotic advection*, not molecular diffusion or a full Navier–Stokes solution.

## Code, poster, and figures

- [Source code and reproduction instructions](https://github.com/JiayuEllieSu/noncommutative-shear-flows)
- [Project poster (PDF)](https://github.com/JiayuEllieSu/noncommutative-shear-flows/blob/main/poster.pdf)
- [Stretching comparison](https://github.com/JiayuEllieSu/noncommutative-shear-flows/blob/main/figures/stretching_comparison.png)
- [Tracer distributions](https://github.com/JiayuEllieSu/noncommutative-shear-flows/blob/main/figures/tracer_protocols.png)
- [Coarse-grained count variance](https://github.com/JiayuEllieSu/noncommutative-shear-flows/blob/main/figures/count_variance_wide.png)
