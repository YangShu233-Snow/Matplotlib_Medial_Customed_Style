from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import f

root_path = Path(__file__).parent
# 修改为要求的样式文件路径
style_file = root_path / './assets/single_linear_regression_scatter_chart.mplstyle'
plt.style.use(style_file)

def main():
    # --- config ---
    xlabel = 'X Value'
    ylabel = 'Y Value'
    title = 'Title'
    img_name = 'example'

    np.random.seed(12)

    # 模拟数据
    x_data = np.random.uniform(3, 10, size=50)
    y_data = x_data + np.random.uniform(-2, 4, size=50)

    r = 2.0

    # --- linear regression ---
    nums = len(x_data)
    slope, intercept = np.polyfit(
        x_data,
        y_data,
        deg=1
    )

    y_regression_data: np.ndarray = x_data * slope + intercept

    mean_y = np.mean(y_data)
    sst_y = np.sum((y_data - mean_y) ** 2)
    ssr_y = np.sum((y_data - y_regression_data) ** 2)

    r_2 = 1 - ssr_y / sst_y
    f_value = r_2 / (1 - r_2) * (nums - 2)
    P_value = 1 - f.cdf(f_value, 1, nums-2)

    # --- figure ---
    fig, ax = plt.subplots(figsize=(5, 5), dpi=300)
    ax.scatter(
        x_data,
        y_data,
        s=np.pi * r ** 2
    )

    sorted_index = np.argsort(x_data)
    ax.plot(
        x_data[sorted_index],
        y_regression_data[sorted_index]
    )

    # --- stats text ---
    stats_text = f"$R^2$ = {r_2:.3f}\n$P$ {('< 0.0001' if P_value < 0.0001 else f'= {P_value:.4f}')}"
    ax.text(
        0.05, 0.95,
        stats_text,
        transform=ax.transAxes,
        verticalalignment='top',
        horizontalalignment='left'
    )

    # --- labels and format ---
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    save_dir = root_path / Path('./img')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_paths = [save_dir / f"{img_name}.png", save_dir / f"{img_name}.pdf"]

    plt.tight_layout()
    for save_path in save_paths:
        plt.savefig(save_path, bbox_inches='tight')

if __name__ == '__main__':
    main()
