"""Multilevel 4-band analysis of a piecewise-smooth signal.

Shows the multiresolution tree (band 0 recursively decomposed), band
energies, and — if matplotlib is installed — a coefficient plot saved to
multilevel_analysis.png.
"""

import numpy as np

import mbandwt
from mbandwt.families import mlt

rng = np.random.default_rng(3)
N = 1024
t = np.arange(N) / N
x = np.sin(2 * np.pi * 5 * t) + 0.5 * (t > 0.6) + 0.05 * rng.standard_normal(N)

bank = mlt(4)
coeffs = mbandwt.wavedec(x, bank, level=3, mode="symmetric")

print(f"bank: {bank.name}   levels: {coeffs.level}   mode: {coeffs.mode}")
print("decomposition tree (band 0 recurses):")
print("x")
for j in range(1, coeffs.level + 1):
    pad = "    " * (j - 1)
    for k in range(1, bank.M):
        print(f"{pad}├── D{j},{k}  (len {coeffs.detail(j, k).shape[-1]})")
    tail = f"A{j}" if j == coeffs.level else f"A{j} ..."
    print(f"{pad}└── {tail}")

print("\nband energies (fraction of total):")
E = coeffs.band_energies()
total = sum(E.values())
for name, e in E.items():
    print(f"  {name:8s} {e / total:8.4f}")

x_rec = mbandwt.waverec(coeffs)
print(f"\nreconstruction error: "
      f"{np.linalg.norm(x - x_rec) / np.linalg.norm(x):.2e}")

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = 1 + coeffs.level
    fig, axes = plt.subplots(rows, 1, figsize=(8, 2 * rows), sharex=False)
    axes[0].plot(x, lw=0.8)
    axes[0].set_title("signal")
    for j in range(1, coeffs.level + 1):
        ax = axes[j]
        for k in range(1, bank.M):
            ax.plot(coeffs.detail(j, k), lw=0.8, label=f"D{j},{k}")
        ax.legend(loc="upper right", fontsize=7)
    fig.tight_layout()
    fig.savefig("multilevel_analysis.png", dpi=120)
    print("wrote multilevel_analysis.png")
except ImportError:
    print("(matplotlib not installed; skipping plot)")
