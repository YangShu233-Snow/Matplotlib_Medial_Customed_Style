<p align="center">
  <img src="/assets/MMCS_LOGO.png" width="250" alt="MMCS Logo">
</p>

# MMCS — Matplotlib Medical Customized Styles

<p align="center"><strong>Reusable · Instant · Professional · Evolving</strong></p>

Publication-ready matplotlib styles and chart builders for the medical and biological sciences.

## Why mmcs?

While `matplotlib` is powerful, its default aesthetics fall short for serious biomedical research.
Existing style libraries like [SciencePlots](https://github.com/garrettj403/SciencePlots) don't cater
well to the conventions of medical and life science journals.

**This library lets you focus on your data, not on tweaking line widths and tick marks.**

## Features

| Feature | Description |
|---|---|
| **Publication-ready aesthetics** | GraphPad Prism, ggplot2, and DeepTools-inspired styles — reproduce journal-quality figures with one line |
| **Zero-config presets** | `mmcs.profile.single_column(data)` generates a complete figure without tuning any parameter |
| **Orthogonal style × chart type** | Any style works with any chart — mix and match freely |
| **Dual API** | High-level `mmcs.bar_chart()` for quick results, low-level renderers for full control |
| **PNG + PDF dual export** | One call saves both formats |

## Core Dependencies

| Package | Purpose |
|---|---|
| [matplotlib](https://matplotlib.org/) | Core plotting engine and rcParams styling |
| [numpy](https://numpy.org/) | Array computation and numerical operations |
| [scipy](https://scipy.org/) | Statistical functions and kernel density estimation |
| [scikit-learn](https://scikit-learn.org/) | KDE bandwidth optimization and DBSCAN clustering |
| [pandas](https://pandas.pydata.org/) | DataFrame input support and tabular data handling |

## Quick Start

```bash
pip install mmcs
```

```python
import mmcs

result = mmcs.profile.single_column(
    values=[1200, 3500],
    groups=["Control", "KO"],
    errors=[300, 400],
    save_as="output.png",
)
```

## Style Gallery

### GraphPad Prism

| Preset | Description | API |
|---|---|---|
| Single Column | Classic two/multi-group bar chart with asymmetric error bars and significance stars | `mmcs.profile.single_column()` |
| Bar with Scatter | Bar chart with individual data points overlaid | `mmcs.profile.bar_scatter()` |
| Grouped Columns | Clustered bar chart with jittered scatter and comparison lines | `mmcs.profile.grouped_columns()` |
| Boxplot | Minimalist box plot with sample size annotation | `mmcs.profile.boxplot()` |
| Violin | KDE violin plot with bandwidth optimization (Scott / Silverman) | `mmcs.profile.violin()` |
| Box-Violin | Overlaid box + violin plot | `mmcs.profile.box_violin()` |
| Scatter & Correlation | Scatter plot with DBSCAN clustering or linear regression with R² / P-value | `mmcs.profile.scatter()` / `mmcs.profile.correlation()` |
| Histogram | Histogram with automatic Freedman-Diaconis binning | `mmcs.profile.histogram()` |
| Density | KDE density plot with smooth curves and semi-transparent fill | `mmcs.profile.density()` |

### R ggplot

| Preset | Description | API |
|---|---|---|
| Bubble | Multi-dimensional bubble plot with size and color encoding | `mmcs.profile.bubble()` |

### DeepTools

| Preset | Description | API |
|---|---|---|
| Heatmap | Clustered heatmap with row/column dendrograms | `mmcs.profile.heatmap()` |

## Next Steps

- [Getting Started](getting-started.md) — installation and your first chart
- [Styles](styles.md) — available style families and customization
- [Profile Presets](profile/single-column.md) — detailed usage for each chart type

## Acknowledgments

Inspired by and built upon the work of:

- [From Data to Viz](https://www.data-to-viz.com/)
- [Matplotlib](https://matplotlib.org/)
- [GraphPad Prism](https://www.graphpad.com/)
- [DeepTools](https://github.com/deeptools/deepTools)
