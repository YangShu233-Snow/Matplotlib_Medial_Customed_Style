"""
mmcs - Matplotlib Medical Customized Styles.

A library providing publication-ready matplotlib styles and chart builders
designed for the medical and biological sciences.
"""

__version__ = "0.1.0"

from mmcs._context import StyleContext
from mmcs._quick_api import (
    ChartResult,
    bar_chart,
    box_chart,
    box_violin_chart,
    scatter_chart,
    violin_chart,
)
from mmcs._registry import Style, get_style, list_styles, list_styles_for
from mmcs._utils._export import save_figure

__all__ = [
    "Style",
    "StyleContext",
    "ChartResult",
    "bar_chart",
    "box_chart",
    "box_violin_chart",
    "scatter_chart",
    "violin_chart",
    "save_figure",
    "list_styles",
    "list_styles_for",
    "get_style",
    "__version__",
]
