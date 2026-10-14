"""Block-transform banks for arbitrary M.

These have length-M filters (no overlap between blocks). Their frequency
selectivity is modest, but they are exactly orthonormal for every ``M``,
which makes them ideal reference banks for testing arbitrary-M machinery.
"""

from __future__ import annotations

import numpy as np

from ..filterbank import FilterBank

__all__ = ["block_dct", "lazy"]


def block_dct(M: int) -> FilterBank:
    """Orthonormal DCT-II block-transform bank with ``M`` channels.

    The k-th analysis filter is the k-th row of the orthonormal DCT-II
    matrix; as a filter bank with decimation ``M`` this is an orthonormal
    block transform (perfect reconstruction for every ``M >= 2``).
    """
    if M < 2:
        raise ValueError("M must be at least 2")
    n = np.arange(M)
    k = np.arange(M)[:, None]
    C = np.sqrt(2.0 / M) * np.cos(np.pi * (n + 0.5) * k / M)
    C[0] /= np.sqrt(2.0)
    return FilterBank(
        [C[i] for i in range(M)],
        name=f"block_dct{M}",
        family="DCT-II block transform (orthonormal, arbitrary M)",
        reference=(
            "K. R. Rao and P. Yip, Discrete Cosine Transform: Algorithms, "
            "Advantages, Applications, Academic Press, 1990."
        ),
    )


def lazy(M: int) -> FilterBank:
    """The lazy filter bank: pure polyphase splitting, ``h_k[n] = delta[n-k]``.

    Trivially orthonormal and PR for every ``M``; useful as an engine sanity
    check (its polyphase matrix is the identity, delay ``M - 1``).
    """
    if M < 2:
        raise ValueError("M must be at least 2")
    filters = []
    for k in range(M):
        h = np.zeros(M)
        h[k] = 1.0
        filters.append(h)
    return FilterBank(
        filters,
        name=f"lazy{M}",
        family="lazy / polyphase identity (arbitrary M)",
        reference=(
            "P. P. Vaidyanathan, Multirate Systems and Filter Banks, "
            "Prentice Hall, 1993."
        ),
    )
