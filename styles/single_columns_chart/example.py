import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
from typing import List
from matplotlib.axes import Axes

root_path = Path(__file__).parent
style_file = root_path / './assets/single_columns_chart.mplstyle'
plt.style.use(style_file)

def caculate_star_y_position(mean: int, sem: int):
    return mean + sem + sem * 0.05

def draw_stars(ax: Axes, groups_id: List[int], stars: List[int], means, errs):
    for index, star in zip(groups_id, stars):
        star_y_position = caculate_star_y_position(means[index], errs[index])

        ax.text(index, star_y_position, '*' * star,
                ha='center', va='bottom')

def generate_prism_colors(num_groups):
    if num_groups == 1:
        return ['black']

    grays = np.linspace(0, 0.8, num_groups)
    return [str(g) for g in grays]

def main():
    # config
    # y轴标签
    ylabel = 'value'
    # 图表标题
    title = 'something'
    # 保存文件名
    img_name = 'example'

    # 示例数据
    groups = ['Con', 'KO']
    means = [1200, 3500]
    errs = [300, 400]
    x_pos = np.arange(len(groups))

    # 默认误差线仅作上半部分，若需要“工”字完整误差线，则asymmetric_errs = [errs] 
    asymmetric_errs = [[0] * len(groups), errs] 

    # 具体图像尺寸大小按需求设置
    fig, ax = plt.subplots(figsize=(len(groups) * 1.5, 4), dpi=300)

    colors = generate_prism_colors(len(groups))

    # 图表柱子的样式
    ax.bar(x_pos, means, yerr=asymmetric_errs, width=0.6,
            color=colors, edgecolor='black', linewidth=2,
            capsize=5, error_kw={'elinewidth': 0.8, 'capthick': 0.8})
    
    draw_stars(ax, groups_id=[1], stars=[3], means=means, errs=errs)

    ax.set_xlim(-0.6, len(groups) - 1 + 0.6)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(groups)
    ax.set_ylabel(ylabel)
    ax.set_title(title, pad=15)

    save_dir = root_path / Path('./img')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_paths = [save_dir / f"{img_name}.png", save_dir / f"{img_name}.pdf"]
    
    plt.tight_layout()
    for save_path in save_paths:
        plt.savefig(save_path, bbox_inches='tight')
    # 如果你在非图形界面的环境下，plt.show()是不可用的（比如SSH登录服务器）
    # plt.show()

if __name__ == '__main__':
    main()