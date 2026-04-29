"""Statistical helpers for biomedical charting.

Provides bandwidth calculation (Scott / Silverman), significance star
annotation, kernel density estimation, and optimal histogram binning.
"""

from __future__ import annotations

from typing import Literal

import numpy as np
from sklearn.neighbors import KernelDensity

BandwidthMethod = Literal["scott", "silverman"]
"""Method for automatic KDE bandwidth selection."""

KernelType = Literal["gaussian", "tophat", "epanechnikov", "exponential", "linear", "cosine"]
"""Kernel shape for KDE estimation. Mirrors ``sklearn.neighbors.KernelDensity``."""


def calculate_bandwidth(data: np.ndarray, method: BandwidthMethod = "scott") -> float:
    """Compute the KDE bandwidth using Scott or Silverman's rule of thumb.

    Args:
        data: Input data array (1-D).
        method: Bandwidth estimation rule. ``"scott"`` uses
            ``sigma * n^(-1/5)``. ``"silverman"`` uses
            ``0.9 * A * n^(-1/5)`` where ``A = min(sigma, IQR / 1.34)``.

    Returns:
        The computed bandwidth value.

    Raises:
        ValueError: If ``method`` is not ``"scott"`` or ``"silverman"``.

    Example:
        >>> data = np.random.normal(0, 1, 100)
        >>> calculate_bandwidth(data, "scott")
        0.412
    """
    n = len(data)
    sigma = np.std(data, ddof=1)
    if method == "scott":
        return float(sigma * (n ** (-1 / 5)))
    if method == "silverman":
        iqr = float(np.subtract(*np.percentile(data, [75, 25])))
        A = min(sigma, iqr / 1.34)
        return float(0.9 * A * (n ** (-1 / 5)))
    msg = f"Unknown bandwidth method: {method}"
    raise ValueError(msg)


def significance_stars(p_value: float) -> str:
    """Convert a p-value to a significance star string.

    Args:
        p_value: The p-value to annotate.

    Returns:
        ``"****"`` if ``p <= 0.0001``, ``"***"`` if ``p <= 0.001``,
        ``"**"`` if ``p <= 0.01``, ``"*"`` if ``p <= 0.05``,
        otherwise ``"ns"``.
    """
    if p_value <= 0.0001:
        return "****"
    if p_value <= 0.001:
        return "***"
    if p_value <= 0.01:
        return "**"
    if p_value <= 0.05:
        return "*"
    return "ns"


def kde(
    data: np.ndarray,
    points: int,
    cut: float,
    kernel: KernelType = "gaussian",
    bw_method: BandwidthMethod = "scott",
    override_bw: float | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute a KDE over a regular grid.

    Uses ``sklearn.neighbors.KernelDensity`` internally.

    Args:
        data: Input data array (1-D).
        points: Number of grid points for the evaluation.
        cut: How many standard deviations beyond the data range to
            extend the grid.
        kernel: KDE kernel type.
        bw_method: Bandwidth selection rule (ignored if
            ``override_bw`` is set).
        override_bw: Explicit bandwidth value. If provided,
            ``bw_method`` is ignored.

    Returns:
        A tuple ``(grid, density)`` where ``grid`` is the evaluation
        positions and ``density`` is the estimated density (not log).
    """
    bw = override_bw if override_bw is not None else calculate_bandwidth(data, bw_method)
    model = KernelDensity(bandwidth=bw, kernel=kernel).fit(data.reshape(-1, 1))

    d_min, d_max = float(data.min()), float(data.max())
    d_std = float(np.std(data))
    extend = d_std * cut
    y_grid = np.linspace(d_min - extend, d_max + extend, points)

    density = np.exp(model.score_samples(y_grid.reshape(-1, 1)))
    return y_grid, density


def optimal_bins(data: np.ndarray, method: str = "freedman_diaconis") -> int:
    """Compute the optimal number of histogram bins.

    Args:
        data: Input data array (1-D).
        method: Bin counting rule. ``"freedman_diaconis"`` (default)
            uses 2 * IQR * n^(-1/3). ``"sturges"`` and ``"sqrt"``
            are also supported.

    Returns:
        The optimal bin count as an integer.

    Example:
        >>> data = np.random.normal(0, 1, 200)
        >>> optimal_bins(data, "freedman_diaconis")
        14
    """
    n = len(data)
    if n < 2:
        return 1

    if method == "sturges":
        return int(np.ceil(np.log2(n) + 1))
    if method == "sqrt":
        return int(np.ceil(np.sqrt(n)))

    q75, q25 = np.percentile(data, [75, 25])
    iqr = q75 - q25

    if iqr == 0:
        return int(np.ceil(np.log2(n) + 1))

    h = 2.0 * iqr * (n ** (-1.0 / 3.0))
    data_range = float(np.max(data) - np.min(data))

    if h == 0:
        return 1
    return int(np.ceil(data_range / h))
