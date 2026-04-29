from __future__ import annotations

from typing import Literal, Optional

import numpy as np
from matplotlib.axes import Axes

from mmcs._utils._stats import optimal_bins

BinMethod = Literal["freedman_diaconis", "sturges", "sqrt"]


def render(
    ax: Axes,
    data: np.ndarray,
    *,
    bins: Optional[int] = None,
    bins_method: BinMethod = "freedman_diaconis",
    rwidth: float = 0.9,
) -> Axes:
    """Draw a histogram with automatic binning.

    Uses the Freedman-Diaconis rule by default to determine the
    optimal number of bins.

    Args:
        ax: The matplotlib Axes to draw on.
        data: Input data array (1-D).
        bins: Explicit number of bins. If None, computed from
            ``bins_method``.
        bins_method: Bin counting rule when ``bins`` is None.
        rwidth: Relative width of each bar as a fraction of bin width.

    Returns:
        The matplotlib Axes with the chart drawn.
    """
    data = np.asarray(data).ravel()

    if bins is None:
        bins = optimal_bins(data, bins_method)

    ax.hist(data, bins=bins, rwidth=rwidth)
    return ax
