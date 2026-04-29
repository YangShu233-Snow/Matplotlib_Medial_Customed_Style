"""Figure export utilities.

Provides ``save_figure`` for saving a figure in multiple formats
(PNG, PDF) to a specified directory.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence, Union

import matplotlib.pyplot as plt


def save_figure(
    fig: plt.Figure,
    save_dir: Union[str, Path],
    img_name: str,
    formats: Optional[Sequence[str]] = None,
    dpi: int = 300,
    bbox_inches: str = "tight",
    tight_layout: bool = True,
) -> list[Path]:
    """Save a matplotlib figure in one or more formats.

    Creates the output directory if it does not exist.

    Args:
        fig: The matplotlib Figure to save.
        save_dir: Directory path for the output files.
        img_name: Base filename (without extension).
        formats: File extensions to save. Defaults to ``("png", "pdf")``.
        dpi: Output resolution in dots per inch.
        bbox_inches: ``bbox_inches`` argument passed to
            ``fig.savefig()``.
        tight_layout: Whether to call ``fig.tight_layout()`` before
            saving.

    Returns:
        A list of ``Path`` objects for each saved file.

    Example:
        >>> fig, ax = plt.subplots()
        >>> ax.plot([1, 2, 3])
        >>> paths = save_figure(fig, "output", "my_plot")
        >>> paths
        [PosixPath('output/my_plot.png'), PosixPath('output/my_plot.pdf')]
    """
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    if formats is None:
        formats = ("png", "pdf")

    if tight_layout:
        fig.tight_layout()

    saved: list[Path] = []
    for ext in formats:
        path = save_dir / f"{img_name}.{ext}"
        fig.savefig(path, dpi=dpi, bbox_inches=bbox_inches)
        saved.append(path)

    return saved
