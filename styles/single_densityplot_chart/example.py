from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KernelDensity

type KernelType = Literal['gaussian', 'tophat', 'epanechnikov', 'exponential', 'linear', 'cosine']
type BandwidthAlgorithm = Literal['scott', 'silverman']

root_path = Path(__file__).parent
# 修改为要求的样式文件路径
style_file = root_path / './assets/single_densityplot_chart.mplstyle'
plt.style.use(style_file)

def calculate_bandwidth(data: np.ndarray, method: BandwidthAlgorithm) -> float:
    """手动计算带宽，考虑数据标准差以避免欠平滑"""
    n = len(data)
    sigma = np.std(data, ddof=1)
    if method == 'scott':
        return 1.06 * sigma * (n ** (-1/5))
    elif method == 'silverman':
        # Silverman 规则通常使用 IQR 以提升鲁棒性
        iqr = np.subtract(*np.percentile(data, [75, 25]))
        # 取 sigma 和 iqr/1.34 中的较小值
        A = min(sigma, iqr / 1.34)
        return 0.9 * A * (n ** (-1/5))
    else:
        raise ValueError(f"Unknown bandwidth method: {method}")

def main():
    # --- config ---
    ylabel = 'Density'
    xlabel = 'Value'
    title = 'Title'
    img_name = 'example'

    kernel: KernelType = 'gaussian'
    bandwidth_algorithm: BandwidthAlgorithm = 'scott'

    # 模拟两组数据：对照组和处理组
    np.random.seed(42)
    all_data = [
        np.random.normal(100, 20, 200),  # Control
        np.random.normal(130, 25, 200)   # Treatment
    ]
    labels = ['Control', 'Treatment']

    # 计算密度分布
    all_density = []
    all_x_pos = []
    for data in all_data:
        bw = calculate_bandwidth(data, bandwidth_algorithm)

        kde = KernelDensity(
            bandwidth=bw,
            kernel=kernel
        ).fit(data.reshape(-1, 1))

        # 优化坐标轴范围：留出充足余量以确保曲线平滑收口
        x_min, x_max = data.min(), data.max()
        margin = (x_max - x_min) * 0.4
        x_pos = np.linspace(x_min - margin, x_max + margin, 1000)

        log_density = kde.score_samples(x_pos.reshape(-1, 1))
        density = np.exp(log_density)

        all_density.append(density)
        all_x_pos.append(x_pos)

    # --- figure ---
    fig, ax = plt.subplots(figsize=(5, 5))

    for x_pos, density, label in zip(all_x_pos, all_density, labels):
        # 绘制轮廓线 (线宽已由 mplstyle 控制)
        line, = ax.plot(x_pos, density, label=label)
        # 绘制半透明填充区域
        ax.fill_between(x_pos, density, alpha=0.3, color=line.get_color())

    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.legend() # 图例样式已由 mplstyle 控制

    save_dir = root_path / Path('./img')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_paths = [save_dir / f"{img_name}.png", save_dir / f"{img_name}.pdf"]

    plt.tight_layout()
    for save_path in save_paths:
        plt.savefig(save_path, bbox_inches='tight')

if __name__ == '__main__':
    main()
