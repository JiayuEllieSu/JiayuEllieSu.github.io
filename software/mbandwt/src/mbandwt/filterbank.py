"""The :class:`FilterBank` object: an arbitrary-M critically sampled
wavelet filter bank with mathematical diagnostics.

The filter bank — not the transform function — is the conceptual center of
``mbandwt``. ``M`` is inferred from the number of filters and is not
restricted by the API.
"""

from __future__ import annotations

import hashlib
from typing import Optional, Sequence

import numpy as np

from . import polyphase as _pp

__all__ = ["FilterBank"]


def _coerce_filters(filters: Sequence, what: str) -> tuple[np.ndarray, ...]:
    out = []
    for i, f in enumerate(filters):
        a = np.atleast_1d(np.asarray(f))
        if a.ndim != 1:
            raise ValueError(f"{what} filter {i} must be one-dimensional")
        if a.size < 1:
            raise ValueError(f"{what} filter {i} is empty")
        if not np.all(np.isfinite(a)):
            raise ValueError(f"{what} filter {i} contains non-finite values")
        dtype = np.complex128 if np.iscomplexobj(a) else np.float64
        a = np.array(a, dtype=dtype, order="C", copy=True)
        a.setflags(write=False)
        out.append(a)
    return tuple(out)


class FilterBank:
    """A critically sampled ``M``-channel analysis/synthesis filter bank.

    Parameters
    ----------
    analysis : sequence of 1-D arrays
        Analysis filters ``h_0 .. h_{M-1}``; ``h_0`` is the lowpass /
        approximation branch by convention. ``M = len(analysis)`` and must
        be at least 2. Filter lengths may differ.
    synthesis : sequence of 1-D arrays, optional
        Synthesis filters ``g_0 .. g_{M-1}``. If omitted, an orthonormal
        bank is assumed and ``g_k[n] = conj(h_k[L_k - 1 - n])``.
    name, family, reference, notes : str, optional
        Provenance metadata. Built-in families always set ``reference``.

    Notes
    -----
    All transform conventions are documented in ``docs/conventions.md``.
    The composite gain and delay of the bank are computed once at
    construction from the distortion function
    ``t = (1/M) * sum_k conv(g_k, h_k)`` and are used by the inverse
    transforms to compensate exactly.
    """

    def __init__(
        self,
        analysis: Sequence,
        synthesis: Optional[Sequence] = None,
        *,
        name: Optional[str] = None,
        family: Optional[str] = None,
        reference: Optional[str] = None,
        notes: Optional[str] = None,
    ):
        analysis = _coerce_filters(analysis, "analysis")
        if len(analysis) < 2:
            raise ValueError("a filter bank needs at least M = 2 channels")
        if synthesis is None:
            synthesis = tuple(np.conj(h[::-1]) for h in analysis)
            synthesis = _coerce_filters(synthesis, "synthesis")
        else:
            synthesis = _coerce_filters(synthesis, "synthesis")
            if len(synthesis) != len(analysis):
                raise ValueError(
                    "analysis and synthesis banks must have the same number "
                    f"of filters (got {len(analysis)} and {len(synthesis)})"
                )

        self._analysis = analysis
        self._synthesis = synthesis
        self.name = name
        self.family = family
        self.reference = reference
        self.notes = notes

        self._gain, self._delay, self._distortion = self._composite_response()
        self._pr_cache: dict = {}
        self._orth_cache: dict = {}

    # ------------------------------------------------------------------
    # basic structure
    # ------------------------------------------------------------------
    @property
    def M(self) -> int:
        """Number of channels (decimation factor)."""
        return len(self._analysis)

    @property
    def analysis(self) -> tuple[np.ndarray, ...]:
        """Analysis filters (read-only views)."""
        return self._analysis

    @property
    def synthesis(self) -> tuple[np.ndarray, ...]:
        """Synthesis filters (read-only views)."""
        return self._synthesis

    @property
    def filter_lengths(self) -> dict:
        return {
            "analysis": tuple(len(h) for h in self._analysis),
            "synthesis": tuple(len(g) for g in self._synthesis),
        }

    @property
    def is_complex(self) -> bool:
        return any(np.iscomplexobj(f) for f in self._analysis + self._synthesis)

    @property
    def gain(self):
        """Composite scalar gain ``c`` of the analysis/synthesis chain."""
        return self._gain

    @property
    def delay(self) -> int:
        """Composite sample-domain delay ``d`` (compensated internally)."""
        return self._delay

    @property
    def signature(self) -> str:
        """Stable hash identifying the bank's filters (coefficient bookkeeping)."""
        m = hashlib.sha1()
        m.update(b"mbandwt-filterbank")
        m.update(str(self.M).encode())
        for f in self._analysis + self._synthesis:
            m.update(str(f.dtype).encode())
            m.update(str(len(f)).encode())
            m.update(np.ascontiguousarray(f).tobytes())
        return m.hexdigest()

    def _composite_response(self):
        convs = [np.convolve(g, h) for g, h in zip(self._synthesis, self._analysis)]
        T = max(len(t) for t in convs)
        dtype = np.result_type(*[t.dtype for t in convs])
        t = np.zeros(T, dtype=dtype)
        for ck in convs:
            t[: len(ck)] += ck
        t = t / self.M
        d = int(np.argmax(np.abs(t)))
        c = t[d]
        if not self.is_complex:
            c = float(np.real(c))
        return c, d, t

    # ------------------------------------------------------------------
    # diagnostics
    # ------------------------------------------------------------------
    def pr_report(self, rtol: float = 1e-8) -> dict:
        """Algebraic polyphase PR test (cached). See :func:`mbandwt.polyphase.pr_check`."""
        if rtol not in self._pr_cache:
            self._pr_cache[rtol] = _pp.pr_check(
                self._analysis, self._synthesis, self.M, rtol=rtol
            )
        return self._pr_cache[rtol]

    def is_pr(self, rtol: float = 1e-8) -> bool:
        """True if the bank satisfies perfect reconstruction (polyphase test)."""
        return bool(self.pr_report(rtol)["pr"])

    def orthogonality_residual(self) -> float:
        """Max deviation of the periodic analysis operator from ``A A^H = c I``."""
        key = "residual"
        if key not in self._orth_cache:
            from .validation import _orthogonality_residual

            self._orth_cache[key] = _orthogonality_residual(self)
        return self._orth_cache[key]

    def is_orthogonal(self, rtol: float = 1e-8) -> bool:
        """True if the analysis operator is orthogonal (paraunitary bank)."""
        return self.is_pr(rtol) and self.orthogonality_residual() < rtol

    def is_biorthogonal(self, rtol: float = 1e-8) -> bool:
        """True if the bank is PR but not orthogonal."""
        return self.is_pr(rtol) and not self.is_orthogonal(rtol)

    def validate(self, rtol: float = 1e-8):
        """Full validation report. See :func:`mbandwt.validation.validate`."""
        from .validation import validate

        return validate(self, rtol=rtol)

    # ------------------------------------------------------------------
    # polyphase access
    # ------------------------------------------------------------------
    def polyphase_analysis(self) -> np.ndarray:
        """Type-I analysis polyphase matrix ``E`` as an ``(M, M, T)`` array."""
        return _pp.analysis_polyphase(self._analysis, self.M)

    def polyphase_synthesis(self) -> np.ndarray:
        """Type-II synthesis polyphase matrix ``R`` as an ``(M, M, T)`` array."""
        return _pp.synthesis_polyphase(self._synthesis, self.M)

    # ------------------------------------------------------------------
    # spectral / moment diagnostics
    # ------------------------------------------------------------------
    def frequency_response(self, n: int = 512, which: str = "analysis"):
        """Frequency responses on ``[0, pi]``.

        Returns ``(w, H)`` with ``w`` of shape ``(n,)`` and ``H`` of shape
        ``(M, n)`` (complex).
        """
        if which not in ("analysis", "synthesis"):
            raise ValueError("which must be 'analysis' or 'synthesis'")
        if not isinstance(n, (int, np.integer)) or isinstance(n, (bool, np.bool_)) or n < 2:
            raise ValueError("n must be an integer of at least 2")
        filters = self._analysis if which == "analysis" else self._synthesis
        w = np.linspace(0.0, np.pi, n)
        H = np.empty((self.M, n), dtype=np.complex128)
        for k, f in enumerate(filters):
            m = np.arange(len(f))
            H[k] = np.exp(-1j * np.outer(w, m)) @ f
        return w, H

    def plot_frequency_response(self, n: int = 512, which: str = "analysis", ax=None):
        """Plot magnitude responses (requires matplotlib)."""
        try:
            import matplotlib.pyplot as plt
        except ImportError as e:  # pragma: no cover
            raise ImportError(
                "matplotlib is required for plotting; install mbandwt[plot]"
            ) from e
        w, H = self.frequency_response(n=n, which=which)
        if ax is None:
            _, ax = plt.subplots()
        for k in range(self.M):
            ax.plot(w / np.pi, 20 * np.log10(np.abs(H[k]) + 1e-300), label=f"band {k}")
        ax.set_xlabel("normalized frequency (x pi rad/sample)")
        ax.set_ylabel("magnitude (dB)")
        ax.set_title(self.name or f"{self.M}-band filter bank ({which})")
        ax.legend()
        return ax

    def vanishing_moments(self, tol: float = 1e-8, max_order: int = 16) -> list[int]:
        """Discrete vanishing-moment count of each analysis filter.

        For filter ``h`` of length ``L``, counts the largest ``V`` such that
        the moments ``m_p = sum_n n^p h[n]`` vanish for all ``p < V``
        relative to the scale ``sum|h| * max(1, L-1)^p``. Detail branches of
        a bank with ``V`` vanishing moments annihilate polynomials of degree
        ``< V``; the lowpass branch reports 0 (its zeroth moment is the DC
        gain).
        """
        counts = []
        for h in self._analysis:
            L = len(h)
            n = np.arange(L, dtype=np.float64)
            base = np.sum(np.abs(h))
            V = 0
            for p in range(max_order + 1):
                scale = base * max(1.0, float(L - 1)) ** p
                if scale == 0 or np.abs(np.sum(h * n**p)) >= tol * scale:
                    break
                V += 1
            counts.append(V)
        return counts

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        label = self.name or "custom"
        la = ",".join(str(len(h)) for h in self._analysis)
        return f"FilterBank(M={self.M}, name={label!r}, analysis_lengths=[{la}])"
