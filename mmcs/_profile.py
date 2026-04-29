from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Sequence, Union

import numpy as np

from mmcs._quick_api import (
    ChartResult,
    bar_chart,
    box_chart,
    box_violin_chart,
    bubble_chart,
    clustered_columns_chart,
    density_chart,
    heatmap_chart,
    histogram_chart,
    regression_chart,
    scatter_chart,
    violin_chart,
)


class _ProfilePresets:
    @staticmethod
    def grouped_columns(
        groups_data: Sequence[tuple[str, Sequence[str], Sequence[np.ndarray]]],
        *,
        comparisons: Optional[Sequence[tuple[int, int, int, int]]] = None,
        style: str = "graphpad_prism",
        save_as: Optional[Union[str, Path]] = None,
        figsize: tuple[float, float] = (8, 6),
        ylabel: Optional[str] = None,
        title: Optional[str] = None,
    ) -> ChartResult:
        return clustered_columns_chart(
            groups_data=groups_data,
            comparisons=comparisons,
            style=style,
            save_as=save_as,
            figsize=figsize,
            ylabel=ylabel,
            title=title,
        )

    @staticmethod
    def single_column(
        values: Any,
        groups: Optional[Sequence[str]] = None,
        *,
        errors: Optional[Sequence[float]] = None,
        style: str = "graphpad_prism",
        save_as: Optional[Union[str, Path]] = None,
        ylabel: Optional[str] = None,
        title: Optional[str] = None,
    ) -> ChartResult:
        return bar_chart(
            data=values,
            groups=groups,
            errors=errors,
            style=style,
            save_as=save_as,
            upper_only=True,
            edge=True,
            ylabel=ylabel,
            title=title,
        )

    @staticmethod
    def bar_scatter(
        values: Any,
        scatter_data: Sequence[np.ndarray],
        groups: Optional[Sequence[str]] = None,
        *,
        errors: Optional[Sequence[float]] = None,
        style: str = "graphpad_prism",
        save_as: Optional[Union[str, Path]] = None,
        ylabel: Optional[str] = None,
        title: Optional[str] = None,
    ) -> ChartResult:
        return bar_chart(
            data=values,
            groups=groups,
            errors=errors,
            scatter_data=scatter_data,
            style=style,
            save_as=save_as,
            upper_only=True,
            edge=True,
            ylabel=ylabel,
            title=title,
        )

    @staticmethod
    def boxplot(
        data: Any,
        groups: Optional[Sequence[str]] = None,
        *,
        style: str = "graphpad_prism",
        save_as: Optional[Union[str, Path]] = None,
        ylabel: Optional[str] = None,
        title: Optional[str] = None,
    ) -> ChartResult:
        return box_chart(
            data=data,
            groups=groups,
            style=style,
            save_as=save_as,
            show_n=True,
            ylabel=ylabel,
            title=title,
        )

    @staticmethod
    def violin(
        data: Any,
        groups: Optional[Sequence[str]] = None,
        *,
        style: str = "graphpad_prism",
        save_as: Optional[Union[str, Path]] = None,
        bandwidth: str = "scott",
        show_n: bool = True,
        ylabel: Optional[str] = None,
        title: Optional[str] = None,
    ) -> ChartResult:
        return violin_chart(
            data=data,
            groups=groups,
            style=style,
            save_as=save_as,
            bandwidth=bandwidth,
            show_n=show_n,
            ylabel=ylabel,
            title=title,
        )

    @staticmethod
    def box_violin(
        data: Any,
        groups: Optional[Sequence[str]] = None,
        *,
        style: str = "graphpad_prism",
        save_as: Optional[Union[str, Path]] = None,
        split: bool = False,
        split_labels: Optional[list[str]] = None,
        ylabel: Optional[str] = None,
        title: Optional[str] = None,
    ) -> ChartResult:
        return box_violin_chart(
            data=data,
            groups=groups,
            style=style,
            save_as=save_as,
            split=split,
            split_labels=split_labels,
            ylabel=ylabel,
            title=title,
        )

    @staticmethod
    def scatter(
        x: Any,
        y: Any,
        *,
        style: str = "graphpad_prism",
        save_as: Optional[Union[str, Path]] = None,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        title: Optional[str] = None,
    ) -> ChartResult:
        return scatter_chart(
            x=x,
            y=y,
            style=style,
            save_as=save_as,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
        )

    @staticmethod
    def correlation(
        x: Any,
        y: Any,
        *,
        style: str = "graphpad_prism",
        save_as: Optional[Union[str, Path]] = None,
        xlabel: str = "X Value",
        ylabel: str = "Y Value",
        title: Optional[str] = None,
    ) -> ChartResult:
        return regression_chart(
            x=x,
            y=y,
            style=style,
            save_as=save_as,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
        )

    @staticmethod
    def histogram(
        data: Any,
        *,
        style: str = "graphpad_prism",
        save_as: Optional[Union[str, Path]] = None,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        title: Optional[str] = None,
    ) -> ChartResult:
        return histogram_chart(
            data=data,
            style=style,
            save_as=save_as,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
        )

    @staticmethod
    def density(
        data: Any,
        groups: Optional[Sequence[str]] = None,
        *,
        style: str = "graphpad_prism",
        save_as: Optional[Union[str, Path]] = None,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        title: Optional[str] = None,
    ) -> ChartResult:
        return density_chart(
            data=data,
            groups=groups,
            style=style,
            save_as=save_as,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
        )

    @staticmethod
    def heatmap(
        data: Any,
        *,
        row_labels: Optional[Sequence[str]] = None,
        col_labels: Optional[Sequence[str]] = None,
        style: str = "deeptools",
        save_as: Optional[Union[str, Path]] = None,
        title: Optional[str] = None,
    ) -> ChartResult:
        return heatmap_chart(
            data=data,
            row_labels=row_labels,
            col_labels=col_labels,
            style=style,
            save_as=save_as,
            title=title,
        )

    @staticmethod
    def bubble(
        categories: Sequence[str],
        x_values: Any,
        bubble_sizes: Any,
        color_values: Any,
        *,
        style: str = "ggplot",
        save_as: Optional[Union[str, Path]] = None,
        title: Optional[str] = None,
    ) -> ChartResult:
        return bubble_chart(
            categories=categories,
            x_values=x_values,
            bubble_sizes=bubble_sizes,
            color_values=color_values,
            style=style,
            save_as=save_as,
            title=title,
        )


profile = _ProfilePresets()
