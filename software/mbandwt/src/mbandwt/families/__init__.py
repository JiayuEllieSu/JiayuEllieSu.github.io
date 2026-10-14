"""Built-in filter-bank catalog.

Every bank carries provenance (``reference``/``family``) so users know
where the construction comes from. Planned but not yet included:
transcribed algebraic 3-/4-band coefficient tables from the M-band
literature (requires careful sourcing; see the roadmap in the README).
"""

from .block import block_dct, lazy
from .cosine import mlt
from .design import paraunitary_from_factors, random_paraunitary
from .dyadic import daubechies, from_pywt, haar

__all__ = [
    "haar",
    "daubechies",
    "from_pywt",
    "block_dct",
    "lazy",
    "mlt",
    "paraunitary_from_factors",
    "random_paraunitary",
]
