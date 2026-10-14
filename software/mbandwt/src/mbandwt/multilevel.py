"""Multilevel M-band decomposition and reconstruction.

``wavedec`` recursively decomposes only band 0 (ordinary multiresolution
analysis); wavelet-packet decomposition, where every band branches, is
deliberately out of scope for v0.x. Each level stores its own bookkeeping
so ``waverec`` reconstructs the exact original array.
"""

from __future__ import annotations

import math
import warnings
from typing import Optional

import numpy as np

from .coefficients import DWTResult, MBandCoefficients
from .filterbank import FilterBank
from .transform import dwt, idwt

__all__ = ["wavedec", "waverec", "max_level"]


def max_level(N: int, bank: FilterBank) -> int:
    """Largest sensible decomposition depth for a length-``N`` signal.

    Analogous to PyWavelets' rule: ``floor(log_M(N / (L_max - 1)))`` where
    ``L_max`` is the longest analysis filter, with natural degenerate cases.
    """
    M = bank.M
    L = max(len(h) for h in bank.analysis)
    if N < 1:
        return 0
    if L <= 1:
        return int(math.floor(math.log(N) / math.log(M))) if N >= M else 0
    if N < L:
        return 0
    return int(math.floor(math.log(N / (L - 1)) / math.log(M)))


def wavedec(
    x,
    bank: FilterBank,
    level: Optional[int] = None,
    mode: str = "periodic",
    axis: int = -1,
) -> MBandCoefficients:
    """Multilevel M-band wavelet decomposition.

    Parameters
    ----------
    x : array_like
    bank : FilterBank
    level : int, optional
        Number of levels. Defaults to :func:`max_level`. Requesting more
        than :func:`max_level` levels emits a ``UserWarning`` (boundary
        effects dominate) but proceeds while the approximation band still
        has at least one sample per polyphase component.
    mode, axis :
        As in :func:`mbandwt.dwt`.
    """
    if not isinstance(bank, FilterBank):
        raise TypeError("bank must be a FilterBank")
    x = np.asarray(x)
    if x.ndim == 0:
        raise ValueError("input signal must have at least one dimension")
    if not isinstance(axis, (int, np.integer)) or isinstance(axis, (bool, np.bool_)):
        raise TypeError("axis must be an integer")
    if not -x.ndim <= axis < x.ndim:
        raise ValueError(f"axis {axis} is out of bounds for {x.ndim}-D input")
    if x.shape[axis] == 0:
        raise ValueError("input signal must have at least one sample along axis")
    N = x.shape[axis]
    ml = max_level(N, bank)
    if level is None:
        level = max(ml, 1)
    if not isinstance(level, (int, np.integer)) or isinstance(level, (bool, np.bool_)):
        raise TypeError("level must be an integer")
    if level < 1:
        raise ValueError("level must be at least 1")
    if level > ml:
        warnings.warn(
            f"requested level {level} exceeds max_level = {ml} for this "
            "signal length and filter bank; boundary effects will dominate "
            "the deepest levels",
            UserWarning,
            stacklevel=2,
        )

    cur = x
    details: list = []
    metas: list = []
    for _ in range(level):
        if cur.shape[axis] < 1:
            raise ValueError("signal became empty before reaching the requested level")
        r = dwt(cur, bank, mode=mode, axis=axis)
        details.append(list(r.bands[1:]))
        metas.append(r.meta)
        cur = r.bands[0]

    return MBandCoefficients(
        approx=cur,
        details=details,
        metas=metas,
        bank=bank,
        mode=mode,
        axis=axis,
        level=level,
        original_length=N,
    )


def waverec(coeffs: MBandCoefficients, bank: FilterBank = None) -> np.ndarray:
    """Multilevel M-band wavelet reconstruction.

    ``bank`` defaults to the bank stored in ``coeffs``; passing a different
    bank with a different signature raises.
    """
    if not isinstance(coeffs, MBandCoefficients):
        raise TypeError(
            "coeffs must be an MBandCoefficients (as returned by mbandwt.wavedec)"
        )
    bank = coeffs.bank if bank is None else bank
    if bank is None:
        raise ValueError("no filter bank available: pass bank= explicitly")

    cur = coeffs.approx
    for j in reversed(range(coeffs.level)):
        r = DWTResult(
            [cur] + list(coeffs.details[j]),
            bank,
            coeffs.mode,
            coeffs.axis,
            coeffs.metas[j],
        )
        cur = idwt(r, bank=bank, axis=coeffs.axis)
    return cur
