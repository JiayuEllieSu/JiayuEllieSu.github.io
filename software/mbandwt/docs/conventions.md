# mbandwt mathematical conventions

This document fixes every convention used by the implementation: filtering
orientation, decimation phase, reconstruction phase, normalization, delay
handling, polyphase definitions, and finite-signal boundary semantics. All
code and all tests refer back to this document. Version: 0.1.0.

## 1. Signal and filter model

Signals are finite arrays `x[n]`, `n = 0 .. N-1`, real or complex, transformed
along one axis of an arbitrary-dimensional array. A filter bank consists of

* `M >= 2` analysis filters `h_k`, `k = 0 .. M-1` (`h_0` is the lowpass /
  approximation branch by convention), and
* `M` synthesis filters `g_k`.

Filters are finite 1-D arrays, indexed causally from 0, of possibly different
lengths. If no synthesis bank is given, `mbandwt` assumes an orthonormal bank
and sets `g_k[n] = conj(h_k[L_k - 1 - n])` (conjugate time reversal).

## 2. Analysis: convolve, then decimate at phase 0

Analysis is plain convolution followed by decimation on the grid `Mn`:

```
c_k[n] = (h_k * x)[M n] = sum_m h_k[m] x[M n - m]
```

The decimation phase is fixed at 0 (samples of the full convolution at
indices `0, M, 2M, ...`). This matches `scipy.signal.upfirdn(h, x, up=1,
down=M)` exactly, which is the low-level engine.

## 3. Synthesis: upsample, filter, sum

```
xt[i] = sum_k (g_k * up_M(c_k))[i],    up_M(c)[Mn] = c[n], 0 otherwise
```

For a perfect-reconstruction (PR) bank the alias terms cancel and the
composite system is a pure scaled delay,

```
xt[i] = c * x[i - d]
```

with **gain** `c` and **delay** `d` determined by the distortion transfer
function `T(z) = (1/M) * sum_k G_k(z) H_k(z) = c z^{-d}`. `mbandwt` computes
`t = (1/M) * sum_k conv(g_k, h_k)` once per bank, takes `d = argmax |t|`,
`c = t[d]`, and the inverse transform **always compensates** the delay and
gain. Users therefore never see the internal delay: for PR banks,
`idwt(dwt(x)) == x` to numerical precision.

## 4. Polyphase representation

Type-I analysis polyphase decomposition (Vaidyanathan, *Multirate Systems and
Filter Banks*, 1993):

```
H_k(z) = sum_{j=0}^{M-1} z^{-j} E_{kj}(z^M),      E_{kj}[n] = h_k[M n + j]
```

Type-II synthesis polyphase decomposition:

```
G_k(z) = sum_{j=0}^{M-1} z^{-(M-1-j)} R_{jk}(z^M), R_{jk}[n] = g_k[M n + M-1-j]
```

The bank is PR if and only if the polynomial matrix product is a scaled
monomial times the identity:

```
P(z) = R(z) E(z) = c z^{-k0} I
```

in which case the overall sample-domain delay is

```
d = M * k0 + (M - 1)
```

`mbandwt` computes `P(z)` by exact polynomial-matrix multiplication and
reports the maximum relative residual `|P - c z^{-k0} I| / |c|`. The delay
implied by the polyphase test is cross-checked against the operational delay
measured by passing a unit impulse through the full periodic
analysis/synthesis chain; the test suite asserts the two agree for every
shipped bank.

A bank is **orthonormal** if its periodic analysis operator `A` (Section 5)
satisfies `A A^H = I`; **biorthogonal** means PR but not orthonormal.

## 5. Periodic mode (`mode="periodic"`)

Circular convolution is implemented through the folding identity: the
circular convolution of period `N` equals the linear convolution folded
modulo `N`,

```
(h (*) x)[i] = sum_{j == i (mod N)} (h * x)[j]
```

Analysis: fold the full linear convolution to length `N`, then decimate
`[::M]`. Synthesis: sum the per-band linear syntheses, fold to length `N`,
circularly shift by `-d`, divide by `c`. This is exact for arbitrary filter
lengths, including filters longer than the signal.

