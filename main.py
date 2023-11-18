import streamlit as st
import pandas as pd

# Define the aircraft specifications in both unit systems as dictionaries
aircraft_specs_si = {
    "Dimensions": {
        "Length (m)": 13.23,
        "Wingspan (m)": 8.95,
        "Height (m)": 4.55,
        "Wing Area (m²)": 20.6
    },
    "Mass": {
        "Empty (kg)": 6700,
        "Maximum Takeoff (kg)": 13000
    },
    "Propulsion": {
        "Engine": "Rolls-Royce Spey 807 turbofan",
        "Thrust (kN)": 49.1
    },
    "Performance": {
        "Maximum Speed (km/h)": 1053,
        "Cruise Speed (km/h)": 807.73,
        "Climb Rate (m/s)": 52.1,
        "Combat Radius (km)": 889
    }
}

# Conversion factors from SI to aviation units
conversion_factors = {
    "Length (m)": 3.281,  # Meters to feet
    "Wingspan (m)": 3.281,  # Meters to feet
    "Height (m)": 3.281,  # Meters to feet
    "Wing Area (m²)": 10.764,  # Square meters to square feet
    "Empty (kg)": 2.205,  # Kilograms to pounds
    "Maximum Takeoff (kg)": 2.205,  # Kilograms to pounds
    "Thrust (kN)": 0.225,  # Kilonewtons to pounds-force
    "Maximum Speed (km/h)": 0.621,  # Kilometers/hour to miles/hour
    "Cruise Speed (km/h)": 0.621,  # Kilometers/hour to miles/hour
    "Climb Rate (m/s)": 3.281,  # Meters/second to feet/second
    "Combat Radius (km)": 0.621  # Kilometers to miles
}

# Function to convert SI units to aviation units
def convert_to_aviation_units(si_specs, factors):
    aviation_specs = {}
    for category, specs in si_specs.items():
        aviation_specs[category] = {}
        for spec, value in specs.items():
            if spec in factors:
                converted_value = value * factors[spec]
                aviation_specs[category][spec.replace('(m)', '(ft)').replace('(kg)', '(lbs)').replace('(kN)', '(lbf)').replace('(km/h)', '(mph)').replace('(m²)', '(ft²)').replace('(km)', '(mi)')] = round(converted_value, 2)
            else:
                aviation_specs[category][spec] = value
    return aviation_specs

# Convert SI units to aviation units
aircraft_specs_av = convert_to_aviation_units(aircraft_specs_si, conversion_factors)

# Sidebar selector for units
unit_system = st.sidebar.selectbox('Choose the unit system:', ('SI Units', 'Aviation Units'))

# Choose the specification dictionary based on the selected unit system
specs_to_display = aircraft_specs_si if unit_system == 'SI Units' else aircraft_specs_av

# Convert the selected specs dictionary to a pandas DataFrame for nice tabular formatting
specs_df = pd.DataFrame.from_dict({(i, j): specs_to_display[i][j] 
                                   for i in specs_to_display.keys() 
                                   for j in specs_to_display[i].keys()},
                                  orient='index')

# Display the aircraft specifications in a table
st.header("Aeroplane Specifications")
st.table(specs_df)
