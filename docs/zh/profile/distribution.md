# 分布图（箱线图 / 小提琴图 / 箱线+小提琴）

数据分布可视化预设：`mmcs.profile.boxplot()`、`mmcs.profile.violin()`、`mmcs.profile.box_violin()`。

## 概述

三种分布可视化预设：

| 预设 | 说明 |
|---|---|
| `boxplot` | 经典箱线图，展示中位数、四分位数和离群值。自动标注每组样本量。 |
| `violin` | 基于 KDE 的小提琴图，支持带宽优化（Scott / Silverman）。支持分割模式用于成对比较。 |
| `box_violin` | 箱线图与小提琴图叠加组合：箱线图精确展示四分位数，小提琴图展示概率密度分布。 |

<figure class="preview-card">
  <img src="/assets/preview_boxplot.png" alt="箱线图" loading="lazy">
  <figcaption>箱线图</figcaption>
</figure>
<figure class="preview-card">
  <img src="/assets/preview_violin.png" alt="小提琴图" loading="lazy">
  <figcaption>小提琴图</figcaption>
</figure>
<figure class="preview-card">
  <img src="/assets/preview_box_violin.png" alt="箱线+小提琴" loading="lazy">
  <figcaption>箱线+小提琴</figcaption>
</figure>

## 参数

### `boxplot`

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `data` | `Sequence[np.ndarray]` | 必填 | 数组列表，每组一个数组 |
| `groups` | `Sequence[str] | None` | `None` | X 轴组标签 |
| `style` | `str` | `"graphpad_prism"` | 风格家族名称 |
| `save_as` | `str | Path | None` | `None` | 保存路径 |
| `ylabel` | `str | None` | `None` | Y 轴标签 |
| `title` | `str | None` | `None` | 图表标题 |

### `violin`

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `data` | `Sequence[np.ndarray]` | 必填 | 数组列表，每组一个数组 |
| `groups` | `Sequence[str] | None` | `None` | 组标签 |
| `style` | `str` | `"graphpad_prism"` | 风格家族名称 |
| `save_as` | `str | Path | None` | `None` | 保存路径 |
| `bandwidth` | `str` | `"scott"` | KDE 带宽：`"scott"` 或 `"silverman"` |
| `show_n` | `bool` | `True` | 在每个小提琴上方标注样本量 |
| `ylabel` | `str | None` | `None` | Y 轴标签 |
| `title` | `str | None` | `None` | 图表标题 |

### `box_violin`

接受 `violin` 的所有参数，额外增加：

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `split` | `bool` | `False` | 分割模式，用于叠加比较 |
| `split_labels` | `list[str] | None` | `None` | 分割两半的标签 |

## 示例

### 箱线图

```python
import numpy as np
import mmcs

np.random.seed(12)
data = [np.random.normal(100, 20, 30), np.random.normal(120, 25, 30)]

result = mmcs.profile.boxplot(data, groups=["Control", "KO"])
```

### 小提琴图

```python
result = mmcs.profile.violin(data, groups=["Control", "KO"], bandwidth="scott")
```

### 箱线+小提琴叠加

```python
result = mmcs.profile.box_violin(data, groups=["Control", "KO"])
```

## 风格兼容性

经测试支持 `graphpad_prism`。小提琴图使用基于 `sklearn.neighbors.KernelDensity` 的自定义 KDE 渲染——**不**使用 matplotlib 原生的 `violinplot`，因为它存在已知的 rcParams 继承问题。

## 相关链接

- Quick API: `mmcs.box_chart()` · `mmcs.violin_chart()` · `mmcs.box_violin_chart()`
- 底层渲染器: `mmcs.charts.boxplot.render()` · `mmcs.charts.violin.render()` · `mmcs.charts.boxviolin.render()`