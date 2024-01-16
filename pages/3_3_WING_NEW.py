### 3_wing.py ###

import streamlit as st
from variables_manager import initialize_session_state, get_variable_value, update_variables, log_changed_variables
from utils import spacer
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import re

root_airfoil_data = ["NACA 65_2-415", 9.0, -2.8, 0.113, 1.62, "D", 16.5, 0.30, 11.5, 0.0040, -0.062, 0.266, -0.062]
tip_airfoil_data = ["NACA 63_4-412", 9.0, -3.0, 0.100, 1.78, "D", 15.0, 0.32, 9.6, 0.0045, -0.075, 0.270, -0.073]

def main():
    
    page_values = [
        'S', 'l0', 'l1', 'b', 'm_sr', 'v_krst', 'T', 'P', 'rho', 'c', 
        'g', 'Re', 'c_z_krst',
        'lambda_wing', 'n', 'phi', 'alpha_n', 'c_z_max_root', 'alpha_0_root', 
        'a_0_root', 'c_z_max_tip', 'alpha_0_tip', 'a_0_tip'
    ]
    initialize_session_state(page_values)

    # Display title and headers
    st.title("3. Wing Lift Calculation")
    st.write('The goal of this section is to construct the lift curve, and for that we need to calculate the following parameters:')
    st.markdown(r"""- $C_{z_{max}}$ - Max lift coefficient
- $\alpha_0$ - Zero-lift angle of attack
- $a_0$ - Lift curve slope XXX
- $\alpha_{krst}$ - Angle of attack at cruise
""")
    
    
    st.header("3.1 Lift characteristics of wing")


    # ==================== EXPANDER FOR INPUT PARAMETERS ====================
    with st.expander("Edit / calculate input parameters"):
        # # alpha crit 
        c_z_krst = st.number_input('Cruise Lift Coefficient', value=get_variable_value('c_z_krst'))
        v_krst = st.number_input('Cruising Speed', value=get_variable_value('v_krst'))
        rho = st.number_input('Air Density at Cruise Altitude (kg/m^3)', value=get_variable_value('rho'))

        st.code("Calculate wing aspect ratio (λ)")
            
        col1, col2 = st.columns(2)
        with col1:
            b = st.number_input('b - Wingspan (m)', value=get_variable_value('b'))
        with col2: 
            S = st.number_input('S - Wing Area (m^2)', value=get_variable_value('S'))
        
        st.code("Calculate wing taper ratio (n)")
        l0 = st.number_input('Tip Chord Length (m)', value=get_variable_value('l0'))
        ls = st.number_input('Root Chord Length (m)', value=get_variable_value('ls'))

    lmbda = b**2 / S
    st.latex(f"\\lambda = \\frac{{b^2}}{{S}} = \\frac{{{b**2:.2f}}}{{{S}}} = {lmbda:.3f}")
    n = l0 / ls
    st.latex(f"n = \\frac{{l_0}} {{l_s}} = \\frac{{{l0}}} {{{ls}}} = {n:.3f}")

    update_variables(page_values, locals())
    log_changed_variables()


    # Display wing inputs
    wing_inputs = f"""
    | # | Parameter Name                 | Symbol                                           | Value                                  | Unit     |
    |---|--------------------------------|--------------------------------------------------|----------------------------------------|----------|
    | 1 | Cruise Lift Coefficient        | $C_{{z_krst}}$                               | {c_z_krst:.3f}                   |          |
    | 2 | Wing Aspect Ratio (λ)          | $add latex$                    | {lmbda:.3f} |          |
    | 3 | Tip Chord Length               | ${l0.latex}$                                     | {l0:.3f}                         | {l0.unit}|
    | 4 | Root Chord Length              | ${l1.latex}$                                     | {l1:.3f}                         | {l1.unit}|
    | 5 | Wing Taper Ratio (n)           | ${n.formula}$                          | {n:.3f}      |          |
    | 6 | Cruising Speed                 | ${v_krst.latex}$                                 | {v_krst:.2f}                     | {v_krst.unit} |
    | 7 | Air Density at Cruise Altitude | ${rho.latex}$                                    | {rho:.5f}                        | {rho.unit} |
    """

    st.markdown(wing_inputs)

    airfoil_inputs = f"""
    | # | Parameter Name | Symbol | Tip | Root |
    |---|----------------|--------|-----|------|
    | 1 | Max Lift Coefficient | Cz_max | {c_z_max_tip} | {c_z_max_root} |
    | 2 | Angle of Zero Lift | α₀ | {alpha_0_tip}° | {alpha_0_root}° |
    | 3 | Lift Gradient | a₀ | {a_0_tip} | {a_0_root} |
    """
    st.markdown(airfoil_inputs)

    st.markdown("***")


    # More code for other parts of the page...

    # Update variables at the end of the session
    update_variables(page_values, locals())
    log_changed_variables()

if __name__ == "__main__":
    main()