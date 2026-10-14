import math

import numpy as np
import pytest

import mbandwt
from mbandwt.boundary import MODES
from mbandwt.families import (
    block_dct,
    daubechies,
    haar,
    lazy,
    mlt,
    random_paraunitary,
)

RNG = np.random.default_rng(42)

BANKS = [
    haar(),
    daubechies(2),
    daubechies(4),
    block_dct(3),
    block_dct(5),
    mlt(2),
    mlt(3),
    mlt(4),
    mlt(5),
    mlt(8),
    lazy(4),
    random_paraunitary(3, 3, seed=0),
    random_paraunitary(5, 2, seed=1),
    random_paraunitary(8, 1, seed=2),
]


def rel(a, b):
    return np.linalg.norm(np.ravel(a - b)) / np.linalg.norm(np.ravel(a))


@pytest.mark.parametrize("bank", BANKS, ids=lambda b: b.name)
@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("N", [5, 37, 64, 200])
def test_roundtrip_exact(bank, mode, N):
    x = RNG.standard_normal(N)
    r = mbandwt.dwt(x, bank, mode=mode)
    xr = mbandwt.idwt(r)
    assert rel(x, xr) < 1e-10


def test_periodic_is_critically_sampled():
    bank = mlt(3)
    for N in [30, 31, 32]:
        r = mbandwt.dwt(np.zeros(N), bank, mode="periodic")
        Nw = M_ceil = bank.M * math.ceil(N / bank.M)
        assert sum(b.shape[-1] for b in r.bands) == Nw
        assert r.meta["pad"] == Nw - N


def test_zero_mode_band_lengths():
    bank = daubechies(3)  # L = 6, M = 2
    N = 50
    r = mbandwt.dwt(np.zeros(N), bank, mode="zero")
    expected = math.ceil((N + 6 - 1) / 2)
    for b in r.bands:
        assert b.shape[-1] == expected


@pytest.mark.parametrize(
    "bank", [haar(), mlt(3), block_dct(4), random_paraunitary(5, 2, seed=3)],
    ids=lambda b: b.name,
)
def test_energy_preservation_orthonormal(bank):
    N = bank.M * 40
    x = RNG.standard_normal(N)
    r = mbandwt.dwt(x, bank, mode="periodic")
    ex = np.sum(x**2)
    ec = sum(np.sum(np.abs(b) ** 2) for b in r.bands)
    assert abs(ex - ec) / ex < 1e-12


def test_complex_signal_roundtrip():
    bank = mlt(3)
    x = RNG.standard_normal(90) + 1j * RNG.standard_normal(90)
    for mode in MODES:
        xr = mbandwt.idwt(mbandwt.dwt(x, bank, mode=mode))
        assert rel(x, xr) < 1e-10


def test_complex_bank_roundtrip():
    M = 4
    F = np.exp(-2j * np.pi * np.outer(np.arange(M), np.arange(M)) / M) / np.sqrt(M)
    bank = mbandwt.FilterBank([F[k] for k in range(M)], name="dft4")
    x = RNG.standard_normal(41)
    xr = mbandwt.idwt(mbandwt.dwt(x, bank, mode="periodic"))
    assert rel(x, xr) < 1e-10


@pytest.mark.parametrize("axis", [0, 1, -1])
def test_batched_and_axis(axis):
    bank = mlt(3)
    x = RNG.standard_normal((4, 33, 2))
    r = mbandwt.dwt(x, bank, mode="symmetric", axis=axis)
    xr = mbandwt.idwt(r)
    assert xr.shape == x.shape
    assert rel(x, xr) < 1e-10
    # symmetric mode: work length = N + 2*(L-1), band length = ceil((work + L - 1)/M)
    N, L, M = x.shape[axis], 6, 3
    expected = math.ceil((N + 2 * (L - 1) + L - 1) / M)
    assert r.bands[0].shape[axis] == expected
    untouched = [s for i, s in enumerate(x.shape) if i != axis % x.ndim]
    got = [s for i, s in enumerate(r.bands[0].shape) if i != axis % x.ndim]
    assert untouched == got


def test_batch_matches_loop():
    bank = daubechies(2)
    x = RNG.standard_normal((3, 40))
    r = mbandwt.dwt(x, bank, mode="periodic", axis=-1)
    for i in range(3):
        ri = mbandwt.dwt(x[i], bank, mode="periodic")
        for b, bi in zip(r.bands, ri.bands):
            assert np.allclose(b[i], bi)


def test_result_object_interface():
    bank = block_dct(3)
    x = RNG.standard_normal(30)
    r = mbandwt.dwt(x, bank)
    assert len(r) == 3
    assert r[0] is r.approx
    assert len(r.details) == 2
    assert [b.shape for b in r] == r.band_shapes()
    assert r.original_length == 30
    assert "DWTResult" in repr(r)


def test_idwt_bank_mismatch_raises():
    x = RNG.standard_normal(30)
    r = mbandwt.dwt(x, mlt(3))
    with pytest.raises(ValueError):
        mbandwt.idwt(r, bank=block_dct(3))


def test_invalid_mode_and_inputs():
    with pytest.raises(ValueError):
        mbandwt.dwt(np.zeros(10), mlt(2), mode="nonsense")
    with pytest.raises(TypeError):
        mbandwt.dwt(np.zeros(10), "not a bank")
    with pytest.raises(ValueError):
        mbandwt.dwt(np.zeros(0), mlt(2))


def test_filters_longer_than_signal():
    bank = mlt(8)  # filter length 16
    for mode in MODES:
        x = RNG.standard_normal(5)
        xr = mbandwt.idwt(mbandwt.dwt(x, bank, mode=mode))
        assert rel(x, xr) < 1e-10


def test_float32_input_roundtrip():
    bank = haar()
    x = RNG.standard_normal(64).astype(np.float32)
    xr = mbandwt.idwt(mbandwt.dwt(x, bank))
    assert rel(x.astype(np.float64), xr) < 1e-5
