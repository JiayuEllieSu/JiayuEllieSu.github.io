"""External regression: the general M-band engine must reduce correctly to
the ordinary dyadic case, with PyWavelets as the independent oracle."""

import numpy as np
import pytest

pywt = pytest.importorskip("pywt")

import mbandwt
from mbandwt.families import daubechies, from_pywt

RNG = np.random.default_rng(2024)


def _matches_up_to_circular_shift(a, b, atol=1e-10):
    """True if b == roll(a, s) or b == -roll(a, s) for some shift s."""
    if a.shape != b.shape:
        return False
    for sign in (1.0, -1.0):
        for s in range(len(a)):
            if np.allclose(np.roll(a, s), sign * b, atol=atol):
                return True
    return False


@pytest.mark.parametrize("p", [1, 2, 3, 4, 5, 8])
def test_daubechies_coefficients_match_pywt(p):
    ours = daubechies(p)
    w = pywt.Wavelet(f"db{p}")
    assert np.allclose(ours.analysis[0], w.dec_lo, atol=1e-12)
    assert np.allclose(ours.synthesis[0], w.rec_lo, atol=1e-12)
    # detail filter matches up to overall sign (QMF sign convention)
    hi = np.asarray(w.dec_hi)
    assert np.allclose(ours.analysis[1], hi, atol=1e-12) or np.allclose(
        ours.analysis[1], -hi, atol=1e-12
    )


def test_db2_closed_form():
    s3 = np.sqrt(3.0)
    ref = np.array([1 + s3, 3 + s3, 3 - s3, 1 - s3]) / (4 * np.sqrt(2.0))
    assert np.allclose(daubechies(2).synthesis[0], ref, atol=1e-12)


@pytest.mark.parametrize("name", ["haar", "db2", "db4", "sym3"])
def test_periodized_transform_shift_equivalence(name):
    """mbandwt mode='periodic' coefficients equal PyWavelets
    mode='periodization' up to a fixed sub-sample alignment: a circular
    shift of the *input* by r in {0, .., M-1} samples combined with a
    circular shift of the coefficient arrays (and sign on the detail
    band). The decimation grids of the two conventions can differ by a
    non-multiple of M, which no coefficient-domain shift alone can absorb
    (docs/conventions.md, Section 10)."""
    bank = from_pywt(name)
    N = 64
    x = RNG.standard_normal(N)
    ours = mbandwt.dwt(x, bank, mode="periodic")
    for r in range(bank.M):
        cA, cD = pywt.dwt(np.roll(x, r), name, mode="periodization")
        if _matches_up_to_circular_shift(ours[0], cA) and _matches_up_to_circular_shift(
            ours[1], cD
        ):
            return
    raise AssertionError(f"no sub-sample alignment matches PyWavelets for {name}")


@pytest.mark.parametrize("name", ["db3", "sym4", "coif2", "bior2.2", "bior3.5"])
def test_bridged_wavelets_are_pr(name):
    bank = from_pywt(name)
    rep = bank.validate()
    assert rep.perfect_reconstruction, name
    x = RNG.standard_normal(100)
    for mode in ["periodic", "zero", "symmetric"]:
        xr = mbandwt.idwt(mbandwt.dwt(x, bank, mode=mode))
        assert np.linalg.norm(x - xr) / np.linalg.norm(x) < 1e-10


def test_bior_classified_biorthogonal():
    bank = from_pywt("bior2.2")
    rep = bank.validate()
    assert rep.biorthogonal and not rep.orthogonal


def test_orthogonal_pywt_classified_orthonormal():
    assert from_pywt("db4").validate().orthogonal


def test_multilevel_roundtrip_pywt_bridge():
    bank = from_pywt("sym5")
    x = RNG.standard_normal(300)
    c = mbandwt.wavedec(x, bank, level=3, mode="symmetric")
    assert np.allclose(mbandwt.waverec(c), x)
