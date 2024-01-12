### 2_airfoil.py ###

import streamlit as st
import pandas as pd
import re
from data import airfoil_data
from variables_manager import initialize_session_state, get_variable_value, update_variables, log_changed_variables
from utils import spacer, emoji_header

# data preparation
def extract_airfoil_specs(naca_name):
    # Regex to capture the thickness pattern after 'NACA'
    thickness_match = re.search(r'NACA.*?-\d(\d{2})', naca_name)
    if thickness_match:
        thickness = int(thickness_match.group(1)) / 100
        return thickness
    else:
        return None

# show table
def display_airfoil_table(df):
    st.write(df.to_html(escape=False), unsafe_allow_html=True)

# ======================== main ======================== #
def main():
    st.title("Airfoil Selection Tool")
    
    initialize_session_state()

    page_values = [
        'c_z_krst'
    ]
    
    
    c_z_krst = st.number_input("Lift coefficient at cruise", value=get_variable_value('c_z_krst'), key='c_z_krst')

    # load and preprocess data
    airfoil_df = pd.DataFrame(airfoil_data, columns=[
        "Name", "M_Re", "alpha_n", "a0", "Cz_max", "letter", "alpha_kr", 
        "Cz_op", "alpha_d", "Cd_min", "Cm_ac", "x_ac", "y_ac"
    ])
    airfoil_df['Thickness'] = airfoil_df['Name'].apply(extract_airfoil_specs)

    # button to display all airfoils
    if st.button("Display Airfoil Table"):
        st.markdown("### All Airfoils")
        st.write("All airfoils:", airfoil_df)

    # User interactions
    emoji_header("1️⃣", "Thickness Ratio", "")
    thickness_ratio = st.select_slider("Choose Thickness Ratio", options=["15:12", "12:10", "12:09", "09:06"])
    root_thickness, tip_thickness = (float(value) / 100 for value in thickness_ratio.split(':'))

    spacer()

    emoji_header("2️⃣", "Lift coefficient", r"C_{Z_{opt}} \approx C_{Z_{krst}}")
    st.write("Selecting the airfoil's optimal lift coefficient by similarity to the one at cruise.")
    # st.latex(r"C_{Z_{opt}} \approx C_{Z_{krst}}")
    airfoil_df['Cz_Diff'] = abs(airfoil_df['Cz_op'] - c_z_krst)
    
    spacer()
   
    emoji_header("3️⃣", "Drag coefficient", r"C_{x_{min}}")
    st.write("Selecting airfoil by lowest drag coefficient.")
    drag_importance = st.slider("Select the importance of minimal drag coefficient (0 - not important, 1 - very important)", 0.0, 1.0, 0.5)

    #==================== PROCESS DATA ====================#
    # Calculate a combined score based on the closeness to the cruise lift coefficient and the drag coefficient
    airfoil_df['Combined_Score'] = airfoil_df['Cz_Diff'] * (1 - drag_importance) + airfoil_df['Cd_min'] * drag_importance

    # Sort the airfoils by the combined score
    root_airfoils = airfoil_df[airfoil_df['Thickness'] == root_thickness].nsmallest(5, 'Combined_Score')
    tip_airfoils = airfoil_df[airfoil_df['Thickness'] == tip_thickness].nsmallest(5, 'Combined_Score')

    # Display tables
    st.markdown("***")
    st.markdown("### Top 5 Root Airfoils")
    # display_airfoil_table(root_airfoils)
    st.write("Root airfoils:", root_airfoils)

    st.markdown("### Top 5 Tip Airfoils")
    st.write("Tip airfoils:", tip_airfoils)

    # debug
    log_changed_variables()

# App Execution
if __name__ == "__main__":
    main()