Periodic mode requires `M | N`. If `N` is not a multiple of `M`, the signal
is first extended **periodically** on the right by `P = (-N) mod M` samples
(indices taken modulo `N`), the padded length `N + P` is transformed, and the
reconstruction is cropped back to `N`. The pad amount is recorded in the
coefficient metadata, so reconstruction is exact for every `N`.

Periodic mode is critically sampled (non-expansive): the total number of
coefficients equals the padded signal length.

## 6. Finite-extension modes (`zero`, `symmetric`, `reflect`, `constant`)

Version 0.1 makes a deliberate design choice: finite-extension modes are
implemented as **expansive transforms with exact reconstruction** for
arbitrary filters and arbitrary `M`.

* `zero`: the signal is treated as zero outside `[0, N-1]`; analysis is the
  full linear convolution decimated at phase 0, with per-band length
  `ceil((N + L_k - 1) / M)`. This keeps every nonzero sample of the
  decimated convolution, so synthesis followed by cropping `[d : d+N]` and
  gain division reconstructs exactly (the composite is `c x[i-d]`).
* `symmetric`, `reflect`, `constant`: the signal is first extended by
  `E = L_max - 1` samples on each side using index maps
  (half-sample symmetry with period `2N`; whole-sample reflection with
  period `2N-2`; edge replication), then transformed in `zero` mode. The
  reconstruction recovers the extended signal exactly and crops the center
  `[E : E+N]`.

Consequences: reconstruction is exact to machine precision for **every** PR
bank and **every** mode, at the price of extra boundary coefficients in the
finite-extension modes. Non-expansive symmetric boundary handling (which
requires linear-phase filter structure) is future work and will be an
additional mode, not a change to these semantics.

Extension-mode index maps, for extended index `i` in `[-E, N-1+E]`:

* `periodic`:  `i mod N`
* `symmetric`: `j = i mod 2N`; use `j` if `j < N` else `2N-1-j`
  (so `x[-1] = x[0]`, `x[N] = x[N-1]`)
* `reflect`:   `j = i mod (2N-2)`; use `j` if `j < N` else `2N-2-j`
  (so `x[-1] = x[1]`, `x[N] = x[N-2]`; degenerates to `constant` for `N = 1`)
* `constant`:  `clip(i, 0, N-1)` (edge replication, PyWavelets' "constant")
* `zero`:      out-of-range samples are 0

## 7. Multilevel transforms

`wavedec` recursively decomposes only band 0 (ordinary multiresolution
analysis). Each level records its own metadata (input length, pad or
extension amount, mode, work length), so `waverec` inverts level by level
with exact bookkeeping. Detail bands are stored finest-first internally;
`MBandCoefficients.to_list()` returns the PyWavelets-style coarse-first
ordering `[A_J, [D_J,1..M-1], ..., [D_1,1..M-1]]`.

The default maximum level is `floor( log(N / (L_max - 1)) / log(M) )`
(with the natural degenerate cases), analogous to PyWavelets' rule.

## 8. Normalization

No normalization is imposed on user filters. Built-in orthonormal families
have unit-gain composite response (`c = 1`); the Daubechies scaling filters
satisfy `sum h = sqrt(2)` and `||h|| = 1`. The transform never rescales
coefficients; gain compensation happens once, in synthesis.

## 9. Complex filters and signals

All engine operations are linear over the complex numbers. Auto-generated
synthesis banks use conjugate time reversal; orthonormality is tested with
the conjugate transpose (`A A^H`).

## 10. Relation to PyWavelets conventions

For `M = 2` orthonormal wavelets, `mbandwt`'s analysis filters correspond to
PyWavelets' `dec_lo` / `dec_hi` used in convolution. Coefficients in
`mode="periodic"` agree with PyWavelets `mode="periodization"` up to a fixed
sub-sample alignment offset: a circular shift of the **input** by
`r` in `{0, ..., M-1}` samples combined with a circular shift of the
coefficient arrays (and a possible sign flip of the detail band). The two
conventions' decimation grids can differ by a number of samples that is not
a multiple of `M` (Haar is such a case), which no coefficient-domain shift
alone can absorb. The regression suite verifies this equivalence explicitly.
