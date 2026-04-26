from pathlib import Path
from typing import List, Literal

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from sklearn.neighbors import KernelDensity

type KernelType = Literal['gaussian', 'tophat', 'epanechnikov', 'exponential', 'linear', 'cosine']
type BandwidthAlgorithm = Literal['scott', 'silverman']

root_path = Path(__file__).parent
# 修改为要求的样式文件路径
style_file = root_path / './assets/single_violinplot_chart.mplstyle'
plt.style.use(style_file)

def calculate_bandwidth(
        data: np.ndarray,
        method: BandwidthAlgorithm
    ):
    n = len(data)
    sigma = np.std(data, ddof=1)
    if method == 'scott':
        return sigma * (n ** (-1/5))
    elif method == 'silverman':
        # 使用 IQR 以提升鲁棒性
        iqr = np.subtract(*np.percentile(data, [75, 25]))
        # 取 sigma 和 iqr/1.34 中的较小值
        A = min(sigma, iqr / 1.34)
        return 0.9 * A * (n ** (-1/5))
    else:
        raise ValueError(f"Unknown bandwidth method: {method}")

def draw_violinplot(
        ax: Axes,
        data: List[np.ndarray],
        points: int,
        widths: float,
        cut: float = 1.5,
        kernel: KernelType = 'gaussian',
        bandwidth_algorithm: BandwidthAlgorithm = 'scott',
    ):

    x_pos = np.arange(len(data))

    for idx, group in enumerate(data):
        # calculate bandwidth
        bandwidth = calculate_bandwidth(group, bandwidth_algorithm)

        # calculate KDE
        kde = KernelDensity(
            bandwidth=bandwidth,
            kernel=kernel
        ).fit(group.reshape(-1, 1))

        # extend tail
        group_max, group_min = group.max(), group.min()
        group_std = np.std(group)
        extend = group_std * cut
        y_grid = np.linspace(
            group_min - extend,
            group_max + extend,
            points
        )

        # estimate density
        density = np.exp(kde.score_samples(y_grid.reshape(-1, 1)))
        standard_density = (density / density.max()) * (widths / 2)

        pos = x_pos[idx]

        ax.fill_betweenx(
            y_grid,
            pos - standard_density,
            pos + standard_density,
            color=plt.rcParams['patch.facecolor'],
            edgecolor=plt.rcParams['patch.edgecolor'],
            linewidth=plt.rcParams['patch.linewidth']
        )

def draw_sample_sizes(ax: Axes, data: List[np.ndarray], x_positions: np.ndarray, cut: float):
    """在每个小提琴上方标注样本量 n=xxx"""
    offset = list(map(lambda x: np.std(x) * cut , data))

    for i, d in enumerate(data):
        n = len(d)
        top_val = np.max(d)
        ax.text(
            x_positions[i],
            top_val + offset[i],
            f'n={n}',
            ha='center',
            va='bottom',
            fontsize=10
        )

def main():
    # --- config ---
    title = 'Standard Violin Plot'
    ylabel = 'Value'
    img_name = 'example'

    points = 60
    widths = 0.7
    show_n = True  # 是否展示样本量
    kernel: KernelType = 'gaussian'
    bandwidth_algorithm: BandwidthAlgorithm = 'scott'
    cut = 1.5

    np.random.seed(12)
    data = [
        np.random.normal(200, 80, 200),
        np.random.normal(800, 500, 200),
        np.random.normal(600, 100, 200)
    ]

    # --- figure ---
    fig, ax = plt.subplots(
        figsize=(5, 5)
    )

    draw_violinplot(
        ax, data, points, widths,
        cut=cut,
        kernel=kernel,
        bandwidth_algorithm=bandwidth_algorithm
    )

    # 应用配置中的标签和标题
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    x_positions = np.arange(len(data))
    ax.set_xticks(x_positions)
    ax.set_xticklabels([f'Sample {i+1}' for i in range(len(data))])

    if show_n:
        draw_sample_sizes(ax, data, x_positions, cut)

    save_dir = root_path / Path('./img')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_paths = [save_dir / f"{img_name}.png", save_dir / f"{img_name}.pdf"]

    plt.tight_layout()
    for save_path in save_paths:
        plt.savefig(save_path, bbox_inches='tight')

if __name__ == '__main__':
    main()
