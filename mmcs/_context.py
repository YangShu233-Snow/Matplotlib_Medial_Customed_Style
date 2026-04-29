"""Runtime style-aware dynamic value injection.

``StyleContext`` bridges the gap between static ``.mplstyle`` files
and runtime data-dependent decisions (e.g. how many colors to allocate,
how large annotation text should be).
"""

from __future__ import annotations

from typing import Any, Union

from matplotlib import pyplot as plt

from mmcs._registry import Style


class StyleContext:
    """A runtime helper that provides style-aware default values.

    ``StyleContext`` reads a style's ``rcParams`` (after ``apply()``),
    examines the runtime data, and returns sensible defaults such as
    bar colors, scatter colors, or box fill colors.

    It is the recommended way to obtain chart colors so that they
    stay consistent with the active style.

    Args:
        style: A style name (``str``) or a ``Style`` instance.

    Example:
        >>> ctxt = StyleContext("graphpad_prism")
        >>> ctxt.apply(plt.rcParams, chart_type="bar")
        >>> colors = ctxt.bar_colors(2)
        >>> colors
        ['003366', 'D32F2F']
    """

    def __init__(self, style: Union[str, Style]) -> None:
        if isinstance(style, str):
            style = Style(style)
        self._style = style

    @property
    def name(self) -> str:
        """The underlying style's name."""
        return self._style.name

    @property
    def info(self) -> dict[str, Any]:
        """A copy of the underlying style's full metadata dict."""
        return self._style.info

    def apply(self, rcParams: dict | None = None, chart_type: str | None = None) -> None:
        """Load the style's rcParams via ``Style.apply()``.

        This must be called before any color methods so that
        ``axes.prop_cycle`` reflects the correct palette.

        Args:
            rcParams: Passed through to ``Style.apply()``.
            chart_type: Passed through to ``Style.apply()``.
        """
        self._style.apply(rcParams, chart_type=chart_type)

    def bar_colors(self, n: int) -> list[str]:
        """Generate ``n`` bar colors by uniform sampling from the palette.

        When ``n >= palette_size``, colors cycle: ``P[i % N]``.
        When ``n < palette_size``, the palette is sampled evenly to
        maximize visual contrast (e.g. 2 bars from an 8-color palette
        get ``P[0]`` and ``P[7]``).

        Args:
            n: Number of colors requested (usually the number of bars).

        Returns:
            A list of ``n`` hex color strings (without ``#`` prefix).
        """
        palette = self._read_palette()
        if n >= len(palette):
            return [palette[i % len(palette)] for i in range(n)]
        return [_uniform_sample(palette, i, n) for i in range(n)]

    def scatter_colors(self) -> list[str]:
        """Return the full palette for scatter points.

        Returns:
            The complete palette as a list of hex color strings.
        """
        return self._read_palette()

    def box_colors(self) -> str:
        """Return the first color of the palette for box fill.

        Returns:
            A single hex color string, or ``"CCCCCC"`` if the palette
            is empty.
        """
        palette = self._read_palette()
        return palette[0] if palette else "CCCCCC"

    def _read_palette(self) -> list[str]:
        cycle = plt.rcParams.get("axes.prop_cycle")
        if cycle is not None:
            return [entry["color"] for entry in cycle]
        return []


def _uniform_sample(palette: list[str], idx: int, total: int) -> str:
    n = len(palette)
    k = round(idx * (n - 1) / (total - 1)) if total > 1 else 0
    return palette[k]
