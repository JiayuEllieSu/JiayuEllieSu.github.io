# Contributing to mbandwt

This is an early-stage, research-oriented software project. Small,
well-tested improvements and reproducible bug reports are welcome.

## Local setup

```bash
python -m pip install -e ".[test,plot]"
python -m pytest -q
```

## Development guidelines

- Preserve the filtering/decimation/delay conventions described in
  [`docs/conventions.md`](docs/conventions.md). Update documentation and
  tests when a convention changes.
- Include a regression test for any bug fix or new bank family.
- Validate new filter coefficients and note their source; do not copy
  unsourced published coefficient tables.
- Keep the core dependency set limited to NumPy and SciPy.
- Describe limitations candidly. A passing round-trip test alone is not
  enough to establish mathematically correct wavelet behavior.

## Scope

The project currently focuses on finite-signal M-band DWTs and
perfect-reconstruction FIR filter banks. Features outside that scope can
be discussed as proposals rather than treated as promised releases.
