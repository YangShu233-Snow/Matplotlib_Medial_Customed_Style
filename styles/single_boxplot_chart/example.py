from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

root_path = Path(__file__).parent
# 修改为要求的样式文件路径
style_file = root_path / './assets/single_boxplot_chart.mplstyle'
plt.style.use(style_file)

def draw_sample_sizes(ax: Axes, data: List[np.ndarray], x_positions: np.ndarray):
    """在每个箱体上方标注样本量 n=xxx"""
    y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
    offset = y_range * 0.02 # 向上偏移 y 轴量程的 2%

    for i, d in enumerate(data):
        n = len(d)
        top_val = np.max(d)
        ax.text(
            x_positions[i],
            top_val + offset,
            f'n={n}',
            ha='center',
            va='bottom'
        )

def main():
    # --- config ---
    title = 'Title'
    ylabel = 'Value'
    img_name = 'example'

    show_mean = True
    is_notch = False
    show_n = True # 是否展示样本量

    # 模拟数据
    np.random.seed(12)
    data = [
        np.random.normal(500, 150, 40),
        np.random.normal(900, 100, 40),
        np.random.normal(380, 80, 40)
    ]

    labels = [f'Sample_{index+1}' for index in range(len(data))]

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.boxplot(
        data,
        tick_labels=labels,
        notch=is_notch,
        showmeans=show_mean,
        patch_artist=True,
        boxprops=dict(facecolor='#CCCCCC')
    )

    # 获取箱线图默认的 x 轴位置 (1, 2, ..., len(data))
    x_positions = np.arange(1, len(data) + 1)

    if show_n:
        draw_sample_sizes(ax, data, x_positions)

    ax.set_title(title)
    ax.set_ylabel(ylabel)

    save_dir = root_path / Path('./img')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_paths = [save_dir / f"{img_name}.png", save_dir / f"{img_name}.pdf"]

    plt.tight_layout()
    for save_path in save_paths:
        plt.savefig(save_path, bbox_inches='tight')

if __name__ == '__main__':
    main()
