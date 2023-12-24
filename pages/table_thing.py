import streamlit as st
import pandas as pd
import re
from data import Variable, airfoil_data

# Global Variables
cz_selector = st.number_input("Cruise Lift Coefficient", value=0.247, step=0.001, format="%.3f")
c_z_krst = Variable("Cruise Lift Coefficient", cz_selector, r"C_{z_{krst}}", "")

# Data Preparation Functions
def extract_airfoil_specs(naca_name):
    thickness_match = re.search(r'NACA.*?-(\d{2})(\d)', naca_name)
    if thickness_match:
        thickness = int(thickness_match.group(1)) / 100
        return thickness
    else:
        return None

def extract_specific_thickness(naca_name):
    # Simple regex to capture a specific pattern like '015'
    if '015' in naca_name:
        return 0.15  # Returning the corresponding thickness as a float
    else:
        return None

# Utility Functions
def display_airfoil_table(df):
    st.write(df.to_html(escape=False), unsafe_allow_html=True)

# Main App Logic
def main():
    
    # add the debug logic all here

    #==================== AIRFOIL SELECTION TOOL ====================
    st.title("Airfoil Selection Tool")
    
    # Load and preprocess data
    airfoil_df = pd.DataFrame(airfoil_data, columns=[
        "Name", "M_Re", "alpha_n", "a0", "Cz_max", "letter", "alpha_kr", 
        "Cz_op", "alpha_d", "Cd_min", "Cm_ac", "x_ac", "y_ac"
    ])
    airfoil_df['Thickness'] = airfoil_df['Name'].apply(extract_airfoil_specs)

    # User interactions
    st.subheader("Select Thickness Ratios")
    thickness_ratio = st.select_slider("Choose Thickness Ratio", options=["15:12", "12:10", "12:09", "09:06"])
    root_thickness, tip_thickness = map(float, thickness_ratio.split(':'))

    # Process data based on user input
    root_airfoils = airfoil_df[airfoil_df['Thickness'] == root_thickness].head(5)
    tip_airfoils = airfoil_df[airfoil_df['Thickness'] == tip_thickness].head(5)

    # Debug: Display filtered DataFrames
    st.write("Root Airfoils debug:", root_airfoils)
    st.write("Tip Airfoils debug:", tip_airfoils)

    # Display tables
    st.markdown("### All Airfoils")
    display_airfoil_table(airfoil_df)

    st.markdown("### Top 5 Root Airfoils")
    display_airfoil_table(root_airfoils)

    st.markdown("### Top 5 Tip Airfoils")
    display_airfoil_table(tip_airfoils)

    #==================== DEBUG ====================
    airfoil_df = pd.DataFrame(airfoil_data, columns=[
        "Name", "M_Re", "alpha_n", "a0", "Cz_max", "letter", "alpha_kr", 
        "Cz_op", "alpha_d", "Cd_min", "Cm_ac", "x_ac", "y_ac"
    ])
    airfoil_df['Thickness'] = airfoil_df['Name'].apply(extract_airfoil_specs)
    airfoil_df['Specific_Thickness'] = airfoil_df['Name'].apply(extract_specific_thickness)

    # User interactions
    st.subheader("Select Thickness Ratios")

    # Process data based on user input for general thickness
    root_airfoils = airfoil_df[airfoil_df['Thickness'] == root_thickness].head(5)
    tip_airfoils = airfoil_df[airfoil_df['Thickness'] == tip_thickness].head(5)

    # Display tables for general thickness
    st.markdown("### Top 5 Root Airfoils - General Thickness")
    display_airfoil_table(root_airfoils)

    st.markdown("### Top 5 Tip Airfoils - General Thickness")
    display_airfoil_table(tip_airfoils)

    # Debugging with specific thickness
    st.markdown("### Debugging: Specific Thickness")
    st.write("DataFrame with Specific Thickness:", airfoil_df)
    
    root_airfoils_debug = airfoil_df[airfoil_df['Specific_Thickness'] == 0.15].head(5)
    tip_airfoils_debug = airfoil_df[airfoil_df['Specific_Thickness'] == 0.12].head(5)  # Example for '012'

    st.write("Root Airfoils with Specific Thickness:", root_airfoils_debug)
    st.write("Tip Airfoils with Specific Thickness:", tip_airfoils_debug)


# App Execution
if __name__ == "__main__":
    main()
