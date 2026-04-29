"""Style discovery, metadata loading, and style application.

This module provides the foundational style management system for mmcs.
It auto-discovers ``.mplstyle`` files and their ``metadata.json`` from
the ``styles/`` directory tree.
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

_STYLES_DIR = Path(__file__).parent / "styles"
_STYLES_CACHE: dict[str, dict[str, Any]] | None = None


def _discover_styles() -> dict[str, dict[str, Any]]:
    global _STYLES_CACHE
    if _STYLES_CACHE is not None:
        return _STYLES_CACHE

    styles: dict[str, dict[str, Any]] = {}
    for meta_path in sorted(_STYLES_DIR.glob("*/metadata.json")):
        with open(meta_path) as f:
            meta = json.load(f)

        name = meta["name"]
        style_dir = meta_path.parent

        base_style = meta.get("base_style")
        base_style_path: str | None = None
        if base_style:
            base_style_path = str(style_dir / base_style)

        chart_styles: dict[str, str] = {}
        for chart_type, style_file in meta.get("chart_styles", {}).items():
            chart_styles[chart_type] = str(style_dir / style_file)

        styles[name] = {
            "name": name,
            "category": meta.get("category", ""),
            "display_name": meta.get("display_name", ""),
            "chart_types": meta.get("chart_types", []),
            "description": meta.get("description", ""),
            "base_style": base_style_path,
            "chart_styles": chart_styles,
            "style_dir": str(style_dir),
        }

    _STYLES_CACHE = styles
    return styles


def list_styles() -> list[dict[str, Any]]:
    """List all available styles with their metadata.

    Returns:
        A list of style info dicts. Each dict contains:
        ``name``, ``category``, ``display_name``, ``chart_types``,
        ``description``, ``base_style``, ``chart_styles``, ``style_dir``.

    Example:
        >>> styles = mmcs.list_styles()
        >>> styles[0]["name"]
        'graphpad_prism'
    """
    return list(_discover_styles().values())


def list_styles_for(chart_type: str) -> list[dict[str, Any]]:
    """List styles that declare compatibility with a given chart type.

    Args:
        chart_type: The chart type name to filter by (e.g. ``"bar"``,
            ``"heatmap"``).

    Returns:
        A list of style info dicts whose ``chart_types`` includes
        ``chart_type``.

    Example:
        >>> mmcs.list_styles_for("bar")
        [{"name": "graphpad_prism", ...}]
    """
    return [s for s in _discover_styles().values() if chart_type in s["chart_types"]]


def get_style(name: str) -> dict[str, Any] | None:
    """Get metadata for a single style by name.

    Args:
        name: The style name (e.g. ``"graphpad_prism"``).

    Returns:
        The style info dict, or ``None`` if no style with that name exists.
    """
    return _discover_styles().get(name)


def clear_cache() -> None:
    """Clear the internal style discovery cache.

    Call this if you modify style files or metadata after import
    and need to force re-discovery.
    """
    global _STYLES_CACHE
    _STYLES_CACHE = None


class Style:
    """A named style that manages ``.mplstyle`` file loading.

    ``Style`` wraps a style discovered from the ``styles/`` directory
    and provides ``apply()`` to load its ``rcParams`` into matplotlib.

    Args:
        name: The style name. Must match a directory name under
            ``mmcs/styles/``.

    Raises:
        ValueError: If ``name`` does not correspond to any installed style.

    Example:
        >>> style = Style("graphpad_prism")
        >>> style.apply(plt.rcParams, chart_type="bar")
    """

    def __init__(self, name: str):
        self._info = get_style(name)
        if self._info is None:
            msg = f"Unknown style: '{name}'. Available: {[s['name'] for s in list_styles()]}"
            raise ValueError(msg)

    @property
    def name(self) -> str:
        """The style's unique identifier (e.g. ``"graphpad_prism"``)."""
        return self._info["name"]

    @property
    def info(self) -> dict[str, Any]:
        """A copy of the style's full metadata dict."""
        return dict(self._info)

    def apply(self, rcParams: dict | None = None, chart_type: str | None = None) -> None:
        """Load the style's ``rcParams`` into matplotlib.

    Loads the base ``.mplstyle`` file, then optionally a chart-type-specific
    override. If ``chart_type`` is not declared in the style's metadata
    (neither in ``chart_types`` nor as a ``chart_styles`` key), a
    ``UserWarning`` is issued.

        Args:
            rcParams: Ignored. Provided for API compatibility with
                ``matplotlib.rcParams``.
            chart_type: Optional chart type to load a type-specific
                style override (e.g. ``"bar"``, ``"violin"``).

        Warns:
            UserWarning: If ``chart_type`` is not known to this style.
        """
        import matplotlib.pyplot as plt

        if chart_type is not None:
            known = set(self._info["chart_types"]) | set(self._info["chart_styles"].keys())
            if chart_type not in known:
                warnings.warn(
                    f"Style '{self.name}' does not declare compatibility with "
                    f"chart type '{chart_type}'. Visual output may not be as intended. "
                    f"Declared: {sorted(known)}",
                    stacklevel=2,
                )

        if self._info["base_style"]:
            plt.style.use(self._info["base_style"])
        if chart_type and chart_type in self._info["chart_styles"]:
            plt.style.use(self._info["chart_styles"][chart_type])
