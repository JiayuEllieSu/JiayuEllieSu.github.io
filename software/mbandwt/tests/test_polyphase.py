import numpy as np
import pytest

from mbandwt import polyphase as pp
from mbandwt.families import block_dct, daubechies, haar, lazy, mlt, random_paraunitary
from mbandwt.validation import _operational_pr


def test_analysis_polyphase_definition():
    h0 = np.arange(1.0, 8.0)  # length 7, M = 3
    h1 = np.arange(10.0, 13.0)
    h2 = np.arange(20.0, 26.0)
    E = pp.analysis_polyphase([h0, h1, h2], 3)
    assert E.shape == (3, 3, 3)
    # E[k, j, n] = h_k[3n + j]
    assert np.allclose(E[0, 0], [1, 4, 7])
    assert np.allclose(E[0, 1], [2, 5, 0])
    assert np.allclose(E[2, 2], [22, 25, 0])


def test_synthesis_polyphase_definition():
    g0 = np.arange(1.0, 7.0)  # M = 2
    g1 = np.arange(10.0, 14.0)
    R = pp.synthesis_polyphase([g0, g1], 2)
    # R[j, k, n] = g_k[2n + 1 - j]
    assert np.allclose(R[0, 0], [2, 4, 6])
    assert np.allclose(R[1, 0], [1, 3, 5])
    assert np.allclose(R[0, 1], [11, 13, 0])


def test_filters_from_polyphase_inverse():
    bank = mlt(4)
    E = bank.polyphase_analysis()
    rebuilt = pp.filters_from_analysis_polyphase(E)
    for h, r in zip(bank.analysis, rebuilt):
        assert np.allclose(np.pad(h, (0, len(r) - len(h))), r)


def test_lazy_polyphase_is_identity():
    bank = lazy(4)
    E = bank.polyphase_analysis()
    R = bank.polyphase_synthesis()
    assert np.allclose(E[:, :, 0], np.eye(4)) and E.shape[2] == 1
    P = pp.polyphase_product(R, E)
    assert np.allclose(P[:, :, 0], np.eye(4))


@pytest.mark.parametrize(
    "bank",
    [haar(), daubechies(4), block_dct(5), mlt(3), mlt(8),
     random_paraunitary(3, 2, seed=9), random_paraunitary(7, 1, seed=10)],
    ids=lambda b: b.name,
)
def test_pr_product_is_monomial_identity(bank):
    rep = bank.pr_report()
    assert rep["pr"]
    assert rep["residual"] < 1e-12
    assert np.isclose(abs(rep["gain"]), 1.0)


@pytest.mark.parametrize(
    "bank",
    [haar(), daubechies(2), daubechies(5), block_dct(3), mlt(2), mlt(5), lazy(6),
     random_paraunitary(4, 3, seed=11)],
    ids=lambda b: b.name,
)
def test_polyphase_delay_matches_operational_delay(bank):
    """The delay implied by R(z)E(z) = c z^{-k0} I (d = M*k0 + M - 1) must
    equal the delay measured by an impulse through the full periodic chain."""
    rep = bank.pr_report()
    j0, val, residual = _operational_pr(bank)
    assert residual < 1e-12
    assert j0 == rep["delay"]
    assert np.isclose(val, rep["gain"])


def test_broken_bank_detected():
    bank = mlt(3)
    bad = [np.array(h) for h in bank.analysis]
    bad[1][2] += 0.05
    from mbandwt import FilterBank

    broken = FilterBank(bad, list(bank.synthesis))
    assert not broken.is_pr()
    assert broken.pr_report()["residual"] > 1e-3


def test_polyphase_shape_errors():
    with pytest.raises(ValueError):
        pp.polyphase_product(np.zeros((2, 3, 1)), np.zeros((3, 3, 1)))
    with pytest.raises(ValueError):
        pp.filters_from_analysis_polyphase(np.zeros((2, 3, 1)))
