# 分簇柱状图

`mmcs.profile.grouped_columns()` — 每个类别下含多个子组的分簇柱状图。

## 概述

创建分簇柱状图，功能包括：

- X 轴上多个类别，每个类别下有多个子组
- 每根柱子上叠加抖动散点
- 可选的组间比较线 + 显著性星号
- 均值和 SEM 自动从原始数据计算

<figure class="preview-card">
  <img src="/assets/preview_grouped_columns.png" alt="分簇柱状图" loading="lazy">
  <figcaption>分簇柱状图</figcaption>
</figure>

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `groups_data` | `Sequence[tuple]` | 必填 | `(类别名, 子组名列表, 原始数据列表)` 元组列表 |
| `comparisons` | `Sequence[tuple] | None` | `None` | `(类别索引, 子组a索引, 子组b索引, 星号数)` 元组列表 |
| `style` | `str` | `"graphpad_prism"` | 风格家族名称 |
| `save_as` | `str | Path | None` | `None` | 保存路径 |
| `figsize` | `tuple[float, float]` | `(8, 6)` | 图形尺寸（英寸） |
| `ylabel` | `str | None` | `None` | Y 轴标签 |
| `title` | `str | None` | `None` | 图表标题 |

### `groups_data` 格式

每个元组包含三个元素：

```python
(
    "Group A",              # str: X 轴类别标签
    ["CON", "KO"],          # Sequence[str]: 子组标签
    [                       # Sequence[np.ndarray]: 原始数据，每个子组一个数组
        np.array([...]),    # "CON" 组的原始值
        np.array([...]),    # "KO" 组的原始值
    ],
)
```

### `comparisons` 格式

每个元组在同一类别内选择两个子组进行比较并标注星号：

```python
(
    0,      # int: 类别索引（从 0 开始）
    0,      # int: 第一个子组索引
    1,      # int: 第二个子组索引
    3,      # int: 星号数量
)
```

## 示例

```python
import numpy as np
import mmcs

np.random.seed(12)

groups_data = [
    (
        "Group A", ["CON", "KO"],
        [np.random.normal(1200, 300, 15), np.random.normal(3500, 400, 15)],
    ),
    (
        "Group B", ["CON", "KO-1", "KO-2"],
        [
            np.random.normal(1500, 200, 20),
            np.random.normal(2200, 300, 20),
            np.random.normal(1000, 500, 20),
        ],
    ),
]

result = mmcs.profile.grouped_columns(
    groups_data,
    comparisons=[(0, 0, 1, 3), (1, 0, 1, 2)],
    save_as="grouped_columns.png",
)
```

## 风格兼容性

经测试支持 `graphpad_prism`。底层使用 `bar_clustered_scatter` 图表样式。

## 相关链接

- Quick API: `mmcs.clustered_columns_chart()`
- 底层渲染器: `mmcs.charts.clustered_columns.render()`