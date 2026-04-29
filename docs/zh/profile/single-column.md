# 单列柱状图

`mmcs.profile.single_column()` — 单组或双组比较的柱状图。

## 概述

最常用的医学科研图表预设。功能包括：

- 非对称误差线（默认仅显示上半部分）
- 可选的组间显著性星号标注
- 可选的在柱子上叠加个体散点

<figure class="preview-card">
  <img src="/assets/preview_bar.png" alt="单列柱状图" loading="lazy">
  <figcaption>单列柱状图</figcaption>
</figure>

## 参数

### `single_column`

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `values` | `Sequence[float]` | 必填 | 各组均值（每根柱子一个值） |
| `groups` | `Sequence[str] | None` | `None` | 柱子标签（每个值对应一个） |
| `errors` | `Sequence[float] | None` | `None` | 误差线值（SEM 或 SD） |
| `style` | `str` | `"graphpad_prism"` | 风格家族名称 |
| `save_as` | `str | Path | None` | `None` | 保存路径（根据后缀自动识别 PNG/PDF） |
| `ylabel` | `str | None` | `None` | Y 轴标签 |
| `title` | `str | None` | `None` | 图表标题 |

### `bar_scatter`

接受 `single_column` 的所有参数，额外增加：

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `scatter_data` | `Sequence[np.ndarray]` | 必填 | 用于散点叠加的原始数据（每根柱子一个数组） |

## 示例

### 基础双组比较

```python
import mmcs

result = mmcs.profile.single_column(
    values=[1200, 3500],
    groups=["Control", "KO"],
    errors=[300, 400],
    save_as="comparison.png",
)
```

### 带显著性标注

```python
from mmcs import bar_chart

result = bar_chart(
    data=[1200, 3500],
    groups=["Control", "KO"],
    errors=[300, 400],
    stars=[0, 3],  # 第二根柱子上标注 3 颗星
)
```

### 叠加散点

```python
import numpy as np
from mmcs import bar_chart

np.random.seed(12)
con = np.random.normal(1200, 300, 15)
ko = np.random.normal(3500, 400, 15)

result = bar_chart(
    data=[float(np.mean(d)) for d in [con, ko]],
    groups=["Control", "KO"],
    errors=[float(np.std(d, ddof=1) / np.sqrt(len(d))) for d in [con, ko]],
    scatter_data=[con, ko],
    stars=[0, 3],
)
```

## 风格兼容性

经测试支持 `graphpad_prism` 风格。其他风格可能产生预期之外的视觉效果。

## 相关链接

- 同类别预设: [带散点的柱状图](bar-scatter.md)
- Quick API: `mmcs.bar_chart()`
- 底层渲染器: `mmcs.charts.bar.render()`