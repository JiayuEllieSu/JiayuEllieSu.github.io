"""Validation-layer tests.

Includes an independent naive reference implementation of the transform
conventions (direct index arithmetic, no upfirdn, no folding trick) and
cross-checks the fast engine against it for M = 2, 3, 5 — an internal
"second implementation" oracle complementing the external PyWavelets
regression (see docs/conventions.md Sections 2, 3, 5).
"""

import numpy as np
import pytest

import mbandwt
from mbandwt import FilterBank
from mbandwt.families import daubechies, mlt, random_paraunitary
from mbandwt.transform import _analyze_periodic, _analyze_zero

RNG = np.random.default_rng(123)


# ----------------------------------------------------------------------
# naive reference implementations of the documented conventions
# ----------------------------------------------------------------------
def naive_zero_band(x, h, M):
    N, L = len(x), len(h)
    Nc = -((N + L - 1) // -M)  # ceil
    c = np.zeros(Nc, dtype=np.result_type(x, h))
    for n in range(Nc):
        acc = 0.0
        for m in range(L):
            i = M * n - m
            if 0 <= i < N:
                acc += h[m] * x[i]
        c[n] = acc
    return c


def naive_periodic_band(x, h, M):
    N = len(x)
    assert N % M == 0
    c = np.zeros(N // M, dtype=np.result_type(x, h))
    for n in range(N // M):
        acc = 0.0
        for m in range(len(h)):
            acc += h[m] * x[(M * n - m) % N]
        c[n] = acc
    return c


@pytest.mark.parametrize(
    "bank", [daubechies(3), mlt(3), random_paraunitary(5, 2, seed=1)],
    ids=lambda b: b.name,
)
def test_engine_matches_naive_zero(bank):
    x = RNG.standard_normal(40)
    fast = _analyze_zero(x, bank.analysis, bank.M)
    for h, f in zip(bank.analysis, fast):
        assert np.allclose(f, naive_zero_band(x, h, bank.M), atol=1e-12)


@pytest.mark.parametrize(
    "bank", [daubechies(2), mlt(3), random_paraunitary(5, 1, seed=2)],
    ids=lambda b: b.name,
)
def test_engine_matches_naive_periodic(bank):
    N = bank.M * 12
    x = RNG.standard_normal(N)
    fast = _analyze_periodic(x, bank.analysis, bank.M)
    for h, f in zip(bank.analysis, fast):
        assert np.allclose(f, naive_periodic_band(x, h, bank.M), atol=1e-12)


def test_periodic_with_filter_longer_than_signal_matches_naive():
    bank = mlt(4)  # filters length 8
    x = RNG.standard_normal(4)
    fast = _analyze_periodic(x, bank.analysis, bank.M)
    for h, f in zip(bank.analysis, fast):
        assert np.allclose(f, naive_periodic_band(x, h, bank.M), atol=1e-12)


# ----------------------------------------------------------------------
# validation reports
# ----------------------------------------------------------------------
def test_report_orthonormal():
    rep = mbandwt.validate(mlt(3))
    assert rep.perfect_reconstruction and rep.orthogonal and not rep.biorthogonal
    assert rep.delay_consistent
    assert rep.classification == "orthonormal"
    s = str(rep)
    assert "Perfect reconstruction:     True" in s
    assert "Classification:             orthonormal" in s


def test_report_biorthogonal():
    # simple hand-made biorthogonal M = 2 bank (PR, not orthonormal)
    a = 2.0
    analysis = [np.array([a]), np.array([0.0, 1.0])]
    synthesis = [np.array([0.0, 1.0 / a]), np.array([1.0, 0.0])]
    bank = FilterBank(analysis, synthesis, name="toy-bior")
    rep = mbandwt.validate(bank)
    assert rep.perfect_reconstruction
    assert not rep.orthogonal and rep.biorthogonal
    assert rep.classification == "biorthogonal"
    x = RNG.standard_normal(20)
    assert np.allclose(mbandwt.idwt(mbandwt.dwt(x, bank)), x)


def test_report_broken():
    h = [np.array([1.0, 0.3]), np.array([0.2, -1.0])]
    bank = FilterBank(h, [np.array([1.0]), np.array([1.0])])
    rep = mbandwt.validate(bank)
    assert not rep.perfect_reconstruction
    assert rep.classification == "not perfect-reconstruction"


def test_orthonormality_residual_magnitudes():
    assert mlt(5).orthogonality_residual() < 1e-13
    assert daubechies(6).orthogonality_residual() < 1e-12
