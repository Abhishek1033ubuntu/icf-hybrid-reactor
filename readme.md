# Sub-Critical Hybrid Fission-Fusion Reactor Paradigm

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0004--6913--096X-green.svg)](https://orcid.org/0009-0004-6913-096X)

An open-source multiphysics simulation and systems engineering benchmark evaluating a **laser-driven Inertial Confinement Fusion (ICF)** spark-ignition core coupled to a **sub-critical FLiBe molten-salt fission blanket** (k<sub>eff</sub> = 0.965). 

This project demonstrates how a sub-break-even fusion driver (Q<sub>fusion</sub> = 0.1618) can be multiplied across a passively safe fission blanket to yield a net commercial electrical output (**+21.5 MW<sub>e</sub>**, Q<sub>electric</sub> = 1.43) while maintaining 3D neutron streaming allowance, dynamic first-wall structural safety, and self-sustaining tritium breeding (TBR = 1.15).

---

## Executive Technical Specification Sheet

### System Performance & Power Balance

| Parameter | Symbol / Unit | Baseline (1D Unoptimized) | Optimized (3D-Aware Paradigm) |
| :--- | :--- | :--- | :--- |
| **Laser Driver Pulse Energy** | E<sub>laser</sub> | 1.80 MJ / shot | **1.80 MJ / shot** |
| **Pulse Repetition Frequency** | f<sub>rep</sub> | 5.0 Hz | **5.0 Hz** |
| **Laser Diode Efficiency (DPSSL)** | &eta;<sub>driver</sub> | 12.0% | **18.0%** |
| **Recirculating Driver Power** | P<sub>recirc</sub> | 75.0 MW<sub>e</sub> | **50.0 MW<sub>e</sub>** |
| **ICF Target Fusion Yield** | E<sub>fusion</sub> | 0.2912 MJ (291.17 kJ) | **0.2912 MJ (291.17 kJ)** |
| **Core Target Energy Gain** | Q<sub>fusion</sub> | 0.1618 | **0.1618** |
| **Sub-Critical Multiplication Factor** | k<sub>eff</sub> | 0.950 | **0.965** (3.5% Safety Margin) |
| **3D Geometric Streaming Loss** | f<sub>stream</sub> | 0.0% (Ideal 4&pi;) | **10.0%** (Port Penetrations) |
| **Blanket Energy Multiplication** | M<sub>blanket</sub> | 87.4x | **113.8x** |
| **Total Thermal Power Output** | P<sub>thermal</sub> | 127.1 MW<sub>th</sub> | **149.0 MW<sub>th</sub>** |
| **Thermal Cycle Efficiency (sCO<sub>2</sub>)** | &eta;<sub>thermal</sub> | 42.0% (650°C Outlet) | **48.0%** (700°C FLiBe Outlet) |
| **Gross Electrical Generation** | P<sub>gross</sub> | 53.4 MW<sub>e</sub> | **71.5 MW<sub>e</sub>** |
| **Net Commercial Electrical Power** | P<sub>net</sub> | -21.6 MW<sub>e</sub> (Energy Sink) | **+21.5 MW<sub>e</sub>** (Net Generator) |
| **Plant Net Electrical Gain** | Q<sub>electric</sub> | 0.71 | **1.43** (Commercial Profitability) |

---

### Core Target, Blanket & Mechanical Specifications

* **Ablator Material:** High-Density Carbon (HDC / Synthetic Diamond, &rho; = 3510 kg/m<sup>3</sup>).
* **Fuel Configuration:** Cryogenic Deuterium-Tritium (D-T) ice layer surrounding central D-T vapor spark core (R<sub>outer</sub> = 1.0 mm).
* **Laser Actuation:** Acousto-Optic Modulator (AOM/EOM) front-end seed pulse shaping driving ablation drive pressures up to ~140 GBar.
* **Core Hotspot Parameters:** Peak central ion temperature T<sub>i</sub> = 24.98 keV at peak spherical convergence (CR &approx; 32).
* **Coolant / Breeding Medium:** FLiBe Molten Salt (Li<sub>2</sub>BeF<sub>4</sub>, &rho; = 1940 kg/m<sup>3</sup>, C<sub>p</sub> = 2380 J/kg/K).
* **Primary Coolant Window:** 550°C (Inlet) to 700°C (Outlet) @ &dot;m = 524.4 kg/s.
* **5 Hz Thermal Damping:** Steady-state temperature ripple &Delta;T &le; 0.45°C per shot (12.0 m<sup>3</sup> active fluid inventory).
* **3D Net Tritium Breeding Ratio:** TBR = 1.15 (+18.75 g/day surplus; 11.37 kg reserve accumulated after 1 year).
* **First-Wall Structure:** EUROFER97 Steel (R<sub>wall</sub> = 1.5 m, t<sub>wall</sub> = 25 mm). Peak dynamic hoop stress &sigma;<sub>&theta;</sub> = 108.9 MPa vs. ASME fatigue yield limit of 160.0 MPa (+31.9% safety margin).

---

## Architectural Physics Overview

```
+--------------------------+       +--------------------------+       +--------------------------+
|   ICF Laser Core Pulse   | ----> |   14.1 MeV D-T Neutrons  | ----> | Sub-Critical Blanket     |
|  (E_laser = 1.80 MJ)     |       |   (1.41 x 10^17 n/MJ)    |       | (k_eff = 0.965, M=113.8) |
+--------------------------+       +--------------------------+       +--------------------------+
             |                                                                     |
             v                                                                     v
  [Recirculating Power]                                                 [Gross Thermal Power]
    (50.0 MWe @ 18% DPSSL)                                              (149.0 MWth @ 48% sCO2)
             |                                                                     |
             +--------------------> [ Net Grid Power Output ] <--------------------+
                                      ( +21.5 MWe Output )
```

### 1. 1D 3T Lagrangian Hydrodynamics Solver
The ICF core solver implements a 1D spherical staggered-grid Lagrangian hydrodynamics model in Python, compiled via `Numba` JIT for high execution speeds. The solver features:
* 3-Temperature decoupling (Ions T<sub>i</sub>, Electrons T<sub>e</sub>, Radiation T<sub>r</sub>).
* Spitzer-Härm thermal electron conduction and electron-ion relaxation kinetics.
* Bounded artificial viscosity caps (q<sub>cell</sub> &le; 2.5 &middot; P<sub>thermal</sub>) to eliminate unphysical numerical breakdown across sharp DT-ice / HDC-ablator density boundaries.
* Bosch-Hale thermonuclear D-T fusion reactivity integration &lang;&sigma;v&rang;.

### 2. Sub-Critical Neutronic Multiplication
Fission blanket physics converts external D-T fusion neutrons into secondary fission cascades without risking prompt criticality:

$$f_{\text{fiss}} = \frac{k_{\text{eff}}}{\bar{\nu}(1 - k_{\text{eff}})} \cdot (1 - f_{\text{stream}})$$

$$M_{\text{blanket}} = 1 + f_{\text{fiss}} \cdot \left( \frac{E_{\text{fission}}}{E_{\text{fusion}}} \right)$$

where E<sub>fission</sub> = 200 MeV, E<sub>fusion</sub> = 17.6 MeV, and &nu;<sub>bar</sub> = 2.5. At k<sub>eff</sub> = 0.965 and accounting for a 10% 3D geometric port loss allowance, each fusion neutron triggers 10.3 fissions, providing a 113.8x blanket energy multiplication.

---

## Repository Structure

```text
icf-hybrid-reactor/
├── README.md                      # Master architecture overview and technical spec sheet
├── LICENSE                        # Open-source license (MIT License)
├── CITATION.cff                   # Machine-readable academic citation metadata
├── docs/
│   ├── Executive_Spec_Sheet.pdf   # Standalone executive specification sheet
│   └── Theory_Formulation.pdf     # Derivations for 3T hydro, neutronics & first-wall mechanics
├── src/
│   ├── solvers/
│   │   ├── hydro_1d_3T.py         # Numba JIT-compiled Lagrangian hydrodynamics solver
│   │   ├── neutronics_blanket.py  # Sub-critical multiplication & power flow model
│   │   ├── thermal_hydraulics.py  # FLiBe coolant loop transient temperature solver
│   │   └── mechanics_firstwall.py # EUROFER97 dynamic stress & SDOF solver
│   └── visualization/
│       └── plot_diagnostics.py    # Dual-axis plotting utilities and formatting tools
└── notebooks/
    └── Full_Reactor_Simulation.ipynb # Interactive Google Colab master notebook
```

---

## Quickstart & Usage

### Running via Google Colab / Python Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/Abhishek1033ubuntu/icf-hybrid-reactor.git
   cd icf-hybrid-reactor
   ```

2. Install dependencies:
   ```bash
   pip install numpy scipy matplotlib numba
   ```

3. Execute the full reactor power balance model:
   ```bash
   python src/solvers/neutronics_blanket.py
   ```

---

## Project Attribution & Author Statements

* **Project Architect & Principal Investigator:** Abhishek Singh
* **ORCID:** [0009-0004-6913-096X](https://orcid.org/0009-0004-6913-096X)
* **Repository:** [github.com/Abhishek1033ubuntu](https://github.com/Abhishek1033ubuntu)
* **Methodology:** Systems Engineering, Computational Multiphysics & Reactor Feasibility Modeling
* **Development Paradigm:** Human-Directed AI-Assisted Computational Workflow (Co-developed in technical collaboration with Google Gemini AI)

### Acknowledgments & AI Collaboration Notice
This project was conceptualized, architecturalized, and directed by **Abhishek Singh**. The computational solver algorithms, numerical stabilization methods, and diagnostic visualization code were co-developed in technical collaboration with **Google Gemini AI**. This repository demonstrates how human physical domain intuition and AI-assisted computational engineering can accelerate open-source research in next-generation energy systems.

---

## License

Copyright © 2026 Abhishek Singh. Distributed under the [MIT License](LICENSE).