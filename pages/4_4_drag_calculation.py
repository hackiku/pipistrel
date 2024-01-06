# 4_drag_calculation.py

import streamlit as st
from data import Variable, save_variables_to_session, load_variables_from_session
from main import c_z_krst as c_z_krst_home, v_krst as v_krst_home, S as S_home, b as b_home


def main():
    # Attempt to load variables from session state
    loaded_variables = load_variables_from_session(['c_z_krst', 'b', 'S'])

    # Use values from session state if available; otherwise, use default values
    c_z_krst = loaded_variables.get('c_z_krst', c_z_krst_home)
    b = loaded_variables.get('b', b_home)
    S = loaded_variables.get('S', S_home)
    
    # Show the values after attempting to load from session state
    st.code(f"czkrst state = {c_z_krst.value}")
    st.code(f"b state = {b.value}")
    st.code(f"S state = {S.value}")

    # Calculate the wing aspect ratio
    lambda_wing = Variable("Wing Aspect Ratio", b.value**2 / S.value, r"\lambda")
    
    # Display the variables and the calculated aspect ratio
    st.write(f"Wingspan (b): {b.value} m")
    st.write(f"Wing Area (S): {S.value} m²")
    st.write(f"Wing Aspect Ratio (λ): {lambda_wing.value}")

    #==================== SESSION STATE ====================#
    st.markdown('***')
    st.text("Variables saved to session state:")
    variables_dict = {
        'c_z_krst': c_z_krst,
        'b': b,
        'S': S,
        'lambda_wing': lambda_wing,
    }
    
    # Update session state with the new values
    save_variables_to_session(variables_dict)

# Run the main function if this script is executed
if __name__ == "__main__":
    main()
