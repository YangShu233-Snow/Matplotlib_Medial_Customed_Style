# Styles

mmcs provides three style families. Each family has a base style (shared rcParams)
and optional chart-specific overrides loaded automatically when you create a chart.

## Available Styles

### graphpad_prism

GraphPad Prism-inspired aesthetics: clean axes with hidden top/right spines, inward ticks,
bold labels, and minimal grid. The default style for most chart types.

- **Base style:** `graphpad_prism.mplstyle`
- **Chart-specific:** bar, scatter, boxplot, violin, box_violin, histogram, density, regression
- **Best for:** Biomedical publications, bar charts, distribution plots

### ggplot

R ggplot2-inspired aesthetics: full axis spines, light gray grid lines, and a
warm color palette.

- **Chart-specific:** bubble
- **Best for:** Bubble plots, multi-dimensional data

### deeptools

DeepTools-inspired aesthetics: genomics color schemes with diverging colormaps.

- **Chart-specific:** heatmap_clustered, heatmap_multi
- **Best for:** Genomic heatmaps, clustered heatmaps

## How Styles Work

When you call a profile preset or Quick API, mmcs:

1. Loads the **base style** (shared rcParams)
2. Loads the **chart-specific style** override (if one exists for the chart type)
3. The renderer then draws using these rcParams

All three layers (base → chart-specific → renderer) stack automatically.

## Style Customization

You can create a custom `.mplstyle` file and use it with any mmcs chart:

```python
from mmcs import Style

custom = Style("graphpad_prism")  # start from a known style
# Or use a custom .mplstyle file directly:
import matplotlib.pyplot as plt
plt.style.use("path/to/your/custom.mplstyle")
```

!!! note "Hex Colors"
    In `.mplstyle` files, write hex colors **without** the `#` prefix.
    For example: `003366`, not `#003366`.

## Listing Styles from Code

```python
import mmcs

# All styles
print(mmcs.list_styles())

# Styles compatible with a specific chart type
print(mmcs.list_styles_for("heatmap"))
```

## See Also

- [Profile Presets](profile/single-column.md) — usage examples for each chart type
- [Getting Started](getting-started.md) — installation and first chart
