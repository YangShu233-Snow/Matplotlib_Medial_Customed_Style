# 直方图与密度图

单变量分布可视化预设：`mmcs.profile.histogram()`、`mmcs.profile.density()`。

## 概述

| 预设 | 说明 |
|---|---|
| `histogram` | 直方图，使用 Freedman-Diaconis 准则自动分箱。八度灰配色。 |
| `density` | KDE 密度分布图，平滑曲线与半透明填充。支持多组叠加。 |

<figure class="preview-card">
  <img src="/assets/preview_histogram.png" alt="直方图" loading="lazy">
  <figcaption>直方图</figcaption>
</figure>
<figure class="preview-card">
  <img src="/assets/preview_density.png" alt="密度图" loading="lazy">
  <figcaption>密度图</figcaption>
</figure>

## 参数

### `histogram`

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `data` | `Sequence[float]` | 必填 | 数据值 |
| `style` | `str` | `"graphpad_prism"` | 风格家族名称 |
| `save_as` | `str | Path | None` | `None` | 保存路径 |
| `xlabel` | `str | None` | `None` | X 轴标签 |
| `ylabel` | `str | None` | `None` | Y 轴标签 |
| `title` | `str | None` | `None` | 图表标题 |

### `density`

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `data` | `Sequence[np.ndarray]` | 必填 | 数组列表，每组一个数组 |
| `groups` | `Sequence[str] | None` | `None` | 组标签 |
| `style` | `str` | `"graphpad_prism"` | 风格家族名称 |
| `save_as` | `str | Path | None` | `None` | 保存路径 |
| `bandwidth` | `str` | `"scott"` | KDE 带宽：`"scott"` 或 `"silverman"` |
| `xlabel` | `str | None` | `None` | X 轴标签 |
| `ylabel` | `str | None` | `None` | Y 轴标签 |
| `title` | `str | None` | `None` | 图表标题 |

## 示例

### 直方图

```python
import numpy as np
import mmcs

np.random.seed(12)
data = np.random.normal(100, 20, 200)

result = mmcs.profile.histogram(data, xlabel="Expression", ylabel="Frequency")
```

### 密度图（多组）

```python
data = [np.random.normal(90, 15, 100), np.random.normal(110, 20, 100)]

result = mmcs.profile.density(
    data,
    groups=["Control", "KO"],
    xlabel="Expression",
)
```

## 风格兼容性

经测试支持 `graphpad_prism`。直方图分箱使用 Freedman-Diaconis 准则，通过 `mmcs._utils._stats.optimal_bins()` 实现。

## 相关链接

- Quick API: `mmcs.histogram_chart()` · `mmcs.density_chart()`
- 底层渲染器: `mmcs.charts.histogram.render()` · `mmcs.charts.density.render()`