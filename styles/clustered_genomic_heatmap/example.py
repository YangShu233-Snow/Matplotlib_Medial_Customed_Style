from pathlib import Path
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import scipy.cluster.hierarchy as sch
from matplotlib.axes import Axes
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

root_path = Path(__file__).parent
# 修改为要求的样式文件路径
style_file = root_path / './assets/clustered_genomic_heatmap.mplstyle'
plt.style.use(style_file)

def draw_dendro(
        ax_row_dendro: Axes,
        ax_col_dendro: Axes,
        row_linkage,
        col_linkage
    )->Tuple[dict, dict]:

    row_dendro = sch.dendrogram(
        row_linkage,
        ax=ax_row_dendro,
        orientation='left',
        link_color_func=lambda _: '000000'
    )
    ax_row_dendro.axis('off')

    col_dendro = sch.dendrogram(
        col_linkage,
        ax=ax_col_dendro,
        orientation="top",
        link_color_func=lambda _: '000000'
    )
    ax_col_dendro.axis('off')

    return col_dendro, row_dendro

def main():
    # --- config ---
    img_name = 'example'
    title = 'Title'
    colorbar_label = '$\\log_2$(Value)'

    clustering_algorithm = 'ward'
    clustering_algorithm_distance = 'euclidean'

    vmin = -3.0
    vmax = 3.0

    # 模拟数据，默认行为基因，列为样本
    # 默认已做好标准化！！！
    # 默认没有做聚类
    np.random.seed(12)
    heatmap_data = np.random.randn(50, 20)

    gene_names = [f"Gene_{i}" for i in range(len(heatmap_data))]
    sample_names = [f"Sample_{i}" for i in range(len(heatmap_data[1, :]))]

    row_linkage = sch.linkage(
        heatmap_data,
        method=clustering_algorithm,
        metric=clustering_algorithm_distance
    )

    col_linkage = sch.linkage(
        heatmap_data.T,
        method=clustering_algorithm,
        metric=clustering_algorithm_distance
    )

    fig, ax = plt.subplots(figsize=(5, 5))
    grids = fig.add_gridspec(
        2, 2,
        width_ratios=[1, 5],
        height_ratios=[1, 5],
        wspace=0.01,
        hspace=0.01
    )

    col_dendro, row_dendro = draw_dendro(
        fig.add_subplot(grids[1, 0]),
        fig.add_subplot(grids[0, 1]),
        col_linkage=col_linkage,
        row_linkage=row_linkage
    )

    col_order = col_dendro['leaves']
    row_order = row_dendro['leaves']


    # 基于排序索引重排原始矩阵
    ordered_data = heatmap_data[row_order, :][:, col_order]

    # 主热图
    ax_heatmap = fig.add_subplot(grids[1, 1])
    im = ax_heatmap.imshow(ordered_data, vmin=-3, vmax=3, aspect='auto')

    # colorbar
    cax: Axes = inset_axes(ax_heatmap, width="25%", height="3%", loc='lower left',
                 bbox_to_anchor=(0.03, -0.2, 1, 1), bbox_transform=ax_heatmap.transAxes)
    cbar = fig.colorbar(im, cax=cax, orientation='horizontal')
    cbar.set_label(
        colorbar_label
    )

    cbar.set_ticks(np.linspace(np.floor(vmin), np.ceil(vmax), num= int(vmax - vmin) if int(vmax - vmin) % 2 else int(vmax - vmin) + 1))
    # 隐藏 Colorbar 的刻度线
    cbar.ax.tick_params(size=0)

    # 标签
    # 样本
    ax_heatmap.set_xticks(np.arange(len(sample_names)))
    ax_heatmap.set_xticklabels(
        np.asarray(sample_names)[col_order],
        rotation=45,
        ha='center'
    )

    # 基因
    ax_heatmap.set_yticks(np.arange(len(gene_names)))
    ax_heatmap.set_yticklabels(
        np.asarray(gene_names)[row_order]
    )
    ax_heatmap.yaxis.tick_right()

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)

    save_dir = root_path / Path('./img')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_paths = [save_dir / f"{img_name}.png", save_dir / f"{img_name}.pdf"]

    for save_path in save_paths:
        plt.savefig(save_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
