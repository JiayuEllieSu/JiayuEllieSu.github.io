import numpy as np
import pytest

from mbandwt import FilterBank
from mbandwt.families import block_dct, daubechies, haar, lazy, mlt


def test_m_inferred_and_auto_synthesis():
    h0 = np.array([1.0, 1.0]) / np.sqrt(2)
    h1 = np.array([-1.0, 1.0]) / np.sqrt(2)
    bank = FilterBank([h0, h1])
    assert bank.M == 2
    # auto synthesis = conjugate time reversal
    assert np.allclose(bank.synthesis[0], h0[::-1])
    assert np.allclose(bank.synthesis[1], h1[::-1])
    assert bank.is_pr() and bank.is_orthogonal()


def test_construction_errors():
    with pytest.raises(ValueError):
        FilterBank([[1.0, 1.0]])  # M < 2
    with pytest.raises(ValueError):
        FilterBank([[1.0], [1.0]], synthesis=[[1.0]])  # count mismatch
    with pytest.raises(ValueError):
        FilterBank([np.ones((2, 2)), np.ones(2)])  # non-1D
    with pytest.raises(ValueError):
        FilterBank([[np.nan, 1.0], [1.0, 0.0]])  # non-finite


def test_metadata_and_repr():
    bank = mlt(3)
    assert bank.name == "mlt3"
    assert "Malvar" in bank.reference
    assert "mlt3" in repr(bank)
    assert bank.filter_lengths["analysis"] == (6, 6, 6)


def test_signature_stable_and_distinct():
    assert mlt(3).signature == mlt(3).signature
    assert mlt(3).signature != mlt(4).signature
    assert daubechies(2).signature != daubechies(3).signature


def test_filters_read_only():
    bank = haar()
    with pytest.raises((ValueError, RuntimeError)):
        bank.analysis[0][0] = 0.0


def test_gain_and_delay_orthonormal():
    for bank in [haar(), daubechies(3), block_dct(4), mlt(5), lazy(3)]:
        assert np.isclose(bank.gain, 1.0)
        assert bank.delay >= 0


def test_lazy_delay_is_M_minus_1():
    for M in [2, 3, 5, 8]:
        assert lazy(M).delay == M - 1


@pytest.mark.parametrize("p", [1, 2, 3, 4, 6])
def test_daubechies_vanishing_moments(p):
    vm = daubechies(p).vanishing_moments()
    assert vm[0] == 0  # lowpass has nonzero DC gain
    assert vm[1] == p  # detail branch annihilates degree < p


def test_frequency_response_shapes_and_dc():
    bank = mlt(4)
    w, H = bank.frequency_response(n=128)
    assert w.shape == (128,) and H.shape == (4, 128)
    # lowpass has the largest DC response
    assert np.argmax(np.abs(H[:, 0])) == 0


def test_complex_bank_supported():
    # complex orthonormal block bank: unitary DFT rows
    M = 3
    F = np.exp(-2j * np.pi * np.outer(np.arange(M), np.arange(M)) / M) / np.sqrt(M)
    bank = FilterBank([F[k] for k in range(M)], name="dft3")
    assert bank.is_complex
    assert bank.is_pr() and bank.is_orthogonal()
