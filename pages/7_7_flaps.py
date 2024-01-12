### 7_flaps.py

import streamlit as st
from variables_manager import initialize_session_state, get_variable_value, update_variables, log_changed_variables

def main():
    st.title("7. Flaps Lift Calculation")
    
    initialize_session_state()

    page_values = [
        'S', 
        'S_f', 
        'S_f_relative'
    ]
    # User inputs
    S = st.number_input("Wing Area", value=get_variable_value('S'), key='S')
    S_f = st.number_input("Flaps Wing Area", value=get_variable_value('S_f'), key='S_f')

    # Calculate S_f_relative
    S_f_relative = S_f / S if S != 0 else 0
    st.latex(f"S_{{f_{{rel}}}} = \\frac{{S_f}}{{S}} = \\frac{{{S_f:.3f}}}{{{S:.3f}}} = {S_f_relative:.3f}")

    # Update all relevant values in session state and JSON at once
    variable_updates = {'S': S, 'S_f': S_f, 'S_f_relative': S_f_relative}
    update_variables({k: v for k, v in variable_updates.items() if k in page_values})

    # Log the changes in variables
    log_changed_variables()

if __name__ == "__main__":
    main()
