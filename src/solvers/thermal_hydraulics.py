"""
FLiBe Molten Salt Thermal-Hydraulic Transient Solver
Lead Author: Abhishek Singh (ORCID: 0009-0004-6913-096X)
Technical Collaboration: Google Gemini AI
"""

import numpy as np

def run_flibe_transient(P_th_MW=149.0, rep_rate_Hz=5.0, V_loop_m3=12.0,
                        T_inlet=550.0, delta_T_target=100.0, t_end=30.0):
    """
    Models primary FLiBe coolant startup temperature evolution
    and 5 Hz steady-state thermal ripple.
    """
    rho_FLiBe = 1940.0
    Cp_FLiBe = 2380.0
    m_loop_kg = V_loop_m3 * rho_FLiBe
    
    period_sec = 1.0 / rep_rate_Hz
    E_pulse_J = (P_th_MW * 1e6) / rep_rate_Hz
    mdot_kg_s = (P_th_MW * 1e6) / (Cp_FLiBe * delta_T_target)
    
    dt = 0.001
    time_pts = np.arange(0.0, t_end, dt)
    N_steps = len(time_pts)
    
    T_out = np.zeros(N_steps)
    T_out[0] = T_inlet
    pulse_width_sec = 0.005
    
    for i in range(1, N_steps):
        t = time_pts[i-1]
        t_in_cycle = t % period_sec
        
        P_in_W = (E_pulse_J / pulse_width_sec) if t_in_cycle < pulse_width_sec else 0.0
        P_out_W = mdot_kg_s * Cp_FLiBe * (T_out[i-1] - T_inlet)
        dT_dt = (P_in_W - P_out_W) / (m_loop_kg * Cp_FLiBe)
        
        T_out[i] = T_out[i-1] + dT_dt * dt
        
    return time_pts, T_out, mdot_kg_s, m_loop_kg

if __name__ == "__main__":
    t, T_out, mdot, m_loop = run_flibe_transient()
    print(f"Coolant Inventory Mass  : {m_loop:.1f} kg")
    print(f"Mass Flow Rate          : {mdot:.2f} kg/s")
    print(f"Steady Outlet Temp      : {np.mean(T_out[t>=25.0]):.2f} deg C")
