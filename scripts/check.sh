#!/bin/bash
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

MD_FILES="README.md CONTRIBUTING.md llms.md AGENTS.md"

echo "========================================"
echo " MMCS — Pre-PR Check"
echo "========================================"
echo ""

# ---- ruff (required) ----
echo -e "${GREEN}[1/5] Running ruff (Python linter)...${NC}"
if command -v ruff &>/dev/null; then
    ruff check . && echo -e "${GREEN}  ruff: OK${NC}" || { echo -e "${RED}  ruff: FAILED${NC}"; exit 1; }
else
    echo -e "${RED}  ruff not found. Install it with: pip install -e \".[dev]\"${NC}"
    exit 1
fi
echo ""

# ---- metadata.json validation (required) ----
echo -e "${GREEN}[2/5] Validating metadata.json files...${NC}"
VALIDATION_FAILED=0
for meta in mmcs/styles/*/metadata.json; do
    if [ -f "$meta" ]; then
        if python -c "import json; json.load(open('$meta'))" 2>/dev/null; then
            echo -e "  ${GREEN}OK${NC}: $meta"
        else
            echo -e "  ${RED}INVALID${NC}: $meta"
            VALIDATION_FAILED=1
        fi
    fi
done
if [ "$VALIDATION_FAILED" -eq 1 ]; then
    echo -e "${RED}  metadata.json validation: FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}  metadata.json: all valid${NC}"
fi
echo ""

# ---- rumdl (optional) ----
echo -e "${GREEN}[3/5] Running rumdl (Markdown linter)...${NC}"
if command -v rumdl &>/dev/null; then
    # shellcheck disable=SC2086
    rumdl check $MD_FILES && echo -e "${GREEN}  rumdl: OK${NC}" || echo -e "${YELLOW}  rumdl: issues found (review above)${NC}"
else
    echo -e "${YELLOW}  rumdl not found — skipping (install: cargo install rumdl)${NC}"
fi
echo ""

# ---- markdownlint-cli (optional) ----
echo -e "${GREEN}[4/5] Running markdownlint-cli (Markdown linter)...${NC}"
if command -v npx &>/dev/null; then
    # shellcheck disable=SC2086
    npx --yes markdownlint-cli@0.48.0 $MD_FILES && echo -e "${GREEN}  markdownlint-cli: OK${NC}" || echo -e "${YELLOW}  markdownlint-cli: issues found (review above)${NC}"
else
    echo -e "${YELLOW}  npx not found — skipping (install Node.js or use rumdl)${NC}"
fi
echo ""

# ---- pytest (required) ----
echo -e "${GREEN}[5/5] Running pytest...${NC}"
if command -v pytest &>/dev/null; then
    pytest -v --mpl --mpl-default-tolerance=20 && echo -e "${GREEN}  pytest: OK${NC}" || { echo -e "${RED}  pytest: FAILED${NC}"; exit 1; }
elif command -v python &>/dev/null && python -m pytest --version &>/dev/null; then
    python -m pytest -v --mpl --mpl-default-tolerance=20 && echo -e "${GREEN}  pytest: OK${NC}" || { echo -e "${RED}  pytest: FAILED${NC}"; exit 1; }
else
    echo -e "${RED}  pytest not found. Install it with: pip install -e \".[dev]\"${NC}"
    exit 1
fi
echo ""

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN} All checks passed!${NC}"
echo -e "${GREEN}========================================${NC}"
