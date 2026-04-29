from __future__ import annotations

from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def render(
    fig: Figure,
    gs: GridSpec,
    categories: Sequence[str],
    x_values: np.ndarray,
    bubble_sizes: np.ndarray,
    color_values: np.ndarray,
    *,
    xlabel: str = "Value",
    color_highlight: bool = True,
    legend_label: str = "legend",
    p_value_ticks: bool = True,
    min_bubble_size: float = 20,
    max_bubble_size: float = 100,
) -> None:
    """Draw a bubble plot.

    A multi-dimensional chart with 2x2 GridSpec layout:
    - Main: bubble scatter (x = value, y = category, size = metric,
      color = p-value or fold change)
    - Top-right: bubble size legend
    - Bottom-right: color bar for p-value

    Args:
        fig: The matplotlib Figure to draw on.
        gs: A ``GridSpec`` of shape ``(2, 2)``.
        categories: Y-axis category labels.
        x_values: X-axis positions (e.g. enrichment scores).
        bubble_sizes: Magnitudes that determine bubble radii.
        color_values: Values mapped to bubble color (e.g. p-values).
        xlabel: X-axis label.
        color_highlight: If True, sort by ``color_values`` descending
            and use a multi-color colormap.
        legend_label: Title for the bubble size legend.
        p_value_ticks: If True, use common p-value thresholds as
            color bar ticks.
        min_bubble_size: Minimum bubble area in points squared.
        max_bubble_size: Maximum bubble area in points squared.
    """
    if color_highlight:
        idx = np.argsort(color_values)[::-1]
        color_values = color_values[idx]
        categories = [categories[i] for i in idx]
        x_values = x_values[idx]
        bubble_sizes = bubble_sizes[idx]

    y_index = np.arange(len(categories))

    scaled = (
        (bubble_sizes - bubble_sizes.min()) / (bubble_sizes.max() - bubble_sizes.min())
        * (max_bubble_size - min_bubble_size) + min_bubble_size
    )

    ax = fig.add_subplot(gs[:, 0])
    ax_legend = fig.add_subplot(gs[0, 1])
    ax_cbar = fig.add_subplot(gs[1, 1])

    prop_cycle = plt.rcParams.get("axes.prop_cycle")
    cmap_colors = [c["color"] for c in prop_cycle] if prop_cycle else ["#999999"]
    if color_highlight:
        cmap = LinearSegmentedColormap.from_list("", cmap_colors)
    else:
        cmap = LinearSegmentedColormap.from_list("", ["#999999", "#999999"])

    scatter = ax.scatter(
        x=x_values, y=y_index,
        s=scaled, c=color_values, cmap=cmap,
    )

    ax.set_yticks(y_index)
    ax.set_yticklabels(list(categories))
    ax.set_xlabel(xlabel)

    if len(x_values) > 0:
        x_min, x_max = float(x_values.min()), float(x_values.max())
        margin = (x_max - x_min) * 0.15 if x_max != x_min else 10
        ax.set_xlim(x_min - margin, x_max + margin)

    percentile = [0, 0.50, 1]
    legend_sizes = [int(np.percentile(x_values, p * 100)) for p in percentile]
    legend_handles = []
    for val in legend_sizes:
        s = ((val - bubble_sizes.min()) / (bubble_sizes.max() - bubble_sizes.min())
             * (max_bubble_size - min_bubble_size) + min_bubble_size)
        handle = ax.scatter([], [], s=s, c="#999999")
        legend_handles.append(handle)

    ax_legend.axis("off")
    leg = ax_legend.legend(
        handles=legend_handles,
        labels=[str(val) for val in legend_sizes],
        title=legend_label,
        loc="center",
        frameon=False,
    )
    leg.get_title().set_ha("center")

    if color_highlight:
        ax_cbar.axis("off")
        cax = inset_axes(ax_cbar, width="15%", height="40%", loc="center")
        cax.set_frame_on(False)
        cbar = fig.colorbar(scatter, cax=cax, orientation="vertical")

        cax.set_title("P_value", pad=12, loc="center", fontsize=11)
        cax.tick_params(length=0)

        if p_value_ticks:
            thresholds = (
                [0.0001, 0.0005] + [0.001, 0.005]
                + [0.02 * n for n in range(1, 5)]
                + [0.1, 0.5]
            )
            ticks = [t for t in thresholds if float(color_values.min()) <= t <= float(color_values.max())]
        else:
            ticks = np.linspace(float(color_values.min()), float(color_values.max()), 4)

        cbar.set_ticks(ticks)
        cbar.set_ticklabels([f"{t:.3f}" for t in ticks])
    else:
        ax_cbar.axis("off")
