from __future__ import annotations

from typing import Literal

import numpy as np
from sklearn.neighbors import KernelDensity

BandwidthMethod = Literal["scott", "silverman"]
KernelType = Literal["gaussian", "tophat", "epanechnikov", "exponential", "linear", "cosine"]


def calculate_bandwidth(data: np.ndarray, method: BandwidthMethod = "scott") -> float:
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
    bw = override_bw if override_bw is not None else calculate_bandwidth(data, bw_method)
    model = KernelDensity(bandwidth=bw, kernel=kernel).fit(data.reshape(-1, 1))

    d_min, d_max = float(data.min()), float(data.max())
    d_std = float(np.std(data))
    extend = d_std * cut
    y_grid = np.linspace(d_min - extend, d_max + extend, points)

    density = np.exp(model.score_samples(y_grid.reshape(-1, 1)))
    return y_grid, density


def optimal_bins(data: np.ndarray, method: str = "freedman_diaconis") -> int:
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
