# data.py
import streamlit as st
import pandas as pd

class Variable:
    def __init__(self, name, value, latex='', unit='', value2=None, unit2='', formula=''):
        self.name = name
        self.value = value
        self.latex = latex or name  # Fallback to name if no latex is provided
        self.unit = unit
        self.value2 = value2
        self.unit2 = unit2
        self.formula = formula
    
    def save_to_session(self):
        st.session_state[self.latex] = self


def save_variables_to_session(variables_dict):
    for var_name, var_value in variables_dict.items():
        if isinstance(var_value, Variable):
            st.session_state[var_value.latex] = var_value
            st.code(f"{var_value.latex} = {var_value.value} {var_value.unit} # {var_value.name}")
    
def load_variables_from_session(variable_names):
    loaded_variables = {}
    for name in variable_names:
        variable = st.session_state.get(name)
        if variable:
            loaded_variables[name] = variable
            # Display the variable for debugging
            st.code(f"{name}: {variable.value} {variable.unit} #### {variable.name}")
    return loaded_variables

# grab specs from data.py
def create_specs_table(aircraft_specs):
    specs_data = []
    for category, data in aircraft_specs.items():
        # Add a category header as a separate entry
        specs_data.append({
            "Specification": f"**{category}**",
            "Value": "", 
            "Unit": "", 
            "LaTeX": ""
        })
        # Add individual specs
        for spec, details in data.items():
            specs_data.append({
                "Specification": spec, 
                "Value": details.get('value', ''), 
                "Unit": details.get('unit', ''),   
                "LaTeX": details.get('latex', '')  
            })
    
    df = pd.DataFrame(specs_data)
    return df

