# 单组线性回归散点图 - GraphPad 风格 (Single Linear Regression Scatter Chart GraphPad Style)

这是一个用于复刻 GraphPad Prism 经典线性回归散点图（包含数据分布点、线性拟合直线以及 $R^2$ 和 $P$ 值统计信息）的 matplotlib 示例。

## 📊 效果预览

![](img/example.png)

## ✨ 核心特性

* **GraphPad 样式预设**：通过 `assets/single_linear_regression_scatter_chart.mplstyle` 实现了字体、轴线粗细、刻度方向、散点颜色和线宽等底层样式的全局接管。
* **线性拟合及统计信息计算**：自动使用 `numpy.polyfit` 计算斜率和截距进行线性拟合，并计算和标注相关的决定系数 ($R^2$) 及统计显著性 ($P$ 值)。
* **样式与逻辑分离**：为了方便后续复用，所有的颜色（散点、拟合线）、线宽以及字体相关的设置都默认隔离在了 `.mplstyle` 样式文件中，而 Python 脚本主要负责数据相关的逻辑计算。

## 🚀 快速运行

确保你已经安装了 `matplotlib`, `numpy` 和 `scipy`。然后在当前目录下运行：

```bash
python example.py
```

运行后，图表将自动生成并保存在 `./img/example.png` 与 `./img/example.pdf` 中，以供高质量学术排版使用。

## 🛠️ 如何替换为你自己的数据？

打开 `example.py`，修改 `main` 函数中的以下配置和数据生成区域，即可应用到你的研究数据中：

```python
# --- config ---
# 图表标签信息
xlabel = 'X Value'
ylabel = 'Y Value'
title = 'Title'
img_name = 'example'

# --- 模拟数据 ---
# 替换为你的真实 x 和 y 数据集
x_data = np.random.uniform(3, 10, size=50)
y_data = x_data + np.random.uniform(-2, 4, size=50)

# 散点半径计算因子 (用于计算散点面积 s=np.pi * r ** 2)
r = 2.0
```

如果需要修改颜色、拟合线宽、散点形状或其他图表视觉效果，推荐编辑 `assets/single_linear_regression_scatter_chart.mplstyle` 文件。
