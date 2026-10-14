"""Regressions for public API validation and filter ownership."""

import numpy as np
import pytest

import mbandwt
from mbandwt.families import mlt


def test_bank_does_not_modify_or_alias_user_filters():
    original = np.array([1.0, 1.0]) / np.sqrt(2)
    original_copy = original.copy()
    bank = mbandwt.FilterBank([original, original[::-1]])
    assert original.flags.writeable
    original[0] = 999
    np.testing.assert_array_equal(bank.analysis[0], original_copy)
    with pytest.raises(ValueError):
        bank.analysis[0][0] = 123


@pytest.mark.parametrize("which", ["invalid", "", "Analysis"])
def test_frequency_response_bad_selector(which):
    with pytest.raises(ValueError, match="which"):
        mlt(3).frequency_response(which=which)


@pytest.mark.parametrize("n", [0, 1, -1, 1.5, True])
def test_frequency_response_bad_grid(n):
    with pytest.raises(ValueError, match="n must"):
        mlt(3).frequency_response(n=n)


@pytest.mark.parametrize("x", [np.array(2.0), np.array([])])
def test_multilevel_invalid_input(x):
    with pytest.raises(ValueError):
        mbandwt.wavedec(x, mlt(3))


@pytest.mark.parametrize("level", [0, -1, 2.5, True])
def test_multilevel_invalid_level(level):
    with pytest.raises((ValueError, TypeError)):
        mbandwt.wavedec(np.ones(90), mlt(3), level=level)


def test_invalid_axis():
    with pytest.raises(ValueError, match="axis"):
        mbandwt.dwt(np.ones(10), mlt(3), axis=2)
    with pytest.raises(ValueError, match="axis"):
        mbandwt.wavedec(np.ones(10), mlt(3), axis=-2)


def test_inverse_axis_must_match():
    c = mbandwt.dwt(np.ones((8, 30)), mlt(3), axis=1)
    with pytest.raises(ValueError, match="inverse axis"):
        mbandwt.idwt(c, axis=0)


def test_detail_levels_are_one_indexed():
    c = mbandwt.wavedec(np.ones(100), mlt(3), level=2)
    for args in [(0, None), (3, None), (1, 0), (1, 3)]:
        with pytest.raises(ValueError):
            c.detail(*args)


def test_paraunitary_bad_factor():
    from mbandwt.families import paraunitary_from_factors

    with pytest.raises(ValueError, match="M x M"):
        paraunitary_from_factors([np.ones(3)])
