### 2_airfoil.py ###

import streamlit as st
import pandas as pd
import re
from data import airfoil_data
from variables_manager import initialize_session_state, get_variable_value,\
     update_variables, log_changed_variables, get_variable_props, display_variable
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


# Example usage:
# airfoil_df = calculate_aerodynamic_parameters(airfoil_df)

# ====================================================== #
# ======================== MAIN ======================== #
# ====================================================== #

def main():
    st.title("Airfoil Selection Tool")
    
    page_values = [
        'c_z_krst'
    ]
    
    initialize_session_state(page_values)

    # crate dataframe
    airfoil_df = pd.DataFrame(airfoil_data, columns=[
        "Name", "M_Re", "alpha_n", "a0", "Cz_max", "letter", "alpha_kr", 
        "Cz_op", "alpha_d", "Cd_min", "Cm_ac", "x_ac", "y_ac"
    ])
    
    airfoil_df['Thickness'] = airfoil_df['Name'].apply(extract_airfoil_specs)
    
    # button to display all airfoils
    if st.button("Show All Airfoils"):
        st.markdown("### All Airfoils")
        st.write("All airfoils:", airfoil_df)

    # ------------------ 1 ------------------ #
    emoji_header("1️⃣", "Thickness Ratio", "")
    thickness_ratio = st.select_slider("Choose Thickness Ratio", options=["15:12", "12:10", "12:09", "09:06"])
    root_thickness, tip_thickness = (float(value) / 100 for value in thickness_ratio.split(':'))

    # ------------------ 2 ------------------ #
    emoji_header("2️⃣", "Optimal lift coefficient", "")
    st.write("Optimal lift coefficient closest to the one at cruise.")
    spacer()
    
    current_value, default_value, _, _ = get_variable_props('c_z_krst')
    
    col1, col2, col3 = st.columns([1,3,3])
    with col1:
        spacer('2em')

        if st.button("⏪ Reset", key="reset_cz_krst"):
            current_value = default_value
    with col2:
        c_z_krst = st.number_input(
            "Lift coefficient at cruise",
            value=current_value,
            key="c_z_krst",
            format="%.3f"
        )
    with col3:
        spacer('1em')
        if c_z_krst != default_value:
            st.warning(f"Value updated from default {default_value:.5f}")
    
    st.code(c_z_krst, "Current Value")
    st.code(default_value, "Default Value")

    st.latex(f"C_{{Z_{{opt}}}} \\approx C_{{Z_{{krst}}}} \\approx {c_z_krst:.3f}")
    airfoil_df['Cz_Diff'] = abs(airfoil_df['Cz_op'] - c_z_krst)
       
    spacer()
   
    emoji_header("3️⃣", "Drag coefficient", r"C_{x_{min}}")
    st.write("Selecting airfoil by lowest drag coefficient.")
    drag_importance = st.slider("Select the importance of minimal drag coefficient (0 - not important, 1 - very important)", 0.0, 1.0, 0.5)

    #==================== PROCESS DATA ====================#
    # Calculate a combined score based on the closeness to the cruise lift coefficient and the drag coefficient
    airfoil_df['Combined_Score'] = airfoil_df['Cz_Diff'] * (1 - drag_importance) + airfoil_df['Cd_min'] * drag_importance

    # Sort the airfoils by the combined score
    root_airfoils = airfoil_df[airfoil_df['Thickness'] == root_thickness].nsmallest(7, 'Combined_Score')
    tip_airfoils = airfoil_df[airfoil_df['Thickness'] == tip_thickness].nsmallest(7, 'Combined_Score')

    # Display tables
    st.markdown("***")
    st.markdown("### Top 5 Root Airfoils")
    # display_airfoil_table(root_airfoils)
    st.write("Root airfoils:", root_airfoils)

    st.markdown("### Top 5 Tip Airfoils")
    st.write("Tip airfoils:", tip_airfoils)


    # ===================== INDIVIDUAL AIRFOILS OPS ===================== #

    st.subheader("Individual Airfoils")
    # avoid division by zero
    airfoil_df['Cx'] = airfoil_df['Cx'].replace(0, 1e-8)
    
    cz = airfoil_df['Cz']
    cz_cx_max = 0.0 # max finesse
    
    root_airfoils['Cz/Cx'] = root_airfoils['Cz'] / root_airfoils['Cx']
    
    def calculate_aerodynamic_parameters(df):
        # Avoid division by zero
        df['Cx'] = df['Cx'].replace(0, 1e-8)
        
        # Calculate the required aerodynamic parameters
        
        df['Cz^3/Cx^2'] = (df['Cz'] ** 3) / (df['Cx'] ** 2)
        df['sqrt(Cz/Cx)'] = (df['Cz'] / df['Cx']) ** 0.5
        
        # Format the calculated values as LaTeX f-strings
        df['Cz/Cx_latex'] = df['Cz/Cx'].apply(lambda x: f"${x:.2f}$")
        df['Cz^3/Cx^2_latex'] = df['Cz^3/Cx^2'].apply(lambda x: f"${x:.2f}$")
        df['sqrt(Cz/Cx)_latex'] = df['sqrt(Cz/Cx)'].apply(lambda x: f"${x:.2f}$")
        
        return df


    # ===================== UPDATE SESSION STATE ===================== #
    # final command to update and debug session state as json
    update_variables(page_values, locals())
    log_changed_variables()

# App Execution
if __name__ == "__main__":
    main()
