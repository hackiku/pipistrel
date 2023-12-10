# 3_wing_pg.py

import streamlit as st
from data import Variable
from utils import spacer, variables_two_columns

# Instantiate variables using the Variable class
c_z_krst = Variable("Cruise Lift Coefficient", 0.200, r"C_{z_{krst}}", "m/s")
c_z_max = Variable("Max Lift Coefficient", 0.247, r"C_{z_{max}}", "m/s")
v_krst = Variable("Cruising Speed", 224.37, r"v_{krst}", "m/s")
alpha_n = Variable("Angle of Attack", -1.3, r"\alpha_n", "degrees")
lambda_wing = Variable("Wing Aspect Ratio", 3.888, r"\lambda")
n = Variable("Wing Taper Ratio", 0.520, "n")
rho = Variable("Air Density at Cruise Altitude", 0.736116, r"\rho", "kg/m^3")

def main():
    st.title("3. Wing Design")
    st.write("Creating lift curve using 4 parameters.")
    
    st.header("3.1 Wing Lift Features")

    # Display variables using the two-column layout
    variables_two_columns(c_z_krst)
    variables_two_columns(c_z_max)
    variables_two_columns(v_krst)
    variables_two_columns(alpha_n)
    variables_two_columns(lambda_wing)
    variables_two_columns(n)
    variables_two_columns(rho)

    st.markdown("***")

if __name__ == "__main__":
    main()
