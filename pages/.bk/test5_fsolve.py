import streamlit as st
from sympy import symbols, diff, solve, Eq

# Define the main function that Streamlit will run
def main():
    
    st.code("Aerodinamicke karakteristike date u obliku")
    # Streamlit number input for user to input parameters
    B = st.number_input("Lift coefficient base (B)", value=0.075, step=0.001, format="%.3f")
    A = st.number_input("Drag coefficient constant (A)", value=0.0105, step=0.0001, format="%.4f")
    a0 = st.number_input("Lift curve slope (a0)", value=0.09, step=0.01)
    cz_minus = st.number_input("Cz minus value", value=0.05, step=0.01)
    alpha_n = st.number_input("Zero-lift angle of attack (α + #)", value=2.0, step=0.1)
    
    # Define the symbols
    alpha = symbols('alpha')
    CL = B * (alpha + alpha_n)
    CD = A + a0 * (CL - cz_minus)**2
    
    # Calculate the glide ratio
    glide_ratio = CL / CD
    
    # Differentiate the glide ratio with respect to alpha
    d_glide_ratio = diff(glide_ratio, alpha)
    
    # Solve for alpha where the derivative is zero (maximum glide ratio)
    alpha_max_glide_ratio = solve(Eq(d_glide_ratio, 0), alpha)

    # Create columns for displaying the equations
    col1, col2 = st.columns(2)
    with col1:
        st.latex(rf"C_L = {B}(\alpha + 2)")
    with col2:
        st.latex(rf"C_D = {A} + {a0} \ (C_L - {cz_minus})^2")
    
    # Display the solution
    if alpha_max_glide_ratio:
        st.success(f"Solution for angle of attack (α) that maximizes the lift-to-drag ratio: {alpha_max_glide_ratio[1]:.4f} degrees")
    else:
        st.error("No solution found. Adjust the parameters.")

# Run the main function in Streamlit
if __name__ == "__main__":
    main()
