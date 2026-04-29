# Scatter & Correlation

Presets for xy data: `mmcs.profile.scatter()`, `mmcs.profile.correlation()`.

## Overview

| Preset | Description |
|---|---|
| `scatter` | Simple scatter plot. No regression line. |
| `correlation` | Scatter plot with linear regression line, R² and P-value annotation. |

<figure class="preview-card">
  <img src="/assets/preview_scatter.png" alt="Scatter" loading="lazy">
  <figcaption>Scatter</figcaption>
</figure>
<figure class="preview-card">
  <img src="/assets/preview_correlation.png" alt="Correlation" loading="lazy">
  <figcaption>Correlation</figcaption>
</figure>

## Parameters

### `scatter`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x` | `Sequence[float]` | required | X values |
| `y` | `Sequence[float]` | required | Y values |
| `style` | `str` | `"graphpad_prism"` | Style family name |
| `save_as` | `str | Path | None` | `None` | Save path |
| `xlabel` | `str | None` | `None` | X-axis label |
| `ylabel` | `str | None` | `None` | Y-axis label |
| `title` | `str | None` | `None` | Chart title |

### `correlation`

Accepts all `scatter` parameters, plus:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `xlabel` | `str` | `"X Value"` | X-axis label |
| `ylabel` | `str` | `"Y Value"` | Y-axis label |

## Examples

### Scatter plot

```python
import numpy as np
import mmcs

np.random.seed(12)
x = np.random.normal(50, 10, 30)
y = x * 0.8 + np.random.normal(0, 5, 30)

result = mmcs.profile.scatter(x, y, xlabel="Dose", ylabel="Response")
```

### Correlation with regression

```python
result = mmcs.profile.correlation(
    x, y,
    xlabel="Dose (mg)",
    ylabel="Response (AU)",
    save_as="correlation.png",
)
```

## Style Compatibility

Tested with `graphpad_prism`. Regression annotation uses `scipy.stats.linregress`
for R² and P-value calculation.

## See Also

- Quick API: `mmcs.scatter_chart()` · `mmcs.regression_chart()`
- Renderers: `mmcs.charts.scatter.render()` · `mmcs.charts.regression.render()`