import streamlit as st
import pandas as pd
import re
from data import Variable, airfoil_data
from utils import spacer, emoji_header, variables_three_columns

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

    # button to display all airfoils
    if st.button("Display Airfoil Table"):
        st.markdown("### All Airfoils")
        st.write("All airfoils:", airfoil_df)

    # User interactions
    emoji_header("1️⃣", "Thickness Ratio")
    st.subheader("Select Thickness Ratios")
    thickness_ratio = st.select_slider("Choose Thickness Ratio", options=["15:12", "12:10", "12:09", "09:06"])
    root_thickness, tip_thickness = (float(value) / 100 for value in thickness_ratio.split(':'))

    emoji_header("2️⃣", "Lift coefficient")
    st.write("Selecting the airfoil's optimal lift coefficient by similarity to the one at cruise.")
    st.latex(r"C_{Z_{opt}} \approx C_{Z_{krst}}")
    cz_selector = st.number_input("Cruise Lift Coefficient", value=0.247, step=0.001, format="%.3f")
    c_z_krst = Variable("Cruise Lift Coefficient", cz_selector, r"C_{z_{krst}}", "")



    #==================== PROCESS DATA ====================#
    # Find airfoils close to the selected cruise lift coefficient
    airfoil_df['Cz_Diff'] = abs(airfoil_df['Cz_op'] - cz_selector)

    # Filter for root airfoils by thickness and lift coefficient closeness
    root_airfoils = airfoil_df[(airfoil_df['Thickness'] == root_thickness)].nlargest(5, 'Cz_op', 'all')
    # Filter for tip airfoils by thickness and lift coefficient closeness
    tip_airfoils = airfoil_df[(airfoil_df['Thickness'] == tip_thickness)].nlargest(5, 'Cz_op', 'all')

    # Display tables
    st.markdown("***")
    st.markdown("### Top 5 Root Airfoils")
    # display_airfoil_table(root_airfoils)
    st.write("Root airfoils:", root_airfoils)

    st.markdown("### Top 5 Tip Airfoils")
    st.write("Tip airfoils:", tip_airfoils)
    display_airfoil_table(tip_airfoils)

# App Execution
if __name__ == "__main__":
    main()
