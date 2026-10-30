---
layout: single
title: "Fourier Series: From Orthogonal Vectors to Heat Flow"
date: 2026-10-30
category: note
description: "A joint lecture I gave with Dawon Suh in July 2026, introducing Fourier series through orthogonality and applying them to the heat equation."
classes: wide
author_profile: true
---

**Presented:** July 2026  
**Co-presenters:** Ellie Su and Dawon Suh  
**Format:** Collaborative mathematics lecture, with a 12-page handout

In July 2026, **Dawon Suh and I gave a lecture on Fourier series**, beginning with the analogy between vectors and functions. We introduced inner products and orthogonality, then derived the complex Fourier coefficient formula by projecting a function onto its exponential modes.

We used **sawtooth, square, and triangle waves** to illustrate how periodic functions can be built from elementary oscillations, discussed the distinction between pointwise and mean-square convergence, and explained the Gibbs phenomenon near discontinuities.

As an application, we used Fourier series to **solve the heat equation on a circular rod**, showing how each spatial frequency evolves independently, why higher-frequency temperature fluctuations dissipate more quickly, and why the average temperature stays constant in an insulated system.

{% assign handout_path = '/assets/papers/fourier-series-lecture-notes.pdf' %}
{% assign handout = site.static_files | where: "path", handout_path | first %}
{% if handout %}
**[Read the lecture notes (PDF, 12 pages)]({{ handout_path | relative_url }})**
{% else %}
*Lecture handout PDF will be added here.*
{% endif %}
