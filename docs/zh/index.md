<p align="center">
  <img src="/assets/MMCS_LOGO.png" width="250" alt="MMCS Logo">
</p>

# MMCS — Matplotlib Medical Customized Styles

<p align="center"><strong>Reusable · Instant · Professional · Evolving</strong></p>

面向医学与生物科学的出版级 Matplotlib 样式和图表构建工具。

## 为什么要用 mmcs？

`matplotlib` 固然强大，但其默认样式远不能满足严肃的医学科研出版需求。
现有的样式库如 [SciencePlots](https://github.com/garrettj403/SciencePlots) 在生命科学与医学领域也存在"水土不服"的问题。

**本库让你专注于数据本身，不再为线宽、刻度等样式细节耗费时间。**

## 特性

| 特性 | 说明 |
|---|---|
| **出版级美学** | 源自 GraphPad Prism、ggplot2 和 DeepTools 的风格，一行代码复现期刊级图表 |
| **零配置预设** | `mmcs.profile.single_column(data)` 无需调参即可生成完整图表 |
| **样式 × 图表正交** | 任意样式可与任意图表自由组合，互不耦合 |
| **双层 API** | 高层 `mmcs.bar_chart()` 一键出图，底层渲染器完全可控 |
| **PNG + PDF 双输出** | 一次调用同时保存两种格式 |

## 核心依赖

| 包 | 用途 |
|---|---|
| [matplotlib](https://matplotlib.org/) | 核心绘图引擎与 rcParams 样式管理 |
| [numpy](https://numpy.org/) | 数组计算与数值运算 |
| [scipy](https://scipy.org/) | 统计函数与核密度估计 |
| [scikit-learn](https://scikit-learn.org/) | KDE 带宽优化与 DBSCAN 聚类 |
| [pandas](https://pandas.pydata.org/) | DataFrame 输入支持与表格数据处理 |

## 快速开始

```bash
pip install mmcs
```

```python
import mmcs

result = mmcs.profile.single_column(
    values=[1200, 3500],
    groups=["Control", "KO"],
    errors=[300, 400],
    save_as="output.png",
)
```

## 样式画廊

### GraphPad Prism 风格

| 预设 | 描述 | API |
|---|---|---|
| 单列柱状图 | 经典的双组/多组比较柱状图，支持非对称误差线和显著性标注 | `mmcs.profile.single_column()` |
| 柱状散点图 | 柱状图叠加个体数据点 | `mmcs.profile.bar_scatter()` |
| 分簇柱状图 | 分组柱状图叠加抖动散点和组间比较线 | `mmcs.profile.grouped_columns()` |
| 箱线图 | 简约箱线图，自动标注样本量 | `mmcs.profile.boxplot()` |
| 小提琴图 | KDE 小提琴图，支持 Scott / Silverman 带宽优化 | `mmcs.profile.violin()` |
| 箱线+小提琴 | 箱线图与小提琴图叠加组合 | `mmcs.profile.box_violin()` |
| 散点与相关性 | DBSCAN 聚类散点图 / 线性回归散点图（自动标注 R²、P 值） | `mmcs.profile.scatter()` / `mmcs.profile.correlation()` |
| 直方图 | 直方图，内置 Freedman-Diaconis 准则自动分箱 | `mmcs.profile.histogram()` |
| 密度图 | KDE 密度分布图，平滑曲线与半透明填充 | `mmcs.profile.density()` |

### R ggplot 风格

| 预设 | 描述 | API |
|---|---|---|
| 气泡图 | 多维度气泡图，支持大小和颜色双变量编码 | `mmcs.profile.bubble()` |

### DeepTools 风格

| 预设 | 描述 | API |
|---|---|---|
| 热图 | 带聚类树的行列聚类热图 | `mmcs.profile.heatmap()` |

## 下一步

- [入门指南](getting-started.md) — 安装与第一个图表
- [样式系统](styles.md) — 可用风格家族与自定义
- [快捷预设](profile/single-column.md) — 每类图表的详细用法

## 致谢

本项目受到以下项目和资料的启发与帮助：

- [From Data to Viz](https://www.data-to-viz.com/)
- [Matplotlib](https://matplotlib.org/)
- [GraphPad Prism](https://www.graphpad.com/)
- [DeepTools](https://github.com/deeptools/deepTools)
