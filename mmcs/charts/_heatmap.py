from __future__ import annotations

from typing import Any, Optional

import matplotlib.pyplot as plt
import numpy as np
import scipy.cluster.hierarchy as sch
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def render(
    fig: Any,
    gs: GridSpec,
    data: np.ndarray,
    *,
    row_labels: Optional[list[str]] = None,
    col_labels: Optional[list[str]] = None,
    vmin: float = -3.0,
    vmax: float = 3.0,
    cmap: Optional[str] = None,
    linkage_method: str = "ward",
    linkage_metric: str = "euclidean",
    colorbar_label: str = "",
) -> dict[str, Any]:
    """Draw a clustered heatmap with row and column dendrograms.

    Uses hierarchical clustering (``scipy.cluster.hierarchy``) to
    reorder rows and columns before displaying the heatmap matrix.
    Dendrograms are drawn in the GridSpec margins.

    Args:
        fig: The matplotlib Figure to draw on.
        gs: A ``GridSpec`` with shape ``(2, 2)`` (row dendrogram,
            column dendrogram, heatmap, and empty corner).
        data: 2-D array of shape ``(n_genes, n_samples)``.
        row_labels: Labels for each row (gene names).
        col_labels: Labels for each column (sample names).
        vmin: Colormap lower bound.
        vmax: Colormap upper bound.
        cmap: Colormap name. Falls back to ``image.cmap`` rcParam.
        linkage_method: Clustering linkage method.
        linkage_metric: Distance metric.
        colorbar_label: Label for the color bar.

    Returns:
        A dict with keys ``"row_order"`` and ``"col_order"``
        containing the reordered indices.
    """
    data = np.asarray(data)
    n_genes, n_samples = data.shape

    if cmap is None:
        cmap = plt.rcParams.get("image.cmap", "RdBu_r")

    row_linkage = sch.linkage(data, method=linkage_method, metric=linkage_metric)
    col_linkage = sch.linkage(data.T, method=linkage_method, metric=linkage_metric)

    ax_row = fig.add_subplot(gs[1, 0])
    ax_col = fig.add_subplot(gs[0, 1])

    row_dendro = sch.dendrogram(row_linkage, ax=ax_row, orientation="left",
                                 link_color_func=lambda _: "000000")
    ax_row.axis("off")

    col_dendro = sch.dendrogram(col_linkage, ax=ax_col, orientation="top",
                                 link_color_func=lambda _: "000000")
    ax_col.axis("off")

    row_order = row_dendro["leaves"]
    col_order = col_dendro["leaves"]
    ordered = data[row_order, :][:, col_order]

    ax_hm = fig.add_subplot(gs[1, 1])
    im = ax_hm.imshow(ordered, vmin=vmin, vmax=vmax, aspect="auto", cmap=cmap)

    cax = inset_axes(ax_hm, width="25%", height="3%", loc="lower left",
                     bbox_to_anchor=(0.03, -0.2, 1, 1),
                     bbox_transform=ax_hm.transAxes)
    cbar = fig.colorbar(im, cax=cax, orientation="horizontal")
    if colorbar_label:
        cbar.set_label(colorbar_label)
    tick_step = max(1, int(np.ceil(vmax - vmin)))
    cbar.set_ticks(np.linspace(np.floor(vmin), np.ceil(vmax), tick_step + 1))
    cbar.ax.tick_params(size=0)

    if col_labels is not None:
        ax_hm.set_xticks(np.arange(n_samples))
        ax_hm.set_xticklabels(np.asarray(col_labels)[col_order], rotation=45, ha="center")
    if row_labels is not None:
        ax_hm.set_yticks(np.arange(n_genes))
        ax_hm.set_yticklabels(np.asarray(row_labels)[row_order])
        ax_hm.yaxis.tick_right()

    ax_row.set_xticks([])
    ax_row.set_yticks([])

    # Redraw to make layout work
    fig.canvas.draw_idle() if hasattr(fig.canvas, "draw_idle") else None

    return {
        "row_order": row_order,
        "col_order": col_order,
    }
