# AGENTS.md — High-signal context for OpenCode

## Read these first

- `llms.md` — primary AI-facing instructions. Read it every session.
- `CONTRIBUTING.md` — PR structure requirements and contribution flow.

## Dev setup

```bash
pip install -e ".[dev]"   # quotes are required in zsh
```

## Commands

- **Scaffold a new style:** `./scripts/new_style.sh <style_name>`
- **Run all tests:** `pytest` (auto-discovers `.mplstyle` and `example.py` files under `styles/`)
- **Run a single test file:** `pytest test/test_examples.py -k <style_dir_name>`

## CRITICAL: Style loading order

`.mplstyle` **MUST** be loaded via `plt.style.use()` **before** any figure or axes are created. Loading after can silently produce wrong output.

```python
plt.style.use(style_file)  # ← before plt.subplots()
fig, ax = plt.subplots()
```

## Conventions

- **Paths:** `pathlib.Path` exclusively. Root reference: `Path(__file__).parent`.
- **Style decoupling:** Keep all styling in `.mplstyle` files, not in `example.py`. Do not hardcode `rcParams` or spine tweaks in Python if the style sheet already covers them.
- **Dual export:** Every `example.py` must save both `.png` and `.pdf` to `img/`.
- **Headless-safe:** Leave `plt.show()` commented out — CI and headless servers have no display.
- **GraphPad aesthetic defaults:** bold labels, hidden top/right spines, inward ticks, upper-only error bars for biological data.

## Test gotchas

- Test discovery is dynamic (`glob` on all `.mplstyle` and `example.py` files). A malformed style or broken example in any directory **blocks CI for everything**.
- `test_examples.py` monkeypatches `plt.show` to a no-op — do not rely on interactive display during tests.
- Tests `chdir` into each style directory before running `example.py`, so relative paths inside scripts work correctly.

## Publishing (release) workflow

When a style is ready for release, execute these 6 steps in order:

1. **Audit `example.py`** — move any hardcoded non-essential styles (colors, line widths, fonts) into the `.mplstyle` file.
2. **Run tests** — `pytest` (use `conda run -n Matplotlib_Medial_Customed_Styles pytest` if using Conda).
3. **Regenerate images** — run `python example.py` inside the style directory to produce fresh `.png` and `.pdf`.
4. **Write/update the style's `readme.md`** — include preview image and usage summary.
5. **Update main `README.md` Styles Gallery** — add the new style to the appropriate table.
6. **Commit** the changes.

## `.mplstyle` parsing gotchas

- **Hex colors:** do NOT use `#` prefix (e.g. write `003366`, not `#003366`). Certain matplotlib parsers misread `#` as a comment character.
- **Style inheritance gap:** some complex chart sub-components (e.g. violinplot bodies) do NOT auto-inherit `rcParams` patch/line properties. You must explicitly apply `plt.rcParams` values in `example.py` for those components — this is the one allowed exception to style decoupling.
- **Composite chart alignment:** when overlaying components (e.g. box+violin in split mode), compute geometric center offsets so components align precisely in visual space.
- **Variant isolation:** when a style has multiple mutually exclusive display modes (e.g. standard vs. split violin), create separate driver scripts (`example.py`, `example_split.py`) rather than conditional logic in a single file.

## Repo quirks

- `GEMINI.md` is in `.gitignore` — it is NOT committed to the repo.
- `.aiignore` exists; translate it to your agent's ignore format (`.cursorignore`, `.geminiignore`, etc.) so generated images and caches are excluded.
- Fonts: output relies on Arial/Helvetica/DejaVu Sans being installed. Missing fonts produce subtle visual differences, not errors.
- Python 3.12 is the CI target (see `.github/workflows/pytest.yaml`).
