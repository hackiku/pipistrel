# 2_2._airfoil.py

import streamlit as st
from data import Variable
from utils import spacer, variables_two_columns

c_z_krst = Variable("Cruise Lift Coefficient", 0.247, r"C_{z_{krst}}", "m/s")
c_z_max = Variable("Max Lift Coefficient", 1.46, r"C_{z_{max}}", "m/s")  # Assuming max lift coefficient is from NACA 65-212
v_krst = Variable("Cruising Speed", 224.37, r"v_{krst}", "m/s")

def main():
    st.title("2. Airfoil tables")


if __name__ == "__main__":
    main()