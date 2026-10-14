"""Polyphase representation and algebraic perfect-reconstruction tests.

Conventions (see ``docs/conventions.md``, Section 4):

* Type-I analysis polyphase:  ``E_{kj}[n] = h_k[M n + j]``
* Type-II synthesis polyphase: ``R_{jk}[n] = g_k[M n + M - 1 - j]``
* Perfect reconstruction  <=>  ``R(z) E(z) = c z^{-k0} I``
* Overall sample-domain delay ``d = M k0 + (M - 1)``.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np

__all__ = [
    "analysis_polyphase",
    "synthesis_polyphase",
    "polyphase_product",
    "pr_check",
    "filters_from_analysis_polyphase",
]


def _component(f: np.ndarray, start: int, M: int) -> np.ndarray:
    comp = np.asarray(f)[start::M]
    if comp.size == 0:
        comp = np.zeros(1, dtype=np.asarray(f).dtype)
    return comp


def _poly_lists_to_cube(P: list) -> np.ndarray:
    """Pack a list-of-lists of 1-D coefficient arrays into an (M, M, T) cube."""
    M = len(P)
    T = max(len(P[i][j]) for i in range(M) for j in range(M))
    dtype = np.result_type(*[P[i][j].dtype for i in range(M) for j in range(M)])
    cube = np.zeros((M, M, T), dtype=dtype)
    for i in range(M):
        for j in range(M):
            cube[i, j, : len(P[i][j])] = P[i][j]
    return cube


def analysis_polyphase(analysis: Sequence[np.ndarray], M: int) -> np.ndarray:
    """Type-I analysis polyphase matrix as an ``(M, M, T)`` array.

    ``E[k, j, n] = h_k[M n + j]`` with trailing zero padding to a common
    polynomial length ``T``.
    """
    comps = [[_component(h, j, M) for j in range(M)] for h in analysis]
    return _poly_lists_to_cube(comps)


def synthesis_polyphase(synthesis: Sequence[np.ndarray], M: int) -> np.ndarray:
    """Type-II synthesis polyphase matrix as an ``(M, M, T)`` array.

    ``R[j, k, n] = g_k[M n + M - 1 - j]``.
    """
    comps = [
        [_component(synthesis[k], M - 1 - j, M) for k in range(M)] for j in range(M)
    ]
    return _poly_lists_to_cube(comps)


def polyphase_product(R: np.ndarray, E: np.ndarray) -> np.ndarray:
    """Polynomial matrix product ``P(z) = R(z) E(z)`` of two ``(M, M, T)`` cubes."""
    M = R.shape[0]
    if E.shape[0] != M or R.shape[1] != M or E.shape[1] != M:
        raise ValueError("polyphase matrices must both be M x M")
    Tp = R.shape[2] + E.shape[2] - 1
    dtype = np.result_type(R.dtype, E.dtype)
    P = np.zeros((M, M, Tp), dtype=dtype)
    for i in range(M):
        for j in range(M):
            acc = np.zeros(Tp, dtype=dtype)
            for k in range(M):
                acc += np.convolve(R[i, k], E[k, j])
            P[i, j] = acc
    return P


def pr_check(
    analysis: Sequence[np.ndarray],
    synthesis: Sequence[np.ndarray],
    M: int,
    rtol: float = 1e-8,
) -> dict:
    """Algebraic perfect-reconstruction test via the polyphase product.

    Returns a dict with keys ``pr`` (bool), ``gain`` (complex/float),
    ``k0`` (monomial delay of the polyphase product), ``delay`` (overall
    sample-domain delay ``M*k0 + M - 1``), and ``residual`` (maximum
    relative deviation of ``P(z)`` from ``c z^{-k0} I``).
    """
    E = analysis_polyphase(analysis, M)
    R = synthesis_polyphase(synthesis, M)
    P = polyphase_product(R, E)

    diag = np.stack([P[i, i] for i in range(M)])  # (M, Tp)
    dbar = diag.mean(axis=0)
    k0 = int(np.argmax(np.abs(dbar)))
    c = dbar[k0]
    scale = np.abs(c)
    if scale == 0 or not np.isfinite(scale):
        return {
            "pr": False,
            "gain": c,
            "k0": k0,
            "delay": M * k0 + (M - 1),
            "residual": np.inf,
        }

    target = np.zeros_like(P)
    for i in range(M):
        target[i, i, k0] = c
    residual = float(np.max(np.abs(P - target)) / scale)

    return {
        "pr": residual < rtol,
        "gain": c,
        "k0": k0,
        "delay": M * k0 + (M - 1),
        "residual": residual,
    }


def filters_from_analysis_polyphase(E: np.ndarray) -> list[np.ndarray]:
    """Rebuild analysis filters from a type-I polyphase cube ``(M, M, T)``.

    Inverse of :func:`analysis_polyphase`: ``h_k[M n + j] = E[k, j, n]``,
    giving filters of length ``M * T``.
    """
    E = np.asarray(E)
    M, M2, T = E.shape
    if M != M2:
        raise ValueError("polyphase cube must be M x M x T")
    filters = []
    for k in range(M):
        h = np.zeros(M * T, dtype=E.dtype)
        for j in range(M):
            h[j::M] = E[k, j]
        filters.append(h)
    return filters