airfoil_data = [
    # first pass not fully checked
    ["NACA 63-006", 9.0, 0.0, 0.110, 0.87, "D", 10.0, 0.00, 7.7, 0.0042, 0.000, 0.258, -0.033],
    ["NACA 63-009", 9.0, 0.0, 0.110, 1.15, "D", 11.0, 0.00, 10.0, 0.0041, 0.000, 0.258, 0.016],
    ["NACA 63_1-012", 9.0, 0.0, 0.114, 1.45, "D", 14.0, 0.00, 12.8, 0.0043, 0.000, 0.265, -0.030],
    ["NACA 63_2-015", 9.0, 0.0, 0.118, 1.50, "D", 15.0, 0.00, 10.5, 0.0049, 0.000, 0.271, -0.034],
    ["NACA 63_3-018", 9.0, 0.0, 0.118, 1.52, "D", 15.0, 0.00, 11.0, 0.0049, 0.000, 0.271, -0.020],
    ["NACA 63_4-021", 9.0, 0.0, 0.115, 1.39, "D", 17.0, 0.00, 10.5, 0.0052, 0.000, 0.273, -0.001],
    ["NACA 63A-010", 9.0, 0.0, 0.105, 1.19, "B", 13.0, 0.00, 10.0, 0.0046, 0.005, 0.254, -0.003],
    ["NACA 63-206", 9.0, -2.0, 0.105, 1.08, "D", 10.5, 0.25, 6.0, 0.0040, -0.039, 0.254, -0.011],
    ["NACA 63-209", 9.0, -1.2, 0.110, 1.41, "D", 12.0, 0.20, 10.8, 0.0048, -0.031, 0.262, -0.032],
    ["NACA 63-210", 9.0, -1.2, 0.110, 1.56, "D", 14.5, 0.20, 9.6, 0.0045, -0.033, 0.261, -0.033],
    ["NACA 63_2-212", 9.0, -2.0, 0.110, 1.62, "D", 14.5, 0.25, 11.4, 0.0045, -0.034, 0.263, -0.029],
    ["NACA 63_2-215", 9.0, -1.2, 0.120, 1.61, "D", 15.0, 0.20, 11.0, 0.0046, -0.031, 0.267, -0.020],
    ["NACA 63_2-218", 9.0, -1.2, 0.120, 1.50, "D", 16.0, 0.20, 11.0, 0.0049, -0.032, 0.271, -0.042],
    ["NACA 63-221", 9.0, -1.3, 0.110, 1.46, "D", 15.0, 0.20, 11.0, 0.0053, -0.030, 0.269, -0.033],
    ["NACA 63_4-412", 9.0, -3.0, 0.100, 1.78, "D", 15.0, 0.32, 9.6, 0.0045, -0.075, 0.270, -0.073],
    ["NACA 63_4-415", 9.0, -3.0, 0.115, 1.67, "D", 15.0, 0.35, 10.0, 0.0049, -0.071, 0.262, -0.036],
    ["NACA 63_4-418", 9.0, -2.6, 0.118, 1.58, "D", 16.0, 0.22, 8.5, 0.0050, -0.071, 0.272, -0.051],
    ["NACA 63_4-420", 9.0, -2.1, 0.110, 1.42, "D", 15.0, 0.05, 9.0, 0.0055, -0.060, 0.265, -0.054],
    ["NACA 63_4-420, a=0.3", 9.0, -2.5, 0.108, 1.35, "D", 16.0, 0.45, 8.0, 0.0058, -0.036, 0.265, 0.000],
    ["NACA 63_4-421", 9.0, -2.7, 0.120, 1.48, "D", 16.0, 0.28, 8.0, 0.0054, -0.063, 0.275, -0.027],
    ["NACA 63_(420)-422", 9.0, -3.1, 0.110, 1.40, "D", 20.0, 0.12, 8.0, 0.0060, -0.064, 0.271, -0.043],
    ["NACA 63_(420)-517", 9.0, -3.0, 0.110, 1.61, "D", 16.0, 0.35, 9.0, 0.0057, -0.085, 0.264, -0.059],
    # page 79 (checked I think)
    ["NACA 63_2-615", 9.0, -3.8, 0.120, 1.67, "D", 15.0, 0.42, 10.0, 0.0048, -0.110, 0.266, -0.040],
    ["NACA 63_3-618", 9.0, -3.8, 0.118, 1.58, "D", 16.0, 0.45, 8.0, 0.0052, -0.098, 0.267, -0.016],
    ["NACA 64-006", 9.0, 0.0, 0.110, 0.80, "D", 9.0, 0.00, 7.8, 0.0040, 0.000, 0.256, -0.014],
    ["NACA 64-009", 9.0, 0.0, 0.110, 1.17, "D", 11.0, 0.00, 10.0, 0.0040, 0.000, 0.262, -0.027],
    ["NACA 64A-010", 9.0, 0.0, 0.110, 1.23, "D", 12.0, 0.00, 11.0, 0.0042, 0.000, 0.253, -0.017],
    ["NACA 64_1-012", 9.0, 0.0, 0.110, 1.45, "B", 15.0, 0.00, 12.5, 0.0042, 0.000, 0.262, -0.002],
    ["NACA 64_2-015", 9.0, 0.0, 0.111, 1.48, "D", 15.0, 0.00, 13.0, 0.0045, 0.000, 0.267, -0.007],
    ["NACA 64_3-018", 9.0, 0.0, 0.111, 1.50, "D", 17.0, 0.00, 12.5, 0.0045, 0.000, 0.266, -0.044],
    ["NACA 64-108", 9.0, -0.4, 0.110, 1.10, "D", 10.0, 0.00, 9.5, 0.0040, -0.021, 0.255, 0.029],
    ["NACA 64-110", 9.0, -1.0, 0.110, 1.40, "B", 13.0, 0.10, 12.0, 0.0042, -0.021, 0.261, -0.022],
    ["NACA 64_1-112", 9.0, -1.0, 0.115, 1.50, "D", 14.0, 0.15, 12.5, 0.0042, -0.020, 0.267, -0.039],
    ["NACA 64-206", 9.0, -1.0, 0.115, 1.03, "D", 12.0, 0.18, 9.0, 0.0040, -0.041, 0.253, -0.020],
    ["NACA 64-208", 9.0, -1.0, 0.112, 1.50, "D", 10.0, 0.22, 9.0, 0.0041, -0.040, 0.267, -0.007],
    ["NACA 64-209", 9.0, -1.3, 0.110, 1.40, "D", 13.5, 0.20, 12.5, 0.0040, -0.041, 0.261, -0.041],
    ["NACA 64-210", 9.0, -1.7, 0.110, 1.54, "B", 14.0, 0.28, 12.0, 0.0040, -0.041, 0.258, -0.011],
    ["NACA 64A-210", 9.0, -1.5, 0.105, 1.44, "B", 13.0, 0.20, 11.5, 0.0040, -0.040, 0.251, -0.013],
    ["NACA 64_1-212", 9.0, -1.2, 0.110, 1.54, "D", 15.0, 0.15, 12.5, 0.0041, -0.028, 0.262, -0.024],
    ["NACA 64_1A-212", 9.0, -1.9, 0.103, 1.53, "B", 14.0, 0.25, None, 0.0045, -0.040, 0.252, -0.021],
    ["NACA 64_2-215", 9.0, -1.3, 0.110, 1.58, "D", 15.0, 0.12, 12, 0.0045, -0.032, 0.265, -0.014],
    ["NACA 64_2-A-215", 9.0, -2.5, 0.112, 1.49, "D", 15.0, 0.35, None, 0.0045, -0.070, 0.260, -0.025],
    ["NACA 64_3-218", 9.0, -1.2, 0.114, 1.53, "D", 18.0, 0.20, 12.0, 0.0047, -0.030, 0.271, -0.053],
    ["NACA 64A-410", 9.0, -3.0, 0.108, 1.61, "B", 15.0, 0.45, 12.5, 0.0044, -0.050, 0.254, -0.033],
    ["NACA 64_1-412", 9.0, -2.8, 0.112, 1.68, "C", 15.0, 0.30, 12.0, 0.0042, -0.073, 0.267, -0.034],
    ["NACA 64_2-415", 9.0, -2.9, 0.112, 1.64, "D", 16.0, 0.35, 10.0, 0.0047, -0.070, 0.264, 0.040],
    ["NACA 64_3-418", 9.0, -3.0, 0.117, 1.58, "D", 20.0, 0.23, 10.0, 0.0050, -0.064, 0.273, -0.049],
    ["NACA 64_4-421", 9.0, -2.5, 0.115, 1.53, "D", 24.0, 0.40, 9.5, 0.0052, -0.065, 0.276, -0.047],
    ["NACA 65-006", 9.0, 0.0, 0.105, 1.00, "D", 10.0, 0.00, 8.0, 0.0035, 0.000, 0.258, -0.033],
    ["NACA 65-009", 9.0, 0.0, 0.110, 1.09, "D", 11.0, 0.00, 10.0, 0.0038, 0.000, 0.259, -0.034],
    ["NACA 65_1-012", 9.0, 0.0, 0.105, 1.37, "D", 14.0, 0.00, 12.0, 0.0040, 0.000, 0.261, -0.012],
    ["NACA 65_2-015", 9.0, 0.0, 0.110, 1.42, "D", 15.0, 0.00, 12.0, 0.0040, 0.000, 0.257, -0.014],
    # page 80
    ["NACA 65_3-018", 9.0, 0.0, 0.105, 1.38, "D", 16.0, 0.00, 12.0, 0.0042, 0.000, 0.267, -0.013],
    ["NACA 65_4-021", 9.0, 0.0, 0.115, 1.40, "D", 19.0, 0.00, 12.0, 0.0045, 0.000, 0.267, -0.025],
    ["NACA 65_(215)-114", 9.0, -0.7, 0.110, 1.43, "D", 16.0, 0.10, 12.0, 0.0040, -0.022, 0.265, -0.027],
    ["NACA 65-206", 9.0, -1.5, 0.102, 1.06, "D", 14.0, 0.18, 8.0, 0.0038, -0.032, 0.257, -0.045],
    ["NACA 65-209", 9.0, -1.2, 0.110, 1.30, "B", 11.5, 0.20, 11.0, 0.0039, -0.032, 0.259, -0.004],
    ["NACA 65-210", 9.0, -1.5, 0.110, 1.40, "B", 15.0, 0.20, 11.5, 0.0037, -0.034, 0.262, -0.020],
    ["NACA 65_1-212", 9.0, -1.0, 0.110, 1.46, "D", 14.0, 0.25, 12.0, 0.0038, -0.033, 0.261, -0.026],
    ["NACA 65_1-212, a=0.6", 9.0, -1.5, 0.108, 1.50, "D", 14.0, 0.25, 12.0, 0.0038, -0.030, 0.269, -0.019],
    ["NACA 65_2-215", 9.0, -1.2, 0.112, 1.51, "D", 16.0, 0.25, 12.0, 0.0040, -0.032, 0.269, -0.033],
    ["NACA 65_3-218", 9.0, -1.2, 0.102, 1.50, "D", 18.0, 0.25, 12.0, 0.0042, -0.029, 0.263, -0.027],
    ["NACA 65_4-221", 9.0, -1.2, 0.110, 1.47, "C", 21.0, 0.28, 10.0, 0.0045, -0.030, 0.274, -0.050],
    ["NACA 65-410", 9.0, -2.5, 0.110, 1.52, "C", 14.0, 0.35, 12.0, 0.0037, -0.066, 0.262, -0.035],
    ["NACA 65_1-412", 9.0, -3.0, 0.110, 1.65, "C", 16.0, 0.38, 12.0, 0.0039, -0.072, 0.265, -0.038],
    ["NACA 65_2-415", 9.0, -2.8, 0.113, 1.62, "D", 16.5, 0.30, 11.5, 0.0040, -0.062, 0.266, -0.062],
    ["NACA 65_2-415, a=0.5", 9.0, -2.5, 0.112, 1.60, "D", 20.0, 0.40, 12.0, 0.0041, -0.056, 0.264, -0.032],
    ["NACA 65_(216)-415", 9.0, -2.8, 0.114, 1.56, "D", None, 0.40, None, 0.0044, -0.057, 0.266, -0.020],
    ["NACA 65_3-418", 9.0, -2.5, 0.110, 1.55, "D", 18.0, 0.35, 8.0, 0.0044, -0.061, 0.265, -0.060],
    ["NACA 65_3-418, a=0.5", 9.0, -3.0, 0.100, 1.50, "D", 20.0, 0.35, 8.0, 0.0044, -0.056, 0.267, -0.047],
    ["NACA 65_(421)-420", 9.0, -2.5, 0.116, 1.52, "D", 20.0, 0.26, 8.0, 0.0045, -0.063, 0.276, -0.046],
    ["NACA 65_4-421, a=0.5", 9.0, -2.8, 0.110, 1.43, "D", 20.0, 0.30, 8.0, 0.0047, -0.055, 0.272, -0.004],
    ["NACA 65_3-618", 9.0, -4.0, 0.115, 1.66, "D", 21.0, 0.50, 8.0, 0.0042, -0.104, 0.276, -0.022],
    ["NACA 65_3-618, a=0.5", 9.0, -4.2, 0.105, 1.50, "D", 22.0, 0.42, 10.0, 0.0048, -0.079, 0.265, -0.026],
    ["NACA 65_3-618", 9.0, -3.8, 0.116, 1.61, "D", 20.0, 0.57, 8.0, 0.0043, -0.100, 0.273, -0.093],
    ["NACA 66-006", 9.0, 0.0, 0.100, 0.80, "D", 10.0, 0.00, 8.0, 0.0032, 0.000, 0.252, 0.000],
    ["NACA 66-009", 9.0, 0.0, 0.107, 1.10, "C", 11.0, 0.00, 10.0, 0.0031, 0.000, 0.259, -0.025],
    ["NACA 66-012", 9.0, 0.0, 0.105, 1.24, "C", 14.0, 0.00, 11.0, 0.0032, 0.000, 0.258, 0.000],
    ["NACA 66_2-015", 9.0, 0.0, 0.102, 1.36, "C", 16.5, 0.00, 12.0, 0.0034, 0.000, 0.265, -0.005],
    ["NACA 66(215)-016", 9.0, 0.0, 0.102, 1.36, "C", 15.0, 0.26, 0.0, 0.0032, 0.000, 0.260, -0.022],
    ["NACA 66_3-018", 9.0, 0.0, 0.102, 1.33, "D", 17.0, 0.00, 12.0, 0.0034, 0.000, 0.264, -0.027],
    ["NACA 66-206", 9.0, -1.5, 0.110, 1.00, "D", 11.0, 0.17, 8.0, 0.0030, -0.039, 0.257, -0.017],
    # page 81
    ["NACA 66-209", 9.0, -1.0, 0.110, 1.18, "D", 11.5, 0.17, 9.0, 0.0030, -0.033, 0.257, -0.013],
    ["NACA 66-210", 9.0, -1.2, 0.108, 1.28, "D", 11.5, 0.20, 10.0, 0.0030, -0.033, 0.261, -0.018],
    ["NACA 66_1-212", 9.0, -1.4, 0.108, 1.46, "D", 15.0, 0.15, 12.0, 0.0032, -0.032, 0.259, -0.015],
    ["NACA 66,1-212", 9.0, -1.2, 0.100, 1.37, "D", 14.0, 0.20, 11.5, 0.0032, -0.039, 0.259, -0.031],
    ["NACA 66_2-215", 9.0, -1.2, 0.100, 1.50, "D", 16.0, 0.27, 13.0, 0.0032, -0.030, 0.260, -0.020],

    ["NACA 66(215)-216", 9.0, -2.0, 0.102, 1.52, "C", 16.0, 0.10, 13.5, 0.0034, -0.045, 0.262, -0.076],
    ["NACA 66(215)-216, a=0.6", 9.0, -1.2, 0.104, 1.48, "C", 16.5, 0.17, 14.0, 0.0034, -0.030, 0.257, -0.043],
    ["NACA 66_3-218", 9.0, -1.5, 0.100, 1.49, "D", 17.0, 0.05, 12.0, 0.0033, -0.035, 0.260, -0.064],
    ["NACA 66_2-415", 9.0, -2.5, 0.104, 1.60, "D", 18.0, 0.35, 12.0, 0.0036, -0.072, 0.260, -0.073],
    ["NACA 66(215)-416", 9.0, -2.6, 0.112, 1.60, "D", 18.0, 0.30, 13.5, 0.0036, -0.070, 0.265, -0.105],
    ["NACA 66_3-418", 9.0, -2.8, 0.106, 1.57, "D", 18.5, 0.35, 14.0, 0.0037, -0.070, 0.262, -0.090],
]


