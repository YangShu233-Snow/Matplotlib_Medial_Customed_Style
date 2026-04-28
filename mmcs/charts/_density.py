from __future__ import annotations

from typing import Optional, Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from sklearn.neighbors import KernelDensity

from mmcs._utils._stats import BandwidthMethod, KernelType, calculate_bandwidth


def render(
    ax: Axes,
    data: Sequence[np.ndarray],
    *,
    labels: Optional[Sequence[str]] = None,
    bandwidth: BandwidthMethod = "scott",
    kernel: KernelType = "gaussian",
    fill: bool = True,
    fill_alpha: float = 0.3,
    n_points: int = 1000,
) -> Axes:
    prop_cycle = plt.rcParams.get("axes.prop_cycle")
    colors = [e["color"] for e in prop_cycle] if prop_cycle else None

    for idx, group in enumerate(data):
        group = np.asarray(group).ravel()
        bw = calculate_bandwidth(group, bandwidth)

        x_min, x_max = float(group.min()), float(group.max())
        margin = (x_max - x_min) * 0.4
        x_pos = np.linspace(x_min - margin, x_max + margin, n_points)

        kde = KernelDensity(bandwidth=bw, kernel=kernel).fit(group.reshape(-1, 1))
        density = np.exp(kde.score_samples(x_pos.reshape(-1, 1)))

        color = colors[idx % len(colors)] if colors else None
        label = labels[idx] if labels else None

        line = ax.plot(x_pos, density, color=color, label=label)[0]
        if fill:
            ax.fill_between(x_pos, density, alpha=fill_alpha, color=line.get_color())

    if labels:
        ax.legend()

    return ax
