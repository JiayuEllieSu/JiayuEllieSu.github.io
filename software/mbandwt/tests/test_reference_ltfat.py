"""Scaffold for M > 2 regression against LTFAT (MATLAB/GNU Octave).

LTFAT cannot run inside this repository's CI, so this test consumes
pre-generated reference data. To produce it, run in Octave with LTFAT
installed, using a matching filter family and the conventions in
docs/conventions.md (account for filter direction, phase, and coefficient
ordering — arrays are compared up to circular shift and sign, mirroring the
PyWavelets regression), then save::

    np.savez("tests/data/ltfat_reference.npz",
             x=x, M=M, level=level,
             filters=np.stack(filters_used),
             bands=np.stack(reference_bands))

Until such data is present the test is skipped, and M > 2 correctness rests
on (a) the algebraic polyphase PR test, (b) the operational impulse test,
(c) the independent naive-implementation cross-check in test_pr.py, and
(d) the constructive orthonormality of the shipped arbitrary-M families.
"""

from pathlib import Path

import numpy as np
import pytest

DATA = Path(__file__).parent / "data" / "ltfat_reference.npz"


@pytest.mark.skipif(not DATA.exists(), reason="LTFAT reference data not generated")
def test_against_ltfat_reference():
    import mbandwt
    from mbandwt import FilterBank

    ref = np.load(DATA)
    bank = FilterBank(list(ref["filters"]))
    r = mbandwt.dwt(ref["x"], bank, mode="periodic")
    for ours, theirs in zip(r.bands, ref["bands"]):
        matched = any(
            np.allclose(np.roll(ours, s), sgn * theirs, atol=1e-8)
            for sgn in (1.0, -1.0)
            for s in range(len(ours))
        )
        assert matched
