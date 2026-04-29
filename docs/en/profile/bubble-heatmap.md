# Bubble & Heatmap

Presets for multi-dimensional data: `mmcs.profile.bubble()`, `mmcs.profile.heatmap()`.

## Overview

| Preset | Description | Default Style |
|---|---|---|
| `bubble` | Multi-dimensional bubble plot encoding 4 variables: x-position, bubble size, bubble color, category labels. | `ggplot` |
| `heatmap` | Clustered heatmap with row and column dendrograms. Supports z-score normalization. | `deeptools` |

<figure class="preview-card">
  <img src="/assets/preview_bubble.png" alt="Bubble" loading="lazy">
  <figcaption>Bubble</figcaption>
</figure>
<figure class="preview-card">
  <img src="/assets/preview_heatmap.png" alt="Heatmap" loading="lazy">
  <figcaption>Heatmap</figcaption>
</figure>

## Parameters

### `bubble`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `categories` | `Sequence[str]` | required | Category labels for y-axis |
| `x_values` | `Sequence[float]` | required | X-axis positions (e.g., enrichment scores) |
| `bubble_sizes` | `Sequence[float]` | required | Bubble radii (e.g., -log10 p-value) |
| `color_values` | `Sequence[float]` | required | Bubble color encoding (e.g., fold change) |
| `style` | `str` | `"ggplot"` | Style family name |
| `save_as` | `str | Path | None` | `None` | Save path |
| `title` | `str | None` | `None` | Chart title |

### `heatmap`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `data` | `np.ndarray` | required | 2D array (genes × samples) |
| `row_labels` | `Sequence[str] | None` | `None` | Labels for each row (gene names) |
| `col_labels` | `Sequence[str] | None` | `None` | Labels for each column (sample names) |
| `style` | `str` | `"deeptools"` | Style family name |
| `save_as` | `str | Path | None` | `None` | Save path |
| `title` | `str | None` | `None` | Chart title |

## Examples

### Bubble plot

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

### Heatmap

```python
import numpy as np
import mmcs

data = np.random.randn(20, 10)  # 20 genes × 10 samples

result = mmcs.profile.heatmap(
    data,
    row_labels=[f"Gene{i}" for i in range(20)],
    col_labels=[f"Sample{i}" for i in range(10)],
    save_as="heatmap.png",
)
```

## Style Compatibility

- `bubble` is tested with `ggplot` (grid lines, full spines).
- `heatmap` is tested with `deeptools` (genomics color schemes).

## See Also

- Quick API: `mmcs.bubble_chart()` · `mmcs.heatmap_chart()`
- Renderers: `mmcs.charts.bubble.render()` · `mmcs.charts.heatmap.render()`