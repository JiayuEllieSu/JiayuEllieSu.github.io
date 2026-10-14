import numpy as np
import pytest

import mbandwt
from mbandwt.families import block_dct, daubechies, mlt, random_paraunitary

RNG = np.random.default_rng(7)


def rel(a, b):
    return np.linalg.norm(np.ravel(a - b)) / np.linalg.norm(np.ravel(a))


@pytest.mark.parametrize(
    "bank",
    [daubechies(3), mlt(3), block_dct(4), random_paraunitary(5, 2, seed=5)],
    ids=lambda b: b.name,
)
@pytest.mark.parametrize("mode", ["periodic", "zero", "symmetric"])
@pytest.mark.parametrize("level", [1, 2, 3])
def test_multilevel_roundtrip(bank, mode, level):
    x = RNG.standard_normal(400)
    c = mbandwt.wavedec(x, bank, level=level, mode=mode)
    xr = mbandwt.waverec(c)
    assert xr.shape == x.shape
    assert rel(x, xr) < 1e-10


def test_structure_and_ordering():
    bank = mlt(3)
    x = RNG.standard_normal(270)
    c = mbandwt.wavedec(x, bank, level=3, mode="periodic")
    assert c.level == 3 and c.M == 3
    assert len(c.details) == 3
    assert all(len(d) == 2 for d in c.details)
    # periodic: level-1 details have length 270/3, level-2 have 270/9, ...
    assert c.details[0][0].shape[-1] == 90
    assert c.details[1][0].shape[-1] == 30
    assert c.details[2][0].shape[-1] == 10
    assert c.approx.shape[-1] == 10
    # to_list is coarse-first
    lst = c.to_list()
    assert lst[0] is c.approx
    assert lst[1][0] is c.details[2][0]
    assert lst[-1][0] is c.details[0][0]
    # detail() accessor (1-indexed)
    assert c.detail(1, 1) is c.details[0][0]
    energies = c.band_energies()
    assert "approx" in energies and "D3,2" in energies


def test_default_level_is_max_level():
    bank = daubechies(2)  # L = 4, M = 2
    N = 512
    ml = mbandwt.max_level(N, bank)
    assert ml == 7  # floor(log2(512/3))
    c = mbandwt.wavedec(RNG.standard_normal(N), bank)
    assert c.level == ml


def test_excess_level_warns_but_reconstructs():
    bank = daubechies(2)
    x = RNG.standard_normal(64)
    with pytest.warns(UserWarning):
        c = mbandwt.wavedec(x, bank, level=6, mode="periodic")
    assert rel(x, mbandwt.waverec(c)) < 1e-10


def test_batched_multilevel_axis0():
    bank = block_dct(3)
    x = RNG.standard_normal((100, 5))
    c = mbandwt.wavedec(x, bank, level=2, mode="reflect", axis=0)
    xr = mbandwt.waverec(c)
    assert xr.shape == x.shape
    assert rel(x, xr) < 1e-10


def test_waverec_bank_default_and_override():
    bank = mlt(4)
    x = RNG.standard_normal(160)
    c = mbandwt.wavedec(x, bank, level=2)
    assert rel(x, mbandwt.waverec(c)) < 1e-10
    assert rel(x, mbandwt.waverec(c, bank=mlt(4))) < 1e-10  # same signature
    with pytest.raises(ValueError):
        mbandwt.waverec(c, bank=mlt(5))


def test_energy_preserved_multilevel_orthonormal():
    bank = mlt(3)
    x = RNG.standard_normal(243)
    c = mbandwt.wavedec(x, bank, level=4, mode="periodic")
    total = sum(c.band_energies().values())
    assert abs(total - np.sum(x**2)) / np.sum(x**2) < 1e-12


def test_level_validation():
    bank = mlt(2)
    with pytest.raises(ValueError):
        mbandwt.wavedec(RNG.standard_normal(32), bank, level=0)
    with pytest.raises(TypeError):
        mbandwt.waverec([1, 2, 3])
