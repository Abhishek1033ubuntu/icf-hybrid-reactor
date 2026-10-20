"""
EUROFER97 First-Wall Dynamic Mechanics & SDOF Stress Solver
Lead Author: Abhishek Singh (ORCID: 0009-0004-6913-096X)
Technical Collaboration: Google Gemini AI
"""

import numpy as np

def run_firstwall_mechanics(P_peak_bar=35.0, R_wall=1.50, t_wall=0.025,
                            f_rep=5.0, t_end=0.80):
    """
    Solves dynamic SDOF ring oscillations and hoop stress in EUROFER97
    first-wall shell under 5 Hz shock pulses.
    """
    E_mod = 210.0e9
    rho_steel = 7800.0
    nu_poisson = 0.30
    sigma_allow_MPa = 160.0
    
    P_peak_Pa = P_peak_bar * 1.0e5
    tau_pulse = 20.0e-6
    period_sec = 1.0 / f_rep
    
    c_speed = np.sqrt(E_mod / (rho_steel * (1.0 - nu_poisson)))
    f_n = c_speed / (2.0 * np.pi * R_wall)
    omega_n = 2.0 * np.pi * f_n
    zeta_damping = 0.03
    
    dt = 1.0e-6
    t_pts = np.arange(0.0, t_end, dt)
    N_steps = len(t_pts)
    sigma_MPa = np.zeros(N_steps)
    
    for i in range(1, N_steps):
        t = t_pts[i]
        t_cycle = t % period_sec
        P_t = P_peak_Pa * np.exp(-t_cycle / (tau_pulse * 0.5)) if t_cycle < tau_pulse else 0.0
        
        d2_sigma = (P_t * R_wall / (2.0 * t_wall)) * (omega_n**2) / 1.0e6                    - 2.0 * zeta_damping * omega_n * (sigma_MPa[i-1] - sigma_MPa[i-2])/dt                    - (omega_n**2) * sigma_MPa[i-1] if i > 1 else 0.0
                   
        sigma_MPa[i] = sigma_MPa[i-1] + d2_sigma * (dt**2)
        
    return t_pts, sigma_MPa, np.max(sigma_MPa), sigma_allow_MPa

if __name__ == "__main__":
    t, sig, p_sig, allow = run_firstwall_mechanics()
    print(f"Peak Dynamic Hoop Stress : {p_sig:.2f} MPa")
    print(f"ASME Yield Design Limit  : {allow:.2f} MPa")
    print(f"Safety Yield Margin      : +{((allow-p_sig)/allow)*100:.1f}%")
