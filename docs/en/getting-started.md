# Getting Started

## Installation

```bash
pip install mmcs
```

For development:

```bash
git clone https://github.com/anomalyco/Matplotlib_Medical_Customized_Styles
cd Matplotlib_Medical_Customized_Styles
pip install -e ".[dev]"
```

!!! warning "Font Dependencies (Linux)"

    GraphPad Prism style uses Arial / Helvetica / DejaVu Sans. On Linux,
    install them to avoid subtle visual differences:

    ```bash
    sudo apt install fonts-liberation msttcorefonts
    ```

## Verify

```python
import mmcs

print(mmcs.list_styles())
# [{'name': 'graphpad_prism', 'category': 'GraphPad Prism', ...}, ...]
```

## Your First Chart

```python
import mmcs

result = mmcs.profile.single_column(
    values=[1200, 3500],
    groups=["Control", "KO"],
    errors=[300, 400],
    save_as="my_first_chart.png",
)
```

<figure class="preview-card">
  <img src="/assets/preview_bar.png" alt="Bar Chart" loading="lazy">
  <figcaption>Single Column</figcaption>
</figure>

That's it. One function call, one publication-ready figure.

## Understanding Profiles

`mmcs.profile` provides 12 zero-config presets organized by chart category:

| Category | Preset | Quick API |
|---|---|---|
| Bar | `single_column` | `bar_chart` |
| Bar | `bar_scatter` | `bar_chart` |
| Bar | `grouped_columns` | `clustered_columns_chart` |
| Distribution | `boxplot` | `box_chart` |
| Distribution | `violin` | `violin_chart` |
| Distribution | `box_violin` | `box_violin_chart` |
| XY | `scatter` | `scatter_chart` |
| XY | `correlation` | `regression_chart` |
| 1D | `histogram` | `histogram_chart` |
| 1D | `density` | `density_chart` |
| Multi | `bubble` | `bubble_chart` |
| Multi | `heatmap` | `heatmap_chart` |

Each preset pre-selects sensible defaults. For full control, use the Quick API directly.

See each preset's page for detailed parameters and examples.

## Choosing a Style

Three style families are available. Pass `style=` to any preset or Quick API:

| Style | Best for | Preview |
|---|---|---|
| `graphpad_prism` | Bar, box, violin, scatter, histogram, density, regression | ![GraphPad](/assets/preview_bar.png) |
| `ggplot` | Bubble plots | ![ggplot](/assets/preview_bubble.png) |
| `deeptools` | Heatmaps, genomic tracks | ![DeepTools](/assets/preview_heatmap.png) |

```python
# Switch style freely
mmcs.profile.boxplot(data, style="graphpad_prism")
mmcs.profile.heatmap(data, style="deeptools")
```

Find compatible styles:

```python
mmcs.list_styles_for("bar")
# [{'name': 'graphpad_prism', ...}]
```

## DataFrame Input

mmcs detects column names automatically:

```python
import pandas as pd

df = pd.DataFrame({
    "Group": ["Con", "Con", "KO", "KO"],
    "Expression": [100, 120, 340, 360],
})

mmcs.profile.boxplot(df)  # "Group" → x  "Expression" → y
```

For non-standard column names, specify explicitly:

```python
mmcs.bar_chart(df, x="Condition", y="Signal")
```

## What's Next

- [Styles](styles.md) — deep dive into style customization
- [Profile Presets](profile/single-column.md) — per-chart details and advanced options
- API Reference — auto-generated from docstrings
