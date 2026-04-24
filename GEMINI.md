# GEMINI.md - Project Context & Instructions

This document provides essential context and instructions for AI agents working on the `matplotlib_GraphPad_style` repository.

## 📌 Project Overview
A collection of custom `matplotlib` styles specifically designed for the medical and biological sciences, mimicking the aesthetic of **GraphPad Prism** and other professional scientific plotting tools (e.g., **DeepTools**).

- **Role:** Expert Scientific Data Visualization Engineer.
- **Core Technologies:** Python, Matplotlib, NumPy, SciPy, Scikit-learn.
- **Main Goal:** Standardize high-quality, publication-ready scientific charts with minimal manual formatting.

## 📁 Directory Structure
The project follows a strict modular structure under the `styles/` directory:
- `styles/<style_name>/`:
    - `assets/`: Contains the `.mplstyle` configuration file (Mandatory: Keep logic here).
    - `img/`: Contains example outputs (Mandatory: Both `.png` and `.pdf`).
    - `example.py`: A self-contained script to reproduce the chart using mock data.
    - `readme.md`: Specific documentation and visual preview for the style.
- `scripts/`: Utility scripts, such as `new_style.sh` for scaffolding.
- `test/`: Automated tests for style validity and example execution.

## 🛠️ Development Workflow

### 1. Environment Setup
Prefer installing development dependencies to enable testing:
```bash
pip install -e ".[dev]"
```

### 2. Adding a New Style
Always use the scaffolding script to ensure consistent structure:
```bash
./scripts/new_style.sh <style_name>
```

### 3. Generating Examples
Navigate to a style directory and run the example script. Ensure it generates both high-res and vector formats:
```bash
python example.py
```

### 4. Testing & Validation (Critical)
Before submitting any changes or finishing a task, run the automated tests:
```bash
pytest
```
- **Style Legality**: Ensures `.mplstyle` files are correctly parsed.
- **Execution**: Validates `example.py` runs without errors and generates images.

## 🎨 Coding Conventions (Mandatory)

1. **Path Management**: Use `pathlib.Path` for all file resolutions.
   ```python
   from pathlib import Path
   root_path = Path(__file__).parent
   style_file = root_path / 'assets/style.mplstyle'
   ```
2. **Style Initialization**: Load the `.mplstyle` file **BEFORE** creating any figure or axis objects.
   ```python
   plt.style.use(style_file)
   ```
3. **Script Structure**: Use a `main()` function, type hints, and follow the template in `CONTRIBUTING.md`.
4. **GraphPad Aesthetics**:
    - **Fonts**: Bold for labels and titles (`font.weight: bold`).
    - **Spines**: Hide top and right spines.
    - **Ticks**: Inward-facing, thick tick marks.
    - **Error Bars**: Prefer asymmetric (upper only) for biological data.

## ⚠️ Pitfalls to Avoid
- **Style Coupling**: Do NOT put style logic inside `example.py`. Keep it in the `.mplstyle` asset.
- **Manual Formatting**: Avoid redundant `plt.rcParams` or `ax.spines` calls if they can be handled by the style sheet.
- **Inconsistent Docs**: Ensure `readme.md` image links and descriptions match the actual generated output.

## 🤖 AI-Specific Instructions (CRITICAL)
- **Read `llms.md` first**: You MUST read `llms.md` at the beginning of every session for the latest repository-wide instructions.
- **Verification**: Always run `pytest` to confirm your changes don't break existing styles or example scripts.
- **Reproducibility**: Ensure every `example.py` is self-contained and produces both `.png` and `.pdf` in the `img/` folder.
- **Contribution**: Strictly follow the folder structure and documentation requirements defined in `CONTRIBUTING.md`.

## 🤝 Contribution Guidelines
Refer to `CONTRIBUTING.md` for detailed PR requirements. Any new style must include a `readme.md` with an embedded preview and a summary of the style's purpose.
