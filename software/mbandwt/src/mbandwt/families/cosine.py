"""Cosine-modulated filter banks (arbitrary M).

The modulated lapped transform (MLT) is a critically sampled M-channel
paraunitary filter bank with length-2M filters obtained by cosine
modulation of a sine prototype window (the filter-bank view of the MDCT
with a sine window). Its orthonormality is verified numerically by the test
suite for every shipped ``M``.
"""

from __future__ import annotations

import numpy as np

from ..filterbank import FilterBank

__all__ = ["mlt"]


def mlt(M: int) -> FilterBank:
    """Modulated lapped transform bank with ``M`` channels (filters length 2M).

    ``h_k[n] = w[n] sqrt(2/M) cos( (pi/M) (k + 1/2) (n + (M+1)/2) )`` with
    the sine window ``w[n] = sin( pi (n + 1/2) / (2M) )``, ``n = 0..2M-1``.
    """
    if M < 2:
        raise ValueError("M must be at least 2")
    n = np.arange(2 * M)
    w = np.sin(np.pi * (n + 0.5) / (2 * M))
    k = np.arange(M)[:, None]
    H = w * np.sqrt(2.0 / M) * np.cos((np.pi / M) * (k + 0.5) * (n + 0.5 + M / 2.0))
    return FilterBank(
        [H[i] for i in range(M)],
        name=f"mlt{M}",
        family="cosine-modulated / modulated lapped transform (arbitrary M)",
        reference=(
            "H. S. Malvar, Signal Processing with Lapped Transforms, Artech "
            "House, 1992; J. P. Princen and A. B. Bradley, IEEE Trans. "
            "Acoust., Speech, Signal Process. 34(5), 1986."
        ),
    )
