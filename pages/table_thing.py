
import streamlit as st
import pandas as pd
import re
from data import Variable, airfoil_data
from utils import spacer, emoji_header, variables_three_columns


# Global Variables
cz_selector = st.number_input("Cruise Lift Coefficient", value=0.247, step=0.001, format="%.3f")
c_z_krst = Variable("Cruise Lift Coefficient", cz_selector, r"C_{z_{krst}}", "")

# Data Preparation Functions
def extract_airfoil_specs(naca_name):
    # Regex to capture the thickness pattern after 'NACA'
    thickness_match = re.search(r'NACA.*?-\d(\d{2})', naca_name)
    if thickness_match:
        thickness = int(thickness_match.group(1)) / 100
        return thickness
    else:
        return None

# Utility Functions
def display_airfoil_table(df):
    st.write(df.to_html(escape=False), unsafe_allow_html=True)


# Main App Logic
def main():
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
    root_thickness, tip_thickness = (float(value) / 100 for value in thickness_ratio.split(':'))

    # Process data based on user input
    root_airfoils = airfoil_df[airfoil_df['Thickness'] == root_thickness].head(20)
    tip_airfoils = airfoil_df[airfoil_df['Thickness'] == tip_thickness].head(20)

    # Display tables
    if st.button("Display Airfoil Table"):
        # display_airfoil_table(airfoil_df)
        st.markdown("### All Airfoils")
        # display_airfoil_table(airfoil_df)
        st.write("All airfoils:", airfoil_df)


    st.markdown("### Top 5 Root Airfoils")
    # display_airfoil_table(root_airfoils)
    st.write("Root airfoils:", root_airfoils)

    st.markdown("### Top 5 Tip Airfoils")
    st.write("Tip airfoils:", tip_airfoils)
    display_airfoil_table(tip_airfoils)

# App Execution
if __name__ == "__main__":
    main()
