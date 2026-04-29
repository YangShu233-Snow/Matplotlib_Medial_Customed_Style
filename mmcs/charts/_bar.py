from __future__ import annotations

from typing import Optional, Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from mmcs._utils._annotation import jitter


def render(
    ax: Axes,
    data: Sequence[float],
    *,
    groups: Optional[Sequence[str]] = None,
    errors: Optional[Sequence[float]] = None,
    upper_only: bool = True,
    colors: Optional[Sequence[str]] = None,
    width: float = 0.6,
    stars: Optional[Sequence[int]] = None,
    edge: bool = True,
    scatter_data: Optional[Sequence[np.ndarray]] = None,
    scatter_r: float = 2.0,
) -> Axes:
    """Draw a vertical bar chart.

    Each bar represents one group mean. Supports error bars (asymmetric,
    upper-only by default), significance stars, and optional individual
    data points overlaid as a jittered scatter plot.

    Args:
        ax: The matplotlib Axes to draw on.
        data: Bar heights, one value per bar.
        groups: X-axis tick labels for each bar.
        errors: Error bar magnitudes (e.g. SEM or SD).
        upper_only: If True, error bars extend upward only (GraphPad
            Prism convention).
        colors: Bar fill colors. Must be same length as ``data``.
        width: Bar width as a fraction of the unit spacing.
        stars: Significance stars per bar. ``0`` means no stars,
            ``3`` means ``***``, etc.
        edge: If True, draw bar edges using ``patch.edgecolor`` rcParam.
        scatter_data: Raw data arrays for jittered scatter overlay,
            one per bar.
        scatter_r: Marker radius for scatter points in points.

    Returns:
        The matplotlib Axes with the chart drawn.
    """
    x_pos = np.arange(len(data))
    means = np.asarray(data)

    yerr = None
    if errors is not None:
        if upper_only:
            yerr = [[0] * len(data), list(errors)]
        else:
            yerr = list(errors)

    edgecolor = plt.rcParams.get("patch.edgecolor") if edge else None
    ax.bar(x_pos, means, yerr=yerr, width=width, color=colors, edgecolor=edgecolor)

    if scatter_data is not None:
        fig_w = ax.figure.get_figwidth() if hasattr(ax.figure, "get_figwidth") else 10
        fig_h = ax.figure.get_figheight() if hasattr(ax.figure, "get_figheight") else 6
        n_bars = len(data)
        all_max = max(means)

        for i, raw in enumerate(scatter_data):
            raw = np.asarray(raw).ravel()
            r_x = n_bars / fig_w * scatter_r / 36
            r_y = all_max / fig_h * scatter_r / 36
            x_jit = jitter(raw, r_x, r_y) + x_pos[i]

            ax.scatter(x_jit, raw, color="white", edgecolor="black",
                       alpha=0.7, linewidths=plt.rcParams.get("lines.linewidth", 1.0),
                       s=np.pi * scatter_r ** 2)

    if stars is not None:
        _draw_stars_simple(ax, means, errors or [0] * len(data), stars,
                           raw_max=_max_of_scatter(scatter_data) if scatter_data else None)

    if groups is not None:
        ax.set_xticks(x_pos)
        ax.set_xticklabels(list(groups))

    ax.set_xlim(-0.6, len(data) - 1 + 0.6)
    return ax


def _draw_stars_simple(
    ax: Axes,
    means: np.ndarray,
    errs: Sequence[float],
    stars: Sequence[int],
    raw_max: float | None = None,
) -> None:
    for idx, n_stars in enumerate(stars):
        top = means[idx] + errs[idx] + errs[idx] * 0.05
        if raw_max is not None:
            top = max(top, raw_max + 20)
        ax.text(idx, top, "*" * n_stars, ha="center", va="bottom", fontsize=14)


def _max_of_scatter(scatter_data: Sequence[np.ndarray]) -> float:
    return max(float(np.max(d)) for d in scatter_data)
