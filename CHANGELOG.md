# Changelog

All notable changes to the **Commercial Sub-Critical Hybrid Fission-Fusion Reactor** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-10-20

### Added
* **1D 3T Lagrangian Hydrodynamics Solver (`hydro_1d_3T.py`):** Numba JIT-accelerated solver modeling target compression, HDC ablator dynamics, and Bosch-Hale D-T fusion reactivity yielding $Q_{\text{fusion}} = 0.1618$ ($291.17\text{ kJ}$).
* **Sub-Critical Blanket Neutronics Solver (`neutronics_blanket.py`):** Power balance solver evaluating sub-critical multiplication ($k_{\text{eff}} = 0.965$, $M_{\text{blanket}} = 113.8\times$), 3D neutron streaming port loss ($10\%$), and plant energy gain ($Q_{\text{electric}} = 1.43$, $+21.5\text{ MW}_e$ net output).
* **FLiBe Thermal-Hydraulics Transient Solver (`thermal_hydraulics.py`):** Coolant loop model computing temperature startup transients ($550^\circ\text{C} \to 700^\circ\text{C}$) and steady-state thermal ripple ($\Delta T \le 0.45^\circ\text{C}$ at $5\text{ Hz}$).
* **EUROFER97 First-Wall Mechanics Solver (`mechanics_firstwall.py`):** Single-Degree-of-Freedom (SDOF) dynamic hoop stress solver evaluating structural response under $3.5\text{ MPa}$ peak pulses ($108.9\text{ MPa}$ peak stress vs $160\text{ MPa}$ ASME limit).
* **Master Interactive Notebook (`notebooks/Full_Reactor_Simulation.ipynb`):** End-to-end simulation workflow ready for Google Colab and local execution.
* **ReportLab PDF Generators:** Automated compilation of standalone technical documentation (`Executive_Spec_Sheet.pdf` and `Theory_Formulation.pdf`).
* **Metadata & Citation Assets:** Machine-readable `CITATION.cff`, GitHub funding portal configuration (`.github/FUNDING.yml`), Shields.io status badges, and MIT License.

### Changed
* Shifted architecture from an unviable pure ICF energy sink ($-21.6\text{ MW}_e$) to a commercially profitable hybrid fission-fusion paradigm ($+21.5\text{ MW}_e$).
* Upgraded DPSSL driver efficiency baseline from $12\%$ to $18\%$ and thermal power cycle efficiency to $48\%$ ($700^\circ\text{C}$ sCO<sub>2</sub> Brayton cycle).

---
