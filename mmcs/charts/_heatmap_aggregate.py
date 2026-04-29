from __future__ import annotations

from typing import Any, Optional, Sequence, Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes


def render(
    axs: Union[Axes, Sequence[Axes]],
    datasets: Union[np.ndarray, Sequence[np.ndarray]],
    *,
    titles: Optional[Sequence[str]] = None,
    vmin: float = -3.5,
    vmax: float = 3.0,
    cmap: Optional[str] = None,
    colorbar_label: str = "",
    scale: float = 0.5,
    scale_label: str = "1 kb",
    ylabel: Optional[str] = None,
    interpolation: str = "nearest",
) -> None:
    """Draw one or more aggregate heatmap panels.

    Used for multi-panel genomic track visualizations. Each panel
    is drawn in its own Axes. A shared color bar and genomic scale
    bar are added to the last Axes.

    Args:
        axs: One or more matplotlib Axes, one per panel.
        datasets: One 2-D array per panel (``features x samples``),
            or a single 2-D array for one panel.
        titles: Panel titles, one per dataset.
        vmin: Colormap lower bound.
        vmax: Colormap upper bound.
        cmap: Colormap name. Falls back to ``image.cmap`` rcParam.
        colorbar_label: Label for the shared color bar.
        scale: Length of the genomic scale bar in data units.
        scale_label: Text label for the scale bar (e.g. ``"1 kb"``).
        ylabel: Y-axis label for the first panel.
        interpolation: Image interpolation method.
    """
    if cmap is None:
        cmap = plt.rcParams.get("image.cmap", "RdYlBu")

    if isinstance(axs, Axes):
        axs = [axs]
    if isinstance(datasets, np.ndarray):
        datasets = [datasets]

    im: Any = None
    for i, (ax, data) in enumerate(zip(axs, datasets)):
        data = np.asarray(data)
        im = ax.imshow(data, aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax,
                       interpolation=interpolation)

        title = titles[i] if titles else ""
        ax.set_title(title, pad=10)

        center = data.shape[1] // 2
        ax.set_xticks([center])
        ax.set_xticklabels(["0"])

        ax.set_yticks([])

        if i == 0 and ylabel:
            ax.set_ylabel(ylabel)

        for spine in ax.spines.values():
            spine.set_linewidth(1.0)

    if im is not None:
        fig = axs[0].figure
        cbar_ax = fig.add_axes([0.4, 0.15, 0.2, 0.02])
        cbar = fig.colorbar(im, cax=cbar_ax, orientation="horizontal")
        if colorbar_label:
            cbar.set_label(colorbar_label, fontsize=12, labelpad=8)

        cbar.set_ticks([])
        cbar_ax.text(-0.03, 0.5, str(vmin), transform=cbar_ax.transAxes,
                     ha="right", va="center")
        cbar_ax.text(1.03, 0.5, str(vmax), transform=cbar_ax.transAxes,
                     ha="left", va="center")
        cbar.ax.tick_params(size=0)

    ax_last = axs[-1]
    ax_last.plot([0.5, 0.5 + scale], [-0.12, -0.12],
                 transform=ax_last.transAxes, color="black",
                 linewidth=1.5, clip_on=False)
    ax_last.text(0.5 + scale / 2, -0.14, scale_label,
                 transform=ax_last.transAxes, ha="center", va="top",
                 fontsize=10)
