#!/bin/bash
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

MD_FILES="README.md CONTRIBUTING.md llms.md AGENTS.md styles/*/readme.md"

echo "========================================"
echo " MMCS — Pre-PR Check"
echo "========================================"
echo ""

# ---- ruff (required) ----
echo -e "${GREEN}[1/4] Running ruff (Python linter)...${NC}"
if command -v ruff &>/dev/null; then
    ruff check . && echo -e "${GREEN}  ruff: OK${NC}" || { echo -e "${RED}  ruff: FAILED${NC}"; exit 1; }
else
    echo -e "${RED}  ruff not found. Install it with: pip install -e \".[dev]\"${NC}"
    exit 1
fi
echo ""

# ---- rumdl (optional) ----
echo -e "${GREEN}[2/4] Running rumdl (Markdown linter)...${NC}"
if command -v rumdl &>/dev/null; then
    rumdl check $MD_FILES && echo -e "${GREEN}  rumdl: OK${NC}" || echo -e "${YELLOW}  rumdl: issues found (review above)${NC}"
else
    echo -e "${YELLOW}  rumdl not found — skipping (install: cargo install rumdl)${NC}"
fi
echo ""

# ---- markdownlint-cli (optional) ----
echo -e "${GREEN}[3/4] Running markdownlint-cli (Markdown linter)...${NC}"
if command -v npx &>/dev/null; then
    npx --yes markdownlint-cli@0.48.0 $MD_FILES && echo -e "${GREEN}  markdownlint-cli: OK${NC}" || echo -e "${YELLOW}  markdownlint-cli: issues found (review above)${NC}"
else
    echo -e "${YELLOW}  npx not found — skipping (install Node.js or use rumdl)${NC}"
fi
echo ""

# ---- pytest (required) ----
echo -e "${GREEN}[4/4] Running pytest...${NC}"
if command -v pytest &>/dev/null; then
    pytest -v && echo -e "${GREEN}  pytest: OK${NC}" || { echo -e "${RED}  pytest: FAILED${NC}"; exit 1; }
elif command -v python &>/dev/null && python -m pytest --version &>/dev/null; then
    python -m pytest -v && echo -e "${GREEN}  pytest: OK${NC}" || { echo -e "${RED}  pytest: FAILED${NC}"; exit 1; }
else
    echo -e "${RED}  pytest not found. Install it with: pip install -e \".[dev]\"${NC}"
    exit 1
fi
echo ""

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN} All checks passed!${NC}"
echo -e "${GREEN}========================================${NC}"
