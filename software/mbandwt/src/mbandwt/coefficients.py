"""Coefficient containers with exact finite-signal bookkeeping.

Transforms never return naked lists: results carry every piece of metadata
needed to reconstruct the exact original array (mode, original length,
padding/extension amounts, work length, transform axis, and the identity of
the filter bank that produced them).
"""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np

__all__ = ["DWTResult", "MBandCoefficients"]


class DWTResult:
    """Result of a one-level M-band DWT.

    ``r[0]`` / ``r.approx`` is the approximation band, ``r[1:]`` /
    ``r.details`` are the ``M - 1`` detail bands. Iteration and indexing run
    over ``r.bands``.
    """

    def __init__(self, bands: Sequence[np.ndarray], bank, mode: str, axis: int, meta: dict):
        self.bands = list(bands)
        self.bank = bank
        self.mode = mode
        self.axis = axis
        self.meta = dict(meta)

    # -- structure -----------------------------------------------------
    @property
    def M(self) -> int:
        return len(self.bands)

    @property
    def approx(self) -> np.ndarray:
        return self.bands[0]

    @property
    def details(self) -> list[np.ndarray]:
        return self.bands[1:]

    def __getitem__(self, i):
        return self.bands[i]

    def __len__(self) -> int:
        return len(self.bands)

    def __iter__(self):
        return iter(self.bands)

    @property
    def original_length(self) -> int:
        return self.meta["original_length"]

    def band_shapes(self) -> list[tuple]:
        return [b.shape for b in self.bands]

    def __repr__(self) -> str:
        lengths = [b.shape[self.axis if self.axis >= 0 else b.ndim + self.axis] for b in self.bands]
        return (
            f"DWTResult(M={self.M}, mode={self.mode!r}, axis={self.axis}, "
            f"band_lengths={lengths}, original_length={self.original_length})"
        )


class MBandCoefficients:
    """Multilevel M-band wavelet coefficients with per-level bookkeeping.

    Attributes
    ----------
    approx : ndarray
        Deepest approximation band ``A_J``.
    details : list of list of ndarray
        ``details[j]`` holds the ``M - 1`` detail bands produced at level
        ``j + 1`` (finest first: ``details[0]`` is level 1).
    level : int
        Number of decomposition levels ``J``.
    metas : list of dict
        Per-level bookkeeping (``metas[j]`` describes level ``j + 1``).
    """

    def __init__(
        self,
        approx: np.ndarray,
        details: list,
        metas: list,
        bank,
        mode: str,
        axis: int,
        level: int,
        original_length: int,
    ):
        self.approx = approx
        self.details = details
        self.metas = metas
        self.bank = bank
        self.mode = mode
        self.axis = axis
        self.level = level
        self.original_length = original_length

    @property
    def M(self) -> int:
        return len(self.details[0]) + 1 if self.details else None

    def detail(self, level: int, band: Optional[int] = None):
        """Detail bands of a given decomposition level (1-indexed, 1 = finest)."""
        if not isinstance(level, (int, np.integer)) or not 1 <= level <= self.level:
            raise ValueError(f"level must be between 1 and {self.level}")
        d = self.details[level - 1]
        if band is not None:
            if not isinstance(band, (int, np.integer)) or not 1 <= band <= len(d):
                raise ValueError(f"band must be between 1 and {len(d)}")
        return d if band is None else d[band - 1]

    def to_list(self) -> list:
        """PyWavelets-style coarse-first list ``[A_J, [D_J,*], ..., [D_1,*]]``."""
        return [self.approx] + [list(self.details[j]) for j in reversed(range(self.level))]

    def band_energies(self) -> dict:
        """Squared l2 norm of each stored band (diagnostic helper)."""
        out = {"approx": float(np.sum(np.abs(self.approx) ** 2))}
        for j, bands in enumerate(self.details):
            for k, b in enumerate(bands):
                out[f"D{j + 1},{k + 1}"] = float(np.sum(np.abs(b) ** 2))
        return out

    def __repr__(self) -> str:
        return (
            f"MBandCoefficients(M={self.M}, level={self.level}, mode={self.mode!r}, "
            f"axis={self.axis}, original_length={self.original_length})"
        )
