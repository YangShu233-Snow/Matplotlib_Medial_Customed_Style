"""Annotation and data-jittering helpers.

Provides ``draw_sample_sizes`` for adding ``n=...`` labels above
chart elements and ``jitter`` for computing non-overlapping scatter
positions.
"""

from __future__ import annotations

from typing import List, Optional

import numpy as np
from matplotlib.axes import Axes


def draw_sample_sizes(
    ax: Axes,
    data: List[np.ndarray],
    x_positions: np.ndarray,
    offset: Optional[float] = None,
    offset_factor: Optional[float] = None,
    fontsize: float = 10,
) -> None:
    """Annotate sample sizes above each group of data points.

    Adds ``n=<count>`` text labels above the maximum value of each
    data array.

    Args:
        ax: The matplotlib Axes to draw on.
        data: One array per group. The length of each array determines
            the ``n`` value.
        x_positions: X-axis positions for the labels, one per group.
        offset: Absolute vertical offset from the top of each group's
            data. If set, ``offset_factor`` is ignored.
        offset_factor: Vertical offset as a multiple of the group's
            standard deviation. Ignored if ``offset`` is set.
        fontsize: Font size for the label text.
    """
    for i, d in enumerate(data):
        n = len(d)
        top_val = np.max(d)

        if offset is not None:
            y_pos = top_val + offset
        elif offset_factor is not None:
            y_pos = top_val + float(np.std(d)) * offset_factor
        else:
            y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
            y_pos = top_val + y_range * 0.02

        ax.text(
            x_positions[i],
            y_pos,
            f"n={n}",
            ha="center",
            va="bottom",
            fontsize=fontsize,
        )


def jitter(
    y: np.ndarray,
    r_x: float,
    r_y: float,
) -> np.ndarray:
    """Compute non-overlapping jitter positions for scatter overlay.

    Uses a greedy rectangle-packing algorithm: data points are sorted
    by y-value and each point is assigned the x-offset closest to zero
    that does not overlap any already-placed point's bounding box.

    Args:
        y: Y-values of the data points.
        r_x: Half-width of the marker bounding box in data units.
        r_y: Half-height of the marker bounding box in data units.

    Returns:
        An array of x-offsets (same length as ``y``) to be added to
        each point's nominal x-position.
    """
    n = len(y)
    x = np.zeros(n)
    D_x = 2 * r_x
    D_y = 2 * r_y

    sorted_idx = np.argsort(y, kind="stable")
    placed: list[int] = []

    for idx in sorted_idx:
        y_i = float(y[idx])
        conflicts = []
        for p_idx in reversed(placed):
            if y_i - float(y[p_idx]) >= D_y:
                break
            conflicts.append(p_idx)

        if not conflicts:
            x[idx] = 0.0
            placed.append(idx)
            continue

        intervals = []
        for c_idx in conflicts:
            dy = y_i - float(y[c_idx])
            y_ratio_sq = (dy / D_y) ** 2
            if y_ratio_sq >= 1.0:
                continue
            dx = D_x * np.sqrt(1.0 - y_ratio_sq) + 1e-8
            x_c = float(x[c_idx])
            intervals.append((x_c - dx, x_c + dx))

        candidates = [0.0]
        for lo, hi in intervals:
            candidates.extend([lo, hi])
        candidates.sort(key=lambda v: (abs(v), v))

        chosen = 0.0
        for cand in candidates:
            if all(not (lo < cand < hi) for lo, hi in intervals):
                chosen = cand
                break

        x[idx] = chosen
        placed.append(idx)

    return np.asarray(x, dtype=float)
