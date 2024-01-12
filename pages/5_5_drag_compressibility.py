# 4_drag_calculation.py

import streamlit as st
import matplotlib.pyplot as plt
from data import Variable, load_variables_from_session, save_variables_to_session
from utils import spacer, emoji_header, variables_two_columns
from math import pi
import math

# Constants
delta = 0.00898  # correction factor for wing sweep and wing thinning
phi_degrees = 27  # Wing sweep angle in degrees
D_T_max = 2.029  # Maximum fuselage diameter in meters
b = 8.95  # Wing span in meters
s = 0.891  # Wing area ratio

def calculate_correction_factor(delta, phi):
    phi_radians = math.radians(phi)  # Convert degrees to radians for calculation
    u = 1 / (1 + delta)
    return u

def interpolate_k(phi_degrees):
    # Here we use the given values to interpolate 'k'
    # This could be replaced with a more accurate interpolation if more data points are provided
    if phi_degrees == 0:
        k = 0.38
    elif phi_degrees == 20:
        k = 0.40
    elif phi_degrees == 35:
        k = 0.45
    else:
        # Linear interpolation (example for phi_degrees = 27)
        k = 0.423
    return k

# Function to calculate the wing aspect ratio
def calculate_aspect_ratio(D_T_max, b):
    return D_T_max / b

# Define a function to calculate the drag coefficient
def calculate_drag_coefficient(C_X_min, k, lambda_wing, u, s):
    return C_X_min + k + (1 / (pi * lambda_wing * u * s))

# Streamlit application
def main():
    st.title("4.2 Određivanje otpora zavisno od uzgona")


    # Input variables
    C_X_min = st.number_input("Minimum drag coefficient (C_X_min)", value=0.01869, format="%.5f")
    k = st.number_input("Factor from wing sweep angle (k)", value=0.00791, format="%.5f")
    lambda_wing = st.number_input("Aspect ratio (lambda)", value=8.95)
    u = st.number_input("Correction factor for induced drag (u)", value=0.9911, format="%.4f")
    s = st.number_input("Wing area ratio (s)", value=0.891, format="%.3f")

    # Calculate drag coefficient
    C_X = calculate_drag_coefficient(C_X_min, k, lambda_wing, u, s)

    # Display results
    st.write(f"The drag coefficient (C_X) is: {C_X:.4f}")

    # math
    st.latex(r"C_X = C_{X_{min}} + k \cdot C_{z}^2 + \frac{C_{z}^2}{\pi \cdot \lambda \cdot (u \cdot s)}")
    st.latex(rf"C_X = {C_X_min:.3f} + {k:.3f} + \frac{{1}}{{\pi \cdot {lambda_wing:.3f} \cdot ({u:.3f} \cdot {s:.3f})}} = {C_X:.4f}")

    # Explain the calculation
    st.markdown("### Explanation:")
    st.markdown("""
    - *C_X_min* is the minimum drag coefficient.
    - *k* is the factor from the wing sweep angle.
    - *λ (lambda_wing)* is the aspect ratio of the wing.
    - *u* is the correction factor for induced drag, taking into account factors like wingtip design.
    - *s* is the wing area ratio, considering the actual exposed wing area versus the reference area.
    """)

    u = calculate_correction_factor(delta, phi_degrees)
    st.write("Factor u calculation:")
    st.latex(r"u = \frac{1}{1 + \delta} = \frac{1}{1 + 0.00898} = 0.9911")

    # Display the formula for the wing aspect ratio
    s_ratio = calculate_aspect_ratio(D_T_max, b)
    st.write("Wing aspect ratio calculation:")
    st.latex(r"s = \frac{D_{T_{max}}}{b} = \frac{2.029}{8.95} = 0.2267")

    # Display the formula for k factor from the graph interpolation
    k = interpolate_k(phi_degrees)
    st.write("Factor k from graph interpolation:")
    st.latex(r"k = 0.423 \cdot C_{X_{min}} = 0.423 \cdot 0.01869 = 0.00791")

    # Display the drag coefficient formula
    C_X_min = 0.01869  # Example value for minimum drag coefficient
    st.write("Drag coefficient calculation:")
    st.latex(rf"C_X = C_{{X_{{min}}}} + k + \frac{1}{{\pi \cdot \lambda \cdot (u \cdot s)}}")

    # Display the value for the drag coefficient
    lambda_value = 8.95  # Wing span in meters, example value
    C_X = C_X_min + k + (1 / (pi * lambda_value * u * s_ratio))
    st.write(f"The drag coefficient (C_X) is: {C_X:.4f}")

    # Display the calculation for the correction factor due to wing sweep and thinning
    st.write("Correction factor due to wing sweep and thinning:")
    st.latex(r"\delta = 0.00898")

    # Display the angle of wing sweep
    st.write("Wing sweep angle:")
    st.latex(rf"\phi = {phi_degrees}^\circ")

    # Display the graph or table for the k factor if you have it
    # For now, we'll just mention it's from a graph
    st.write("The k factor is interpolated from a graph based on the wing sweep angle.")

    st.markdown("***")
    #==============================oswald====================================
    st.subheader("4.2.1. Određivanje Osvaldovog faktora e i člana uz CZ2")

    # Calculate the Oswald efficiency factor 'e'
    e = 1 / (pi * lambda_wing * k + 1 / (u * s))

    # Calculate the term B associated with Cz^2
    B = 1 / (pi * e * lambda_wing)

    # Given minimum drag coefficient
    C_X_min = 0.018623

    # Display Oswald efficiency factor 'e' calculation
    st.write("Oswald efficiency factor (e) calculation:")
    st.latex(r"e = \frac{1}{\pi \cdot \lambda \cdot k + \frac{1}{u \cdot s}} = 0.81365")

    # Display term B calculation
    st.write("Term \( B \) associated with \( C_{Z}^2 \) calculation:")
    st.latex(r"B = \frac{1}{\pi \cdot e \cdot \lambda} = 0.1006")

    # Display the aircraft polar equation
    st.subheader("4.2.2. Proračunska polara aviona")
    st.write("Aircraft polar equation \( C_{X} = A + B \cdot C_{Z}^2 \):")
    st.latex(r"C_{X} = C_{X_{min}} + B \cdot C_{Z}^2")
    st.latex(r"C_{X} = 0.018623 + 0.1006 \cdot C_{Z}^2")

    # Explain the calculation
    st.markdown("""
    - \( e \) is the Oswald efficiency factor which corrects for the less-than-ideal distribution of lift across the span of the wing.
    - \( B \) is a term that represents the induced drag's dependence on the square of the lift coefficient \( C_{Z} \).
    - \( A \) is the minimum drag coefficient \( C_{X_{min}} \).
    - The equation represents the aircraft's drag polar, which is a plot of total drag coefficient \( C_{X} \) against the lift coefficient \( C_{Z} \) squared.
    """)

    # Allow user to input CZ and calculate CX
    C_Z = st.number_input("Enter lift coefficient (C_Z)", value=0.0, format="%.5f")
    C_X = C_X_min + B * C_Z**2
    st.write(f"The total drag coefficient (C_X) for C_Z = {C_Z} is: {C_X:.5f}")

if __name__ == "__main__":
    main()
