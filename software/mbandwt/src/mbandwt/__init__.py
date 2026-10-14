"""mbandwt: general M-band discrete wavelet transforms and
perfect-reconstruction filter banks in Python.

The number of channels ``M`` is an arbitrary property of the wavelet filter
bank rather than a hard-coded dyadic assumption. See ``docs/conventions.md``
for the exact mathematical conventions.
"""

from . import families, polyphase
from .coefficients import DWTResult, MBandCoefficients
from .families import (
    block_dct,
    daubechies,
    from_pywt,
    haar,
    lazy,
    mlt,
    paraunitary_from_factors,
    random_paraunitary,
)
from .filterbank import FilterBank
from .multilevel import max_level, wavedec, waverec
from .transform import dwt, idwt
from .validation import ValidationReport, validate

__version__ = "0.1.0"

__all__ = [
    "FilterBank",
    "dwt",
    "idwt",
    "wavedec",
    "waverec",
    "max_level",
    "validate",
    "ValidationReport",
    "DWTResult",
    "MBandCoefficients",
    "families",
    "polyphase",
    "haar",
    "daubechies",
    "from_pywt",
    "block_dct",
    "lazy",
    "mlt",
    "paraunitary_from_factors",
    "random_paraunitary",
    "__version__",
]
