"""Filter-bank validation.

Two independent perfect-reconstruction tests are combined:

* **algebraic** — the polyphase product ``R(z) E(z)`` must be a scaled
  monomial times the identity (:func:`mbandwt.polyphase.pr_check`);
* **operational** — a unit impulse is passed through the full periodic
  analysis/synthesis chain (without compensation) and the output must be a
  single scaled, shifted impulse; the measured shift must equal the delay
  implied by the polyphase test.

Orthogonality is tested operationally: the periodic analysis operator ``A``
(built by transforming an identity basis) must satisfy ``A A^H = c I``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .filterbank import FilterBank

__all__ = ["ValidationReport", "validate"]


def _fmt_gain(c) -> str:
    if np.iscomplexobj(np.asarray(c)) and abs(np.imag(c)) > 1e-12 * max(abs(np.real(c)), 1e-300):
        return f"{complex(c):.12g}"
    return f"{float(np.real(c)):.12f}"


@dataclass
class ValidationReport:
    M: int
    perfect_reconstruction: bool
    gain: complex
    delay: int
    pr_residual_polyphase: float
    pr_residual_operational: float
    delay_operational: int
    delay_consistent: bool
    orthogonal: bool
    orthogonality_residual: float
    biorthogonal: bool

    @property
    def classification(self) -> str:
        if not self.perfect_reconstruction:
            return "not perfect-reconstruction"
        return "orthonormal" if self.orthogonal else "biorthogonal"

    def __str__(self) -> str:
        lines = [
            "mbandwt filter-bank validation",
            "------------------------------",
            f"M:                          {self.M}",
            f"Perfect reconstruction:     {self.perfect_reconstruction}",
            f"Gain:                       {_fmt_gain(self.gain)}",
            f"Delay (samples):            {self.delay}",
            f"PR residual (polyphase):    {self.pr_residual_polyphase:.1e}",
            f"PR residual (operational):  {self.pr_residual_operational:.1e}",
            f"Delay check (operational):  "
            + (
                "consistent"
                if self.delay_consistent
                else (
                    "n/a (bank is not PR)"
                    if not self.perfect_reconstruction
                    else f"MISMATCH ({self.delay_operational})"
                )
            ),
            f"Orthonormal:                {self.orthogonal}",
            f"Orthonormality residual:    {self.orthogonality_residual:.1e}",
            f"Classification:             {self.classification}",
        ]
        return "\n".join(lines)


def _operational_test_length(bank: FilterBank) -> int:
    M = bank.M
    Lh = max(len(h) for h in bank.analysis)
    Lg = max(len(g) for g in bank.synthesis)
    return M * (math.ceil((Lh + Lg) / M) + 2)


def _operational_pr(bank: FilterBank):
    """Impulse response of the uncompensated periodic analysis+synthesis chain."""
    from .transform import _analyze_periodic, _synthesize_periodic_raw

    N = _operational_test_length(bank)
    x = np.zeros(N)
    x[0] = 1.0
    bands = _analyze_periodic(x, bank.analysis, bank.M)
    raw = _synthesize_periodic_raw(bands, bank.synthesis, bank.M, N)
    j0 = int(np.argmax(np.abs(raw)))
    val = raw[j0]
    if val == 0:
        return j0, val, np.inf
    rest = raw.copy()
    rest[j0] = 0.0
    residual = float(np.max(np.abs(rest)) / np.abs(val))
    return j0, val, residual


def _orthogonality_residual(bank: FilterBank) -> float:
    """Max relative deviation of the periodic analysis operator from c*I."""
    from .transform import _analyze_periodic

    N = _operational_test_length(bank)
    X = np.eye(N)
    if bank.is_complex:
        X = X.astype(np.complex128)
    bands = _analyze_periodic(X, bank.analysis, bank.M)  # each (N, N/M)
    C = np.concatenate(bands, axis=-1)  # rows: images of basis vectors
    G = C @ np.conj(C.T)
    alpha = float(np.real(np.trace(G)) / N)
    if alpha <= 0 or not np.isfinite(alpha):
        return np.inf
    return float(np.max(np.abs(G - alpha * np.eye(N))) / alpha)


def validate(bank: FilterBank, rtol: float = 1e-8) -> ValidationReport:
    """Run the full validation program on a filter bank."""
    pp = bank.pr_report(rtol)
    j0, val, op_res = _operational_pr(bank)
    orth_res = bank.orthogonality_residual()

    delay_consistent = (int(j0) == int(pp["delay"]))
    pr = bool(pp["pr"]) and op_res < rtol and delay_consistent
    orth = pr and orth_res < rtol
    return ValidationReport(
        M=bank.M,
        perfect_reconstruction=pr,
        gain=pp["gain"],
        delay=int(pp["delay"]),
        pr_residual_polyphase=float(pp["residual"]),
        pr_residual_operational=float(op_res),
        delay_operational=int(j0),
        delay_consistent=delay_consistent if bool(pp["pr"]) else False,
        orthogonal=orth,
        orthogonality_residual=float(orth_res),
        biorthogonal=pr and not orth,
    )
