# main_streamlit_app.py
import streamlit as st
import pandas as pd
from calcs import convert_units, aircraft_specs

def display_specs(specs, units="SI"):
    """Displays aircraft specifications in a table format."""
    if units == "Aviation":
        specs = convert_units(specs)  # Convert to aviation units if needed
    specs_df = pd.DataFrame.from_dict(specs, orient='index').transpose()  # Transpose DataFrame
    st.table(specs_df)  # Display DataFrame as a table

def main():

    st.title("Aerodynamics of the Pipistrel")
    st.header("Aircraft Specifications")
    unit_system = st.radio("Select Unit System", ('SI Units', 'Aviation Units'))
    display_specs(aircraft_specs, units=unit_system)  # Display specs based on unit system

    st.header("Airframe choice")
    st.write("It's necessary to be an ST in the nowadays.")

    st.subheader("")

if __name__ == "__main__":
    main()
