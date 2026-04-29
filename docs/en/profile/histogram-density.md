# Histogram & Density

Presets for univariate distribution: `mmcs.profile.histogram()`, `mmcs.profile.density()`.

## Overview

| Preset | Description |
|---|---|
| `histogram` | Histogram with automatic binning using the Freedman-Diaconis rule. Octave-gray color scheme. |
| `density` | KDE density plot with smooth curves and semi-transparent fill. Supports multiple groups. |

<figure class="preview-card">
  <img src="/assets/preview_histogram.png" alt="Histogram" loading="lazy">
  <figcaption>Histogram</figcaption>
</figure>
<figure class="preview-card">
  <img src="/assets/preview_density.png" alt="Density" loading="lazy">
  <figcaption>Density</figcaption>
</figure>

## Parameters

### `histogram`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `data` | `Sequence[float]` | required | Data values |
| `style` | `str` | `"graphpad_prism"` | Style family name |
| `save_as` | `str | Path | None` | `None` | Save path |
| `xlabel` | `str | None` | `None` | X-axis label |
| `ylabel` | `str | None` | `None` | Y-axis label |
| `title` | `str | None` | `None` | Chart title |

### `density`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `data` | `Sequence[np.ndarray]` | required | List of arrays, one per group |
| `groups` | `Sequence[str] | None` | `None` | Group labels |
| `style` | `str` | `"graphpad_prism"` | Style family name |
| `save_as` | `str | Path | None` | `None` | Save path |
| `bandwidth` | `str` | `"scott"` | KDE bandwidth: `"scott"` or `"silverman"` |
| `xlabel` | `str | None` | `None` | X-axis label |
| `ylabel` | `str | None` | `None` | Y-axis label |
| `title` | `str | None` | `None` | Chart title |

## Examples

### Histogram

```python
import numpy as np
import mmcs

np.random.seed(12)
data = np.random.normal(100, 20, 200)

result = mmcs.profile.histogram(data, xlabel="Expression", ylabel="Frequency")
```

### Density plot (multi-group)

```python
data = [np.random.normal(90, 15, 100), np.random.normal(110, 20, 100)]

result = mmcs.profile.density(
    data,
    groups=["Control", "KO"],
    xlabel="Expression",
)
```

## Style Compatibility

Tested with `graphpad_prism`. Histogram binning uses the
Freedman-Diaconis rule via `mmcs._utils._stats.optimal_bins()`.

## See Also

- Quick API: `mmcs.histogram_chart()` · `mmcs.density_chart()`
- Renderers: `mmcs.charts.histogram.render()` · `mmcs.charts.density.render()`