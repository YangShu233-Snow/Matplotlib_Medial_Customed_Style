import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
from typing import List
from matplotlib.axes import Axes

root_path = Path(__file__).parent
# 修改为要求的样式文件路径
style_file = root_path / './assets/single_box_volinplot_chart.mplstyle'
plt.style.use(style_file)

def scott_MISE(data: List[np.ndarray]) -> float:
    n_avg = np.mean([len(d) for d in data])
    return float(n_avg ** (-1/5))

def draw_sample_sizes(ax: Axes, data: List[np.ndarray], x_positions: np.ndarray):
    """在每个图表上方标注样本量 n=xxx"""
    y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
    offset = y_range * 0.02
    for i, d in enumerate(data):
        n = len(d)
        top_val = np.max(d)
        ax.text(x_positions[i], top_val + offset, f'n={n}', ha='center', va='bottom', fontsize=10)

def draw_box_violinplot(ax: Axes, data: List[np.ndarray], points: int, v_widths: float, b_widths: float):
    x_pos = np.arange(len(data))
    bw_method = scott_MISE(data)

    # 绘制背景的小提琴图
    parts = ax.violinplot(
        data, positions=x_pos, points=points, widths=v_widths, 
        bw_method=bw_method, showextrema=False
    )
    
    # 应用 rcParams 样式
    for pc in parts['bodies']:
        pc.set_facecolor(plt.rcParams['patch.facecolor'])
        pc.set_edgecolor(plt.rcParams['patch.edgecolor'])
        pc.set_linewidth(plt.rcParams['patch.linewidth'])
        pc.set_alpha(1)

    # 绘制内部叠加的箱线图 (窄箱体，黑色填充)
    ax.boxplot(
        data, positions=x_pos, widths=b_widths, showfliers=False,
        patch_artist=plt.rcParams['boxplot.patchartist'],
        boxprops=dict(facecolor='black')
    )

def main():
    # --- config ---
    title = 'Box-Violin Plot'
    ylabel = 'Value'
    img_name = 'example'
    
    points = 60
    v_widths = 0.7  # 小提琴图宽度
    b_widths = 0.1  # 内部箱线图宽度
    show_n = True   # 是否展示样本量

    # 模拟数据
    np.random.seed(12)
    data = [
        np.random.normal(200, 80, 200),
        np.random.normal(800, 500, 150),
        np.random.normal(600, 100, 180)
    ]

    fig, ax = plt.subplots(figsize=(5, 5))

    draw_box_violinplot(ax, data, points, v_widths, b_widths)
    
    x_positions = np.arange(len(data))
    if show_n:
        draw_sample_sizes(ax, data, x_positions)

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xticks(x_positions)
    ax.set_xticklabels([f'Sample {i+1}' for i in range(len(data))])

    save_dir = root_path / Path('./img')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_paths = [save_dir / f"{img_name}.png", save_dir / f"{img_name}.pdf"]

    plt.tight_layout()
    for save_path in save_paths:
        plt.savefig(save_path, bbox_inches='tight')

if __name__ == '__main__':
    main()
