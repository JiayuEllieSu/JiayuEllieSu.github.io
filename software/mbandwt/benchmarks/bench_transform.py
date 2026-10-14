"""Objective benchmarks: forward/inverse runtime and reconstruction error
across signal lengths, M, and levels; internal naive-convolution vs
upfirdn-engine comparison; optional PyWavelets column at M = 2.

Run:  python benchmarks/bench_transform.py
"""

import time

import numpy as np

import mbandwt
from mbandwt.families import daubechies, mlt

RNG = np.random.default_rng(0)


def timeit(fn, repeats=5):
    best = np.inf
    for _ in range(repeats):
        t0 = time.perf_counter()
        out = fn()
        best = min(best, time.perf_counter() - t0)
    return best, out


def naive_dwt_periodic(x, bank):
    """Direct index-arithmetic reference (also used by the test suite)."""
    N, M = len(x), bank.M
    out = []
    for h in bank.analysis:
        c = np.zeros(N // M)
        for n in range(N // M):
            acc = 0.0
            for m in range(len(h)):
                acc += h[m] * x[(M * n - m) % N]
            c[n] = acc
        out.append(c)
    return out


def main():
    print(f"{'bank':>8} {'N':>8} {'level':>5} {'fwd (ms)':>9} {'inv (ms)':>9} "
          f"{'rel err':>9}")
    for M, mk in [(2, lambda: daubechies(4)), (3, lambda: mlt(3)),
                  (4, lambda: mlt(4)), (8, lambda: mlt(8))]:
        bank = mk()
        for logN in [12, 14, 16, 18]:
            N = 2**logN
            x = RNG.standard_normal(N)
            level = min(4, mbandwt.max_level(N, bank))
            tf, c = timeit(lambda: mbandwt.wavedec(x, bank, level=level))
            ti, xr = timeit(lambda: mbandwt.waverec(c))
            err = np.linalg.norm(x - xr) / np.linalg.norm(x)
            print(f"{bank.name:>8} {N:>8} {level:>5} {tf * 1e3:>9.2f} "
                  f"{ti * 1e3:>9.2f} {err:>9.1e}")

    print("\nengine vs naive convolution (one level, periodic):")
    bank = mlt(4)
    for N in [2**10, 2**12]:
        x = RNG.standard_normal(N)
        t_fast, _ = timeit(lambda: mbandwt.dwt(x, bank), repeats=3)
        t_naive, _ = timeit(lambda: naive_dwt_periodic(x, bank), repeats=1)
        print(f"  N={N:>6}: engine {t_fast * 1e3:8.2f} ms   "
              f"naive {t_naive * 1e3:8.2f} ms   speedup {t_naive / t_fast:6.1f}x")

    try:
        import pywt

        print("\nM = 2 sanity vs PyWavelets (not a performance claim):")
        bank = daubechies(4)
        for N in [2**14, 2**16]:
            x = RNG.standard_normal(N)
            t_ours, _ = timeit(lambda: mbandwt.wavedec(x, bank, level=4))
            t_pywt, _ = timeit(
                lambda: pywt.wavedec(x, "db4", level=4, mode="periodization")
            )
            print(f"  N={N:>6}: mbandwt {t_ours * 1e3:8.2f} ms   "
                  f"pywt {t_pywt * 1e3:8.2f} ms")
    except ImportError:
        print("\n(PyWavelets not installed; skipping M = 2 comparison)")


if __name__ == "__main__":
    main()
