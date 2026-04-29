from __future__ import annotations

from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from mmcs._utils._annotation import jitter


def render(
    ax: Axes,
    groups: Sequence[tuple[str, Sequence[str], Sequence[np.ndarray]]],
    *,
    bar_width: float = 0.3,
    scatter_r: float = 1.5,
    comparisons: Sequence[tuple[int, int, int, int]] | None = None,
    fraction_length: int = 20,
) -> Axes:
    """Draw a clustered column chart with jittered scatter overlay.

    Each category on the x-axis contains multiple sub-groups (bars).
    Each bar is overlaid with jittered individual data points.
    Optionally draws comparison lines with significance stars
    between selected sub-groups.

    Args:
        ax: The matplotlib Axes to draw on.
        groups: A list of ``(category_name, sub_group_names,
            raw_data_arrays)`` tuples.
        bar_width: Width of each bar.
        scatter_r: Marker radius for jittered scatter points.
        comparisons: A list of ``(cat_idx, sub_a_idx, sub_b_idx,
            n_stars)`` tuples specifying which sub-groups to compare.
        fraction_length: Scaling factor for comparison line and
            star placement.

    Returns:
        The matplotlib Axes with the chart drawn.
    """
    n_categories = len(groups)
    all_means: list[list[float]] = []
    all_errs: list[list[float]] = []
    all_raw: list[list[np.ndarray]] = []
    all_names: list[str] = []
    all_bar_pos: list[float] = []

    for cat_name, sub_names, raw_data_list in groups:
        means = [float(np.mean(d)) for d in raw_data_list]
        errs = [float(np.std(d, ddof=1) / np.sqrt(len(d))) for d in raw_data_list]
        all_means.append(means)
        all_errs.append(errs)
        all_raw.append([np.asarray(d).ravel() for d in raw_data_list])
        all_names.extend(sub_names)

    flat = [m for ms in all_means for m in ms]
    total = len(flat)

    x_base = np.linspace(0, (total + n_categories - 1) * bar_width * 2, total + n_categories)
    fig_w = ax.figure.get_figwidth() if hasattr(ax.figure, "get_figwidth") else 10
    fig_h = ax.figure.get_figheight() if hasattr(ax.figure, "get_figheight") else 6

    group_idx = 0
    for cat_idx in range(n_categories):
        means = all_means[cat_idx]
        errs = all_errs[cat_idx]
        raw = all_raw[cat_idx]
        n_sub = len(means)
        colors = [str(g) for g in np.linspace(0.1, 0.8, n_sub)]

        x_positions: list[float] = []
        for i in range(n_sub):
            x_pos = x_base[group_idx] + bar_width
            group_idx += 1
            x_positions.append(x_pos)
            all_bar_pos.append(x_pos)

            ax.bar(x_pos, means[i], yerr=[errs[i]], width=bar_width,
                   align="center", color=colors[i])

        for i, d in enumerate(raw):
            r_x = total / fig_w * scatter_r / 54
            r_y = max(flat) / fig_h * scatter_r / 54 if max(flat) != 0 else scatter_r / 72
            x_jit = jitter(d, r_x, r_y) + x_positions[i]
            ax.scatter(x_jit, d, color="white", edgecolor="black",
                       alpha=0.75, linewidths=plt.rcParams.get("lines.linewidth", 1.0),
                       s=np.pi * scatter_r ** 2)

        group_idx += 1

    ax.set_xticks(x_base)
    ax.set_xticklabels([])
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.set_xticks(all_bar_pos, minor=True)
    ax.set_xticklabels(all_names, minor=True, rotation=45)

    if comparisons:
        cat_groups: dict[int, list[tuple[int, int, int]]] = {}
        for cat_idx, sub_a, sub_b, n_stars in comparisons:
            cat_groups.setdefault(cat_idx, []).append((sub_a, sub_b, n_stars))

        start = 0
        for cat_idx, cat_comps in cat_groups.items():
            n_sub = len(all_means[cat_idx])
            _draw_category_comparisons(
                ax, cat_comps, all_bar_pos[start:start + n_sub],
                all_raw[cat_idx], all_means[cat_idx], all_errs[cat_idx],
                fraction_length,
            )
            start += n_sub

    return ax


def _draw_category_comparisons(
    ax: Axes,
    comps: list[tuple[int, int, int]],
    bar_pos: list[float],
    raw_data: list[np.ndarray],
    means: list[float],
    errs: list[float],
    fraction_length: int,
) -> None:
    max_y_line = 0.0
    max_y_star = 0.0
    min_gap = 20 * fraction_length

    for sub_a, sub_b, n_stars in comps:
        x1, x2 = bar_pos[sub_a], bar_pos[sub_b]
        d_a, d_b = raw_data[sub_a], raw_data[sub_b]
        m_a, e_a = means[sub_a], errs[sub_a]
        m_b, e_b = means[sub_b], errs[sub_b]

        top = max(float(np.max(d_a)), m_a + e_a,
                  float(np.max(d_b)), m_b + e_b)

        if top - max_y_star > min_gap:
            max_y_line = top
        else:
            max_y_line += min_gap
            top = max_y_line

        line_y = top + fraction_length * 5
        max_y_star = max(line_y, max_y_star)

        ax.plot([x1, x1, x2, x2],
                [line_y - fraction_length, line_y, line_y, line_y - fraction_length],
                c="black", linewidth=1.0)
        ax.text((x1 + x2) / 2, line_y, "*" * n_stars, ha="center", va="bottom")
