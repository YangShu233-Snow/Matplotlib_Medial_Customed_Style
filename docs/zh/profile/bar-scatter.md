# 带散点的柱状图

`mmcs.profile.bar_scatter()` — 在柱状图上叠加个体数据点。

!!! tip
    本预设是 `single_column()` 的别名，自动传入 `scatter_data` 参数。
    完整参数参考见 [单列柱状图](single-column.md)。

<figure class="preview-card">
  <img src="/assets/preview_bar_scatter.png" alt="柱状散点图" loading="lazy">
  <figcaption>柱状散点图</figcaption>
</figure>

## 适用场景

当需要同时展示聚合统计量（柱子）和个体观测值（散点）时使用。这是生物医学出版物对于每组样本数约 30 以下时的标准做法。

## 示例

```python
import numpy as np
import mmcs

np.random.seed(12)
con = np.random.normal(1200, 300, 15)
ko = np.random.normal(3500, 400, 15)

result = mmcs.profile.bar_scatter(
    values=[float(np.mean(d)) for d in [con, ko]],
    scatter_data=[con, ko],
    groups=["Control", "KO"],
    errors=[float(np.std(d, ddof=1) / np.sqrt(len(d))) for d in [con, ko]],
    save_as="bar_scatter.png",
)
```

## 相关链接

- 同类别预设: [单列柱状图](single-column.md)
- Quick API: `mmcs.bar_chart()`
- 底层渲染器: `mmcs.charts.bar.render()`