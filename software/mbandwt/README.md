# mbandwt

**M-band discrete wavelet transforms and FIR filter-bank analysis in Python.**

`mbandwt` is a small, experimental NumPy/SciPy package for working with
critically sampled, finite-length, M-channel filter banks. Unlike a standard
two-channel DWT, the number of subbands `M` is configurable.

The package provides one-level and multilevel transforms, inverse transforms,
filter-bank construction, polyphase representations, and numerical
perfect-reconstruction diagnostics. It is intended for learning,
experimentation, and research prototypes.

> **Status:** Early open-source release (v0.1.0). The public API may change.
> The package has automated tests, but has not undergone an independent
> software audit. This is a source-code release, not a PyPI package or a paper.

## Requirements and installation

- Python 3.9 or newer
- NumPy and SciPy
- Optional: PyWavelets for cross-checking, matplotlib for plotting

Download/clone the project source, change into the `mbandwt` directory, then:

```bash
python -m pip install -e .
```

To run the included tests:

```bash
python -m pip install -e ".[test]"
python -m pytest -q
```

For plotting helpers, install `.[plot]`. Nothing is uploaded or executed
remotely by the library.

## Quickstart

```python
import numpy as np
import mbandwt
from mbandwt.families import mlt

bank = mlt(3)                  # three-channel lapped transform bank
print(bank.validate())        # numerical/algebraic diagnostics

x = np.random.default_rng(0).standard_normal(486)
coeffs = mbandwt.wavedec(x, bank, level=4, mode="periodic")
x_reconstructed = mbandwt.waverec(coeffs)

error = np.linalg.norm(x - x_reconstructed) / np.linalg.norm(x)
print(f"relative reconstruction error: {error:.2e}")
```

The inverse uses length/padding/delay metadata recorded by the forward
transform; do not discard this metadata if you want exact length recovery.
`periodic` mode extends inputs as necessary to reach a multiple of `M`.

## Features

- `FilterBank(analysis, synthesis=None)` with any number of channels `M >= 2`;
  a custom bank must satisfy perfect reconstruction for accurate inversion.
- `dwt` / `idwt` for one level; `wavedec` / `waverec` for multilevel analysis.
- Boundary modes: `periodic`, `zero`, `symmetric`, `reflect`, `constant`.
- Transform along a chosen axis of a multidimensional NumPy array.
- Complex-valued signals and filter coefficients.
- Polyphase representations, PR testing, orthogonality tests, and
  frequency-response plots (matplotlib optional).
- Built-in examples: Haar, Daubechies, DCT block banks, cosine-modulated
  lapped transforms, lazy banks, and random paraunitary constructions.

### Custom filter bank

```python
from mbandwt import FilterBank

# Replace h0, h1, h2, g0, g1, g2 with your own filter coefficient arrays.
bank = FilterBank(
    analysis=[h0, h1, h2],
    synthesis=[g0, g1, g2],
    name="custom-3-band",
)
report = bank.validate()
print(report)
if not report.perfect_reconstruction:
    raise ValueError("this filter bank is not perfect-reconstruction")
```

Filter-bank construction does **not** automatically guarantee PR for arbitrary
coefficients. When `synthesis` is omitted, conjugate-reversed analysis filters
are used, which is appropriate for orthonormal constructions but does not
make an arbitrary input bank orthonormal.

## Limitations and conventions

- `periodic` uses critical sampling on the padded signal; non-multiple lengths
  add a few periodic samples. Other boundary modes are **expansive** rather
  than minimal-length/non-expansive transforms.
- Only the approximation channel is further decomposed in multilevel mode.
  Wavelet packets, 2D transforms, CWT, denoising, and GPU support are not
  currently included.
- PR and orthogonality diagnostics use floating-point tolerances.
- Large numbers of channels or long filters increase memory and compute cost.
- Consult [the mathematical conventions](docs/conventions.md) for filtering
  orientation, decimation phase, delay and gain compensation, and boundaries.

## Project files

- [`src/mbandwt/`](src/mbandwt/): implementation
- [`tests/`](tests/): round-trip, polyphase, PR, and regression tests
- [`examples/`](examples/): executable examples
- [`docs/conventions.md`](docs/conventions.md): transform conventions
- [`benchmarks/`](benchmarks/): optional microbenchmarks

Development: [`CONTRIBUTING.md`](CONTRIBUTING.md). Licensed under the
[MIT License](LICENSE). Maintained by Jiayu Ellie Su.

The original implementation was developed with AI assistance and reviewed
and tested as part of this project. Test success does not imply formal
verification or publication. Contributions and bug reports are welcome.
