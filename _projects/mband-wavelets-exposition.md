---
layout: single
title: "From Fourier Analysis to M-Band Wavelets"
date: 2026-10-30
description: "An exposition of multiresolution analysis, M-band filter banks, and the algebraic conditions for perfect reconstruction."
category: project
kind: "Expository paper"
materials: "12-page paper (PDF), LaTeX source, and numerical illustrations"
primary_label: "Read paper (PDF)"
primary_url: "https://github.com/JiayuEllieSu/mbandwt/blob/main/docs/paper/mband_wavelets.pdf"
secondary_label: "LaTeX source"
secondary_url: "https://github.com/JiayuEllieSu/mbandwt/blob/main/docs/paper/mband_wavelets.tex"
contributors_label: "Author"
contributors: "Ellie Su"
classes: wide
author_profile: true
---

{% include work-meta.html %}

This exposition begins with the Haar transform and the idea of representing a signal in an orthogonal basis. It then develops the discrete wavelet transform through multiresolution analysis and extends the construction to \(M\)-band filter banks.

I discuss the roles of low-pass and detail filters, vanishing moments, and the algebraic conditions for perfect reconstruction. Polyphase matrices provide a way of expressing those conditions, and paraunitary factorizations give a constructive approach to filter design.

The final sections connect the mathematical theory with my Python project, [`mbandwt`]({{ '/projects/mbandwt/' | relative_url }}), and include numerical illustrations of filter frequency responses and multilevel decomposition.

**[Read the exposition (PDF)](https://github.com/JiayuEllieSu/mbandwt/blob/main/docs/paper/mband_wavelets.pdf)**

[LaTeX source](https://github.com/JiayuEllieSu/mbandwt/blob/main/docs/paper/mband_wavelets.tex) | [Python package](https://github.com/JiayuEllieSu/mbandwt)