aircraft_specs = {
    "Model": {
        "Name": {"value": "VIRUS SW 121A – EXPLORER", "description": "Model name of the aircraft"},
        "Engine": {"value": "Rotax 912 S3", "description": "Type of engine used in the aircraft"},
        "Max Power": {
            "value": 73.5, "unit": "kW", 
            "value_alt": 100, "unit_alt": "hp", 
            "description": "Maximum power of the engine"
        },
        # ... other model data
    },
    "Dimensions": {
        "Length": {
            "value": 6.42, "unit": "m", 
            "value_alt": 21.06, "unit_alt": "ft", 
            "description": "Total length of the aircraft"
        },
        "Wingspan": {
            "value": 10.70, "unit": "m", 
            "value_alt": 35.10, "unit_alt": "ft", 
            "description": "Distance from one wingtip to the other"
        },
        "Height": {
            "value": 1.90, "unit": "m", 
            "value_alt": 6.23, "unit_alt": "ft", 
            "description": "Height of the aircraft"
        },
        "Wing Area": {
            "value": 9.51, "unit": "m²", 
            "value_alt": 102.4, "unit_alt": "ft²", 
            "description": "Total area of the wings"
        },
        "Mean Aerodynamic Chord": {
            "value": 0.898, "unit": "m", 
            "value_alt": 2.95, "unit_alt": "ft", 
            "description": "Average distance from the leading edge to the trailing edge of the wing"
        },
        "Aspect Ratio": {
            "value": 12.04, "unit": "", 
            "description": "Ratio of the wingspan to the mean chord"
        },
        # ... other dimensions
    },
    "Weights": {
        "Design Empty Weight": {
            "value": 371, "unit": "kg", 
            "value_alt": 818, "unit_alt": "lb", 
            "description": "Weight of the aircraft without payload or fuel"
        },
        "Max Take Off Weight": {
            "value": 600, "unit": "kg", 
            "value_alt": 1323, "unit_alt": "lb", 
            "description": "Maximum weight for takeoff"
        },
        "Design Useful Load": {
            "value": 229, "unit": "kg", 
            "value_alt": 505, "unit_alt": "lb", 
            "description": "Weight of passengers, cargo, and fuel the aircraft can carry"
        },
        "Max Baggage Weight": {
            "value": 25, "unit": "kg", 
            "value_alt": 55, "unit_alt": "lb", 
            "description": "Maximum weight of baggage"
        },
        # ... other weights
    },
    "Performance": {
        "Never Exceed Speed": {
            "value": 301.9, "unit": "km/h",  
            "value_alt": 163, "unit_alt": "KTAS",
            "description": "Maximum speed the aircraft should not exceed",
            "latex": "V_{ne}"
        },
        "Max Structural Cruising Speed": {
            "value": 222.2, "unit": "km/h",  
            "value_alt": 120, "unit_alt": "KIAS",
            "description": "Maximum cruising speed except in smooth air",
            "latex": "V_{no}"
        },
        "Max Operating Manoeuvring Speed": {
            "value": 185.2, "unit": "km/h",  
            "value_alt": 100, "unit_alt": "KIAS",
            "description": "Maximum speed for safe maneuvering",
            "latex": "V_{a}"
        },
        "Max Flaps Extended Speed": {
            "value": 149.7, "unit": "km/h",  
            "value_alt": 81, "unit_alt": "KIAS",
            "description": "Maximum speed with flaps extended",
            "latex": "V_{fe}"
        },
        "Max Airbrakes Extended Speed": {
            "value": 185.2, "unit": "km/h",  
            "value_alt": 100, "unit_alt": "KIAS",
            "description": "Maximum speed with airbrakes extended",
            "latex": "V_{ae}"
        },
        "Stall Speed With Flaps": {
            "value": 87, "unit": "km/h",  
            "value_alt": 47, "unit_alt": "KIAS",
            "description": "Stall speed with flaps extended",
            "latex": "V_{s0}"
        },
        "Stall Speed Without Flaps": {
            "value": 98.2, "unit": "km/h",  
            "value_alt": 53, "unit_alt": "KIAS",
            "description": "Stall speed without flaps",
            "latex": "V_{s}"
        },
        "Best Climb Speed": {
            "value": 144.8, "unit": "km/h",  
            "value_alt": 78, "unit_alt": "KIAS",
            "description": "Optimal speed for maximum climb rate",
            "latex": "V_{y}"
        },
        "Max Climb Rate": {
            "value": 5.33, "unit": "m/s",
            "value_alt": 1050, "unit_alt": "ft/min",
            "description": "Maximum rate at which the aircraft can climb",
            "latex": "R_{climb}"
        },
        "Take Off Distance at SL": {
            "value": 160, "unit": "m",
            "value_alt": 525, "unit_alt": "ft",
            "description": "Distance required for takeoff at sea level",
            "latex": "D_{to, SL}"
        },
        "Maximum Take-Off Altitude": {
            "value": 3048, "unit": "m",
            "value_alt": 10000, "unit_alt": "ft",
            "description": "Maximum altitude for take-off",
            "latex": "H_{max, TO}"
        },
        "Maximum Operating Altitude": {
            "value": 5486, "unit": "m",
            "value_alt": 18000, "unit_alt": "ft",
            "description": "Maximum altitude for aircraft operation",
            "latex": "H_{max, op}"
        },
        "Permitted Fuel": {
            "value": "AVGAS, MOGAS, or car fuel (min RON 95; EN228 Premium or Premium plus with max. 10% Ethanol)",
            "description": "Types of fuel that can be used",
            "latex": "F_{type}"
        },
        "Fuel Consumption at 2000 ft. 75% Power": {
            "value": 18.4, "unit": "l/h",
            "value_alt": 4.86, "unit_alt": "gal/h",
            "description": "Fuel consumption at 2000 feet with 75% power",
            "latex": "FC_{2000ft, 75%}"
        },
        "Endurance at 4000 ft., 65% Power": {
            "value": "5 h 33 min", "unit": "",
            "description": "Endurance time at 4000 feet with 65% power, plus 30 min reserve",
            "latex": "E_{4000ft, 65%}"
        },
        "Range Distance at 4000 ft., 65% Power": {
            "value": 1189, "unit": "km",
            "value_alt": 642, "unit_alt": "nmi",
            "description": "Range distance at 4000 feet with 65% power, plus 30 min reserve",
            "latex": "R_{4000ft, 65%}"
        },
        "Noise Level": {
            "value": 70, "unit": "dB(A)",
            "description": "Noise level as measured by ICAO Annex 16, Chapter 10",
            "latex": "NL_{ICAO}"
        },
        "Flight Load Factor Limits": {
            "value": "+4.0 g / -2.0 g",
            "description": "Operational load factor limits for the aircraft",
            "latex": "LF_{limits}"
        },
        # ... any additional performance data
    },
    # ... other categories
}