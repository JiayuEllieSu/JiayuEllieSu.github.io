"""Dyadic (M = 2) reference families.

These serve two roles: regression anchors against PyWavelets (the general
M-band engine must reduce correctly to the ordinary dyadic case) and a
familiar starting point for users.
"""

from __future__ import annotations

from math import comb

import numpy as np

from ..filterbank import FilterBank

__all__ = ["haar", "daubechies", "from_pywt"]

_DAUB_REF = (
    "I. Daubechies, Ten Lectures on Wavelets, SIAM, 1992. Coefficients "
    "generated at runtime by spectral factorization of the maxflat "
    "half-band product filter."
)


def _daubechies_scaling(p: int) -> np.ndarray:
    """Length-2p minimum-phase Daubechies scaling filter (sum = sqrt(2))."""
    if p < 1:
        raise ValueError("p must be a positive integer")
    # binomial part (1 + z^{-1})^p
    b = np.array([1.0])
    for _ in range(p):
        b = np.convolve(b, [1.0, 1.0])
    if p == 1:
        return b / np.sqrt(2.0)  # Haar
    # P(y) = sum_{k=0}^{p-1} C(p-1+k, k) y^k, roots in y
    a = np.array([comb(p - 1 + k, k) for k in range(p)], dtype=np.float64)
    yroots = np.roots(a[::-1])
    zroots = []
    for y0 in yroots:
        # y = (2 - z - 1/z)/4  =>  z^2 - (2 - 4y) z + 1 = 0
        bq = -(2.0 - 4.0 * y0)
        disc = np.sqrt(bq * bq - 4.0 + 0j)
        r1 = (-bq + disc) / 2.0
        r2 = (-bq - disc) / 2.0
        zroots.append(r1 if abs(r1) < 1.0 else r2)
    q = np.real(np.poly(zroots))
    h = np.convolve(b, q)
    h *= np.sqrt(2.0) / h.sum()
    return h


def _qmf(h: np.ndarray) -> np.ndarray:
    """Quadrature mirror highpass: h1[n] = (-1)^n h0[L-1-n]."""
    L = len(h)
    n = np.arange(L)
    return ((-1.0) ** n) * h[::-1]


def daubechies(p: int) -> FilterBank:
    """Orthonormal Daubechies bank with ``p`` vanishing moments (M = 2).

    Analysis filters follow the PyWavelets ``dec_lo``/``dec_hi`` orientation
    (time-reversed scaling/wavelet coefficients used in convolution), so the
    coefficient arrays are directly comparable in the regression tests.
    """
    h0 = _daubechies_scaling(p)
    h1 = _qmf(h0)
    bank = FilterBank(
        [h0[::-1], h1[::-1]],
        name=f"db{p}",
        family="Daubechies (orthonormal, M=2)",
        reference=_DAUB_REF,
    )
    return bank


def haar() -> FilterBank:
    """Orthonormal Haar bank (M = 2), the p = 1 Daubechies bank."""
    bank = daubechies(1)
    bank.name = "haar"
    bank.family = "Haar (orthonormal, M=2)"
    return bank


def from_pywt(name: str) -> FilterBank:
    """Wrap a PyWavelets discrete wavelet as an M = 2 :class:`FilterBank`.

    Requires the optional dependency ``PyWavelets``. Both orthogonal (``dbN``,
    ``symN``, ``coifN``, ...) and biorthogonal (``biorX.Y``) wavelets are
    supported; the resulting bank passes ``mbandwt``'s PR validation.
    """
    try:
        import pywt
    except ImportError as e:  # pragma: no cover
        raise ImportError(
            "from_pywt requires PyWavelets: pip install PyWavelets"
        ) from e
    w = pywt.Wavelet(name)
    analysis = [np.asarray(w.dec_lo, dtype=np.float64), np.asarray(w.dec_hi, dtype=np.float64)]
    synthesis = [np.asarray(w.rec_lo, dtype=np.float64), np.asarray(w.rec_hi, dtype=np.float64)]
    return FilterBank(
        analysis,
        synthesis,
        name=f"pywt:{name}",
        family="PyWavelets bridge (M=2)",
        reference=(
            "G. R. Lee et al., PyWavelets: A Python package for wavelet "
            "analysis, J. Open Source Software 4(36), 1237, 2019."
        ),
    )
