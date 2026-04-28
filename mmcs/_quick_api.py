from __future__ import annotations

import base64
import io
from pathlib import Path
from typing import Any, Optional, Sequence, Union

import matplotlib.pyplot as plt
import numpy as np

from mmcs._context import StyleContext
from mmcs._registry import Style
from mmcs.charts import bar, boxplot, boxviolin, scatter, violin


class ChartResult:
    def __init__(self, fig: plt.Figure, stats: Optional[dict[str, Any]] = None):
        self.fig = fig
        self.stats = stats or {}

    def to_base64(self, fmt: str = "png", dpi: int = 300) -> str:
        buf = io.BytesIO()
        self.fig.savefig(buf, format=fmt, dpi=dpi, bbox_inches="tight")
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")


def bar_chart(
    data: Any,
    groups: Optional[Sequence[str]] = None,
    errors: Optional[Sequence[float]] = None,
    *,
    x: Optional[str] = None,
    y: Optional[str] = None,
    style: Union[str, Style] = "graphpad_prism",
    save_as: Optional[Union[str, Path]] = None,
    figsize: Optional[tuple[float, float]] = None,
    dpi: int = 300,
    upper_only: bool = True,
    colors: Optional[Sequence[str]] = None,
    stars: Optional[Sequence[int]] = None,
    width: float = 0.6,
    edge: bool = True,
    title: Optional[str] = None,
    ylabel: Optional[str] = None,
    **kwargs: Any,
) -> ChartResult:
    arr, grp = _resolve_frame(data, x, y)
    ctxt = StyleContext(style)
    ctxt.apply(plt.rcParams, "bar")
    if figsize is None:
        figsize = (len(arr) * 1.5, 4)
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    if colors is None:
        colors = ctxt.bar_colors(len(arr))
    bar.render(ax, arr, groups=grp if grp is not None else groups,
               errors=errors, colors=colors, stars=stars, width=width,
               upper_only=upper_only, edge=edge, **kwargs)
    _label(ax, ylabel=ylabel, title=title)
    _handle_save(fig, save_as)
    return ChartResult(fig, stats={"n_groups": len(arr)})


def box_chart(
    data: Any,
    *,
    x: Optional[str] = None,
    y: Optional[str] = None,
    groups: Optional[Sequence[str]] = None,
    style: Union[str, Style] = "graphpad_prism",
    save_as: Optional[Union[str, Path]] = None,
    figsize: Optional[tuple[float, float]] = None,
    dpi: int = 300,
    show_n: bool = True,
    patch_facecolor: str = "#CCCCCC",
    title: Optional[str] = None,
    ylabel: Optional[str] = None,
    **kwargs: Any,
) -> ChartResult:
    arr, grp = _resolve_frame(data, x, y)
    ctxt = StyleContext(style)
    ctxt.apply(plt.rcParams, "boxplot")
    if figsize is None:
        figsize = (5, 5)
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    boxplot.render(ax, arr, labels=grp if grp is not None else groups,
                   show_n=show_n, patch_facecolor=patch_facecolor, **kwargs)
    _label(ax, ylabel=ylabel, title=title)
    _handle_save(fig, save_as)
    return ChartResult(fig, stats={"n_groups": len(arr)})


def scatter_chart(
    x: Any,
    y: Any,
    *,
    style: Union[str, Style] = "graphpad_prism",
    save_as: Optional[Union[str, Path]] = None,
    figsize: Optional[tuple[float, float]] = None,
    dpi: int = 300,
    c: Any = None,
    s: float = 20.0,
    cmap: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    title: Optional[str] = None,
    **kwargs: Any,
) -> ChartResult:
    ctxt = StyleContext(style)
    ctxt.apply(plt.rcParams, "scatter")
    if figsize is None:
        figsize = (5, 5)
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    scatter.render(ax, x, y, c=c, s=s, cmap=cmap, **kwargs)
    _label(ax, xlabel=xlabel, ylabel=ylabel, title=title)
    _handle_save(fig, save_as)
    return ChartResult(fig, stats={"n_points": len(np.asarray(x))})


