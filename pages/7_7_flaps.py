import json
import streamlit as st

VARIABLES_JSON_PATH = 'variables.json'
page_variables = ['S', 'S_f', 'S_f_relative']

def load_variables():
    with open(VARIABLES_JSON_PATH, 'r') as file:
        return json.load(file)

variables_data = load_variables()

def update_session_state():
    for var in page_variables:
        user_value = st.session_state.get(var, variables_data[var]['default'])
        variables_data[var]['value'] = user_value
        st.session_state[var] = user_value

def save_variables():
    with open(VARIABLES_JSON_PATH, 'w') as file:
        json.dump(variables_data, file, indent=4)

def main():
    st.title("7. Flaps Lift Calculation")
    
    # Update session state with the latest values
    update_session_state()

    # for var in page_variables:
        # st.number_input(variables_data[var]['name'], value=st.session_state[var], key=var)
    
    S = st.number_input(variables_data['S']['name'], value=st.session_state['S'], key='S')
    S_f = st.number_input(variables_data['S_f']['name'], value=st.session_state['S_f'], key='S_f')
    
    S_f_relative = S_f / S
    st.latex(f"S_{{f_{{rel}}}} = \\frac{{S_f}}{{S}} = \\frac{{{S_f:.3f}}}{{{S:.3f}}} = {S_f_relative:.3f}")
    
    save_variables()

if __name__ == "__main__":
    main()
