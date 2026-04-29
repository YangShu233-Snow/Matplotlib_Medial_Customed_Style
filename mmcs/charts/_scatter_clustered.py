from __future__ import annotations

from typing import Any, Generator, Optional, Tuple

import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap
from matplotlib.patches import Ellipse
from scipy.spatial import ConvexHull
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors


def render(
    ax: Axes,
    x: np.ndarray,
    y: np.ndarray,
    *,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    color_by_cluster: bool = True,
    show_convex_hull: bool = True,
    show_confidence_ellipse: bool = True,
    min_samples: int = 4,
    scatter_size: float = 1.0,
) -> Axes:
    """Draw a DBSCAN-clustered scatter plot.

    Automatically estimates the DBSCAN ``eps`` parameter using the
    knee-point method. Optionally draws convex hulls and confidence
    ellipses for each cluster.

    Args:
        ax: The matplotlib Axes to draw on.
        x: X-coordinates.
        y: Y-coordinates.
        xlabel: X-axis label.
        ylabel: Y-axis label.
        color_by_cluster: If True, color points by their cluster label.
        show_convex_hull: If True, draw convex hull boundaries for
            each cluster.
        show_confidence_ellipse: If True, draw a 2-sigma confidence
            ellipse for each cluster.
        min_samples: Minimum samples for DBSCAN (controls sensitivity).
        scatter_size: Marker radius in points.

    Returns:
        The matplotlib Axes with the chart drawn.
    """
    x_arr = np.asarray(x).ravel()
    y_arr = np.asarray(y).ravel()

    labels = _cluster(x_arr, y_arr, min_samples)
    custom_cmap = _build_cmap()

    scatter_color = labels if color_by_cluster else None
    ax.scatter(x_arr, y_arr, c=scatter_color, cmap=custom_cmap,
               s=np.pi * scatter_size ** 2)

    if show_convex_hull or show_confidence_ellipse:
        for _hull, points in _iter_clusters(x_arr, y_arr, labels):
            if show_convex_hull:
                for simplex in _hull.simplices:
                    ax.plot(points[simplex, 0], points[simplex, 1],
                            color="grey", linewidth=0.75, alpha=0.75, linestyle=":")

            if show_confidence_ellipse:
                _confidence_ellipse(points[:, 0], points[:, 1], ax, n_std=2.0)

    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)

    return ax


def _cluster(x: np.ndarray, y: np.ndarray, min_samples: int) -> np.ndarray:
    data = np.column_stack([x, y])
    X = (data - np.mean(data, axis=0)) / np.sqrt(np.var(data, axis=0, ddof=1))
    eps = _estimate_eps(X, min_samples)
    return DBSCAN(eps=eps, min_samples=min_samples).fit(X).labels_


def _estimate_eps(X: np.ndarray, k: int) -> float:
    neigh = NearestNeighbors(n_neighbors=k)
    nbrs = neigh.fit(X)
    distances, _ = nbrs.kneighbors(X)
    sort_d = np.sort(distances[:, k - 1], axis=0)

    n = len(sort_d)
    coords = np.column_stack([np.arange(n), sort_d])
    first, last = coords[0], coords[-1]
    line_vec = last - first
    line_norm = line_vec / np.sqrt(np.sum(line_vec ** 2))

    vec_from_first = coords - first
    scalar = np.sum(vec_from_first * line_norm, axis=1)
    vec_to_line = vec_from_first - np.outer(scalar, line_norm)
    dist_to_line = np.sqrt(np.sum(vec_to_line ** 2, axis=1))

    return float(sort_d[np.argmax(dist_to_line)])


def _iter_clusters(
    x: np.ndarray, y: np.ndarray, labels: np.ndarray,
) -> Generator[Tuple[ConvexHull, np.ndarray], Any, None]:
    points = np.column_stack([x, y])
    for label in np.unique(labels):
        if label == -1:
            continue
        mask = labels == label
        cluster_pts = points[mask]
        yield ConvexHull(cluster_pts), cluster_pts


def _confidence_ellipse(x: np.ndarray, y: np.ndarray, ax: Axes, n_std: float = 2.0) -> Ellipse:
    cov = np.cov(x, y)
    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])

    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      color="grey", alpha=0.25, linewidth=0)

    scale_x = np.sqrt(cov[0, 0]) * n_std
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_x, mean_y = float(np.mean(x)), float(np.mean(y))

    transform = (
        transforms.Affine2D()
        .rotate_deg(45)
        .scale(scale_x, scale_y)
        .translate(mean_x, mean_y)
    )
    ellipse.set_transform(transform + ax.transData)
    return ax.add_patch(ellipse)


def _build_cmap() -> ListedColormap:
    prop_cycle = plt.rcParams.get("axes.prop_cycle")
    colors = [e["color"] for e in prop_cycle] if prop_cycle else ["333333", "666666", "999999"]
    return ListedColormap(colors)
