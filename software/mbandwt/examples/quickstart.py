"""Quickstart: validate a 3-band bank, transform, and reconstruct."""

import numpy as np

import mbandwt
from mbandwt.families import mlt

bank = mlt(3)
print(bank.validate())
print()

rng = np.random.default_rng(0)
# N = 2 * 3^5: divisible by M = 3 at every level, so the orthonormal energy
# identity holds exactly (with awkward lengths, periodic wrap-padding
# duplicates a few samples and the coefficient energy slightly exceeds the
# signal energy — reconstruction stays exact either way).
x = rng.standard_normal(486)

coeffs = mbandwt.wavedec(x, bank, level=4, mode="periodic")
x_rec = mbandwt.waverec(coeffs)

err = np.linalg.norm(x - x_rec) / np.linalg.norm(x)
print(f"levels: {coeffs.level}   M: {coeffs.M}")
print(f"relative reconstruction error: {err:.3e}")

energies = coeffs.band_energies()
total = sum(energies.values())
print(f"energy captured by coefficients / signal energy: {total / np.sum(x**2):.12f}")
