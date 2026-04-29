# 样式系统

mmcs 提供三种风格家族。每个家族包含一个基础样式（共享 rcParams）和可选的图表类型专用覆盖样式，
在创建图表时自动加载。

## 可用风格

### graphpad_prism

受 GraphPad Prism 启发的极简美学：隐藏顶部和右侧坐标轴、刻度线朝内、标签加粗、无网格线。
大多数图表类型的默认风格。

- **基础样式:** `graphpad_prism.mplstyle`
- **图表专用:** 柱状图、散点图、箱线图、小提琴图、箱线+小提琴、直方图、密度图、回归图
- **适用场景:** 生物医学出版物、柱状图、分布图

### ggplot

受 R ggplot2 启发的美学：完整坐标轴框架、浅灰色网格线、温暖色调色板。

- **图表专用:** 气泡图
- **适用场景:** 气泡图、多维数据

### deeptools

受 DeepTools 启发的美学：基因组学配色方案，使用发散型色图。

- **图表专用:** 聚类热图、多面板热图
- **适用场景:** 基因组学热图、聚类热图

## 样式加载机制

当调用 Profile 预设或 Quick API 时，mmcs：

1. 加载**基础样式**（共享 rcParams）
2. 加载**图表专用样式**覆盖（如果该图表类型存在）
3. 渲染器使用最终的 rcParams 进行绘制

三层（基础 → 图表专用 → 渲染器）自动叠加。

## 自定义样式

你可以创建自定义 `.mplstyle` 文件并与任何 mmcs 图表一起使用：

```python
from mmcs import Style

custom = Style("graphpad_prism")  # 从已知风格开始
# 或者直接使用自定义 .mplstyle 文件：
import matplotlib.pyplot as plt
plt.style.use("path/to/your/custom.mplstyle")
```

!!! note "Hex 颜色"
    在 `.mplstyle` 文件中，hex 颜色**不要**加 `#` 前缀。
    例如：写 `003366`，不要写 `#003366`。

## 在代码中列出风格

```python
import mmcs

# 所有风格
print(mmcs.list_styles())

# 兼容某类图表的风格
print(mmcs.list_styles_for("heatmap"))
```

## 相关链接

- [快捷预设](profile/single-column.md) — 每类图表的用法示例
- [入门指南](getting-started.md) — 安装与第一个图表
