"""
Sub-Critical Blanket Neutronics & Plant Power Balance Solver
Lead Author: Abhishek Singh (ORCID: 0009-0004-6913-096X)
Technical Collaboration: Google Gemini AI
"""

import numpy as np

E_FUSION_MEV = 17.6
E_FISS_MEV = 200.0
NEUT_PER_FISS = 2.5

def analyze_plant_performance(k_eff=0.965, eta_driver=0.18, eta_thermal=0.48,
                              E_laser_MJ=1.80, E_fusion_MJ=0.2912, rep_rate_Hz=5.0,
                              streaming_loss_pct=10.0):
    """
    Computes net electrical power output, blanket multiplication M,
    and net plant efficiency Q_electric.
    """
    f_3D_coverage = 1.0 - (streaming_loss_pct / 100.0)
    P_laser_wall_plug = (E_laser_MJ / eta_driver) * rep_rate_Hz
    
    f_fiss = (k_eff / (NEUT_PER_FISS * (1.0 - k_eff))) * f_3D_coverage
    M_blanket = 1.0 + f_fiss * (E_FISS_MEV / E_FUSION_MEV)
    
    P_thermal_MW = (E_fusion_MJ * f_3D_coverage) * M_blanket * rep_rate_Hz
    P_gross_elec_MW = P_thermal_MW * eta_thermal
    P_net_elec_MW = P_gross_elec_MW - P_laser_wall_plug
    Q_electric = P_gross_elec_MW / P_laser_wall_plug
    
    return {
        "k_eff": k_eff,
        "P_recirc_MW": P_laser_wall_plug,
        "M_blanket": M_blanket,
        "P_thermal_MW": P_thermal_MW,
        "P_gross_elec_MW": P_gross_elec_MW,
        "P_net_elec_MW": P_net_elec_MW,
        "Q_electric": Q_electric
    }

if __name__ == "__main__":
    res = analyze_plant_performance()
    print("OPTIMIZED HYBRID PLANT PERFORMANCE:")
    print(f"  k_eff                   : {res['k_eff']:.3f}")
    print(f"  Recirculating Power     : {res['P_recirc_MW']:.1f} MWe")
    print(f"  Blanket Multiplication M: {res['M_blanket']:.1f}x")
    print(f"  Thermal Power Output    : {res['P_thermal_MW']:.1f} MWth")
    print(f"  Gross Electrical Power  : {res['P_gross_elec_MW']:.1f} MWe")
    print(f"  Net Commercial Power    : {res['P_net_elec_MW']:.1f} MWe")
    print(f"  Plant Electrical Gain Q : {res['Q_electric']:.2f}")
