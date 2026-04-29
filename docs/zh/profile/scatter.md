# 散点与相关性

XY 数据可视化预设：`mmcs.profile.scatter()`、`mmcs.profile.correlation()`。

## 概述

| 预设 | 说明 |
|---|---|
| `scatter` | 简单散点图，不包含回归线。 |
| `correlation` | 散点图叠加线性回归线，自动标注 R² 和 P 值。 |

<figure class="preview-card">
  <img src="/assets/preview_scatter.png" alt="散点图" loading="lazy">
  <figcaption>散点图</figcaption>
</figure>
<figure class="preview-card">
  <img src="/assets/preview_correlation.png" alt="相关性分析" loading="lazy">
  <figcaption>相关性分析</figcaption>
</figure>

## 参数

### `scatter`

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `x` | `Sequence[float]` | 必填 | X 值 |
| `y` | `Sequence[float]` | 必填 | Y 值 |
| `style` | `str` | `"graphpad_prism"` | 风格家族名称 |
| `save_as` | `str | Path | None` | `None` | 保存路径 |
| `xlabel` | `str | None` | `None` | X 轴标签 |
| `ylabel` | `str | None` | `None` | Y 轴标签 |
| `title` | `str | None` | `None` | 图表标题 |

### `correlation`

接受 `scatter` 的所有参数。

## 示例

### 散点图

```python
import numpy as np
import mmcs

np.random.seed(12)
x = np.random.normal(50, 10, 30)
y = x * 0.8 + np.random.normal(0, 5, 30)

result = mmcs.profile.scatter(x, y, xlabel="Dose", ylabel="Response")
```

### 相关性分析

```python
result = mmcs.profile.correlation(
    x, y,
    xlabel="Dose (mg)",
    ylabel="Response (AU)",
    save_as="correlation.png",
)
```

## 风格兼容性

经测试支持 `graphpad_prism`。回归标注使用 `scipy.stats.linregress` 计算 R² 和 P 值。

## 相关链接

- Quick API: `mmcs.scatter_chart()` · `mmcs.regression_chart()`
- 底层渲染器: `mmcs.charts.scatter.render()` · `mmcs.charts.regression.render()`