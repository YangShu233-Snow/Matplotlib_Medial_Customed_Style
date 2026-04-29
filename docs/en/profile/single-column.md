# Single Column

`mmcs.profile.single_column()` — bar chart for one or two groups.

## Overview

<figure class="preview-card">
  <img src="/assets/preview_bar.png" alt="Single Column" loading="lazy">
  <figcaption>Single Column</figcaption>
</figure>

Single Column is the most common biomedical chart preset. It creates a bar chart with:

- Asymmetric error bars (upper-only by default)
- Optional significance stars between bars
- Optional individual scatter points overlaid on bars

## Parameters

### `single_column`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `values` | `Sequence[float]` | required | Group means (one value per bar) |
| `groups` | `Sequence[str] | None` | `None` | Bar labels (one per value) |
| `errors` | `Sequence[float] | None` | `None` | Error bar values (SEM or SD) |
| `style` | `str` | `"graphpad_prism"` | Style family name |
| `save_as` | `str | Path | None` | `None` | Save path (auto-detects PNG/PDF from extension) |
| `ylabel` | `str | None` | `None` | Y-axis label |
| `title` | `str | None` | `None` | Chart title (appears above axes) |

### `bar_scatter`

Accepts all `single_column` parameters, plus:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `scatter_data` | `Sequence[np.ndarray]` | required | Raw data arrays for scatter overlay (one per bar) |

## Examples

### Basic two-group comparison

```python
import mmcs

result = mmcs.profile.single_column(
    values=[1200, 3500],
    groups=["Control", "KO"],
    errors=[300, 400],
    save_as="comparison.png",
)
```

### With significance stars

```python
from mmcs import bar_chart

result = bar_chart(
    data=[1200, 3500],
    groups=["Control", "KO"],
    errors=[300, 400],
    stars=[0, 3],  # 3 stars on the second bar
)
```

### With scatter overlay

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

## Style Compatibility

Tested with `graphpad_prism`. Other styles may work but output is not guaranteed.

## See Also

- Profile: [Bar with Scatter](bar-scatter.md)
- Quick API: `mmcs.bar_chart()`
- Renderer: `mmcs.charts.bar.render()`