from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

root_path = Path(__file__).parent
# 修改为要求的样式文件路径
style_file = root_path / './assets/single_columns_scatter_chart.mplstyle'
plt.style.use(style_file)

def calculate_star_y_position(mean: float, sem: float, top_val: float):
    star_y_postion_1 = mean + sem + sem * 0.05
    star_y_postion_2 = top_val + 20

    return star_y_postion_1 if star_y_postion_1 > star_y_postion_2 else star_y_postion_2

def draw_stars(
        ax: Axes,
        x_positions: List[float],
        stars_list: List[int],
        raw_data: List[np.ndarray],
        means: List[float],
        errs: List[float]
    ):
    for i, x_pos in enumerate(x_positions):
        mean = means[i]
        err = errs[i]
        stars = stars_list[i]

        # 必须考虑到散点图的最大值，防止星号与散点重叠
        group_max = np.max(raw_data)
        error_max = mean + err
        top_val = max(group_max, error_max)

        star_y_position = calculate_star_y_position(mean, err, top_val)

        ax.text(x_pos, star_y_position, '*' * stars,
                ha='center', va='bottom', fontsize=14)

def generate_prism_colors(num_groups):
    if num_groups == 1:
        return ['black']

    grays = np.linspace(0.1, 0.8, num_groups)
    return [str(g) for g in grays]

def generate_jittered_x(y: np.ndarray, r_x: float, r_y: float) -> np.ndarray:
    """
    生成独立的X轴和Y轴防重叠抖动。

    :param y: 原数据的 Y 坐标
    :param r_x: X 轴方向的排斥半径 (通常很小，例如 0.02~0.05)
    :param r_y: Y 轴方向的排斥半径 (根据数据量级决定，例如 50~100)
    """
    n = len(y)
    x = np.zeros(n)

    # 分别计算 X 和 Y 方向的安全直径
    D_x = 2 * r_x
    D_y = 2 * r_y

    sorted_indices = np.argsort(y, kind='stable')
    placed_indices = []

    for idx in sorted_indices:
        y_i = y[idx]

        # 1. 找到可能发生重叠的已放置点
        conflicts = []
        for prev_idx in reversed(placed_indices):
            dy = y_i - y[prev_idx]
            if dy >= D_y:
                break
            conflicts.append(prev_idx)

        if not conflicts:
            x[idx] = 0.0
            placed_indices.append(idx)
            continue

        # 2. 计算禁区 (使用椭圆公式)
        intervals = []
        for c_idx in conflicts:
            dy = y_i - y[c_idx]

            # 归一化 Y 距离的平方
            y_ratio_sq = (dy / D_y)**2
            if y_ratio_sq >= 1.0:
                continue

            # 根据椭圆方程计算 X 轴需要偏移的最小距离
            dx = D_x * np.sqrt(1.0 - y_ratio_sq) + 1e-8

            x_c = x[c_idx]
            intervals.append((x_c - dx, x_c + dx))

        # 3. 收集候选点
        candidates = [0.0]
        for iv in intervals:
            candidates.extend([iv[0], iv[1]])
        candidates.sort(key=lambda val: (abs(val), val))

        # 4. 寻找最优位置
        chosen_x = 0.0
        for cand in candidates:
            is_valid = True
            for iv in intervals:
                if iv[0] < cand < iv[1]:
                    is_valid = False
                    break
            if is_valid:
                chosen_x = cand
                break

        x[idx] = chosen_x
        placed_indices.append(idx)

    return np.asarray(x, dtype=float)

def main():
    # --- config ---
    ylabel = 'Value'
    title = 'Title'
    img_name = 'example'

    # 生成模拟数据
    np.random.seed(12)
    groups = ['Con', 'KO']

    # 模拟Con组数据 (均值约1200)
    data_con = np.random.normal(1200, 300, 15)
    # 模拟KO组数据 (均值约3500)
    data_ko = np.random.normal(3500, 400, 15)

    raw_data = [data_con, data_ko]

    stars_mark = [
        (1, 3)
    ]

    r = 2

    # 根据原始数据计算均值和标准误 (SEM)
    means = [np.mean(d) for d in raw_data]
    errs = [np.std(d, ddof=1) / np.sqrt(len(d)) for d in raw_data]
    x_pos = np.arange(len(groups))

    asymmetric_errs = [errs]

    # 具体图像尺寸大小按需求设置
    fig_width = len(raw_data) * 0.3 + 2.5
    fig_heigth = 1.5 + np.max(means) / np.min(means)
    fig, ax = plt.subplots(figsize=(fig_width, fig_heigth), dpi=300)

    colors = generate_prism_colors(len(groups))

    # 1. 绘制柱状图底色 (设置透明度以便看清散点)
    ax.bar(x_pos, means, yerr=asymmetric_errs, width=0.6,
            color=colors, error_kw={'zorder': 4})

    # 2. 绘制分布散点 (Scatter/Jitter)
    for i, data in enumerate(raw_data):
        x_jittered = generate_jittered_x(data, r_x=len(groups) / fig_width * r / 72, r_y= np.max(means) / fig_heigth * r / 36) + x_pos[i]
        ax.scatter(x_jittered, data,
                   color='white',
                   edgecolor='black',
                   alpha=0.7,
                   s=np.pi * r ** 2)

    # 3. 绘制显著性星号，传入原始数据以计算最高点
    stars_indexes = [star_mark[0] for star_mark in stars_mark]
    stars = [star_mark[1] for star_mark in stars_mark]
    stars_raw_data = [raw_data[index] for index in stars_indexes]
    stars_means = [means[index] for index in stars_indexes]
    stars_errs = [errs[index] for index in stars_indexes]
    draw_stars(
        ax,
        [int(x_pos[i])],
        stars,
        stars_raw_data,
        stars_means,
        stars_errs
    )

    # 4. 图表格式化设置
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

if __name__ == '__main__':
    main()
