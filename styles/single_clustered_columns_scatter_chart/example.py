from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

root_path = Path(__file__).parent
style_file = root_path / './assets/single_clustered_columns_scatter_chart.mplstyle'
plt.style.use(style_file)

def calculate_line_y_position(top_val: float, min_dis: int):
    return top_val + min_dis * 5

def draw_stars(
        ax: Axes,
        x_positions: List[Tuple[float, float]],
        stars_list: List[int],
        raw_data: List[Tuple[np.ndarray, np.ndarray]],
        means: List[Tuple[float, float]],
        errs: List[Tuple[float, float]],
        fraction_length: int = 20
    ):
    max_y_line_pos = 0
    max_y_star_pos = 0
    min_gap = 20 * fraction_length
    for i, (con_x_pos, x_pos) in enumerate(x_positions):
        con_mean, mean = means[i]
        con_err, err = errs[i]
        con_data, data = raw_data[i]
        stars = stars_list[i]

        # 必须考虑到散点图的最大值，防止星号与散点重叠
        top_val = max((max(np.max(data), mean + err)), (max(np.max(con_data), con_mean + con_err)))

        if (top_val - max_y_star_pos) > min_gap:
            max_y_line_pos = top_val
        else:
            max_y_line_pos += min_gap
            top_val = max_y_line_pos

        line_y_position = calculate_line_y_position(top_val, fraction_length)
        star_y_position = line_y_position
        star_x_position = (con_x_pos + x_pos) / 2.0

        max_y_star_pos = max(star_y_position, max_y_star_pos)

        ax.plot(
            [con_x_pos, con_x_pos, x_pos, x_pos],
            [line_y_position - fraction_length, line_y_position, line_y_position, line_y_position - fraction_length],
            c='black',
            linewidth=1.0
        )
        ax.text(star_x_position, star_y_position, '*' * stars,
                ha='center', va='bottom')


def generate_prism_colors(num_groups):
    if num_groups == 1:
        return ['black']

    grays = np.linspace(0.1, 0.8, num_groups)
    return [str(g) for g in grays]


def generate_jittered_x(y: np.ndarray, r_x: float, r_y: float) -> np.ndarray:
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
    # --- 配置区 ---
    ylabel = 'Value'
    title = 'Title'
    img_name = 'example'
    bar_width = 0.3

    # --- 示例数据 ---
    categories = [
        ('Group A', ['CON', 'KO']),
        ('Group B', ['CON', 'KO-1', 'KO-2']),
        ('Group C', ['CON', 'KO'])
        ]

    np.random.seed(12)
    all_raw_data = [
        [np.random.normal(1200, 300, 15), np.random.normal(3500, 400, 15)],
        [np.random.normal(1500, 200, 20), np.random.normal(2200, 300, 20), np.random.normal(1000, 500, 20)],
        [np.random.normal(1100, 150, 15), np.random.normal(1050, 100, 15)]
    ]

    all_means = []
    all_errs = []
    for raw_data in all_raw_data:
        all_means.append([np.mean(data) for data in raw_data])
        all_errs.append([np.std(data, ddof=1) / np.sqrt(len(data)) for data in raw_data])

    stars_marks = [
        [(0, 1, 3)],
        [(0, 1, 2), (0, 2, 3)],
        []
    ]

    r = 1.5

    # --- 图表初始化 ---
    all_means_extend = [mean for means in all_means for mean in means]
    groups_count = sum(len(category[1]) for category in categories)
    fig_width = (groups_count + len(categories)) * bar_width + 2.5
    fig_heigth = 1.5 + np.max(all_means_extend) / np.min(all_means_extend)
    fig, ax = plt.subplots(figsize=(fig_width, fig_heigth), dpi=300)

    # --- 提取组名 ---
    all_groups_name = [item for category in categories for item in category[1]]

    # --- 计算柱子位置 ---
    x_base = np.linspace(
        0,
        (groups_count + len(categories) - 1) * bar_width * 2,
        groups_count + len(categories)
    )
    group_index = 0

    all_bar_positions = []
    for index, category in enumerate(categories):
        means = all_means[index]
        errs = all_errs[index]
        raw_data = all_raw_data[index]

        n_subgroups = len(category[1])

        colors = generate_prism_colors(n_subgroups)

        all_x_positions = []
        for i in range(n_subgroups):
            x_current: float = x_base[group_index] + bar_width
            group_index += 1
            all_x_positions.append(x_current)
            all_bar_positions.append(x_current)

            asymmetric_errs = [errs[i]]
            ax.bar(x_current, means[i], yerr=asymmetric_errs, width=bar_width, align='center',
               label=category[1][i], color=colors[i])

        group_index += 1

        for i, data in enumerate(raw_data):
            x_jittered = generate_jittered_x(
                data,
                r_x=len(categories) / fig_width * r / 36,
                r_y=np.max(all_means_extend) / fig_heigth * r / 36
            ) + all_x_positions[i]

            ax.scatter(x_jittered, data,
                    color='white',
                    edgecolor='black',
                    alpha=0.75,
                    s=np.pi * r ** 2)

        stars_mark = stars_marks[index]
        stars_indexes = [(star_mark[0], star_mark[1]) for star_mark in stars_mark]
        stars = [star_mark[2] for star_mark in stars_mark]
        x_positions = [(all_x_positions[con_i], all_x_positions[i]) for con_i, i in stars_indexes]
        stars_raw_data = [(raw_data[con_i], raw_data[i]) for con_i, i in stars_indexes]
        stars_means = [(means[con_i], means[i]) for con_i, i in stars_indexes]
        stars_errs = [(errs[con_i], errs[i]) for con_i, i in stars_indexes]

        draw_stars(
            ax,
            x_positions,
            stars,
            stars_raw_data,
            stars_means,
            stars_errs
        )

    # --- 格式化设置 ---
    ax.set_xticks(x_base)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.set_xticklabels([])

    ax.set_xticks(all_bar_positions, minor=True)
    ax.set_xticklabels(all_groups_name, minor=True, rotation=45)

    ax.set_ylabel(ylabel)
    ax.set_title(title)

    # --- 保存图表 ---
    save_dir = root_path / Path('./img')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_paths = [save_dir / f"{img_name}.png", save_dir / f"{img_name}.pdf"]

    plt.tight_layout()
    for save_path in save_paths:
        plt.savefig(save_path, bbox_inches='tight')

if __name__ == '__main__':
    main()
