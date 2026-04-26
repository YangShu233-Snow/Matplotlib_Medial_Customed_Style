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

def scott_MISE(
        data: List[np.ndarray]
    )->float:
    n_avg = np.mean([len(d) for d in data])
    return float(n_avg ** (-1/5))

def calculate_bandwidth(
        data: np.ndarray,
        method: BandwidthAlgorithm
    ):
    n = len(data)
    sigma = np.std(data, ddof=1)
    if method == 'scott':
        return sigma * (n ** (-1/5))
    elif method == 'silverman':
        # S使用 IQR 以提升鲁棒性
        iqr = np.subtract(*np.percentile(data, [75, 25]))
        # 取 sigma 和 iqr/1.34 中的较小值
        A = min(sigma, iqr / 1.34)
        return 0.9 * A * (n ** (-1/5))
    else:
        raise ValueError(f"Unknown bandwidth method: {method}")

def draw_split_violinplot(
        ax: Axes,
        data: List[List[np.ndarray]],
        points: int,
        widths: float,
        labels: List[str] = ['Group 1', 'Group 2'],
        cut: float = 1.5,
        kernel: KernelDensity = 'gaussian',
        bandwidth_algorithm: BandwidthAlgorithm = 'scott',
        use_independent_bandwidths: bool = False
    ):

    x_pos = np.arange(len(data))

    # 从 rcParams 的 prop_cycle 中获取颜色
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = [c['color'] for c in prop_cycle]

    handles = []
    for idx, d in enumerate(data):
        high_group = d[0]
        low_group = d[1]

        # calculate bw
        bandwidths = []
        if use_independent_bandwidths:
            bandwidths.append(calculate_bandwidth(high_group, bandwidth_algorithm))
            bandwidths.append(calculate_bandwidth(low_group, bandwidth_algorithm))
        else:
            bandwidth = calculate_bandwidth(
                np.concatenate((high_group, low_group)),
                bandwidth_algorithm
            )
            bandwidths.extend([bandwidth] * 2)

        for i, (side, group, label, bw_method) in enumerate(zip(('low', 'high'), (low_group, high_group), labels, bandwidths)):
            # calculate KDE
            kde = KernelDensity(
                bandwidth=bw_method,
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

            color = colors[i % len(colors)]
            pos = x_pos[idx]

            if side == 'high':
                ax.fill_betweenx(y_grid, pos, pos + standard_density, color=color)
            else:
                ax.fill_betweenx(y_grid, pos - standard_density, pos, color=color)

            # 为图例创建 Patch
            if idx == 0:
                from matplotlib.patches import Patch
                handles.append(Patch(facecolor=color, edgecolor=color, label=label))

    return handles

def draw_sample_sizes(ax: Axes, data: List[List[np.ndarray]], x_positions: np.ndarray, cut: float):
    """在每个分离小提琴上方标注样本量 n=x/y"""
    offsets = list(map(
        lambda x: max(
            np.std(x[0]) * cut,
            np.std(x[1]) * cut
        ),
        data
    ))

    for i, sub_data in enumerate(data):
        n_low = len(sub_data[0])
        n_high = len(sub_data[1])
        top_val = max(np.max(sub_data[0]), np.max(sub_data[1]))
        ax.text(
            x_positions[i],
            top_val + offsets[i],
            f'n={n_low}/{n_high}',
            ha='center',
            va='bottom',
            fontsize=10
        )

def main():
    # --- config ---
    title = 'Treatment Comparison'
    ylabel = 'Relative Expression'
    img_name = 'example_split'

    points = 60
    widths = 0.7
    labels = ['Control', 'Treatment']
    show_n = True  # 是否展示样本量
    use_independent_bandwidths = False # 是否对一个大组内使用独立的bandwidth
    kernel: KernelType = 'gaussian'
    bandwidth_algothrim: BandwidthAlgorithm = 'scott'
    cut = 1.5

    np.random.seed(12)
    # split 模式数据格式: [ [group1, group2], [group1, group2], ... ]
    data = [
        [np.random.normal(200, 50, 100), np.random.normal(250, 60, 100)],
        [np.random.normal(800, 150, 100), np.random.normal(700, 180, 100)],
        [np.random.normal(400, 80, 100), np.random.normal(500, 90, 100)]
    ]

    # --- figure ---
    fig, ax = plt.subplots(
        figsize=(6, 5)
    )

    handles = draw_split_violinplot(
        ax, data, points, widths,
        labels=labels,
        cut = cut,
        kernel=kernel,
        bandwidth_algorithm=bandwidth_algothrim,
        use_independent_bandwidths=use_independent_bandwidths
    )
    ax.legend(handles=handles, frameon=False, loc='upper right')

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

    for save_path in save_paths:
        plt.savefig(save_path, bbox_inches='tight')

if __name__ == '__main__':
    main()
