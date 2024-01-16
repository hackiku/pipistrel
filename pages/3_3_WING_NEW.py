### 3_wing.py ###

import streamlit as st
from variables_manager import initialize_session_state, get_variable_value, update_variables, log_changed_variables
from utils import spacer
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import re

# Define the page-specific variables
page_values = [
    'S', 'l0', 'l1', 'b', 'm_sr', 'v_krst', 'T', 'P', 'rho', 'c', 
    'g', 'Re', 'c_z_krst',
    'lambda_wing', 'n', 'phi', 'alpha_n', 'c_z_max_root', 'alpha_0_root', 
    'a_0_root', 'c_z_max_tip', 'alpha_0_tip', 'a_0_tip'
]

def main():
    initialize_session_state(page_values)

    # Display title and headers
    st.title("3. Wing Design")
    st.header("3.1 Lift characteristics of wing")

    # ==================== EXPANDER FOR INPUT PARAMETERS ====================
    with st.expander("Edit / calculate input parameters"):
        # User inputs for basic variables
        S = st.number_input('Wing Area (m^2)', value=get_variable_value('S'))
        b = st.number_input('Wingspan (m)', value=get_variable_value('b'))
        rho = st.number_input('Air Density at Cruise Altitude (kg/m^3)', value=get_variable_value('rho'))
        
        # More inputs for other variables as needed...

        # Calculations for derived variables like lambda_wing
        lambda_wing = b**2 / S  # Replace this formula with the correct one
        st.session_state['lambda_wing'] = lambda_wing  # Updating session state

        # Display calculated lambda_wing
        st.write(f"Wing Aspect Ratio (λ): {lambda_wing}")

        # More calculations and inputs...

    # Display wing inputs
    wing_inputs = f"""
    | # | Parameter Name                 | Symbol                                           | Value                                  | Unit     |
    |---|--------------------------------|--------------------------------------------------|----------------------------------------|----------|
    | 1 | Wing Area                      | S                                                | {S}                                    | m^2      |
    | 2 | Wingspan                       | b                                                | {b}                                    | m        |
    | 3 | Wing Aspect Ratio (λ)          | λ                                                | {lambda_wing}                          |          |
    | 4 | Air Density at Cruise Altitude | ρ                                                | {rho}                                  | kg/m^3   |
    """
    st.markdown(wing_inputs)

    # More code for other parts of the page...

    # Update variables at the end of the session
    update_variables(page_values, locals())
    log_changed_variables()

if __name__ == "__main__":
    main()
