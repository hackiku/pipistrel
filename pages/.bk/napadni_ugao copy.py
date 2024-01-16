import streamlit as st
import numpy as np
from scipy.optimize import fsolve

# Define the main function that Streamlit will run
def main():
    
    # Streamlit number input for user to input parameters
    A = st.number_input("Baseline drag coefficient (A)", value=0.0105, step=0.0001, format="%.4f")
    B = st.number_input("Induced drag coefficient (B)", value=0.075, step=0.001, format="%.3f")
    alfan = st.number_input("Zero-lift angle of attack (α + #)", value=2.0, step=0.1)
    a0 = st.number_input("Lift curve slope (a0)", value=0.09, step=0.01)
    cz_minus = st.number_input("Cz 0.05", value=0.05, step=0.1)
    # Inner function that calculates the equation based on alpha
    def equation(alfa):
        Cz = a0 * (alfa + alfan)
        Cx = A + B * Cz**2
        # Cx = A + B * (Cz - cz_minus)**2
        finesse = Cz/Cx
        # return -finesse
        return alfa - (90 - np.degrees(np.arctan(Cz / Cx)))

    initial_guess = 5
    alfa_solution = fsolve(equation, initial_guess)

    col1, col2 = st.columns(2)
    with col1:
        st.latex(rf"C_z = {B}(\alpha + {alfan:.1f})")
        st.latex(rf"C_x = {A} + {a0} \ (C_z - {cz_minus})^2")
    with col2:
        st.latex(r"C_z = a_0(\alpha + \alpha_{\text{n}})")
        st.latex(r"C_x = A + BC_z^2")


    st.success(f"Solution for alfa: {alfa_solution[0]:.5f} degrees")



# Run the main function in Streamlit
if __name__ == "__main__":
    main()
