# 气泡图与热图

多维数据可视化预设：`mmcs.profile.bubble()`、`mmcs.profile.heatmap()`。

## 概述

| 预设 | 说明 | 默认风格 |
|---|---|---|
| `bubble` | 多维气泡图，编码 4 个变量：X 位置、气泡大小、气泡颜色、类别标签。 | `ggplot` |
| `heatmap` | 带行列聚类树的热图，支持 Z 值标准化。 | `deeptools` |

<figure class="preview-card">
  <img src="/assets/preview_bubble.png" alt="气泡图" loading="lazy">
  <figcaption>气泡图</figcaption>
</figure>
<figure class="preview-card">
  <img src="/assets/preview_heatmap.png" alt="热图" loading="lazy">
  <figcaption>热图</figcaption>
</figure>

## 参数

### `bubble`

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `categories` | `Sequence[str]` | 必填 | Y 轴类别标签 |
| `x_values` | `Sequence[float]` | 必填 | X 轴位置（如富集分数） |
| `bubble_sizes` | `Sequence[float]` | 必填 | 气泡半径（如 -log10 P 值） |
| `color_values` | `Sequence[float]` | 必填 | 气泡颜色编码（如 Fold Change） |
| `style` | `str` | `"ggplot"` | 风格家族名称 |
| `save_as` | `str | Path | None` | `None` | 保存路径 |
| `title` | `str | None` | `None` | 图表标题 |

### `heatmap`

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `data` | `np.ndarray` | 必填 | 二维数组（基因 × 样本） |
| `row_labels` | `Sequence[str] | None` | `None` | 每行标签（基因名） |
| `col_labels` | `Sequence[str] | None` | `None` | 每列标签（样本名） |
| `style` | `str` | `"deeptools"` | 风格家族名称 |
| `save_as` | `str | Path | None` | `None` | 保存路径 |
| `title` | `str | None` | `None` | 图表标题 |

## 示例

### 气泡图

```python
import numpy as np
import mmcs

categories = ["Gene A", "Gene B", "Gene C", "Gene D", "Gene E"]
x_values = [0.5, 1.2, 2.5, 1.8, 0.9]
bubble_sizes = [30, 50, 80, 40, 60]
color_values = [3.5, 1.2, 0.8, 2.1, 4.5]

result = mmcs.profile.bubble(
    categories, x_values, bubble_sizes, color_values,
    save_as="bubble.png",
)
```

### 热图

```python
import numpy as np
import mmcs

data = np.random.randn(20, 10)  # 20 基因 × 10 样本

result = mmcs.profile.heatmap(
    data,
    row_labels=[f"Gene{i}" for i in range(20)],
    col_labels=[f"Sample{i}" for i in range(10)],
    save_as="heatmap.png",
)
```

## 风格兼容性

- `bubble` 经测试支持 `ggplot` 风格（网格线、完整坐标轴框架）
- `heatmap` 经测试支持 `deeptools` 风格（基因组学配色方案）

## 相关链接

- Quick API: `mmcs.bubble_chart()` · `mmcs.heatmap_chart()`
- 底层渲染器: `mmcs.charts.bubble.render()` · `mmcs.charts.heatmap.render()`