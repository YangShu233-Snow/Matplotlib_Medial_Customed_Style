# 聚类散点图 - GraphPad 风格 (Clustered Scatter Chart GraphPad Style)

这是一个用于复刻 GraphPad Prism 风格聚类散点图的 matplotlib 示例，集成了 DBSCAN 聚类算法并支持自动参数估计。

## 📊 效果预览

![Clustered Scatter Plot](./img/example.png)

## ✨ 核心特性

- **GraphPad 样式预设**：通过 `assets/clustered_scatter_chart.mplstyle` 实现了符合学术出版标准的字体、轴线粗-细、刻度方向等样式的全局接管。
- **自动聚类分析**：内置 `clustering_data` 函数，利用 DBSCAN 算法自动识别数据中的簇结构并进行着色。
- **智能参数估计**：使用 `estimate_eps` 函数（向量投影法/肘部法则）自动计算聚类所需的 `eps` 参数，无需繁琐的手动调参。
- **可视化增强选项**：
  - **置信椭圆 (Confidence Ellipse)**：自动计算并绘制数据的分布范围。
  - **凸包 (Convex Hull)**：自动勾勒簇的最外层边缘。

## 🚀 快速运行

确保你已经安装了 `matplotlib`、`numpy`、`scikit-learn` 和 `scipy`。然后在当前目录下运行：

```bash
python example.py
```

运行后，图表将自动生成并保存在 `./img/example.png`。

## 🛠️ 如何配置与替换数据？

打开 `example.py`，您可以修改以下配置来定制您的图表：

```python
# 1. 绘图功能开关
clustered_with_color = True              # 是否启用聚类着色
clustered_with_convex_hull = True       # 是否绘制凸包轮廓
clustered_with_confidence_ellipse = True # 是否绘制置信椭圆

# 2. 文本信息
title = 'Your Plot Title'
xlabel = 'Your X-axis Label'
ylabel = 'Your Y-axis Label'

# 3. 数据信息
# 将 x_data 和 y_data 替换为你自己的 NumPy 数组
x_data = np.array([...])
y_data = np.array([...])
```