def violin_chart(
    data: Any,
    groups: Optional[Sequence[str]] = None,
    *,
    style: Union[str, Style] = "graphpad_prism",
    save_as: Optional[Union[str, Path]] = None,
    figsize: Optional[tuple[float, float]] = None,
    dpi: int = 300,
    split: bool = False,
    split_labels: Optional[list[str]] = None,
    bandwidth: str = "scott",
    points: int = 60,
    widths: float = 0.7,
    cut: float = 1.5,
    show_n: bool = True,
    title: Optional[str] = None,
    ylabel: Optional[str] = None,
) -> ChartResult:
    ctxt = StyleContext(style)
    ctxt.apply(plt.rcParams, "violin")
    if figsize is None:
        figsize = (5, 5)
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    if split:
        handles = violin.render_split(
            ax, data, points=points, widths=widths, cut=cut,
            bandwidth=bandwidth, labels=split_labels, show_n=show_n,
        )
        if split_labels:
            ax.legend(handles=handles, frameon=False, loc="upper right")
    else:
        violin.render(ax, data, points=points, widths=widths,
                      cut=cut, bandwidth=bandwidth, show_n=show_n)

    x_positions = np.arange(len(data))
    ax.set_xticks(x_positions)
    if groups is not None:
        ax.set_xticklabels(list(groups))

    _label(ax, ylabel=ylabel, title=title)
    _handle_save(fig, save_as)
    return ChartResult(fig, stats={"n_groups": len(data)})


def box_violin_chart(
    data: Any,
    groups: Optional[Sequence[str]] = None,
    *,
    style: Union[str, Style] = "graphpad_prism",
    save_as: Optional[Union[str, Path]] = None,
    figsize: Optional[tuple[float, float]] = None,
    dpi: int = 300,
    split: bool = False,
    split_labels: Optional[list[str]] = None,
    bandwidth: str = "scott",
    v_widths: float = 0.7,
    b_widths: float = 0.1,
    points: int = 60,
    cut: float = 1.5,
    show_n: bool = True,
    title: Optional[str] = None,
    ylabel: Optional[str] = None,
) -> ChartResult:
    ctxt = StyleContext(style)
    ctxt.apply(plt.rcParams, "box_violin")
    if figsize is None:
        figsize = (5, 5)
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    if split:
        handles = boxviolin.render_split(
            ax, data, v_widths=v_widths, b_widths=b_widths,
            points=points, cut=cut, bandwidth=bandwidth,
            labels=split_labels, show_n=show_n,
        )
        if split_labels:
            ax.legend(handles=handles, frameon=False, loc="upper right")
    else:
        boxviolin.render(
            ax, data, v_widths=v_widths, b_widths=b_widths,
            points=points, cut=cut, bandwidth=bandwidth,
            show_n=show_n,
        )

    x_positions = np.arange(len(data))
    ax.set_xticks(x_positions)
    if groups is not None:
        ax.set_xticklabels(list(groups))

    _label(ax, ylabel=ylabel, title=title)
    _handle_save(fig, save_as)
    return ChartResult(fig, stats={"n_groups": len(data)})


def _handle_save(fig: plt.Figure, save_as: Optional[Union[str, Path]]) -> None:
    if save_as is not None:
        fig.savefig(Path(save_as), bbox_inches="tight")
    else:
        fig.tight_layout()


def _label(
    ax: plt.Axes,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    title: Optional[str] = None,
) -> None:
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)


def _resolve_frame(
    data: Any,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
) -> tuple[Any, Optional[Any]]:
    if x_col is None and y_col is None:
        return data, None
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("pandas is required when using x=/y= parameters") from None
    if not isinstance(data, pd.DataFrame):
        raise TypeError("x=/y= parameters require a pandas DataFrame")

    values = data[y_col].values if y_col else data
    groups = data[x_col].values if x_col else None
    return values, groups
