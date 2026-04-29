# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-04-29

### Added

- **Profile presets** — 12 zero-config `mmcs.profile.*` presets wrapping the Quick API with sensible defaults (`single_column`, `bar_scatter`, `grouped_columns`, `boxplot`, `violin`, `box_violin`, `scatter`, `correlation`, `histogram`, `density`, `bubble`, `heatmap`).
- **DataFrame auto-detection** — automatically infer x (group) and y (value) columns from column names and dtypes when a DataFrame is passed without explicit column arguments.
- **Documentation site** — MkDocs Material site with zh/en bilingual support, 12 profile preset pages, Getting Started guide, Styles reference, and auto-generated API Reference via mkdocstrings.
- **All source docstrings** — complete Google-style docstrings for every public function, method, class, and type alias across the entire codebase (67 new docstrings).
- **Extended style compatibility check** — `Style.apply()` now checks both `chart_types` and `chart_styles` keys to avoid false-positive warnings for style variants.
- **Tests for auto-detection** — 25 new parameterized tests covering column name matching, fallback heuristics, and `_resolve_frame` integration.

### Changed

- Bumped version to 0.2.0.
- `mmcs.__version__` now tracked in `mmcs/__init__.py`.

## [0.1.0] - 2026-04-28

### Added

- **Core library** — `mmcs` package with pip-installable Python library structure.
- **Style registry** — auto-discovery of `.mplstyle` files and `metadata.json` from `mmcs/styles/`. Public API: `list_styles()`, `list_styles_for()`, `get_style()`, `Style` class.
- **StyleContext** — runtime dynamic value injector connecting static `.mplstyle` config with data-dependent defaults. Color methods: `bar_colors()`, `scatter_colors()`, `box_colors()`.
- **Chart renderers** — 13 low-level rendering modules in `mmcs/charts/`: bar, boxplot, scatter, DBSCAN scatter, violin, box-violin, clustered columns, histogram, density, heatmap, aggregate heatmap, bubble, regression.
- **Quick API** — 12 high-level `mmcs.*_chart()` functions wrapping renderers with StyleContext integration.
- **Utility modules** — statistical helpers (`_stats.py`: bandwidth, significance stars, KDE, optimal bins), annotation helpers (`_annotation.py`: sample sizes, jitter), export helpers (`_export.py`: dual-format save).
- **Chart examples** — 17 runnable example scripts in `examples/`.
- **Test suite** — 130 tests (96 unit + 25 auto-detection + 9 golden image), parameterized across chart types and input formats.
- **Style families** — three `.mplstyle` families: GraphPad Prism (11 chart types), DeepTools (2), ggplot (1).
- **Metadata system** — `metadata.json` per style family declaring style name, category, chart types, and chart-style file mapping.
- **Compatibility warning** — `UserWarning` when applying a style to an undeclared chart type.
- **Golden image tests** — `pytest-mpl` regression tests with 9 baseline images.
- **CI configuration** — GitHub Actions workflow (`check.yaml`) running ruff + pytest.
- **Check script** — `scripts/check.sh` for local validation.
- **New style scaffold** — `scripts/new_style.sh` for bootstrapping new style directories.

[unreleased]: https://github.com/YangShu233-Snow/Matplotlib_Medial_Customized_Styles/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/YangShu233-Snow/Matplotlib_Medial_Customized_Styles/releases/tag/v0.2.0
[0.1.0]: https://github.com/YangShu233-Snow/Matplotlib_Medial_Customized_Styles/releases/tag/v0.1.0
