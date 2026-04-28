from __future__ import annotations

from typing import Optional, Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.patches import Patch

from mmcs._utils._annotation import draw_sample_sizes
from mmcs._utils._stats import BandwidthMethod, KernelType, calculate_bandwidth, kde


def render(
    ax: Axes,
    data: Sequence[np.ndarray],
    *,
    v_widths: float = 0.7,
    b_widths: float = 0.1,
    points: int = 60,
    cut: float = 1.5,
    kernel: KernelType = "gaussian",
    bandwidth: BandwidthMethod = "scott",
    show_n: bool = True,
) -> Axes:
    x_pos = np.arange(len(data))

    for idx, group in enumerate(data):
        group = np.asarray(group).ravel()
        y_grid, density = kde(group, points, cut, kernel, bandwidth)
        standard_density = (density / density.max()) * (v_widths / 2)
        pos = x_pos[idx]

        ax.fill_betweenx(
            y_grid,
            pos - standard_density,
            pos + standard_density,
            color=plt.rcParams["patch.facecolor"],
            edgecolor=plt.rcParams.get("patch.edgecolor", "none"),
            linewidth=plt.rcParams.get("patch.linewidth", 0),
        )

    ax.boxplot(
        data, positions=x_pos, widths=b_widths, showfliers=False,
        patch_artist=plt.rcParams.get("boxplot.patchartist", True),
        boxprops=dict(facecolor="#00000000"),
    )

    if show_n:
        draw_sample_sizes(ax, [np.asarray(d).ravel() for d in data],
                          x_pos, offset_factor=cut)

    return ax


def render_split(
    ax: Axes,
    data: Sequence[tuple[np.ndarray, np.ndarray]],
    *,
    v_widths: float = 0.7,
    b_widths: float = 0.08,
    points: int = 60,
    cut: float = 1.5,
    kernel: KernelType = "gaussian",
    bandwidth: BandwidthMethod = "scott",
    labels: Optional[list[str]] = None,
    show_n: bool = True,
) -> list[Patch]:
    x_pos = np.arange(len(data))
    prop_cycle = plt.rcParams["axes.prop_cycle"]
    colors = [c["color"] for c in prop_cycle]

    low_group = [np.asarray(d[0]).ravel() for d in data]
    high_group = [np.asarray(d[1]).ravel() for d in data]

    for idx, (lo, hi) in enumerate(zip(low_group, high_group)):
        joint = np.concatenate([lo, hi])
        joint_bw = calculate_bandwidth(joint, bandwidth)
        pos = x_pos[idx]

        for side_idx, (side, group) in enumerate(zip(("low", "high"), (lo, hi))):
            y_grid, density = kde(group, points, cut, kernel, bandwidth, override_bw=joint_bw)
            std_density = (density / density.max()) * (v_widths / 2)
            color = colors[side_idx % len(colors)]

            if side == "high":
                ax.fill_betweenx(y_grid, pos, pos + std_density, color=color)
            else:
                ax.fill_betweenx(y_grid, pos - std_density, pos, color=color)

    for side_idx, (side, group) in enumerate(zip(("low", "high"), (low_group, high_group))):
        shift = -v_widths / 4 if side == "low" else v_widths / 4
        ax.boxplot(
            group, positions=x_pos + shift, widths=b_widths,
            showfliers=False,
            patch_artist=plt.rcParams.get("boxplot.patchartist", True),
            boxprops=dict(facecolor="#00000000"),
        )

    handles: list[Patch] = []
    if labels:
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
        offset = max(float(np.std(lo) * cut), float(np.std(hi) * cut))
        top_val = max(float(np.max(lo)), float(np.max(hi)))
        ax.text(
            x_positions[i],
            top_val + offset,
            f"n={len(lo)}/{len(hi)}",
            ha="center",
            va="bottom",
            fontsize=10,
        )
