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
    return list(_discover_styles().values())


def list_styles_for(chart_type: str) -> list[dict[str, Any]]:
    return [s for s in _discover_styles().values() if chart_type in s["chart_types"]]


def get_style(name: str) -> dict[str, Any] | None:
    return _discover_styles().get(name)


def clear_cache() -> None:
    global _STYLES_CACHE
    _STYLES_CACHE = None


class Style:
    def __init__(self, name: str):
        self._info = get_style(name)
        if self._info is None:
            msg = f"Unknown style: '{name}'. Available: {[s['name'] for s in list_styles()]}"
            raise ValueError(msg)

    @property
    def name(self) -> str:
        return self._info["name"]

    @property
    def info(self) -> dict[str, Any]:
        return dict(self._info)

    def apply(self, rcParams: dict | None = None, chart_type: str | None = None) -> None:
        import matplotlib.pyplot as plt

        if chart_type is not None and chart_type not in self._info["chart_types"]:
            warnings.warn(
                f"Style '{self.name}' does not declare compatibility with "
                f"chart type '{chart_type}'. Visual output may not be as intended. "
                f"Declared chart types: {self._info['chart_types']}",
                stacklevel=2,
            )

        if self._info["base_style"]:
            plt.style.use(self._info["base_style"])
        if chart_type and chart_type in self._info["chart_styles"]:
            plt.style.use(self._info["chart_styles"][chart_type])
