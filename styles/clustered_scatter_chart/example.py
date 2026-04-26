from pathlib import Path
from typing import Any, Generator, Tuple

import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap
from matplotlib.patches import Ellipse, Patch
from scipy.spatial import ConvexHull
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors

root_path = Path(__file__).parent
# 修改为要求的样式文件路径
style_file = root_path / './assets/clustered_scatter_chart.mplstyle'
plt.style.use(style_file)

# 加载散点颜色表
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
custom_cmap = ListedColormap(colors)

def estimate_eps(
        X: np.ndarray,
        k: int,
    )->int:
    neigh = NearestNeighbors(n_neighbors=k)
    nbrs = neigh.fit(X)
    distances, _ = nbrs.kneighbors(X)
    sort_distances = np.sort(distances[:, k-1], axis=0)

    # 向量投影法
    n_points = len(sort_distances)
    coords = np.vstack((np.arange(n_points), sort_distances)).T

    # 取首尾两点连为向量 L，标准化为单位向量u
    first_pt = coords[0]
    last_pt = coords[-1]
    line_vec = last_pt - first_pt
    line_vec_norm = line_vec / np.sqrt(np.sum(line_vec**2))

    # 计算各点至向量u所在直线的垂直距离，取最大值为肘部拐点
    vec_from_first = coords - first_pt
    scalar_product = np.sum(vec_from_first * line_vec_norm, axis=1)
    vec_to_line = vec_from_first - np.outer(scalar_product, line_vec_norm)
    dist_to_line = np.sqrt(np.sum(vec_to_line**2, axis=1))
    knee_idx = np.argmax(dist_to_line)

    return sort_distances[knee_idx]

def clustering_data(
        x_data: np.ndarray,
        y_data: np.ndarray,
        min_samples: int = 4
    ):

    scatter_data = np.vstack((x_data, y_data)).T

    # 标准化
    X = (scatter_data - np.mean(scatter_data, axis=0)) / np.sqrt(np.var(scatter_data, axis=0, ddof=1))
    standardzed_eps = estimate_eps(X, min_samples)

    # 聚类
    db = DBSCAN(standardzed_eps, min_samples=min_samples).fit(X)
    labels = db.labels_

    return labels

def calculate_convex_hull(x_data: np.ndarray, y_data: np.ndarray, labels: np.ndarray)->Generator[Tuple[ConvexHull, np.ndarray], Any, Any]:
    points = np.vstack((x_data, y_data)).T
    unique_label = np.unique(labels)
    for label in unique_label:
        if label == -1:
            continue

        mask =  (labels == label)
        cluster_points = points[mask]
        cluster_hull = ConvexHull(cluster_points)

        yield cluster_hull, cluster_points

# confidence_ellipse func code come from matplotlib examples
# https://matplotlib.org/stable/gallery/statistics/confidence_ellipse.html
# thanks for their excellent work!
def confidence_ellipse(x_data: np.ndarray, y_data: np.ndarray, ax: Axes, n_std=3.0)->Patch:
    cov = np.cov(x_data, y_data)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensional dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2, color='grey', alpha=0.25, linewidth=0)

    # Calculating the standard deviation of x_data from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x_data)

    # calculating the standard deviation of y_data ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y_data)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(float(mean_x), float(mean_y))

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

def main():
    # --- config ---
    title = 'Title'
    xlabel = 'x_value'
    ylabel = 'y_value'
    img_name = 'example'

    clustered_with_color = True
    clustered_with_convex_hull = True
    clustered_with_confidence_ellipse = True

    # 模拟数据
    np.random.seed(12)
    x_data = np.concatenate((np.random.normal(50, 10, 50), np.random.normal(500, 100, 50)))
    y_data = np.concatenate((np.random.normal(600, 200, 50), np.random.normal(60, 10, 50)))

    r = 1

    labels = clustering_data(x_data, y_data)

    fig, ax = plt.subplots(figsize=(5, 5), dpi=300)

    # 绘制基础散点图
    scatter_color = labels if clustered_with_color else None
    ax.scatter(x_data, y_data, c=scatter_color, cmap=custom_cmap,
               s=np.pi * r ** 2)

    # 绘制增强视觉元素
    if clustered_with_convex_hull or clustered_with_confidence_ellipse:
        for index, (hull, cluster_points) in enumerate(calculate_convex_hull(x_data, y_data, labels)):
            if clustered_with_convex_hull:
                for simplex in hull.simplices:
                    ax.plot(cluster_points[simplex, 0], cluster_points[simplex, 1],
                            color='grey',
                            linewidth=0.75,
                            alpha=0.75,
                            linestyle=':')

            if clustered_with_confidence_ellipse:
                confidence_ellipse(cluster_points[:, 0], cluster_points[:, 1], ax, n_std=2.0)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, pad=15)

    save_dir = root_path / Path('./img')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_paths = [save_dir / f"{img_name}.png", save_dir / f"{img_name}.pdf"]

    plt.tight_layout()
    for save_path in save_paths:
        plt.savefig(save_path, bbox_inches='tight')

if __name__ == '__main__':
    main()
