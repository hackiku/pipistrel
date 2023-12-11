# 2_2._airfoil.py

import streamlit as st
from data import Variable, airfoils
from utils import spacer, variables_two_columns

c_z_krst = Variable("Cruise Lift Coefficient", 0.247, r"C_{z_{krst}}", "m/s")

# Streamlit app code
def main():
    st.title("Airfoil Data")
    st.write("Prioritet parametara koje uzimamo u obzir pri izboru aeroprofila može varirati od jedne do druge kategorije letelica, pa se zato univerzalna metodologija teško može propisati. Pristup u izboru koji će biti prikazan u nastavku ima za cilj da ukaže na najbitnije parametre koji se uzimaju u obzir. Na osnovu relativne debljine aeroprofila i uslova da je cZopt ≈ cZkrst bira se po pet aeroprofila za koren i za kraj krila, a zatim se gleda koji su aeroprofili najpogodniji.")

    # Airfoil selection (for future filtering implementation)
    selected_airfoil = st.selectbox("Select an Airfoil", list(airfoils.keys()))
    airfoil_data = airfoils[selected_airfoil]

    # Display airfoil data for the selected airfoil
    st.markdown("### Airfoil Data")
    st.markdown(display_airfoil_table(airfoil_data), unsafe_allow_html=True)

def display_airfoil_table(airfoil_data):
    # Start the table and hide the headers with an HTML comment
    table = "<!--- | " + " | ".join(airfoil_data.keys()) + " | --->\n"
    table += "| " + " | ".join([f'<span title="{var.name}">${var.latex}$</span>' for var in airfoil_data.values()]) + " |\n"
    table += "|---" * len(airfoil_data) + "|\n"
    table += "| " + " | ".join([str(var.value) for var in airfoil_data.values()]) + " |\n"

    return table

if __name__ == "__main__":
    main()
