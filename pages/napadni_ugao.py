import streamlit as st
import numpy as np
from scipy.optimize import fsolve

# Define the main function that Streamlit will run
def main():
    
    col1, col2 = st.columns(2)
    with col1:
        st.latex(r"C_z = 0.08(\alpha + 4)")
        st.latex(r"C_z = a_0(\alpha + \alpha_{\text{n}})")
    with col2:
        st.latex(r"C_x = 0.0092 + 0.074C_z^2")
        st.latex(r"C_x = A + BC_z^2")

    # Streamlit number input for user to input parameters
    A = st.number_input("Baseline drag coefficient (A)", value=0.0092, step=0.0001, format="%.4f")
    B = st.number_input("Induced drag coefficient (B)", value=0.074, step=0.001, format="%.3f")
    alfan = st.number_input("Zero-lift angle of attack (alfan in degrees)", value=4.0, step=0.1)
    a0 = st.number_input("Lift curve slope (a0)", value=0.08, step=0.01)

    # Inner function that calculates the equation based on alpha
    def equation(alfa):
        Cz = a0 * (alfa + alfan)
        Cx = A + B * Cz**2
        return alfa - (90 - np.degrees(np.arctan(Cz / Cx)))

    # Initial guess for alfa, user can change it
    # initial_guess = st.number_input("Initial guess for angle of attack (alfa)", value=10.0, step=1.0)
    initial_guess = 10.0

    # Button to solve the equation
    if st.button('Calculate angle of attack (alfa)'):
        # Solve the equation using the user's inputs
        alfa_solution = fsolve(equation, initial_guess)

        # Display the solution using Streamlit's success message
        st.success(f"Solution for alfa: {alfa_solution[0]:.5f} degrees")

        # Also print the solution to the console
        print("Solution for alfa:", alfa_solution)

# Run the main function in Streamlit
if __name__ == "__main__":
    main()
