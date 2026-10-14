"""One-level M-band DWT and inverse DWT.

Engine layering (plan: public API -> bookkeeping -> boundary handling ->
FilterBank -> transform engine -> upfirdn/NumPy/SciPy):

* ``zero`` mode is the primitive: analysis is
  ``scipy.signal.upfirdn(h, x, up=1, down=M)`` (full linear convolution
  decimated at phase 0), synthesis is ``upfirdn(g, c, up=M, down=1)``
  summed over bands, then delay/gain compensated and cropped.
* ``periodic`` mode is derived from it through the folding identity
  (circular convolution = linear convolution folded modulo N).
* ``symmetric``/``reflect``/``constant`` modes extend the signal by
  ``E = L_max - 1`` samples per side and run the ``zero`` primitive on the
  extended signal; reconstruction crops the center. All modes reconstruct
  exactly for PR banks. See ``docs/conventions.md``.
"""

from __future__ import annotations

import numpy as np
from scipy.signal import upfirdn

from .boundary import MODES, extend, periodic_right_pad
from .coefficients import DWTResult
from .filterbank import FilterBank

__all__ = ["dwt", "idwt"]


# ----------------------------------------------------------------------
# low-level helpers (all along the last axis)
# ----------------------------------------------------------------------
def _fold(y: np.ndarray, N: int) -> np.ndarray:
    """Fold the last axis modulo ``N``: out[i] = sum_{j == i mod N} y[j]."""
    L = y.shape[-1]
    pad = (-L) % N
    if pad:
        widths = [(0, 0)] * (y.ndim - 1) + [(0, pad)]
        y = np.pad(y, widths)
    shape = y.shape[:-1] + (-1, N)
    return y.reshape(shape).sum(axis=-2)


def _sum_to_length(arrays: list[np.ndarray], min_len: int) -> np.ndarray:
    T = max(min_len, max(a.shape[-1] for a in arrays))
    dtype = np.result_type(*[a.dtype for a in arrays])
    acc = np.zeros(arrays[0].shape[:-1] + (T,), dtype=dtype)
    for a in arrays:
        acc[..., : a.shape[-1]] += a
    return acc


def _analyze_zero(x: np.ndarray, filters, M: int) -> list[np.ndarray]:
    """c_k[n] = (h_k * x)[M n] for n = 0 .. ceil((N + L_k - 1)/M) - 1."""
    return [upfirdn(h, x, 1, M, axis=-1) for h in filters]


def _synthesize_zero_raw(bands, filters, M: int, min_len: int) -> np.ndarray:
    """sum_k g_k * up_M(c_k), zero-padded to at least ``min_len``."""
    parts = [upfirdn(g, c, M, 1, axis=-1) for g, c in zip(filters, bands)]
    return _sum_to_length(parts, min_len)


