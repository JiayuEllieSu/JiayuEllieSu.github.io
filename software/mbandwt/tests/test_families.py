import numpy as np
import pytest

from mbandwt.families import (
    block_dct,
    daubechies,
    haar,
    lazy,
    mlt,
    paraunitary_from_factors,
    random_paraunitary,
)


def test_haar_is_db1():
    assert np.allclose(haar().analysis[0], daubechies(1).analysis[0])
    assert np.allclose(haar().analysis[0], np.array([1.0, 1.0]) / np.sqrt(2))


@pytest.mark.parametrize("p", [2, 3, 5, 7, 10])
def test_daubechies_properties(p):
    bank = daubechies(p)
    h0 = bank.synthesis[0]
    assert len(h0) == 2 * p
    assert np.isclose(h0.sum(), np.sqrt(2.0))
    assert np.isclose(np.sum(h0**2), 1.0)
    assert bank.is_orthogonal()


@pytest.mark.parametrize("M", [2, 3, 4, 5, 8, 11])
def test_block_dct_orthonormal(M):
    bank = block_dct(M)
    assert all(len(h) == M for h in bank.analysis)
    assert bank.is_orthogonal()


@pytest.mark.parametrize("M", [2, 3, 4, 5, 6, 8, 12])
def test_mlt_orthonormal_arbitrary_M(M):
    bank = mlt(M)
    assert all(len(h) == 2 * M for h in bank.analysis)
    assert bank.is_orthogonal()
    assert bank.validate().delay_consistent


@pytest.mark.parametrize("M", [2, 4, 7])
def test_lazy_orthonormal(M):
    assert lazy(M).is_orthogonal()


def test_random_paraunitary_deterministic_and_orthonormal():
    a = random_paraunitary(5, 3, seed=99)
    b = random_paraunitary(5, 3, seed=99)
    assert a.signature == b.signature
    assert a.is_orthogonal()
    assert all(len(h) == 5 * 4 for h in a.analysis)


def test_paraunitary_from_factors_rejects_non_unitary():
    with pytest.raises(ValueError):
        paraunitary_from_factors([np.ones((3, 3))])
    with pytest.raises(ValueError):
        paraunitary_from_factors([])


def test_paraunitary_from_explicit_rotations():
    th = 0.3
    V0 = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    V1 = np.eye(2)
    bank = paraunitary_from_factors([V0, V1])
    assert bank.is_orthogonal()


def test_provenance_present_everywhere():
    for bank in [haar(), daubechies(3), block_dct(3), mlt(4), lazy(3),
                 random_paraunitary(3, 1, seed=0)]:
        assert bank.reference and bank.family and bank.name


def test_invalid_M():
    for ctor in [block_dct, mlt, lazy]:
        with pytest.raises(ValueError):
            ctor(1)
    with pytest.raises(ValueError):
        random_paraunitary(1)
