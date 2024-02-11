### 7_flaps.py

import streamlit as st
from variables_manager import initialize_session_state, get_variable_value, update_variables, log_changed_variables

def main():
    st.title("7. Flaps Lift Calculation")
    
    page_values = [
        'S', 
        'S_f', 
        'S_f_relative'
    ]
    initialize_session_state(page_values)

    # get user input and update session state
    S = st.number_input("Wing Area", value=get_variable_value('S'), key='S')
    S_f = st.number_input("Flaps Wing Area", value=get_variable_value('S_f'), key='S_f')

    # Calculate S_f_relative
    S_f_relative = S_f / S if S != 0 else 0
    st.latex(f"S_{{f_{{rel}}}} = \\frac{{S_f}}{{S}} = \\frac{{{S_f:.3f}}}{{{S:.3f}}} = {S_f_relative:.3f}")


    # update json (locals auto-added to session state)
    update_variables(page_values, locals())
    log_changed_variables()

if __name__ == "__main__":
    main()
