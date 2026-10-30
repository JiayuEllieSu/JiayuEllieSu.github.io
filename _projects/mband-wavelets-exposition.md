---
layout: single
title: "From Fourier Analysis to M-Band Wavelets"
date: 2026-10-30
category: note
description: "An exposition on orthogonal discrete wavelets, M-band filter banks, multiresolution analysis, and perfect reconstruction."
classes: wide
author_profile: true
---

**Written:** October 2026  
**Format:** Mathematical exposition (12 pages)

This exposition begins with the Haar transform and the idea of representing a signal in an orthogonal basis. It then develops the discrete wavelet transform through multiresolution analysis and extends the construction to (M)-band filter banks.

I discuss the roles of low-pass and detail filters, vanishing moments, and the algebraic conditions for perfect reconstruction. Polyphase matrices provide a way of expressing those conditions, and paraunitary factorizations give a constructive approach to filter design.

The final sections connect the mathematical theory with my Python project, [`mbandwt`]({{ '/projects/mbandwt/' | relative_url }}), and include numerical illustrations of filter frequency responses and multilevel decomposition.

**[Read the exposition (PDF)](https://github.com/JiayuEllieSu/mbandwt/blob/main/docs/paper/mband_wavelets.pdf)**

[LaTeX source](https://github.com/JiayuEllieSu/mbandwt/blob/main/docs/paper/mband_wavelets.tex) | [Python package](https://github.com/JiayuEllieSu/mbandwt)
