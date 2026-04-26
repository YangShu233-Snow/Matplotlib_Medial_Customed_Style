from pathlib import Path
from typing import List, Literal

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from sklearn.neighbors import KernelDensity

type KernelType = Literal['gaussian', 'tophat', 'epanechnikov', 'exponential', 'linear', 'cosine']
type BandwidthAlgorithm = Literal['scott', 'silverman']

root_path = Path(__file__).parent
style_file = root_path / './assets/single_box_violinplot_chart.mplstyle'
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
        iqr = np.subtract(*np.percentile(data, [75, 25]))
        A = min(sigma, iqr / 1.34)
        return 0.9 * A * (n ** (-1/5))
    else:
        raise ValueError(f"Unknown bandwidth method: {method}")

def draw_split_box_violinplot(
        ax: Axes,
        data: List[List[np.ndarray]],
        points: int,
        v_widths: float,
        b_widths: float,
        labels: List[str],
        cut: float = 1.5,
        kernel: KernelType = 'gaussian',
        bandwidth_algorithm: BandwidthAlgorithm = 'scott',
        use_independent_bandwidths: bool = False
    ):
    x_pos = np.arange(len(data))
    low_group = [sub_data[0] for sub_data in data]
    high_group = [sub_data[1] for sub_data in data]

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = [c['color'] for c in prop_cycle]

    # 绘制背景的半边小提琴图 (手动 KDE)
    for idx, d in enumerate(data):
        high_data = d[0]
        low_data = d[1]

        bandwidths = []
        if use_independent_bandwidths:
            bandwidths.append(calculate_bandwidth(high_data, bandwidth_algorithm))
            bandwidths.append(calculate_bandwidth(low_data, bandwidth_algorithm))
        else:
            bandwidth = calculate_bandwidth(
                np.concatenate((high_data, low_data)),
                bandwidth_algorithm
            )
            bandwidths.extend([bandwidth] * 2)

        for i, (side, group, bw_method) in enumerate(zip(('low', 'high'), (low_data, high_data), bandwidths)):
            color = colors[i % len(colors)]

            kde = KernelDensity(
                bandwidth=bw_method,
                kernel=kernel
            ).fit(group.reshape(-1, 1))

            group_max, group_min = group.max(), group.min()
            group_std = np.std(group)
            extend = group_std * cut
            y_grid = np.linspace(
                group_min - extend,
                group_max + extend,
                points
            )

            density = np.exp(kde.score_samples(y_grid.reshape(-1, 1)))
            standard_density = (density / density.max()) * (v_widths / 2)

            pos = x_pos[idx]
            if side == 'high':
                ax.fill_betweenx(y_grid, pos, pos + standard_density, color=color)
            else:
                ax.fill_betweenx(y_grid, pos - standard_density, pos, color=color)

    # 绘制内部叠加的箱线图 (窄箱体，半透明填充，偏移对齐)
    handles = []
    for i, (side, group) in enumerate(zip(('low', 'high'), (low_group, high_group))):
        color = colors[i % len(colors)]

        shift = -v_widths / 4 if side == 'low' else v_widths / 4
        box_pos = x_pos + shift

        ax.boxplot(
            group, positions=box_pos, widths=b_widths, showfliers=False,
            patch_artist=plt.rcParams['boxplot.patchartist'],
            boxprops=dict(facecolor='#00000000')
        )

        from matplotlib.patches import Patch
        handles.append(Patch(facecolor=color, edgecolor=color, label=labels[i]))

    return handles

def draw_sample_sizes(ax: Axes, data: List[List[np.ndarray]], x_positions: np.ndarray, cut: float):
    """在每个分离叠加图上方标注样本量 n=x/y"""
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
    title = 'Split Box-Violin Plot'
    ylabel = 'Relative Expression'
    img_name = 'example_split'

    points = 60
    v_widths = 0.7
    b_widths = 0.08
    labels = ['Control', 'Treatment']
    show_n = True
    use_independent_bandwidths = False
    kernel: KernelType = 'gaussian'
    bandwidth_algorithm: BandwidthAlgorithm = 'scott'
    cut = 1.5

    np.random.seed(12)
    data = [
        [np.random.normal(200, 50, 100), np.random.normal(250, 60, 100)],
        [np.random.normal(800, 150, 100), np.random.normal(700, 180, 100)],
        [np.random.normal(400, 80, 100), np.random.normal(500, 90, 100)]
    ]

    fig, ax = plt.subplots(figsize=(6, 5))

    handles = draw_split_box_violinplot(
        ax, data, points, v_widths, b_widths, labels=labels,
        cut=cut,
        kernel=kernel,
        bandwidth_algorithm=bandwidth_algorithm,
        use_independent_bandwidths=use_independent_bandwidths
    )
    ax.legend(handles=handles, frameon=False, loc='upper right')

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
