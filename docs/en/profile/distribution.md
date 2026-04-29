# Distribution (Boxplot / Violin / Box-Violin)

Presets for visualizing data distributions: `mmcs.profile.boxplot()`, `mmcs.profile.violin()`, `mmcs.profile.box_violin()`.

## Overview

Three presets for distribution visualization:

| Preset | Description |
|---|---|
| `boxplot` | Classic box plot showing median, quartiles, and outliers. Auto-annotates sample size per group. |
| `violin` | KDE-based violin plot with bandwidth optimization (Scott / Silverman). Supports split mode for paired comparisons. |
| `box_violin` | Overlaid box + violin: box plot for exact quartiles, violin for probability density. |

<figure class="preview-card">
  <img src="/assets/preview_boxplot.png" alt="Boxplot" loading="lazy">
  <figcaption>Boxplot</figcaption>
</figure>
<figure class="preview-card">
  <img src="/assets/preview_violin.png" alt="Violin" loading="lazy">
  <figcaption>Violin</figcaption>
</figure>
<figure class="preview-card">
  <img src="/assets/preview_box_violin.png" alt="Box-Violin" loading="lazy">
  <figcaption>Box-Violin</figcaption>
</figure>

## Parameters

### `boxplot`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `data` | `Sequence[np.ndarray]` | required | List of arrays, one per group |
| `groups` | `Sequence[str] | None` | `None` | Group labels for x-axis |
| `style` | `str` | `"graphpad_prism"` | Style family name |
| `save_as` | `str | Path | None` | `None` | Save path |
| `ylabel` | `str | None` | `None` | Y-axis label |
| `title` | `str | None` | `None` | Chart title |

### `violin`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `data` | `Sequence[np.ndarray]` | required | List of arrays, one per group |
| `groups` | `Sequence[str] | None` | `None` | Group labels |
| `style` | `str` | `"graphpad_prism"` | Style family name |
| `save_as` | `str | Path | None` | `None` | Save path |
| `bandwidth` | `str` | `"scott"` | KDE bandwidth: `"scott"` or `"silverman"` |
| `show_n` | `bool` | `True` | Annotate sample size above each violin |
| `ylabel` | `str | None` | `None` | Y-axis label |
| `title` | `str | None` | `None` | Chart title |

### `box_violin`

Accepts all `violin` parameters plus:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `split` | `bool` | `False` | Split mode for overlaid comparison |
| `split_labels` | `list[str] | None` | `None` | Labels for split halves |

## Examples

### Boxplot

```python
import numpy as np
import mmcs

np.random.seed(12)
data = [np.random.normal(100, 20, 30), np.random.normal(120, 25, 30)]

result = mmcs.profile.boxplot(data, groups=["Control", "KO"])
```

### Violin

```python
result = mmcs.profile.violin(data, groups=["Control", "KO"], bandwidth="scott")
```

### Split violin

```python
# data is a list of two arrays, each with two halves
result = mmcs.profile.violin(
    data, groups=["Control", "KO"],
    bandwidth="scott",
)
```

### Box + Violin overlay

```python
result = mmcs.profile.box_violin(data, groups=["Control", "KO"])
```

## Style Compatibility

Tested with `graphpad_prism`. Violins use custom KDE rendering
via `sklearn.neighbors.KernelDensity` — the native `matplotlib.violinplot`
is **not** used due to known rcParams inheritance issues.

## See Also

- Quick API: `mmcs.box_chart()` · `mmcs.violin_chart()` · `mmcs.box_violin_chart()`
- Renderers: `mmcs.charts.boxplot.render()` · `mmcs.charts.violin.render()` · `mmcs.charts.boxviolin.render()`