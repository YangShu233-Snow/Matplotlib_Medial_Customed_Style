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
    points: int = 60,
    widths: float = 0.7,
    cut: float = 1.5,
    kernel: KernelType = "gaussian",
    bandwidth: BandwidthMethod = "scott",
    show_n: bool = True,
    sample_size_offset: float | None = None,
) -> Axes:
    """Draw a standard violin plot using KDE.

    Uses a custom ``sklearn`` KDE instead of ``matplotlib.violinplot``
    for better control over bandwidth and kernel selection.

    Args:
        ax: The matplotlib Axes to draw on.
        data: One array per group. Each array contains raw values.
        points: Number of grid points for the KDE evaluation.
        widths: Violin width as a fraction of unit spacing.
        cut: How many standard deviations beyond the data to extend
            the KDE grid.
        kernel: KDE kernel shape.
        bandwidth: Bandwidth selection rule (``"scott"`` or
            ``"silverman"``).
        show_n: If True, annotate sample size above each violin.
        sample_size_offset: Explicit vertical offset for the sample
            size label. If None, computed from ``cut``.

    Returns:
        The matplotlib Axes with the chart drawn.
    """
    x_pos = np.arange(len(data))

    for idx, group in enumerate(data):
        group = np.asarray(group).ravel()
        y_grid, density = kde(group, points, cut, kernel, bandwidth)
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
    """Draw a split violin plot for paired comparisons.

    Each violin is split vertically: one half for one condition
    (e.g. treated) and the other half for the paired condition
    (e.g. control). Colors are drawn from the style's prop_cycle.

    Args:
        ax: The matplotlib Axes to draw on.
        data: One ``(low_group, high_group)`` tuple per violin.
        points: Number of KDE grid points.
        widths: Violin width fraction.
        cut: KDE grid extension factor.
        kernel: KDE kernel shape.
        bandwidth: Bandwidth selection rule.
        labels: Legend labels for the two halves (usually 2 elements).
        show_n: If True, annotate ``n=<lo>/<hi>`` above each violin.

    Returns:
        A list of ``Patch`` handles for use with ``ax.legend()``.
    """
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
            y_grid, density = kde(group, points, cut, kernel, bandwidth, override_bw=joint_bw)
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
