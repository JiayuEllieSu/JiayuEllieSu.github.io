"""The laboratory workflow: enter filter coefficients, let mbandwt decide.

A researcher takes an M-band filter bank from a paper, types in the
coefficients, and asks whether it satisfies perfect reconstruction, with
what gain and delay, and whether it is orthonormal — before transforming
anything.
"""

import numpy as np

import mbandwt
from mbandwt import FilterBank
from mbandwt.families import random_paraunitary

# Stand-in for "coefficients from a paper": a valid 4-band orthonormal bank.
paper_bank = random_paraunitary(4, order=2, seed=7)
H = [np.array(h) for h in paper_bank.analysis]

bank = FilterBank(H, name="entered-from-paper", reference="Doe et al. (20xx), Table 2")
print("--- bank as published ---")
print(bank.validate())

# A transcription error: one coefficient off in the third decimal place.
H_typo = [h.copy() for h in H]
H_typo[2][3] += 0.004
broken = FilterBank(H_typo, name="entered-with-typo")
print("\n--- bank with a transcription typo ---")
rep = broken.validate()
print(rep)

# The diagnostics quantify how badly reconstruction fails:
x = np.random.default_rng(1).standard_normal(200)
xr = mbandwt.idwt(mbandwt.dwt(x, broken))
print(f"\nroundtrip error with the typo: "
      f"{np.linalg.norm(x - xr) / np.linalg.norm(x):.2e}")

# Polyphase and moment inspection
E = bank.polyphase_analysis()
print(f"\npolyphase E(z): shape {E.shape} (M x M polynomial matrix)")
print(f"vanishing moments per filter: {bank.vanishing_moments()}")
