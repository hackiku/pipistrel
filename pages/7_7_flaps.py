import json
import streamlit as st

VARIABLES_JSON_PATH = 'variables.json'

def load_variables():
    with open(VARIABLES_JSON_PATH, 'r') as file:
        return json.load(file)

def save_variables(variables_data):
    with open(VARIABLES_JSON_PATH, 'w') as file:
        json.dump(variables_data, file, indent=4)

def reset_values_to_defaults(variables_data):
    for var in variables_data.values():
        var['value'] = var['default']

def main():
    st.title("7. Flaps Lift Calculation")
    
    if 'initialized' not in st.session_state:
        variables_data = load_variables()
        reset_values_to_defaults(variables_data)
        save_variables(variables_data)
        st.session_state['initialized'] = True
    else:
        variables_data = load_variables()
    
    variables_data = load_variables()

    # User inputs to update variables
    S = st.number_input("Wing Area", value=variables_data['S']['value'], key='S')
    S_f = st.number_input("Flaps Wing Area", value=variables_data['S_f']['value'], key='S_f')

    # Calculate S_f_relative and display
    S_f_relative = S_f / S if S != 0 else 0  # Avoid division by zero
    st.latex(f"S_{{f_{{rel}}}} = \\frac{{S_f}}{{S}} = \\frac{{{S_f:.3f}}}{{{S:.3f}}} = {S_f_relative:.3f}")

    # Update values in variables_data
    variables_data['S']['value'] = S
    variables_data['S_f']['value'] = S_f

    save_variables(variables_data)

    # Display variables with different value/default (optional)
    variable_details = []
    for var_name, var_details in variables_data.items():
        if var_details['value'] != var_details['default']:
            variable_details.append(f"Variable name: {var_details['name']}, Value: {var_details['value']}, Default value: {var_details['default']}")

    st.code("\n".join(variable_details))

if __name__ == "__main__":
    main()
