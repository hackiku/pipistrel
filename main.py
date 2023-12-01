import streamlit as st
import pandas as pd
from virus_model_streamlit.virus_viewer_component import virus_viewer
import inspect
from calcs import convert_units, aircraft_specs, calculate_cruise_speed


# specs table
def display_specs(specs, units="SI"):
    if units == "Aviation":
        specs = convert_units(specs)  # aviation units
    specs_df = pd.DataFrame.from_dict(specs, orient='index').transpose()
    st.table(specs_df)  # Display DataFrame as a table

def main():

    st.title("Aerodynamics of the Pipistrel")

    # Aircraft Specifications
    st.header("Aircraft Specifications")
    unit_system = st.radio("Select Unit System", ('SI Units', 'Aviation Units'))
    display_specs(aircraft_specs, units=unit_system)

    # Airframe choice
    st.header("Airframe choice")
    st.markdown("""
    Za izbor aeroprofila potrebni su sledeći ulazni podaci:
    - Proizvodna površina krila
    - Maksimalna masa na poletanju
    - Karakteristike vazduha
    - Brzina krstarenja
    """)

    st.subheader("ISA Atmosphere")
    col1, col2 = st.columns(2)

    with col1:
        st.latex(r"\rho = 0.736116 \, \text{kg/m}^3")
        st.latex(r"P = 101325 \, \text{Pa}")
        st.latex(r"T = 288.15 \, \text{K}")
        st.latex(r"c = 340.29 \, \text{m/s}")

    with col2:
        st.code("""
        # Temperature
        T = 288.15  # K
        Pressure
        P = 101325  # Pa
        # Density
        rho = 0.736116  # kg/m^3
        c = 340.29  # Speed of Sound (m/s)
        """, language='python')    

    st.subheader("Cruise Speed Calculation")

    col1, col2 = st.columns(2)

    with col1:
        st.latex(r"v_{krst} = 7.0 \cdot c = 320.529 \cdot 7.0 = 224.37 \, \text{m/s} = 807.73 \, \text{km/h}")

    with col2:
        cruise_speed_code = inspect.getsource(calculate_cruise_speed)
        st.code(cruise_speed_code, language='python')

    
if __name__ == "__main__":
    main()
