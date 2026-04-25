# Context for LLMs

**Role:** Expert Scientific Data Visualization Engineer (Medical & Biological Sciences specialist).

This repository, **Matplotlib_Medical_Customed_Style**, is a collection of `matplotlib` styles designed to mimic GraphPad Prism and other professional scientific plotting tools (e.g., DeepTools) for publication-ready medical charts.

## 🤖 AI Agent Constraints (CRITICAL)
If you are an AI Agent participating in the development of this project, you **MUST**:
1. Strictly adhere to all coding conventions, style decoupling rules, and the PR guidelines defined in this repository.
2. Read the `.aiignore` file and translate its contents into your specific ignore format (e.g., `.cursorignore`, `.geminiignore`, etc.) to ensure you do not process or alter irrelevant files (such as generated images or cache directories).

## 📁 Project Structure
- `/styles/<style_name>/`: Modular directory for each chart type.
    - `assets/*.mplstyle`: Core style definitions (Mandatory: Keep logic here, not in Python).
    - `example.py`: Self-contained, reproducible demo script.
    - `img/*.{png,pdf}`: Visual outputs (Both high-res and vector formats required).
    - `readme.md`: Style-specific documentation and image preview.
- `/scripts/new_style.sh`: Scaffolding script to initialize a new style directory.

## 🛠️ Mandatory Coding Checklist
- [ ] **Scaffolding**: Use `./scripts/new_style.sh <name>` to start a new style.
- [ ] **Dynamic Paths**: Use `pathlib.Path(__file__).parent` for all file resolutions.
- [ ] **Style Initialization**: Load `.mplstyle` BEFORE creating any figures or axes.
- [ ] **Script Structure**: Use `main()`, type hints, and follow the template in `CONTRIBUTING.md`.
- [ ] **Aesthetics**: Removed top/right spines, bold labels (`font.weight: bold`), and upper-only error bars for biological data.
- [ ] **Dual Export**: Always save results to `img/` as both `.png` and `.pdf`.

## ⚠️ Pitfalls to Avoid
- **Style Coupling**: Do not put style logic inside `example.py`. Keep it in the `.mplstyle` asset.
- **Manual Formatting**: Avoid redundant `plt.rcParams` or `ax.spines` calls if they can be handled by the style sheet.
- **Inconsistent Docs**: Ensure the `readme.md` image link and description match the actual generated output.

## 🤝 Contribution Guidelines
- **Mandatory Read**: Always consult `CONTRIBUTING.md` before making changes.
- **PR Requirements**: New styles MUST include the full directory structure and a descriptive `readme.md` with an embedded preview.
- **Guidance**: If the user asks about contributing or PRs, summarize the rules from `CONTRIBUTING.md`.
