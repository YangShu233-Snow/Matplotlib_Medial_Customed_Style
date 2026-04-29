from __future__ import annotations

import numpy as np
from matplotlib.axes import Axes
from scipy.stats import f


def render(
    ax: Axes,
    x: np.ndarray,
    y: np.ndarray,
    *,
    xlabel: str = "X Value",
    ylabel: str = "Y Value",
    scatter_size: float = 2.0,
) -> Axes:
    """Draw a scatter plot with linear regression line.

    Computes and displays the regression equation, R-squared, and
    p-value (from F-test) in the top-left corner of the axes.

    Args:
        ax: The matplotlib Axes to draw on.
        x: X-coordinates.
        y: Y-coordinates.
        xlabel: X-axis label.
        ylabel: Y-axis label.
        scatter_size: Marker radius in points.

    Returns:
        The matplotlib Axes with the chart drawn.
    """
    x_arr = np.asarray(x).ravel()
    y_arr = np.asarray(y).ravel()
    n = len(x_arr)

    slope, intercept = np.polyfit(x_arr, y_arr, deg=1)
    y_pred = x_arr * slope + intercept

    sst = np.sum((y_arr - np.mean(y_arr)) ** 2)
    ssr = np.sum((y_arr - y_pred) ** 2)
    r2 = 1.0 - ssr / sst
    f_val = r2 / (1.0 - r2) * (n - 2)
    p_val = 1.0 - f.cdf(f_val, 1, n - 2)

    ax.scatter(x_arr, y_arr, s=np.pi * scatter_size ** 2)

    order = np.argsort(x_arr)
    ax.plot(x_arr[order], y_pred[order])

    p_str = "< 0.0001" if p_val < 0.0001 else f"= {p_val:.4f}"
    stats_text = f"$R^2$ = {r2:.3f}\n$P$ {p_str}"
    ax.text(0.05, 0.95, stats_text, transform=ax.transAxes,
            va="top", ha="left")

    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)

    return ax
