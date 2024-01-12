import json
import streamlit as st

VARIABLES_JSON_PATH = 'variables.json'

def load_variables():
    with open(VARIABLES_JSON_PATH, 'r') as file:
        return json.load(file)

def save_variables(variables_data):
    with open(VARIABLES_JSON_PATH, 'w') as file:
        json.dump(variables_data, file, indent=4)

def initialize_session_state():
    if 'initialized' not in st.session_state:
        variables_data = load_variables()
        for var in variables_data.values():
            var['value'] = var['default']
        save_variables(variables_data)
        st.session_state['variables_data'] = variables_data
        st.session_state['initialized'] = True
    else:
        st.session_state['variables_data'] = load_variables()

def update_variable(var_name, new_value):
    if var_name in st.session_state['variables_data']:
        st.session_state['variables_data'][var_name]['value'] = new_value
        save_variables(st.session_state['variables_data'])

def get_variable_value(var_name):
    return st.session_state['variables_data'].get(var_name, {}).get('value', None)

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
