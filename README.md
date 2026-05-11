# TME Engine — Tumor Microenvironment Simulation Engine

A multiscale agent-based model of the tumor microenvironment (TME), built on [PhysiCell](http://physicell.org/). This repository tracks our implementation of a physics-coupled TME simulator with hypoxia-driven necrosis, immune chemotaxis, CAF activation, ECM remodeling, image-to-simulation pipelines, neural network potentials, and LLM agent control.

> **Status:** Week 1 in progress — hypoxic spheroid with oxygen-driven necrosis is functional.

---

## Table of Contents

- [Project Roadmap](#project-roadmap)
- [Progress Tracker](#progress-tracker)
- [Quick Start](#quick-start)
- [Repository Structure](#repository-structure)
- [Open Source Credits & Citations](#open-source-credits--citations)
- [License](#license)

---

## Project Roadmap

This roadmap follows our 14-week curriculum to build a credible, documented TME simulation prototype.

### Week 1: The Hypoxic Spheroid
**Goal:** A 3-cell-type virtual spheroid with oxygen-driven necrosis.

- [x] **Mon:** Read Hanahan & Weinberg 2022 + Weinberg Ch 13
- [x] **Tue:** Install PhysiCell. Compile and run heterogeneity sample. Understand `custom_modules/`
- [x] **Wed:** Add oxygen substrate field. Implement Michaelis-Menten consumption: `uptake_rate = Vmax * [O2] / (Km + [O2])`
- [x] **Thu:** Add necrosis rule: if `[O2] < 0.1 mmHg` for `>6 hours`, cell enters necrotic state and lyses
- [ ] **Fri:** Run 7-day simulated time. Vary initial O2 diffusion constant. Observe necrotic core formation
- [ ] **Weekend:** Plot viable rim thickness vs. O2 diffusion coefficient + 10-second animation

**Breakpoint:** Central necrotic core surrounded by viable cells.

### Week 2: Immune Exclusion Dynamics
**Goal:** T cells chemotax toward cancer, but hypoxia traps them peripherally.

- [ ] **Mon:** Read Jain 2014 + Semenza 2012
- [ ] **Tue:** Add CXCL12 chemoattractant. Cancer secretes it proportional to HIF-1α
- [ ] **Wed:** Add T cells. Chemotaxis up CXCL12 gradient. Contact-based killing
- [ ] **Thu:** Run normoxic vs. hypoxic scenarios
- [ ] **Fri:** Quantify immune infiltration depth
- [ ] **Weekend:** Side-by-side plots of T cell distributions

**Breakpoint:** Under hypoxia, `>60%` of T cells remain in outer `20%` of spheroid radius.

### Week 3: ECM, CAFs, and Mechanical Remodeling
**Goal:** TGF-β-driven CAF activation and collagen deposition.

- [ ] **Mon:** Read Sahai et al. 2020 + Kalli & Stylianopoulos 2018
- [ ] **Tue:** Add fibroblasts. Add collagen substrate field
- [ ] **Wed:** TGF-β secretion by cancer. CAF activation rule
- [ ] **Thu:** MMP secretion. Haptotaxis up collagen gradient
- [ ] **Fri:** Run and observe collagen alignment
- [ ] **Weekend:** ECM density heatmap + phenotype switching time-lapse

**Breakpoint:** CAF activation visibly alters T cell infiltration patterns.

### Week 4: Image-to-Simulation Pipeline
**Goal:** Turn real microscopy into simulation initial conditions.

- [ ] **Mon:** Install Cellpose 2.0. Run on public tumor spheroid image
- [ ] **Tue:** Install squidpy + scanpy. Load 10x Visium breast cancer dataset
- [ ] **Wed:** Segment Visium slide into cancer/CAF/T-cell/macrophage niches
- [ ] **Thu:** Write converter: Cellpose masks / Visium spots → PhysiCell `cells.csv`
- [ ] **Fri:** Run PhysiCell initialized from real image topology
- [ ] **Weekend:** Initial frame visually resembles input microscopy image

**Breakpoint:** Cell type ratios within `25%` of image ratios.

### Week 5: MD Literacy with Foundation NNPs
**Goal:** Run stable neural-potential MD, not master it.

- [ ] **Mon:** Install mace, ase, openmm. Verify GPU
- [ ] **Tue:** Download MACE-MP-0. Run 100 ps NVT of water/alanine dipeptide
- [ ] **Wed:** Check energy conservation. Plot E vs t. Compute O-O RDF
- [ ] **Thu:** Run same system with TIP3P in OpenMM. Compare RDFs
- [ ] **Fri:** Read Siretskiy et al. 2025. Know when MACE-MP-0 fails
- [ ] **Weekend:** `md_literacy.ipynb` with stable trajectory, RDF comparison, cheat sheet

**Breakpoint:** Energy drift `< 2 kcal/mol` over 100 ps. RDF peak at `~2.8 Å`.

### Week 6: Binding Landscapes (Conceptual)
**Goal:** Understand free energy methods without becoming a PLUMED expert.

- [ ] **Mon:** Read Bussi & Laio 2020 metadynamics review
- [ ] **Tue:** Download pre-computed metadynamics trajectory
- [ ] **Wed:** Practice reweighting: extract unbiased FES
- [ ] **Thu:** Run umbrella sampling on alanine dipeptide phi angle in OpenMM
- [ ] **Fri:** Conceptual exercise: barrier `5 kcal/mol` at `310 K` → estimate timescale via TST
- [ ] **Weekend:** PMF plot + notebook page deriving rate from barrier

**Breakpoint:** Explain why metadynamics explores faster than unbiased MD, and why TST rates are approximate.

### Week 7: The Signaling ODE (Mesoscale Part 1)
**Goal:** A standalone, validated TGF-β/SMAD module.

- [ ] **Mon:** Read Alberts Ch 15. Find published TGF-β/SMAD ODE model
- [ ] **Tue:** Implement ODE system in SciPy (`solve_ivp`)
- [ ] **Wed:** Calibrate to literature dose-response
- [ ] **Thu:** Add Hill-function wrapper: CAF activation probability from nuclear SMAD
- [ ] **Fri:** Sensitivity analysis: vary each parameter `10×`
- [ ] **Weekend:** `signaling_module.py` with dose-response, EC50 annotated, tornado diagram

**Breakpoint:** EC50 within `0.1–10 ng/mL`.

### Week 8: Receptor Kinetics at the Surface (Mesoscale Part 2)
**Goal:** Ligand-receptor binding as a stochastic cellular event.

- [ ] **Mon:** Derive receptor occupancy from mass action. Implement as continuous ODE
- [ ] **Tue:** Implement kinetic Monte Carlo (kMC) version
- [ ] **Wed:** Couple kMC to Week 7 ODE
- [ ] **Thu:** Test with varying `kon (10×, 0.1×)`
- [ ] **Fri:** Add ligand depletion. Solve reaction-diffusion for extracellular TGF-β
- [ ] **Weekend:** 1D/2D spatial model showing TGF-β gradient → receptor occupancy → activation

**Breakpoint:** `10×` change in `kon` produces `>2×` change in activation threshold.

### Week 9: Full Coupling to PhysiCell (Mesoscale Part 3)
**Goal:** The MD-derived rate flows into tissue-scale ECM remodeling.

- [ ] **Mon:** Unit conversion workshop. Write `units.py`
- [ ] **Tue:** Integrate Week 8 kMC-ODE into PhysiCell custom code
- [ ] **Wed:** Debug the full loop: cancer → TGF-β → fibroblast → SMAD → myofibroblast → collagen → T cell exclusion
- [ ] **Thu:** Run coupled system. Run Week 3 rule-based version with matched parameters
- [ ] **Fri:** Quantitative comparison: time to 50% CAF activation, collagen density at 48h, T cell depth
- [ ] **Weekend:** Side-by-side report: "Rule-based vs. Physics-coupled"

**Breakpoint:** Physics-coupled version shows time-delayed response that rule-based cannot capture.

### Week 10: Spatial Omics & Calibration
**Goal:** Match simulation to real data via Approximate Bayesian Computation.

- [ ] **Mon:** Load public tumor spatial transcriptomics dataset. Compute Ripley's L
- [ ] **Tue:** Generate synthetic spatial omics from PhysiCell
- [ ] **Wed:** Define distance metric between real and simulated patterns
- [ ] **Thu:** Implement ABC with pyABC or custom rejection sampler
- [ ] **Fri:** Plot posterior. Run MAP estimate vs. prior
- [ ] **Weekend:** Posterior distribution + calibrated growth curve within `20%` of target

**Breakpoint:** Posterior tighter than prior (information was gained).

### Week 11: Uncertainty & Negative Results
**Goal:** Know exactly how and why your model lies.

- [ ] **Mon:** Deep ensembles: run 5 simulations from posterior. Plot mean ± std of invasion depth
- [ ] **Tue:** Adversarial test 1: drug binds TGF-β receptor tightly but `koff` extremely high
- [ ] **Wed:** Adversarial test 2: mis-segment input image (swap cancer/CAF labels)
- [ ] **Thu:** Adversarial test 3: LLM proposes biologically impossible rule. Verify parameter schema rejects it
- [ ] **Fri:** Write 2-page "Failure Mode & Uncertainty" report
- [ ] **Weekend:** Report + ensemble prediction plots with explicit error bands

**Breakpoint:** Articulate why each failure occurs in terms of model structure.

### Week 12: Active Learning / Bayesian Experimental Design
**Goal:** The simulator proposes its own calibration experiments.

- [ ] **Mon:** Read Rainforth et al. 2024. Install BoTorch or scikit-optimize
- [ ] **Tue:** Build GP surrogate mapping 2–3 ABM parameters → observables
- [ ] **Wed:** Implement Expected Improvement (EI) acquisition function
- [ ] **Thu:** "Hidden ground truth": high-fidelity ABM with known parameters. Use BO to propose 5 conditions
- [ ] **Fri:** Update GP after each experiment. Plot convergence
- [ ] **Weekend:** BO convergence plot showing parameter uncertainty vs. iteration

**Breakpoint:** Uncertainty drops `>50%` within 8 iterations.

### Week 13: LLM Agent Interface
**Goal:** Natural language control of the TME simulator.

- [ ] **Mon:** Read Yao et al. 2022 (ReAct). Design tool schema
- [ ] **Tue:** Implement tools in Python: `run_tme_sim()`, `load_image()`, `get_spatial_stats()`, `plot_field()`
- [ ] **Wed:** Build agent using LangChain or raw OpenAI function-calling
- [ ] **Thu:** Add reflection layer: unphysical parameters raise `ValueError`, agent retries
- [ ] **Fri:** Build minimal UI (Gradio or Streamlit)
- [ ] **Weekend:** Working chat interface handling 3 distinct query types

**Breakpoint:** Agent refuses at least one biologically impossible query gracefully.

### Week 14: Capstone & Roadmap
**Goal:** A credible, documented prototype.

- [ ] **Mon:** Define capstone case: HER2+ breast cancer spheroid with CAFs and PBMCs, with/without trastuzumab + anti-PD-1
- [ ] **Tue:** Run full pipeline: image → segmentation → PhysiCell IC → MACE-derived drug effect → ABM → time-lapse → LLM summary
- [ ] **Wed:** Stress test: swap therapeutic agent. Does pipeline run without code changes?
- [ ] **Thu:** Write README with install instructions, dependency versions, 5-minute demo GIF
- [ ] **Fri:** Write 2-page technical roadmap: "Days 101–365"
- [ ] **Weekend:** Public GitHub repository. Colleague can clone, install, and run `python demo.py` in `<30 min`

**Final Breakpoint:** The repo runs on a fresh environment without your intervention.

---

## Progress Tracker

| Week | Theme | Status | Key Deliverable |
|------|-------|--------|-----------------|
| 1 | Hypoxic Spheroid | 🟡 In progress | Necrotic core + viable rim |
| 2 | Immune Exclusion | ⚪ Not started | T cell spatial distributions |
| 3 | ECM & CAFs | ⚪ Not started | ECM density heatmap |
| 4 | Image-to-Sim | ⚪ Not started | PhysiCell IC from microscopy |
| 5 | MD Literacy | ⚪ Not started | `md_literacy.ipynb` |
| 6 | Binding Landscapes | ⚪ Not started | PMF + rate derivation |
| 7 | TGF-β/SMAD ODE | ⚪ Not started | `signaling_module.py` |
| 8 | Receptor Kinetics | ⚪ Not started | 1D spatial model |
| 9 | Full Coupling | ⚪ Not started | Rule-based vs. physics-coupled report |
| 10 | Spatial Omics & ABC | ⚪ Not started | Posterior distribution plot |
| 11 | Uncertainty | ⚪ Not started | Failure mode report |
| 12 | Active Learning | ⚪ Not started | BO convergence plot |
| 13 | LLM Agent | ⚪ Not started | Working chat UI |
| 14 | Capstone | ⚪ Not started | Public repo + demo |

**Legend:** 🟢 Done | 🟡 In progress | ⚪ Not started

---

## Quick Start

### Prerequisites

- macOS with Apple Silicon (or Linux/x86_64 with adjustments)
- Xcode Command Line Tools
- Homebrew
- Python 3.10+

### Install & Run

```bash
# Clone
git clone https://github.com/muuki2/tempest.git
cd tempest

# Build PhysiCell
make clean && make

# Run simulation
make data-cleanup
./heterogeneity

# Analyze results
./run_analysis.sh

# View outputs
open output/cell_counts.png
open output/rim_thickness.png
open output/spheroid.mp4
```

### Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Optional: Movie Generation

```bash
brew install librsvg ffmpeg
```

---

## Repository Structure

```
.
├── BioFVM/                  # BioFVM transport solver (PhysiCell dependency)
├── core/                    # PhysiCell core library
├── modules/                 # PhysiCell standard modules
├── custom_modules/          # ★ Our custom cell behavior code
│   ├── custom.cpp           # MM uptake + necrosis + oncoprotein logic
│   └── custom.h             # Custom module headers
├── config/                  # ★ Simulation configuration
│   └── PhysiCell_settings.xml
├── sample_projects/         # PhysiCell sample projects (reference)
├── analysis.py              # ★ Python post-processing
├── run_analysis.sh          # ★ Convenience runner (auto-activates .venv)
├── requirements.txt         # ★ Pinned Python dependencies
├── README_WEEK1.md          # ★ Week 1 detailed notes
└── README.md                # ★ This file
```

Files marked with ★ are our original work or significant modifications.

---

## Open Source Credits & Citations

This project is built on outstanding open-source software and published research. We gratefully acknowledge:

### Core Simulation Framework

**PhysiCell** — Agent-based cell simulator
> A Ghaffarizadeh, R Heiland, SH Friedman, SM Mumenthaler, and P Macklin, *PhysiCell: an Open Source Physics-Based Cell Simulator for Multicellular Systems*, PLoS Comput. Biol. 14(2): e1005991, 2018. DOI: [10.1371/journal.pcbi.1005991](https://doi.org/10.1371/journal.pcbi.1005991)

**BioFVM** — Diffusive transport solver (bundled with PhysiCell)
> A Ghaffarizadeh, SH Friedman, and P Macklin, *BioFVM: an efficient parallelized diffusive transport solver for 3-D biological simulations*, Bioinformatics 32(8): 1256-8, 2016. DOI: [10.1093/bioinformatics/btv730](https://doi.org/10.1093/bioinformatics/btv730)

### Python Ecosystem

- **NumPy** — Harris et al., *Array programming with NumPy*, Nature 585, 357–362 (2020)
- **Matplotlib** — Hunter, *Matplotlib: A 2D Graphics Environment*, Computing in Science & Engineering 9(3): 90-95 (2007)
- **CairoSVG** — Kozea, SVG rendering via Cairo

### System Tools

- **libomp** (Homebrew) — OpenMP runtime for Apple Clang
- **librsvg** — SVG rendering library (used for movie generation)
- **ffmpeg** — Video encoding

### Key Reading

The curriculum is built around these foundational papers (see roadmap for week-by-week assignments):

1. Hanahan & Weinberg, *Hallmarks of Cancer: New Dimensions*, Cancer Discovery 2022
2. Jain, *Normalizing Tumor Microenvironment to Treat Cancer*, JCO 2014
3. Binnewies et al., *Understanding the Tumor Immune Microenvironment*, Nature Medicine 2018
4. Sahai et al., *A Framework for Advancing Our Understanding of Cancer-Associated Fibroblasts*, Nature Reviews Cancer 2020
5. Kalli & Stylianopoulos, *Defining the Role of Solid Stress and Matrix Stiffness*, Annual Review of Biomedical Engineering 2018
6. Ghaffarizadeh et al., *PhysiCell*, PLoS Computational Biology 2018
7. Batatia et al., *MACE: Higher Order Equivariant Message Passing*, ICML 2022
8. Siretskiy et al., *Machine-Learning Interatomic Potentials from a User's Perspective*, JCIM 2025
9. Rainforth et al., *An Introduction to Bayesian Experimental Design*, FnT Machine Learning 2024
10. Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models*, ICLR 2023

See `README_WEEK1.md` and the full 14-week roadmap above for the complete reading list.

---

## License

Our original code (`custom_modules/custom.cpp`, `analysis.py`, `run_analysis.sh`, `README_WEEK1.md`, and modifications to `config/PhysiCell_settings.xml` and `Makefile`) is provided under the same BSD 3-Clause license as PhysiCell itself, to maintain compatibility.

PhysiCell and BioFVM are copyright (c) 2015-2025, Paul Macklin and the PhysiCell Project, and licensed under the BSD 3-Clause License. See `licenses/` for full text.

---

> *"The goal is not a clinically validated digital twin. The goal is a credible, documented prototype that teaches you how multiscale modeling actually works."*
