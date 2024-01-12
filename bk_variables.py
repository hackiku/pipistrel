### variables.py ###

import json
import streamlit as st

# Assuming we have a JSON file 'variables.json' with default values
with open('variables.json', 'r') as file:
    default_values = json.load(file)

def get_page_variables(variable_names):
    page_vars = {}
    for name in variable_names:
        # If the variable exists in the session, use it, otherwise use the default
        page_vars[name] = st.session_state.get(name, default_values[name]['value'])
    return page_vars

def check_state_changed(variable_names, page_vars):
    changed_variables = []
    for name in variable_names:
        if page_vars[name] != default_values[name]['value']:
            changed_variables.append(name)
    return changed_variables

def save_variables_to_session(page_vars):
    for var_name, var_value in page_vars.items():
        st.session_state[var_name] = var_value


class Variable:
    def __init__(self, name, value, python, latex='', unit='', value2=None, unit2='', formula=''):
        self.name = name
        self.value = value
        self.python = python
        self.latex = latex or name  # Fallback to name if no latex is provided
        self.unit = unit
        self.value2 = value2
        self.unit2 = unit2
        self.formula = formula
    
    def save_to_session(self):
        st.session_state[self.latex] = self

# def save_variables_to_session(variables_dict):
#     for var_name, var_value in variables_dict.items():
#         if isinstance(var_value, Variable):
#             st.session_state[var_value.python] = var_value  # Use python attribute for session state key
#             st.code(f"{var_value.python} = {var_value.value} {var_value.unit} # {var_value.name}")
    
# def load_variables_from_session(variable_names):
#     loaded_variables = {}
#     code_display = "" 
#     for name in variable_names:
#         variable = st.session_state.get(name)
#         if variable:
#             loaded_variables[name] = variable
#             code_display += f"{name}: {variable.value} {variable.unit} # {variable.name} \n"
#     return loaded_variables, code_display


# Function to update the session state variable
# def update_session_variable(var_name, default=None):
#     if var_name not in st.session_state or default is not None:
#         st.session_state[var_name] = variables[var_name]["default_value"]
#     return st.session_state[var_name]



# Definitions of variables for different pages could be added here
# e.g., def home_variables(), def wing_variables(), etc.
