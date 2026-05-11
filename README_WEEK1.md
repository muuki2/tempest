# Week 1: The Hypoxic Spheroid

## What was implemented

### Tuesday: PhysiCell installation & heterogeneity sample
- Downloaded PhysiCell 1.14.2
- Fixed Makefile for Apple Clang + libomp (OpenMP) on macOS
- Compiled and ran the heterogeneity sample project

### Wednesday: Oxygen substrate + Michaelis-Menten consumption
- Configured `oxygen` substrate in `config/PhysiCell_settings.xml`
  - Units: mmHg
  - Diffusion coefficient: 1000 μm²/min (tissue-realistic)
  - Decay rate: 0 min⁻¹ (O2 does not spontaneously decay)
  - Dirichlet BC: 38 mmHg at domain boundaries (normoxia)
- Implemented Michaelis-Menten uptake in `custom_modules/custom.cpp`:
  ```cpp
  phenotype.secretion.uptake_rates[oxygen_index] = Vmax / (Km + pO2);
  ```
  This gives effective consumption = Vmax * [O2] / (Km + [O2]) when coupled to BioFVM's first-order solver.
  - Default parameters: Vmax = 10 /min, Km = 5 mmHg

### Thursday: Timer-based necrosis
- Added `hypoxic_duration` custom data variable to each cancer cell
- Implemented necrosis rule in `tumor_cell_phenotype_with_oncoprotein`:
  - If local [O2] < 0.1 mmHg → increment `hypoxic_duration` by dt
  - If `hypoxic_duration` > 360 min (6 h) → trigger necrosis via `pCell->start_death(necrosis_index)`
  - If [O2] recovers above 0.1 mmHg → reset timer to 0
- Proliferation is also O2-dependent (linear interpolation between threshold=5 and saturation=38 mmHg)

## Running the simulation

```bash
cd /Users/murat/Documents/tempest/PhysiCell
make clean && make
make data-cleanup
./heterogeneity
```

## Analysis

We use a Python virtual environment for reproducibility:

```bash
# One-time setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Optional: for MP4 movie generation
brew install librsvg ffmpeg

# Run analysis (the script below auto-activates the venv)
./run_analysis.sh
```

Or manually:

```bash
source .venv/bin/activate
python3 analysis.py
```

Generates:
- `output/cell_counts.png` — Live, necrotic, and apoptotic cell counts vs time
- `output/rim_thickness.png` — Viable rim thickness vs time
- `output/spheroid.mp4` — Time-lapse animation (requires `librsvg` and `ffmpeg`)

## Key results (7-day run)

- Initial cells: ~900
- Final live cells: ~430
- Necrotic cells: ~161 (stable after ~10 h)
- Mean necrotic radius: ~154 μm
- Viable rim thickness: ~60–70 μm

**Breakpoint passed:** Central necrotic core surrounded by viable cells is clearly observed.

## Files modified

- `Makefile` — OpenMP flags for macOS Apple Clang
- `config/PhysiCell_settings.xml` — Oxygen substrate parameters, custom data, user parameters
- `custom_modules/custom.cpp` — `tumor_cell_phenotype_with_oncoprotein` with MM uptake + timer necrosis
- `analysis.py` — Post-processing script
