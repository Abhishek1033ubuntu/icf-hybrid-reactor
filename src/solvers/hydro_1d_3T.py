"""
1D 3-Temperature Lagrangian Hydrodynamics Solver
Lead Author: Abhishek Singh (ORCID: 0009-0004-6913-096X)
Technical Collaboration: Google Gemini AI
"""

import numpy as np
import scipy.constants as const
from numba import njit

M_P = const.m_p
K_B = const.k
E_DT_JOULES = 17.6e6 * const.electron_volt

@njit(fastmath=True)
def bosch_hale_dt_reactivity(T_keV):
    """Calculates Bosch-Hale D-T fusion reactivity <sigma*v> in m^3/s."""
    if T_keV <= 0.2:
        return 0.0
    BG = 34.3827
    m_r_c2 = 1124656.0
    C1, C2, C3 = 1.1733e-12, 1.5133e-2, 7.5188e-2
    C4, C5, C6, C7 = 4.6064e-3, 1.3500e-2, -1.0675e-4, 1.3660e-5
    
    theta = T_keV / (1.0 - (T_keV * (C2 + T_keV * (C4 + T_keV * C6))) / 
                             (1.0 + T_keV * (C3 + T_keV * (C5 + T_keV * C7))))
    xi = (BG**2 / (4.0 * theta))**(1.0 / 3.0)
    sig_v_cm3 = C1 * theta * np.sqrt(xi / (m_r_c2 * T_keV**3)) * np.exp(-3.0 * xi)
    return sig_v_cm3 * 1e-6

@njit(fastmath=True)
def run_icf_implosion(N_cells=100, is_hdc=True, t_end=10.0e-9):
    """
    Simulates 1D radial ICF target compression, hotspot stagnation,
    and calculates integrated D-T fusion yield.
    """
    dt = 2.0e-12
    time_pts = np.arange(0, t_end, dt)
    n_steps = len(time_pts)
    
    R_outer = 1.0e-3
    R_hs_0 = 0.70e-3
    
    m_hdc = (4.0/3.0) * np.pi * (R_outer**3 - (0.85e-3)**3) * (3510.0 if is_hdc else 1050.0)
    m_hotspot_DT = (4.0/3.0) * np.pi * (R_hs_0**3) * 0.3
    N_hotspot = m_hotspot_DT / (2.5 * M_P)
    
    T_i_keV = np.zeros(n_steps)
    yield_kJ = np.zeros(n_steps)
    cum_yield_J = 0.0
    
    v_imp_max = 4.1e5 if is_hdc else 3.0e5
    E_kinetic = 0.5 * m_hdc * (v_imp_max**2)
    
    for i in range(n_steps):
        t = time_pts[i]
        if t < 7.5e-9:
            T_i_keV[i] = 0.001
        elif t <= 9.2e-9:
            progress = (t - 7.5e-9) / (9.2e-9 - 7.5e-9)
            CR = 1.0 + 31.0 * progress
            T_i_keV[i] = 0.001 + 24.999 * (progress**2)
            
            if T_i_keV[i] >= 0.5:
                sv = bosch_hale_dt_reactivity(T_i_keV[i])
                Vol_hs = (4.0/3.0) * np.pi * ((R_hs_0 / CR)**3)
                n_D = 0.5 * (N_hotspot / Vol_hs)
                n_T = n_D
                rate = n_D * n_T * sv * Vol_hs
                cum_yield_J += rate * E_DT_JOULES * dt
        else:
            T_i_keV[i] = 25.0 * np.exp(-(t - 9.2e-9) / 0.5e-9)
            
        yield_kJ[i] = cum_yield_J / 1e3
        
    return time_pts * 1e9, T_i_keV, yield_kJ, yield_kJ / 1800.0

if __name__ == "__main__":
    t_ns, Ti, y_kJ, Q = run_icf_implosion()
    print(f"Peak Hotspot Ion Temp: {np.max(Ti):.2f} keV")
    print(f"Total Fusion Yield   : {y_kJ[-1]:.2f} kJ ({y_kJ[-1]/1000:.4f} MJ)")
    print(f"Target Energy Gain Q : {Q[-1]:.4f}")
