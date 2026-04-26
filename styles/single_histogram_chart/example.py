from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# 设置路径
root_path = Path(__file__).parent
style_file = root_path / './assets/single_histogram_chart.mplstyle'
plt.style.use(style_file)

def calculate_optimal_bins(data: np.ndarray) -> int:
    """
    使用 Freedman-Diaconis 准则动态计算最优直方图分组数。
    该算法对异常值具有较好的鲁棒性。
    """
    n = len(data)
    if n < 2:
        return 1

    # 计算四分位距 (IQR)
    q75, q25 = np.percentile(data, [75, 25])
    iqr = q75 - q25

    if iqr == 0:
        # 如果 IQR 为 0，退化到 Sturges 准则
        return int(np.ceil(np.log2(n) + 1))

    # Freedman-Diaconis 宽度计算公式: h = 2 * IQR * n^(-1/3)
    h = 2 * iqr * (n ** (-1/3))
    data_range = np.max(data) - np.min(data)

    if h == 0:
        return 1

    return int(np.ceil(data_range / h))

def main():
    # 1. 配置信息
    xlabel = 'Value'
    ylabel = 'Frequency'
    title = 'Title'
    img_name = 'example'

    # 2. 生成模拟数据 (正态分布)
    np.random.seed(12)
    data = np.random.normal(loc=50, scale=10, size=1000)

    # 3. 创建图表
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)

    # 动态计算分组数
    optimal_bins = calculate_optimal_bins(data)

    # 绘制直方图
    # 样式已经在 .mplstyle 中定义
    ax.hist(data, bins=optimal_bins, rwidth=0.9)

    # 设置标签和标题
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, pad=15)

    # 4. 保存图片
    save_dir = root_path / 'img'
    save_dir.mkdir(parents=True, exist_ok=True)

    plt.tight_layout()
    for ext in ['png', 'pdf']:
        save_path = save_dir / f"{img_name}.{ext}"
        plt.savefig(save_path, bbox_inches='tight')

    print(f"Optimal bins calculated: {optimal_bins}")
    print(f"Images saved to {save_dir}")

if __name__ == '__main__':
    main()
