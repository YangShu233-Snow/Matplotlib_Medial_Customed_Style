# Bar with Scatter

`mmcs.profile.bar_scatter()` — bar chart with individual data points overlaid.

!!! tip
    This is an alias for `mmcs.profile.single_column()` with the `scatter_data` parameter
    filled. See [Single Column](single-column.md) for full parameter documentation.

<figure class="preview-card">
  <img src="/assets/preview_bar_scatter.png" alt="Bar with Scatter" loading="lazy">
  <figcaption>Bar with Scatter</figcaption>
</figure>

## When to Use

Use `bar_scatter` when you want to show both the aggregate statistics (bars) and the
individual observations (scatter points). This is the standard in biomedical publications
for sample sizes under ~30 per group.

## Example

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

## See Also

- Profile: [Single Column](single-column.md)
- Quick API: `mmcs.bar_chart()`
- Renderer: `mmcs.charts.bar.render()`