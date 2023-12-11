import streamlit as st
from data import Variable
from utils import spacer, variables_two_columns

c_z_krst = Variable("Cruise Lift Coefficient", 0.247, r"C_{z_{krst}}", "m/s")

airfoil_raw_data = [
    ["NACA WIN", 9.0, -2.0, 0.110, 1.62, 14.5, 0.25, 0.0045, -0.034, 0.263, -0.029],
    ["NACA 63(1)-212", 10.0, -2.0, 0.110, 1.62, 14.5, 0.25, 0.0045, -0.034, 0.263, -0.029],
    ["Clark Y-14", 8.5, -1.5, 0.115, 1.55, 13.5, 0.30, 0.0050, -0.030, 0.270, -0.025],
    ["Supermarine 504", 10.0, -2.5, 0.120, 1.70, 15.0, 0.20, 0.0040, -0.035, 0.260, -0.030],
    ["Go 1900", 9.5, -1.8, 0.113, 1.60, 14.0, 0.22, 0.0043, -0.033, 0.265, -0.028],
]

airfoils = []
for data in airfoil_raw_data:
    airfoil_dict = {
        "Name": data[0],
        "M_Re": Variable("MRe", data[1], "", ""),
        "alpha_n": Variable("Angle of Attack at Zero Lift", data[2], r"\alpha_n", "degrees"),
        "a0": Variable("Lift Curve Slope", data[3], "a_0", ""),
        "Cz_max": Variable("Max Lift Coefficient", data[4], "C_{z_{max}}", ""),
        "alpha_kr": Variable("Alpha Critical", data[5], r"\alpha_{kr}", "degrees"),
        "Cz_op": Variable("Operational Lift Coefficient", data[6], "C_{z_{op}}", ""),
        "Cd_min": Variable("Min Drag Coefficient", data[7], "C_{d_{min}}", ""),
        "Cm_ac": Variable("Moment Coefficient about Aerodynamic Center", data[8], "C_{m_{ac}}", ""),
        "x_ac": Variable("x-position of Aerodynamic Center", data[9], r"\left( \frac{x}{l} \right)_{ac}", ""),
        "y_ac": Variable("y-position of Aerodynamic Center", data[10], r"\left( \frac{y}{l} \right)_{ac}", ""),
    }
    airfoils.append(airfoil_dict)

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

def main():
    st.title("Airfoil Data")
    st.write("Prioritet parametara koje uzimamo u obzir pri izboru aeroprofila može varirati od jedne do druge kategorije letelica, pa se zato univerzalna metodologija teško može propisati. Pristup u izboru koji će biti prikazan u nastavku ima za cilj da ukaže na najbitnije parametre koji se uzimaju u obzir. Na osnovu relativne debljine aeroprofila i uslova da je cZopt ≈ cZkrst bira se po pet aeroprofila za koren i za kraj krila, a zatim se gleda koji su aeroprofili najpogodniji.")

    st.latex(f"{c_z_krst.latex} = {airfoils[0]['Cz_op'].latex}")

    def calculate_relative_airfoil_width():
        # logic here later
        return
    
    def update_table():
        # now just make it update
        return

    # Display airfoil data in a single table
    st.markdown("### Airfoil Data")
    st.markdown(display_airfoil_table(airfoils), unsafe_allow_html=True)

    

if __name__ == "__main__":
    main()
