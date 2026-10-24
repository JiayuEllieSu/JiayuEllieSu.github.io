---
layout: single
title: "mbandwt: M-Band Transform Experiments"
description: "A Python project exploring M-band FIR filter banks, multilevel transforms, and signal reconstruction."
category: project
date: 2026-10-13
classes: wide
author_profile: true
---

**mbandwt** is a Python project I started while learning about wavelets and multirate signal processing. A typical discrete wavelet transform separates a signal into two channels at each level. I wanted to see how the same ideas work with \(M\) channels, and what it takes to reconstruct the original signal from the resulting coefficients.

The project began with a one-level orthogonal cosine *block* transform in NumPy. I later expanded it to experiment with overlapping finite impulse response (FIR) filter banks and multilevel M-band decomposition. The block transform remains as a simpler example; it is not itself an overlapping wavelet filter bank.

## What it includes

- **M-channel FIR filter banks:** analysis filters split a signal into downsampled subbands; synthesis filters combine them to reconstruct the signal.
- **Multilevel transforms:** `wavedec` recursively decomposes the approximation channel, and `waverec` reverses the process.
- **Polyphase analysis:** matrix representations and numerical checks for perfect reconstruction, including gain and delay.
- **Filter families:** two-channel Haar and Daubechies examples, plus M-channel cosine, lapped, and paraunitary constructions.
- **Experiments:** frequency responses, coefficient energies, boundary extension, padding, and reconstruction error.

## Example: three bands, four levels

```python
import numpy as np
from mbandwt import wavedec, waverec
from mbandwt.families import mlt

bank = mlt(3)
signal = np.random.default_rng(4).normal(size=486)

coeffs = wavedec(signal, bank, level=4, mode="periodic")
recovered = waverec(coeffs)

print("levels:", coeffs.level)
print("max error:", np.max(np.abs(signal - recovered)))
```

The example uses a three-channel lapped filter bank. Each level decomposes only the approximation channel, leaving the other two channels as detail coefficients. The inverse combines the saved bands in reverse order.

## What I was interested in

The main questions were how the number and design of filters affect the decomposition, how boundary handling changes coefficient lengths, and how to tell whether analysis followed by synthesis actually reconstructs the input. I also experimented with polyphase conditions for perfect reconstruction rather than relying only on a small numerical error in a single test signal.

The library is an **experimental learning project**, not production signal-processing software. In particular, a custom filter bank is not guaranteed to have perfect reconstruction merely because it has \(M\) analysis and synthesis filters.

**[View the code on GitHub](https://github.com/JiayuEllieSu/mbandwt)**

The repository includes [installation instructions and examples](https://github.com/JiayuEllieSu/mbandwt#readme), [multilevel analysis code](https://github.com/JiayuEllieSu/mbandwt/blob/main/examples/multilevel_analysis.py), and [mathematical conventions](https://github.com/JiayuEllieSu/mbandwt/blob/main/docs/conventions.md).
