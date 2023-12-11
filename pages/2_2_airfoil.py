import streamlit as st
from data import Variable, airfoils
from utils import spacer, variables_two_columns

c_z_krst = Variable("Cruise Lift Coefficient", 0.247, r"C_{z_{krst}}", "m/s")
Cz_op = Variable("Cruise Lift Coefficient", 0.247, r"C_{z_{krst}}", "m/s")

def main():
    st.title("Airfoil Data")
    st.write("Prioritet parametara koje uzimamo u obzir pri izboru aeroprofila može varirati od jedne do druge kategorije letelica, pa se zato univerzalna metodologija teško može propisati. Pristup u izboru koji će biti prikazan u nastavku ima za cilj da ukaže na najbitnije parametre koji se uzimaju u obzir. Na osnovu relativne debljine aeroprofila i uslova da je cZopt ≈ cZkrst bira se po pet aeroprofila za koren i za kraj krila, a zatim se gleda koji su aeroprofili najpogodniji.")

    # Display airfoil data in a single table
    st.markdown("### Airfoil Data")
    st.markdown(display_airfoil_table(airfoils), unsafe_allow_html=True)

def display_airfoil_table(airfoils_data):
    # Create the header row, excluding the "Designation" key
    header_keys = list(next(iter(airfoils_data.values())).keys())[1:]  # Skip the first key which is "Designation"
    headers = ["Airfoil"] + header_keys
    table = "<!--- | " + " | ".join(headers) + " | --->\n"
    table += "| " + " | ".join(['<span style="font-size: 0.75em;">Airfoil</span>'] + [f'<span style="font-size: 0.75em;" title="{var.name}">${var.latex}$</span>' for var in next(iter(airfoils_data.values())).values()][1:]) + " |\n"
    table += "|---" * len(headers) + "|\n"

    # Add a row for each airfoil, excluding the "Designation" data
    for name, data in airfoils_data.items():
        row = "| " + f'<span style="font-size: 0.85em;">{name}</span>' + " | "
        row += " | ".join([f'<span style="font-size: 0.8em;">{str(var.value)}</span>' for var in list(data.values())[1:]]) + " |\n"
        table += row

    return table

if __name__ == "__main__":
    main()
