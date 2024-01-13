### variables_manager.py
import json
import streamlit as st

VARIABLES_JSON_PATH = 'variables.json'

def load_variables():
    with open(VARIABLES_JSON_PATH, 'r') as file:
        return json.load(file)

def save_variables(variables_data):
    with open(VARIABLES_JSON_PATH, 'w') as file:
        json.dump(variables_data, file, indent=4)

def initialize_session_state(page_variables=None):
    if 'initialized' not in st.session_state:
        variables_data = load_variables()
        if page_variables is not None:
            # Initialize only the specified variables
            for var in page_variables:
                if var in variables_data:
                    variables_data[var]['value'] = variables_data[var]['default']
        else:
            # Initialize all variables to their default values
            for var in variables_data.values():
                var['value'] = var['default']
        
        save_variables(variables_data)
        st.session_state['variables_data'] = variables_data
        st.session_state['initialized'] = True
    else:
        st.session_state['variables_data'] = load_variables()

"""
def initialize_session_state_all():
    if 'initialized' not in st.session_state:
        variables_data = load_variables()
        for var in variables_data.values():
            var['value'] = var['default']
        save_variables(variables_data)
        st.session_state['variables_data'] = variables_data
        st.session_state['initialized'] = True
    else:
        st.session_state['variables_data'] = load_variables()
"""

def update_variables(page_values, local_vars):
    variables_data = st.session_state['variables_data']
    for var_name in page_values:
        if var_name in st.session_state:
            # Update from session state if it's a user input variable
            new_value = st.session_state[var_name]
        elif var_name in local_vars:
            # Update from local variables if it's a calculated variable
            new_value = local_vars[var_name]
        else:
            continue  # Skip if variable is neither in session state nor local_vars

        if var_name in variables_data:
            variables_data[var_name]['value'] = new_value

    save_variables(variables_data)

#=================== extract variable data ===================
def get_variable_value(var_name):
    return st.session_state['variables_data'].get(var_name, {}).get('value', None)
# def get_variable_value(*var_names):
#     return tuple(st.session_state['variables_data'].get(var_name, {}).get('value', None) for var_name in var_names)

def get_variable_props(var_key):
    var_data = st.session_state['variables_data'].get(var_key, {})
    return var_data.get('value'), var_data.get('latex'), var_data.get('unit')

def display_variable(var_key, help=None):
    value, latex, unit = get_variable_props(var_key)
    if latex and unit:
        st.latex(rf"{latex} = {value} \, {unit}")
    elif latex:
        st.latex(rf"{latex} = {value}")
    else:
        st.text(f"{var_key}: {value}")

#=================== extract variable data ===================
def log_changed_variables():
    variable_details = ["Changed Variables:"]
    for var_name, var_value in st.session_state['variables_data'].items():
        if var_value['value'] != var_value['default']:
            detail = (f" - {var_value['name']} (Key: '{var_name}'): "
                      f"Current Value = {var_value['value']} | "
                      f"Default Value = {var_value['default']}")
            variable_details.append(detail)
    
    if len(variable_details) > 1:
        st.code("\n".join(variable_details))
    else:
        st.code("No variables have been changed from their default values.")
