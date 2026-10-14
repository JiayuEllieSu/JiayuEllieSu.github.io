"""Constructive paraunitary bank design for arbitrary M.

Every FIR paraunitary (orthonormal) M-channel polyphase matrix can be
written as a product of unitary matrices and elementary delay factors
(Vaidyanathan, 1993, Ch. 6):

    E(z) = V_K Lambda(z) V_{K-1} Lambda(z) ... Lambda(z) V_0,
    Lambda(z) = diag(1, ..., 1, z^{-1}).

Building E(z) this way and reading the filters off the polyphase components
yields orthonormal PR banks for any ``M`` and any McMillan degree — an
unlimited supply of valid test cases and design starting points.
"""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np

from ..filterbank import FilterBank
from ..polyphase import filters_from_analysis_polyphase

__all__ = ["paraunitary_from_factors", "random_paraunitary"]

_REF = (
    "P. P. Vaidyanathan, Multirate Systems and Filter Banks, Prentice "
    "Hall, 1993, Ch. 6 (degree-one paraunitary factorization)."
)


def _apply_delay_factor(E: np.ndarray) -> np.ndarray:
    """Multiply the polyphase cube on the left by Lambda(z) = diag(1,..,1,z^{-1})."""
    M, _, T = E.shape
    out = np.zeros((M, M, T + 1), dtype=E.dtype)
    out[:-1, :, :T] = E[:-1]
    out[-1, :, 1:] = E[-1]
    return out


def paraunitary_from_factors(unitaries: Sequence[np.ndarray], name: Optional[str] = None) -> FilterBank:
    """Build an orthonormal bank ``E(z) = V_K L(z) ... L(z) V_0`` from unitaries.

    Parameters
    ----------
    unitaries : sequence of (M, M) unitary/orthogonal matrices
        ``K + 1`` factors ``V_0 .. V_K``; delay factors are inserted between
        consecutive matrices. Filters have length ``M * (K + 1)``.
    """
    Vs = [np.asarray(V) for V in unitaries]
    if not Vs:
        raise ValueError("need at least one unitary factor")
    if Vs[0].ndim != 2 or Vs[0].shape[0] < 2 or Vs[0].shape[0] != Vs[0].shape[1]:
        raise ValueError("each factor must be an M x M matrix with M >= 2")
    M = Vs[0].shape[0]
    for V in Vs:
        if V.shape != (M, M):
            raise ValueError("all factors must be square matrices of the same size")
        if np.max(np.abs(np.conj(V.T) @ V - np.eye(M))) > 1e-10:
            raise ValueError("factors must be unitary/orthogonal to working precision")
    E = Vs[0].astype(np.complex128 if any(np.iscomplexobj(V) for V in Vs) else np.float64)
    E = E[:, :, None]
    for V in Vs[1:]:
        E = _apply_delay_factor(E)
        E = np.einsum("ij,jkt->ikt", V, E)
    filters = filters_from_analysis_polyphase(E)
    return FilterBank(
        filters,
        name=name or f"paraunitary(M={M}, order={len(Vs) - 1})",
        family="paraunitary factorization (arbitrary M)",
        reference=_REF,
    )


def random_paraunitary(M: int, order: int = 2, seed: Optional[int] = None) -> FilterBank:
    """Random orthonormal M-channel bank of the given polyphase order.

    Filters have length ``M * (order + 1)``. Deterministic for a fixed
    ``seed``. Primarily intended for testing and experimentation.
    """
    if M < 2:
        raise ValueError("M must be at least 2")
    if order < 0:
        raise ValueError("order must be non-negative")
    rng = np.random.default_rng(seed)

    def rand_orth() -> np.ndarray:
        Q, R = np.linalg.qr(rng.standard_normal((M, M)))
        return Q * np.sign(np.diag(R))

    bank = paraunitary_from_factors(
        [rand_orth() for _ in range(order + 1)],
        name=f"random_paraunitary(M={M}, order={order}, seed={seed})",
    )
    return bank
