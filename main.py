# main_streamlit_app.py
import streamlit as st
import pandas as pd
from virus_model_streamlit.virus_viewer_component import virus_viewer
from calcs import convert_units, aircraft_specs

# specs table
def display_specs(specs, units="SI"):
    if units == "Aviation":
        specs = convert_units(specs) # aviation units
    specs_df = pd.DataFrame.from_dict(specs, orient='index').transpose()
    st.table(specs_df)  # Display DataFrame as a table

def main():

    st.title("Aerodynamics of the Pipistrel")

    st.header("3D Model Viewer")
    virus_viewer()  # This will display your React component

    st.header("Aircraft Specifications")
    unit_system = st.radio("Select Unit System", ('SI Units', 'Aviation Units'))
    display_specs(aircraft_specs, units=unit_system)  # Display specs based on unit system

    st.header("Airframe choice")
    st.write("Choosing the airframe & airfoil.")

    st.subheader("Computational area")
    st.latex("formula")

if __name__ == "__main__":
    main()