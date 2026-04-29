from __future__ import annotations

from typing import Optional, Sequence

import numpy as np
from matplotlib.axes import Axes

from mmcs._utils._annotation import draw_sample_sizes


def render(
    ax: Axes,
    data: Sequence[np.ndarray],
    *,
    labels: Optional[Sequence[str]] = None,
    show_n: bool = True,
    patch_facecolor: str = "#CCCCCC",
) -> Axes:
    """Draw a vertical box plot.

    One box per group. Supports sample size annotation above each box.

    Args:
        ax: The matplotlib Axes to draw on.
        data: One array per group. Each array contains the raw values
            for that group.
        labels: X-axis tick labels, one per group.
        show_n: If True, annotate ``n=<count>`` above each box.
        patch_facecolor: Fill color for the box patch.

    Returns:
        The matplotlib Axes with the chart drawn.
    """
    data_list = [np.asarray(d) for d in data]

    ax.boxplot(
        data_list,
        tick_labels=list(labels) if labels is not None else None,
        patch_artist=True,
        boxprops=dict(facecolor=patch_facecolor),
    )

    x_positions = np.arange(1, len(data_list) + 1)

    if show_n:
        draw_sample_sizes(ax, data_list, x_positions)

    if labels is not None:
        ax.set_xticks(x_positions)
        ax.set_xticklabels(list(labels))

    return ax
