# Release Process

This document describes the steps to publish a new version of `mmcs` to PyPI.

## Prerequisites

- Python >= 3.9
- [build](https://pypi.org/project/build/): `pip install build`
- [twine](https://pypi.org/project/twine/): `pip install twine`
- A PyPI account with access to the `mmcs` project

## Step-by-step

### 1. Update the version

The canonical version is in `mmcs/__init__.py`:

```python
__version__ = "0.2.0"
```

Also update `pyproject.toml`:

```toml
version = "0.2.0"
```

### 2. Update CHANGELOG.md

Move the `[Unreleased]` section to a new version heading and add the release date:

```markdown
## [0.2.0] - 2026-04-29
```

### 3. Commit and tag

```bash
git add mmcs/__init__.py pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to 0.2.0"
git tag v0.2.0
git push origin main --tags
```

### 4. Build distributions

```bash
python -m build
```

This creates `dist/mmcs-0.2.0.tar.gz` and `dist/mmcs-0.2.0-py3-none-any.whl`.

### 5. Upload to PyPI

```bash
twine upload dist/*
```

### 6. Verify

```bash
pip install mmcs==0.2.0
python -c "import mmcs; print(mmcs.__version__)"
```

## Version numbering

mmcs follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (x.0.0): breaking API changes
- **MINOR** (0.x.0): new features, backward-compatible
- **PATCH** (0.0.x): bug fixes, backward-compatible

Pre-release suffixes follow PEP 440: `0.3.0a1`, `0.3.0rc1`.

## Branch strategy

- `main` — latest stable code
- Tagged commits correspond to PyPI releases
- Feature branches merge into `main` via PR
