from __future__ import annotations

from typing import Literal, Optional, Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.patches import Patch
from sklearn.neighbors import KernelDensity

from mmcs._utils._annotation import draw_sample_sizes
from mmcs._utils._stats import BandwidthMethod, calculate_bandwidth

KernelType = Literal["gaussian", "tophat", "epanechnikov", "exponential", "linear", "cosine"]


def render(
    ax: Axes,
    data: Sequence[np.ndarray],
    *,
    points: int = 60,
    widths: float = 0.7,
    cut: float = 1.5,
    kernel: KernelType = "gaussian",
    bandwidth: BandwidthMethod = "scott",
    show_n: bool = True,
    sample_size_offset: float | None = None,
) -> Axes:
    x_pos = np.arange(len(data))

    for idx, group in enumerate(data):
        group = np.asarray(group).ravel()
        y_grid, density = _kde(group, points, cut, kernel, bandwidth)
        standard_density = (density / density.max()) * (widths / 2)
        pos = x_pos[idx]

        ax.fill_betweenx(
            y_grid,
            pos - standard_density,
            pos + standard_density,
            color=plt.rcParams["patch.facecolor"],
            edgecolor=plt.rcParams.get("patch.edgecolor", "none"),
            linewidth=plt.rcParams.get("patch.linewidth", 0),
        )

    if show_n:
        kwargs = {"offset_factor": sample_size_offset} if sample_size_offset is not None else {}
        draw_sample_sizes(ax, [np.asarray(d).ravel() for d in data], x_pos, offset_factor=cut, **kwargs)

    return ax


def render_split(
    ax: Axes,
    data: Sequence[tuple[np.ndarray, np.ndarray]],
    *,
    points: int = 60,
    widths: float = 0.7,
    cut: float = 1.5,
    kernel: KernelType = "gaussian",
    bandwidth: BandwidthMethod = "scott",
    labels: Optional[list[str]] = None,
    show_n: bool = True,
) -> list[Patch]:
    x_pos = np.arange(len(data))
    prop_cycle = plt.rcParams["axes.prop_cycle"]
    colors = [c["color"] for c in prop_cycle]

    handles: list[Patch] = []

    for idx, (high_group, low_group) in enumerate(data):
        high_group = np.asarray(high_group).ravel()
        low_group = np.asarray(low_group).ravel()

        joint = np.concatenate([high_group, low_group])
        joint_bw = calculate_bandwidth(joint, bandwidth)

        for side_idx, (side, group) in enumerate((("high", high_group), ("low", low_group))):
            y_grid, density = _kde(group, points, cut, kernel, bandwidth, override_bw=joint_bw)
            standard_density = (density / density.max()) * (widths / 2)
            pos = x_pos[idx]
            color = colors[side_idx % len(colors)]

            if side == "high":
                ax.fill_betweenx(y_grid, pos, pos + standard_density, color=color)
            else:
                ax.fill_betweenx(y_grid, pos - standard_density, pos, color=color)

        if idx == 0 and labels:
            for i, label in enumerate(labels):
                handles.append(Patch(facecolor=colors[i % len(colors)], label=label))

    if show_n:
        _draw_split_sample_sizes(ax, data, x_pos, cut)

    return handles


def _draw_split_sample_sizes(
    ax: Axes,
    data: Sequence[tuple[np.ndarray, np.ndarray]],
    x_positions: np.ndarray,
    cut: float,
) -> None:
    for i, (lo, hi) in enumerate(data):
        lo = np.asarray(lo).ravel()
        hi = np.asarray(hi).ravel()
        offsets = [float(np.std(g) * cut) for g in (lo, hi)]
        offset = max(offsets)
        top_val = max(float(np.max(lo)), float(np.max(hi)))
        ax.text(
            x_positions[i],
            top_val + offset,
            f"n={len(lo)}/{len(hi)}",
            ha="center",
            va="bottom",
            fontsize=10,
        )


def _kde(
    data: np.ndarray,
    points: int,
    cut: float,
    kernel: KernelType,
    bw_method: BandwidthMethod,
    override_bw: float | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    bw = override_bw if override_bw is not None else calculate_bandwidth(data, bw_method)
    kde = KernelDensity(bandwidth=bw, kernel=kernel).fit(data.reshape(-1, 1))

    d_min, d_max = data.min(), data.max()
    d_std = float(np.std(data))
    extend = d_std * cut
    y_grid = np.linspace(d_min - extend, d_max + extend, points)

    density = np.exp(kde.score_samples(y_grid.reshape(-1, 1)))
    return y_grid, density
