# 3_wing_pg.py

import streamlit as st
from data import Variable
from utils import spacer, variables_two_columns
import math

# Instantiate variables using the Variable class
c_z_krst = Variable("Cruise Lift Coefficient", 0.247, r"C_{z_{krst}}", "m/s")
c_z_max = Variable("Max Lift Coefficient", 1.46, r"C_{z_{max}}", "m/s")  # Assuming max lift coefficient is from NACA 65-212
v_krst = Variable("Cruising Speed", 224.37, r"v_{krst}", "m/s")
alpha_n = Variable("Angle of Attack", -1.3, r"\alpha_n", "degrees")
lambda_wing = Variable("Wing Aspect Ratio", 3.888, r"\lambda")
n = Variable("Wing Taper Ratio", 0.520, "n")
rho = Variable("Air Density at Cruise Altitude", 0.736116, r"\rho", "kg/m^3")

l_s = Variable("Chord Length", 3.028, "l_s", "m")
l_0 = Variable("Root Chord Length", 1.576, "l_0", "m")

# n = 1.576 / l_s  # Taper ratio (n)

# NACA Airfoil characteristics
naca_65_212_c_z_max = 1.46
naca_64_209_c_z_max = 1.40
alpha_n_65_212 = -1  # Angle of attack at zero lift for NACA 65-212
alpha_n_64_209 = -1.3  # Angle of attack at zero lift for NACA 64-209
a_0_65_212 = 0.110  # Lift curve slope for NACA 65-212
correction_factor = 0.859  # Correction for the angle of attack

def main():
    st.title("3. Wing Design")
    st.write("Creating lift curve using 4 parameters.")
    
    st.header("3.1 Wing Lift Features")

    # Display variables using the two-column layout
    
    variables_two_columns(c_z_max)
    variables_two_columns(alpha_n)
    
    st.markdown("***")

    # 3.1.1.
    st.subheader("3.1.1. Max lift coefficient of wings")
    st.write("Za proračun uzgonskih karakteristika krila i dobijanje podataka za formiranje krive uzgona je korišćen program Trapezno krilo - Glauert, a ulazni parametri su:")

    # vkrst = 224.37 m/s = 807.73 km/h
    # # alpha crit 
    variables_two_columns(c_z_krst)
    variables_two_columns(v_krst)
    variables_two_columns(rho) # ρ
    

    # lambda      
    st.markdown("***")
    st.write("Calculate wing aspect ratio (λ):")

    col1, col2, col3 = st.columns(3)
    with col1:
        b = st.number_input('Wingspan b [m]', value=8.942, step=0.01)
    with col2:
        S = st.number_input('Wing area S [m²]', value=20.602, step=0.1)
    with col3:
        lambda_wing.value = b**2 / S 
        lambda_calculated = st.number_input('Aspect Ratio λ', value=lambda_wing.value, step=0.001, format="%.3f")

    st.latex("\\lambda = \\frac{b^2}{S} = \\frac{" + f"{b:.2f}^2" + "}{ " + f"{S:.2f}" + "} = " + f"{lambda_calculated:.3f}" + "")


    
    st.markdown("***")

    st.write("Calculate taper ratio (n):")
    
    variables_two_columns(n)
    
    col1, col2, col3 = st.columns(3)
    
    


    with col1:
        l_0_value = st.number_input('Root Chord Length l_0 [m]', value=1.576, step=0.01)
    with col2:
        l_s_value = st.number_input('Chord Length l_s [m]', value=3.028, step=0.01)
    with col3:
        n_calculated = l_0_value / l_s_value
        st.write(f"n = {n_calculated:.3f}")
        n.value = n_calculated  # Update the variable's value


    

    st.markdown("***")

if __name__ == "__main__":
    main()
