import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
from typing import List
from matplotlib.axes import Axes

root_path = Path(__file__).parent
style_file = root_path / './assets/column_chart_graphpad.mplstyle'
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
    ylabels = ['value', 'value', 'value']
    # 图表标题
    titles = ['something', 'something', 'something']
    # 保存文件名
    img_name = 'example.png'

    # 示例数据
    all_groups = [['Con', 'KO'], ['Con', 'KO']]
    all_means = [[1200, 3500], [1200, 3500]]
    all_errs = [[300, 400], [300, 400]]
    stars_marks = [[[1], [3]], [[1], [4]]]
    
    total_columns_count = len([item for groups in all_groups for item in groups])
    total_charts_count = len(all_groups)

    fig, axs = plt.subplots(1, total_charts_count, figsize=(total_columns_count * 1.5 + total_charts_count * 2 , 5), dpi=300)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.8, hspace=0.4)

    for index, (ylabel, title, groups, means, errs, (groups_id, stars)) in enumerate(zip(ylabels, titles, all_groups, all_means, all_errs, stars_marks)):
        x_pos = np.arange(len(groups))
        # 默认误差线仅作上半部分，若需要“工”字完整误差线，则asymmetric_errs = [errs] 
        asymmetric_errs = [[0] * len(groups), errs] 

        colors = generate_prism_colors(len(groups))

        # 图表柱子的样式
        axs[index].bar(x_pos, means, yerr=asymmetric_errs, width=0.6,
                color=colors, edgecolor='black', linewidth=2,
                capsize=5, error_kw={'elinewidth': 0.8, 'capthick': 0.8})
        
        draw_stars(axs[index], groups_id=groups_id, stars=stars, means=means, errs=errs)

        axs[index].set_xlim(-0.6, len(groups) - 1 + 0.6)
        axs[index].set_xticks(x_pos)
        axs[index].set_xticklabels(groups)
        axs[index].set_ylabel(ylabel)
        axs[index].set_title(title, pad=15)

    save_path = root_path / Path('./img') / img_name

    plt.savefig(save_path, bbox_inches='tight')
    # 如果你在非图形界面的环境下，plt.show()是不可用的（比如SSH登录服务器）
    # plt.show()

if __name__ == '__main__':
    main()