def _analyze_periodic(x: np.ndarray, filters, M: int) -> list[np.ndarray]:
    """Circular analysis of a last-axis-periodic signal with M | N."""
    N = x.shape[-1]
    if N % M:
        raise ValueError("periodic analysis requires M | N")
    # Decimate the linear convolution first, then fold modulo N/M. This is
    # equivalent to fold-then-decimate because, with M | N, the indices
    # congruent to M*n modulo N are exactly the multiples of M in the
    # congruence class of n modulo N/M — and it computes M times fewer
    # samples.
    return [_fold(upfirdn(h, x, 1, M, axis=-1), N // M) for h in filters]


def _synthesize_periodic_raw(bands, filters, M: int, N: int) -> np.ndarray:
    """Circular synthesis (before delay/gain compensation)."""
    parts = [upfirdn(g, c, M, 1, axis=-1) for g, c in zip(filters, bands)]
    return _fold(_sum_to_length(parts, N), N)


# ----------------------------------------------------------------------
# public API
# ----------------------------------------------------------------------
def dwt(x, bank: FilterBank, mode: str = "periodic", axis: int = -1) -> DWTResult:
    """One-level M-band discrete wavelet transform.

    Parameters
    ----------
    x : array_like
        Input signal; may be n-dimensional (the transform is applied along
        ``axis``, all other axes are batched).
    bank : FilterBank
        The M-channel filter bank.
    mode : {"periodic", "zero", "symmetric", "reflect", "constant"}
        Boundary handling (see ``docs/conventions.md``). ``periodic`` is
        non-expansive; the finite-extension modes are expansive with exact
        reconstruction.
    axis : int
        Axis along which to transform.

    Returns
    -------
    DWTResult
        ``result[0]`` is the approximation band, ``result[1:]`` the
        ``M - 1`` detail bands, plus bookkeeping metadata.
    """
    if not isinstance(bank, FilterBank):
        raise TypeError("bank must be a FilterBank")
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}, got {mode!r}")
    x = np.asarray(x)
    if x.ndim == 0:
        raise ValueError("input signal must have at least one dimension")
    if not isinstance(axis, (int, np.integer)) or isinstance(axis, (bool, np.bool_)):
        raise TypeError("axis must be an integer")
    if not -x.ndim <= axis < x.ndim:
        raise ValueError(f"axis {axis} is out of bounds for {x.ndim}-D input")
    if x.shape[axis] == 0:
        raise ValueError("input signal must have at least one sample along axis")
    if not np.issubdtype(x.dtype, np.number):
        raise TypeError("input signal must contain numeric data")
    M = bank.M
    xl = np.moveaxis(x, axis, -1)
    N = xl.shape[-1]

    if mode == "periodic":
        xp, P = periodic_right_pad(xl, M)
        bands = _analyze_periodic(xp, bank.analysis, M)
        meta = {
            "original_length": N,
            "work_length": N + P,
            "pad": P,
            "extension": 0,
            "signature": bank.signature,
        }
    else:
        if mode == "zero":
            E = 0
            xe = xl
        else:
            E = max(len(h) for h in bank.analysis) - 1
            xe = extend(xl, E, E, mode)
        bands = _analyze_zero(xe, bank.analysis, M)
        meta = {
            "original_length": N,
            "work_length": xe.shape[-1],
            "pad": 0,
            "extension": E,
            "signature": bank.signature,
        }

    bands = [np.moveaxis(b, -1, axis) for b in bands]
    return DWTResult(bands, bank, mode, axis, meta)


def idwt(coeffs: DWTResult, bank: FilterBank = None, axis: int = None) -> np.ndarray:
    """Inverse one-level M-band DWT.

    Reconstructs the exact original array (length, dtype-promoted) from a
    :class:`DWTResult`, compensating the bank's composite delay and gain.
    ``bank`` and ``axis`` default to the values stored in ``coeffs``.
    """
    if not isinstance(coeffs, DWTResult):
        raise TypeError("coeffs must be a DWTResult (as returned by mbandwt.dwt)")
    bank = coeffs.bank if bank is None else bank
    axis = coeffs.axis if axis is None else axis
    if axis != coeffs.axis:
        ndim = np.asarray(coeffs.bands[0]).ndim
        if not isinstance(axis, (int, np.integer)) or axis % ndim != coeffs.axis % ndim:
            raise ValueError("inverse axis must match the transform axis")
    if bank is None:
        raise ValueError("no filter bank available: pass bank= explicitly")
    if bank.signature != coeffs.meta["signature"]:
        raise ValueError(
            "these coefficients were produced with a different filter bank"
        )
    if len(coeffs.bands) != bank.M:
        raise ValueError("number of coefficient bands does not match bank.M")

    meta = coeffs.meta
    N = meta["original_length"]
    Nw = meta["work_length"]
    d = bank.delay
    c = bank.gain
    if not np.isfinite(c) or c == 0:
        raise ValueError("filter bank has zero or non-finite reconstruction gain")
    bands = [np.moveaxis(np.asarray(b), axis, -1) for b in coeffs.bands]

    if coeffs.mode == "periodic":
        expected = Nw // bank.M
        for b in bands:
            if b.shape[-1] != expected:
                raise ValueError(
                    f"band length {b.shape[-1]} inconsistent with work length {Nw}"
                )
        raw = _synthesize_periodic_raw(bands, bank.synthesis, bank.M, Nw)
        y = np.roll(raw, -d, axis=-1) / c
        y = y[..., :N]
    else:
        raw = _synthesize_zero_raw(bands, bank.synthesis, bank.M, d + Nw)
        y = raw[..., d : d + Nw] / c
        E = meta["extension"]
        y = y[..., E : E + N]

    return np.moveaxis(y, -1, axis)
