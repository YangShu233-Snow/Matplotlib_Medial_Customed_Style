from __future__ import annotations

import base64
import io
from pathlib import Path
from typing import Any, Optional, Union

import matplotlib.pyplot as plt


class ChartResult:
    def __init__(self, fig: plt.Figure, stats: Optional[dict[str, Any]] = None):
        self.fig = fig
        self.stats = stats or {}

    def to_base64(self, fmt: str = "png", dpi: int = 300) -> str:
        buf = io.BytesIO()
        self.fig.savefig(buf, format=fmt, dpi=dpi, bbox_inches="tight")
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")


def _handle_save(fig: plt.Figure, save_as: Optional[Union[str, Path]]) -> None:
    """Save a figure or call tight_layout.

    If ``save_as`` is provided, saves the figure to that path.
    Otherwise calls ``fig.tight_layout()``.

    For figures created with ``plt.subplots()``.
    """
    if save_as is not None:
        fig.savefig(Path(save_as), bbox_inches="tight")
    else:
        fig.tight_layout()


def _handle_save_gs(fig: plt.Figure, save_as: Optional[Union[str, Path]]) -> None:
    """Save a GridSpec-based figure.

    Like ``_handle_save`` but does NOT call ``tight_layout``
    (which misbehaves with ``GridSpec`` layouts).

    For figures created with ``fig.add_gridspec()``.
    """
    if save_as is not None:
        fig.savefig(Path(save_as), bbox_inches="tight")


def _label(
    ax: plt.Axes,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    title: Optional[str] = None,
) -> None:
    """Set axis label(s) if provided.

    Each of ``xlabel``, ``ylabel``, ``title`` is set independently;
    ``None`` values are silently skipped.
    """
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)


_X_COL_NAMES = {
    "group", "groups", "treatment", "condition", "category", "categories",
    "genotype", "strain", "celltype", "cell_type", "sample", "samples",
    "timepoint", "time", "dose", "concentration",
}

_Y_COL_NAMES = {
    "value", "values", "expression", "signal", "score", "intensity",
    "count", "counts", "level", "levels", "measurement", "measurements",
    "response", "activity", "fold_change", "foldchange",
}


def _auto_detect_columns(df: Any) -> tuple[Optional[str], Optional[str]]:
    """Automatically infer x (group) and y (value) columns from a DataFrame.

    Uses a two-pass strategy:
    1. Match column names (case-insensitive) against known name sets.
    2. Fallback: first categorical column → x, first numeric column → y.

    Args:
        df: A pandas DataFrame.

    Returns:
        A tuple ``(x_col_name, y_col_name)`` where either may be
        ``None`` if no suitable column was found.
    """
    x_col: Optional[str] = None
    y_col: Optional[str] = None

    num_cols = [c for c in df.columns if hasattr(df[c], "dtype") and df[c].dtype.kind in "iufcb"]
    cat_cols = [c for c in df.columns if c not in num_cols]

    for col in df.columns:
        key = col.lower().replace(" ", "_").replace("-", "_")
        if key in _X_COL_NAMES and x_col is None:
            x_col = col
        if key in _Y_COL_NAMES and y_col is None and col in num_cols:
            y_col = col

    if x_col is None and cat_cols:
        x_col = cat_cols[0]
    if y_col is None and num_cols:
        if x_col and x_col in num_cols:
            remaining = [c for c in num_cols if c != x_col]
            if remaining:
                y_col = remaining[0]
        else:
            y_col = num_cols[0]

    return x_col, y_col


def _resolve_frame(
    data: Any,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
) -> tuple[Any, Optional[Any]]:
    """Extract values and group labels from a DataFrame or raw data.

    When both ``x_col`` and ``y_col`` are ``None``, behaves as a
    pass-through for non-DataFrame inputs. For DataFrames, attempts
    automatic column detection via ``_auto_detect_columns()``.

    When either is set, validates the DataFrame and extracts the
    named columns.

    Args:
        data: A pandas DataFrame, or raw data (list / array).
        x_col: Name of the column to use as group labels.
        y_col: Name of the column to use as values.

    Returns:
        A tuple ``(values, groups)``. ``groups`` is ``None`` when
        no x column is available.

    Raises:
        ImportError: If ``x_col`` or ``y_col`` is set but pandas is
            not installed.
        TypeError: If ``x_col`` or ``y_col`` is set but ``data`` is
            not a DataFrame.
    """
    if x_col is None and y_col is None:
        try:
            import pandas as pd
        except ImportError:
            return data, None
        if isinstance(data, pd.DataFrame):
            auto_x, auto_y = _auto_detect_columns(data)
            if auto_x is not None and auto_y is not None:
                return data[auto_y].values, data[auto_x].values
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


from mmcs._quick_api._bar import bar_chart  # noqa: E402
from mmcs._quick_api._box import box_chart  # noqa: E402
from mmcs._quick_api._boxviolin import box_violin_chart  # noqa: E402
from mmcs._quick_api._bubble import bubble_chart  # noqa: E402
from mmcs._quick_api._clustered_columns import clustered_columns_chart  # noqa: E402
from mmcs._quick_api._density import density_chart  # noqa: E402
from mmcs._quick_api._heatmap import (  # noqa: E402
    heatmap_aggregate_chart,
    heatmap_chart,
)
from mmcs._quick_api._histogram import histogram_chart  # noqa: E402
from mmcs._quick_api._regression import regression_chart  # noqa: E402
from mmcs._quick_api._scatter import (  # noqa: E402
    scatter_chart,
    scatter_clustered_chart,
)
from mmcs._quick_api._violin import violin_chart  # noqa: E402

__all__ = [
    "ChartResult",
    "bar_chart",
    "box_chart",
    "box_violin_chart",
    "bubble_chart",
    "clustered_columns_chart",
    "density_chart",
    "heatmap_aggregate_chart",
    "heatmap_chart",
    "histogram_chart",
    "regression_chart",
    "scatter_chart",
    "scatter_clustered_chart",
    "violin_chart",
]
