
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
b = Variable("Wingspan", 8.942, "b", "m")
S = Variable("Wing Area", 20.602, "S", "m²")


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

    # key variables 
    variables_two_columns(c_z_max)
    variables_two_columns(alpha_n)
    
    st.markdown("***")

    # 3.1.1.
    st.subheader("3.1.1. Max lift coefficient of wings")
    st.write("Za proračun uzgonskih karakteristika krila i dobijanje podataka za formiranje krive uzgona je korišćen program Trapezno krilo - Glauert, a ulazni parametri su:")

    # # alpha crit 
    variables_two_columns(c_z_krst)
    variables_two_columns(v_krst) # = 224.37 m/s = 807.73 km/h
    variables_two_columns(rho) # ρ

    with st.expander("Calculate wing aspect ratio (λ)"):
        
        def calculate_lambda_wing():
            lambda_wing.value = b.value**2 / S.value
            numbers = "=" + f"\\frac{{{b.value:.2f}^2}}{{{S.value:.2f}}}"
            lambda_wing.formula = f"\\lambda = \\frac{{{b.latex}^2}}{{{S.latex}}} {numbers}"
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            b.value = st.number_input(f'{b.name} {b.unit}', value=b.value, step=0.01, format="%.3f")
        with col2:
            S.value = st.number_input(f'{S.name} {S.unit}', value=S.value, step=0.1, format="%.3f")
        with col3:
          st.latex(f"{b.latex} = {b.value:.3f} \ {b.unit}")
        with col4:
          st.latex(f"{S.latex} = {S.value:.3f} \ {S.unit}")
            # st.latex = (S.latex)
        # st.latex(lambda_wing.formula)               
    
    calculate_lambda_wing()
    variables_two_columns(lambda_wing, display_formula=True) # λ

    with st.expander("Calculate wing taper ratio (n)"):
      def calculate_taper_ratio():
          n.value = l_0.value / l_s.value
          numbers = "=" + f"\\frac{{{l_0.value:.2f}}}{{{l_s.value:.2f}}}"
          n.formula = f"n = \\frac{{{l_0.latex}}}{{{l_s.latex}}} {numbers}"

      col1, col2, col3 = st.columns(3)
      with col1:
          l_0.value = st.number_input(f'{l_0.name} {l_0.unit}', value=l_0.value, step=0.01, format="%.3f")
      with col2:
          l_s.value = st.number_input(f'{l_s.name} {l_s.unit}', value=l_s.value, step=0.01, format="%.3f")
      with col3:
          st.latex(f"{l_0.latex} = {l_0.value:.3f} \ {l_0.unit}")
          st.latex(f"{l_s.latex} = {l_s.value:.3f} \ {l_s.unit}")

    calculate_taper_ratio()
    variables_two_columns(n, display_formula=True)  # n
        
    st.markdown("***")


    

    st.markdown("***")

if __name__ == "__main__":
    main()
