# Grouped Columns

`mmcs.profile.grouped_columns()` — clustered bar chart with multiple sub-groups per category.

## Overview

Creates a clustered column chart with:

- Multiple categories on the x-axis, each with multiple sub-groups
- Jittered scatter points overlaid on each bar
- Optional comparison lines with significance stars between selected sub-groups
- Means and SEM computed automatically from raw data

<figure class="preview-card">
  <img src="/assets/preview_grouped_columns.png" alt="Grouped Columns" loading="lazy">
  <figcaption>Grouped Columns</figcaption>
</figure>

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `groups_data` | `Sequence[tuple]` | required | List of `(category_name, sub_group_names, raw_data_arrays)` tuples |
| `comparisons` | `Sequence[tuple] | None` | `None` | List of `(category_idx, sub_a_idx, sub_b_idx, n_stars)` tuples |
| `style` | `str` | `"graphpad_prism"` | Style family name |
| `save_as` | `str | Path | None` | `None` | Save path |
| `figsize` | `tuple[float, float]` | `(8, 6)` | Figure dimensions in inches |
| `ylabel` | `str | None` | `None` | Y-axis label |
| `title` | `str | None` | `None` | Chart title |

### `groups_data` Format

Each tuple has three elements:

```python
(
    "Category Name",        # str: x-axis category label
    ["CON", "KO"],          # Sequence[str]: sub-group labels
    [                       # Sequence[np.ndarray]: raw data arrays, one per sub-group
        np.array([...]),    # raw values for "CON"
        np.array([...]),    # raw values for "KO"
    ],
)
```

### `comparisons` Format

Each tuple selects two sub-groups within a category and assigns stars:

```python
(
    0,      # int: category index (0-based)
    0,      # int: first sub-group index
    1,      # int: second sub-group index
    3,      # int: number of stars to draw
)
```

## Example

```python
import numpy as np
import mmcs

np.random.seed(12)

groups_data = [
    (
        "Group A", ["CON", "KO"],
        [np.random.normal(1200, 300, 15), np.random.normal(3500, 400, 15)],
    ),
    (
        "Group B", ["CON", "KO-1", "KO-2"],
        [
            np.random.normal(1500, 200, 20),
            np.random.normal(2200, 300, 20),
            np.random.normal(1000, 500, 20),
        ],
    ),
]

result = mmcs.profile.grouped_columns(
    groups_data,
    comparisons=[(0, 0, 1, 3), (1, 0, 1, 2)],
    save_as="grouped_columns.png",
)
```

## Style Compatibility

Tested with `graphpad_prism`. Uses `bar_clustered_scatter` chart style under the hood.

## See Also

- Quick API: `mmcs.clustered_columns_chart()`
- Renderer: `mmcs.charts.clustered_columns.render()`