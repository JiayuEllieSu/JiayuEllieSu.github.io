"""Finite-signal boundary handling.

Extension is implemented with explicit index maps (see
``docs/conventions.md``, Section 6) rather than :func:`numpy.pad`, so that
extensions longer than the signal itself are handled uniformly for every
mode. All functions operate along the last axis.
"""

from __future__ import annotations

import numpy as np

__all__ = ["MODES", "extend", "periodic_right_pad"]

#: Supported boundary modes.
MODES = ("periodic", "zero", "symmetric", "reflect", "constant")


def _extension_indices(N: int, left: int, right: int, mode: str) -> np.ndarray:
    """Index map for extended positions ``-left .. N-1+right`` (mode != zero)."""
    i = np.arange(-left, N + right)
    if mode == "periodic":
        return np.mod(i, N)
    if mode == "constant":
        return np.clip(i, 0, N - 1)
    if mode == "symmetric":
        j = np.mod(i, 2 * N)
        return np.where(j < N, j, 2 * N - 1 - j)
    if mode == "reflect":
        if N == 1:  # whole-sample reflection degenerates to edge replication
            return np.zeros_like(i)
        j = np.mod(i, 2 * N - 2)
        return np.where(j < N, j, 2 * N - 2 - j)
    raise ValueError(f"unknown extension mode {mode!r}")


def extend(x: np.ndarray, left: int, right: int, mode: str) -> np.ndarray:
    """Extend ``x`` along the last axis by ``left``/``right`` samples."""
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}, got {mode!r}")
    if left < 0 or right < 0:
        raise ValueError("extension lengths must be non-negative")
    if left == 0 and right == 0:
        return x
    N = x.shape[-1]
    if N == 0:
        raise ValueError("cannot extend an empty signal")
    if mode == "zero":
        pad = [(0, 0)] * (x.ndim - 1) + [(left, right)]
        return np.pad(x, pad, mode="constant", constant_values=0)
    idx = _extension_indices(N, left, right, mode)
    return np.take(x, idx, axis=-1)


def periodic_right_pad(x: np.ndarray, M: int) -> tuple[np.ndarray, int]:
    """Periodically pad the last axis on the right to a multiple of ``M``.

    Returns the padded array and the pad length ``P = (-N) mod M``.
    """
    N = x.shape[-1]
    P = (-N) % M
    if P == 0:
        return x, 0
    return extend(x, 0, P, "periodic"), P
