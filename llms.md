# Context for LLMs

**Role:** Expert Scientific Data Visualization Engineer (Medical & Biological Sciences specialist).

This repository, **MMCS (Matplotlib Medical Customized Styles)**, is a Python library that provides publication-ready `matplotlib` styles and chart builders designed for the medical and biological sciences. It wraps GraphPad Prism, ggplot2, and DeepTools-inspired aesthetics into a pip-installable package (`mmcs`).

## 🤖 AI Agent Constraints

If you are an AI Agent participating in the development of this project, you **MUST**:

1. Read `AGENTS.md` first — it contains the high-signal workflow instructions.
2. Read `PLAN.md` — it documents the full refactoring architecture, API design decisions, and phased roadmap.
3. Read `CONTRIBUTING.md` before making any contribution.
4. Translate `.aiignore` into your tool's ignore format (e.g., `.cursorignore`, `.geminiignore`).
5. Use `conda activate Matplotlib_Medial_Customzied_Styles` to activate the development environment.

## 📁 Project Structure

```text
mmcs/                            # Python package (pip install mmcs)
  __init__.py                    # Public API: profile, chart functions, Style, StyleContext
  _registry.py                   # Style discovery + metadata loading
  _context.py                    # StyleContext — dynamic rcParams injection
  _profile.py                    # 12 zero-config profile presets
  _quick_api/                    # Quick API layer (11 submodules)
    _bar.py, _box.py, _violin.py, ...
  charts/                        # Chart renderers (13 submodules)
    _bar.py, _boxplot.py, _violin.py, ...
  _utils/                        # Utility functions
    _stats.py                    # Bandwidth, significance stars, KDE, optimal bins
    _annotation.py               # Sample sizes, jitter
    _export.py                   # PNG/PDF dual export
  styles/                        # .mplstyle files (3 style families)
    graphpad_prism/
    ggplot/
    deeptools/
examples/                        # 17 example scripts
docs/                            # MkDocs Material documentation site (zh/en)
tests/                           # 130+ tests
scripts/                         # new_style.sh, check.sh
```

## 🛠️ Mandatory Coding Checklist

- [ ] **Scaffolding**: Use `./scripts/new_style.sh <name>` to start a new style family.
- [ ] **Paths**: Use `pathlib.Path` exclusively (root reference: `Path(__file__).parent`).
- [ ] **Style loading**: Load `.mplstyle` via `plt.style.use()` **BEFORE** `plt.subplots()`.
- [ ] **Style decoupling**: Keep all styling in `.mplstyle` files, not in Python code.
- [ ] **Dual export**: Always save as both `.png` and `.pdf` to `img/`.
- [ ] **Headless-safe**: Leave `plt.show()` commented out.
- [ ] **Docstrings**: All public API must have Google-style docstrings.
- [ ] **Aesthetics**: Hidden top/right spines, bold labels, inward ticks, upper-only error bars.

## ⚠️ Critical Design Rules

- **Style × Chart = Orthogonal**: Any style works with any chart type. Declare compatibility via `metadata.json` (`chart_types` and `chart_styles` keys).
- **Three API Layers**: Profile presets → Quick API → Renderers. Profile is the highest level.
- **StyleContext**: General dynamic injection layer for runtime defaults (colors, spacing, etc.). Not just a color manager.
- **Renderer purity**: Renderers do NOT infer default values. All defaults come from the caller (via `StyleContext`).
- **Colors**: `.mplstyle` defines `axes.prop_cycle` palette. `bar.render()` uniformly samples from it. No hardcoded colors.
- **Heatmap cmap**: Read from `plt.rcParams["image.cmap"]` (set by `.mplstyle`), not hardcoded.

## ⚠️ .mplstyle Pitfalls

- **Hex colors**: Do NOT use `#` prefix (e.g. write `003366`, not `#003366`).
- **Violinplot**: matplotlib native `violinplot` does NOT inherit `patch.rcParams`. Use the custom KDE renderer in `mmcs.charts._violin`.
- **Composite alignment**: When overlaying components (e.g. box+violin), compute geometric center offsets.

## 🤝 Contribution Guidance

- Read `CONTRIBUTING.md` and `AGENTS.md` before making changes.
- PR requirements: run `./scripts/check.sh` (ruff + pytest), follow Conventional Commits format.
- New chart renderers need: module in `mmcs/charts/`, Quick API in `mmcs/_quick_api/`, Profile preset in `mmcs/_profile.py`, tests, and docs.
