#!/bin/bash
# Run analysis inside the virtual environment
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate venv
source .venv/bin/activate

# Run analysis
python3 analysis.py

echo ""
echo "Plots saved to output/cell_counts.png and output/rim_thickness.png"
echo "Open them with: open output/cell_counts.png"
