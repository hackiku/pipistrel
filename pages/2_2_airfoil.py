import streamlit as st
import pandas as pd
from data import Variable, airfoil_data
from utils import spacer, emoji_header, variables_three_columns
import re

cz_selector = st.number_input("Cruise Lift Coefficient", value = 0.247, step = 0.001, format = "%.3f")
c_z_krst = Variable("Cruise Lift Coefficient", cz_selector, r"C_{z_{krst}}", "")

# Function to extract the relative thickness from the NACA name
def extract_thickness(naca_name):
    match = re.search(r'(\d{4})$', naca_name)
    if match:
        # The thickness is the last two digits divided by 100
        return int(match.group(1)[-2:]) / 100
    else:
        # Handle names that do not match the expected pattern
        return None

# Convert the list of lists into a pandas dataframe
airfoil_df = pd.DataFrame(airfoil_data, columns=[
    "Name", "M_Re", "alpha_n", "a0", "Cz_max", "letter", "alpha_kr", 
    "Cz_op", "alpha_d", "Cd_min", "Cm_ac", "x_ac", "y_ac"
])

def extract_airfoil_specs(naca_name):
    thickness_match = re.search(r'-(\d{2})$', naca_name)
    thickness = int(thickness_match.group(1)) / 100 if thickness_match else None

    lift_coefficient_match = re.search(r'-(\d)', naca_name)
    lift_coefficient = int(lift_coefficient_match.group(1)) / 10 if lift_coefficient_match else None

    return thickness, lift_coefficient

# Apply the regex pattern to extract specs for each airfoil
airfoil_df['Thickness'], airfoil_df['Design_Lift_Coefficient'] = zip(*airfoil_df['Name'].apply(extract_airfoil_specs))

# -----------------------------
airfoils = []
for data in airfoil_data:
    airfoil_dict = {
        "Name": data[0],
        "M_Re": Variable("MRe", data[1], "", ""),
        "alpha_n": Variable("Angle of Attack at Zero Lift", data[2], r"\alpha_n", "degrees"),
        "a0": Variable("Lift Curve Slope", data[3], "a_0", ""),
        "Cz_max": Variable("Max Lift Coefficient", data[4], "C_{z_{max}}", ""),
        "letter": Variable("Letter", data[5], "{/}", ""),
        "alpha_kr": Variable("Alpha Critical", data[6], r"\alpha_{kr}", "degrees"),
        "Cz_op": Variable("Operational Lift Coefficient", data[7], "C_{z_{op}}", ""),
        "Cd_min": Variable("Min Drag Coefficient", data[8], "C_{d_{min}}", ""),
        "Cm_ac": Variable("Moment Coefficient about Aerodynamic Center", data[9], "C_{m_{ac}}", ""),
        "x_ac": Variable("x-position of Aerodynamic Center", data[10], r"\left( \frac{x}{l} \right)_{ac}", ""),
        "y_ac": Variable("y-position of Aerodynamic Center", data[11], r"\left( \frac{y}{l} \right)_{ac}", ""),
    }
    airfoils.append(airfoil_dict)


# Apply the function to the 'Name' column
airfoil_df['Relative_Thickness'] = airfoil_df['Name'].apply(extract_thickness)

def display_airfoil_table(df):
    st.markdown(
        f'<div style="height: 300px; overflow-y: scroll;">{df.to_html(index=False)}</div>', 
        unsafe_allow_html=True
    )


"""
def display_airfoil_table(airfoils_data):
    # Create the header row
    header_keys = list(next(iter(airfoils_data)).keys())[1:]  # Skip the first key which is "Name"
    headers = ["Airfoil"] + header_keys
    table = "<!--- | " + " | ".join(headers) + " | --->\n"
    table += "| " + " | ".join(['<span style="font-size: 0.75em;">Airfoil</span>'] + [f'<span style="font-size: 0.75em;" title="{var.name}">${var.latex}$</span>' for var in list(next(iter(airfoils_data)).values())[1:]]) + " |\n"
    table += "|---" * len(headers) + "|\n"
    
    for airfoil in airfoils_data:
        row = "| " + f'<span style="font-size: 0.85em;">{airfoil["Name"]}</span>' + " | "
        row += " | ".join([f'<span style="font-size: 0.8em;">{str(var.value)}</span>' for var in list(airfoil.values())[1:]]) + " |\n"
        table += row
    return table
"""
def main():
    st.title("Airfoil Data")
    st.write("Prioritet parametara koje uzimamo u obzir pri izboru aeroprofila može varirati od jedne do druge kategorije letelica, pa se zato univerzalna metodologija teško može propisati. Pristup u izboru koji će biti prikazan u nastavku ima za cilj da ukaže na najbitnije parametre koji se uzimaju u obzir. Na osnovu relativne debljine aeroprofila i uslova da je cZopt ≈ cZkrst bira se po pet aeroprofila za koren i za kraj krila, a zatim se gleda koji su aeroprofili najpogodniji.")

    st.latex(f"{c_z_krst.latex} ≈ {airfoils[0]['Cz_op'].latex}")

    # Display airfoil data in a single table
    st.markdown("### Wing root airfoils")
    st.markdown(display_airfoil_table(airfoils), unsafe_allow_html=True)

    spacer()

    st.subheader("Selection criteria")

    emoji_header("1️⃣", "Relative thickness")
    st.write("The relative thickness of the airfoil is extracted from NACA names using Regex")
    
    thickness_ratios = {
        "15:12": (0.15, 0.12),
        "12:10": (0.12, 0.10),
        "12:09": (0.12, 0.09),
        "09:06": (0.09, 0.06),
    }

    def sort_airfoils(df, thickness_root, thickness_tip, n=5):
        # Filter based on thickness
        root_airfoils = df[df['Thickness'] == thickness_root]
        tip_airfoils = df[df['Thickness'] == thickness_tip]

        # Sort based on other criteria (pseudo-code, replace with your actual logic)
        # root_sorted = sort_based_on_criteria(root_airfoils)
        # tip_sorted = sort_based_on_criteria(tip_airfoils)

        # Select the top N airfoils
        root_selection = root_airfoils.head(n)
        tip_selection = tip_airfoils.head(n)

        return root_selection, tip_selection


    st.latex(r"\frac{M}{Re} = \frac{M}{\rho V_{\infty} c} = \frac{M}{\rho V_{\infty} \sqrt{\frac{S}{b}}} = \frac{M}{\rho V_{\infty} \sqrt{\frac{S}{b}}} = \frac{M}{\rho V_{\infty} \sqrt{\frac{S}{b}}} = \frac{M}{\rho V_{\infty} \sqrt{\frac{S}{b}}}")
    

if __name__ == "__main__":
    main()
