from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

root_path = Path(__file__).parent
style_file = root_path / './assets/genomic_heatmap.mplstyle'
plt.style.use(style_file)

def generate_dummy_genomic_data(rows: int = 2000, cols: int = 100, pattern: str = 'center_peak') -> np.ndarray:
    x = np.linspace(-3, 3, cols)
    if pattern == 'center_peak':
        peak = np.exp(-(x**2) / 0.5) * 3
        row_multipliers = np.linspace(1.5, 0.2, rows)[:, np.newaxis]
        noise = np.random.normal(0, 0.5, (rows, cols))
        data = peak * row_multipliers + noise
    else:
        # 模拟 IgG 对照组：全背景噪音
        data = np.random.normal(-1.5, 1.5, (rows, cols))

    return np.clip(data, -3.5, 3)

def format_heatmap_axes(ax: Axes, title: str, is_first: bool = False):
    ax.set_title(title, pad=10)

    ax.set_xticks([49])
    ax.set_xticklabels(['0'])

    ax.set_yticks([])

    # 仅在最左侧的子图添加 Y 轴标签
    if is_first:
        ax.set_ylabel('MYC reproducible\nenriched windows')

    # 设置边框粗细 (符合学术图表要求)
    for spine in ax.spines.values():
        spine.set_linewidth(1.0)

def main():
    # config
    img_name = 'example'
    titles = ['ANY R1', 'ANY R2', 'IgG R1', 'IgG R2']
    red_to_blue = True
    vmin, vmax = -3.5, 3.0
    colorbar_label = '$\\log_2$FC CLIP/input'
    scale = 0.5
    scale_label = "1 kb"

    # 这里手动生成了四组数据，在实际案例中，应当将 datasets 换成你自己的数据，并按照你想要的绘图顺序排列
    # 默认你提供的数据已经完成了聚类
    # datasets 的元素应当都是 numpy.ndarray
    # 数据维度：假设有2000个可重复富集窗口，每个窗口切分为100个Bins
    rows, cols = 2000, 100

    # 模拟生成 4 个样本的矩阵数据
    data_myc_r1 = generate_dummy_genomic_data(rows, cols, pattern='center_peak')
    data_myc_r2 = generate_dummy_genomic_data(rows, cols, pattern='center_peak')
    data_igg_r1 = generate_dummy_genomic_data(rows, cols, pattern='noise')
    data_igg_r2 = generate_dummy_genomic_data(rows, cols, pattern='noise')

    datasets = [data_myc_r1, data_myc_r2, data_igg_r1, data_igg_r2]

    fig, axes = plt.subplots(nrows=1, ncols=len(datasets), figsize=(1.2 * len(datasets) + 0.2, 6), dpi=300, sharey=True)
    axes: List[Axes]

    plt.subplots_adjust(wspace=0.1, bottom=0.25)

    if red_to_blue:
        cmap = 'RdYlBu'
    else:
        cmap = 'RdYlBu_r'

    im = None
    for i, (ax, data, title) in enumerate(zip(axes, datasets, titles)):
        im = ax.imshow(data, aspect='auto', cmap=cmap, vmin=vmin, vmax=vmax, interpolation='nearest')
        format_heatmap_axes(ax, title=title, is_first=(i == 0))

    # 添加 Colorbar
    cbar_ax: Axes = fig.add_axes([0.4, 0.15, 0.2, 0.02])
    cbar = fig.colorbar(im, cax=cbar_ax, orientation='horizontal')
    cbar.set_label(colorbar_label, fontsize=12, labelpad=8)

    # 极值标在两端
    cbar.set_ticks([])
    cbar_ax.text(-0.03, 0.5, str(vmin), transform=cbar_ax.transAxes, ha='right', va='center')
    cbar_ax.text(1.03, 0.5, str(vmax), transform=cbar_ax.transAxes, ha='left', va='center')

    # 隐藏 Colorbar 的刻度线
    cbar.ax.tick_params(size=0)

    ax_last = axes[-1]
    ax_last.plot([0.5, 0.5 + scale], [-0.12, -0.12], transform=ax_last.transAxes, color='black', linewidth=1.5, clip_on=False)
    ax_last.text(0.5 + scale / 2, -0.14, scale_label, transform=ax_last.transAxes, ha='center', va='top', fontsize=10)

    save_dir = root_path / Path('./img')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_paths = [save_dir / f"{img_name}.png", save_dir / f"{img_name}.pdf"]

    for save_path in save_paths:
        plt.savefig(save_path, bbox_inches='tight')
    # plt.show()

if __name__ == '__main__':
    main()
