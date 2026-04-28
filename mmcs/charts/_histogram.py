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
    data = np.asarray(data).ravel()

    if bins is None:
        bins = optimal_bins(data, bins_method)

    ax.hist(data, bins=bins, rwidth=rwidth)
    return ax
