### 3_wing.py ###

import streamlit as st
from variables_manager import initialize_session_state, get_variable_value, update_variables, log_changed_variables
from utils import spacer
from data import airfoil_data
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import re

# TODO hardcoded airfoil array
root_airfoil_data = ["NACA 65_2-415", 9.0, -2.8, 0.113, 1.62, "D", 16.5, 0.30, 11.5, 0.0040, -0.062, 0.266, -0.062]
tip_airfoil_data = ["NACA 63_4-412", 9.0, -3.0, 0.100, 1.78, "D", 15.0, 0.32, 9.6, 0.0045, -0.075, 0.270, -0.073]

# TODO hardcoded airfoil values
c_z_max_root = root_airfoil_data[4]
alpha_0_root = root_airfoil_data[2] # Angle of Zero Lift at Root
a_0_root = root_airfoil_data[3] # Lift Gradient at Root
c_z_max_tip = tip_airfoil_data[4]
alpha_0_tip = tip_airfoil_data[2]
a_0_tip = tip_airfoil_data[3]


def regex_fortran(output):
    table_data = []
    start_extracting = False
    for line in output.split('\n'):
        if start_extracting:
            # Adjusted regex to include the format '-.000'
            values = re.findall(r"-?\d*\.\d+", line)
            if len(values) == 5:
                y_b2, czmax_ap, czmax_ap_cb_ca, cz_lok, pmax_n_m = map(float, values)
                table_data.append({
                    "y/(b/2)": y_b2,
                    "Czmax ap.": czmax_ap,
                    "Czmax-Cb/Ca": czmax_ap_cb_ca,
                    "Czlok": cz_lok,
                    "Pmax [N/m]": pmax_n_m
                })
        if "y/(b/2)         Czmax ap." in line:
            start_extracting = True  # Begin capturing data from the next line

    # Part 2: Extract final CZmax value
    czmax_final_regex = r"Maksimalni koeficijent uzgona krila CZmax = (\d+\.\d+)"
    czmax_final_match = re.search(czmax_final_regex, output)
    czmax_final_value = float(czmax_final_match.group(1)) if czmax_final_match else None

    return table_data, czmax_final_value

# ======================================================================#
# ================================ MAIN ================================#
# ======================================================================#

def main():
    
    page_values = [
        'S', 'l0', 'l1', 'b', 'm_sr', 'v_krst', 'T', 'P', 'rho', 'c', 
        'g', 'Re', 'c_z_krst',
        'lambda_wing', 'n', 'phi', 'alpha_n', 'c_z_max_root', 'alpha_0_root', 
        'a_0_root', 'c_z_max_tip', 'alpha_0_tip', 'a_0_tip'
    ]
    initialize_session_state(page_values)

    # Display title and headers
    st.title("3. Wing Lift Calculation")
    st.write('The goal of this section is to construct the lift curve, and for that we need to calculate the following parameters:')
    st.markdown(r"""- $C_{z_{max}}$ - Max lift coefficient
- $\alpha_0$ - Zero-lift angle of attack
- $a_0$ - Lift curve slope XXX
- $\alpha_{krst}$ - Angle of attack at cruise
""")
    
    
    st.header("FORTRAN input values")
    st.write("The following values are used in the FORTRAN program below. Values are default unless you calculated them on other pages, and you can change them here as well.")

    # ==================== INPUT PARAMETERS ====================
    c_z_krst = st.number_input('Cruise Lift Coefficient `c_z_krst`', value=get_variable_value('c_z_krst'))
    col1, col2 = st.columns(2)
    with col1:
        v_krst = st.number_input('Cruising Speed (m/s) `v_krst`', value=get_variable_value('v_krst'))
    with col2:
        v_krst_kmh = st.number_input('Cruising Speed (km/h) `v_krst_kmh`', value=get_variable_value('v_krst') * 3.6)
    rho = st.number_input('Air Density at Cruise Altitude (kg/m^3) `rho`', value=get_variable_value('rho'))

    st.write("Calculate wing aspect ratio (λ) `lmbda`")
        
    col1, col2 = st.columns(2)
    with col1:
        b = st.number_input('Wingspan (m) `b`', value=get_variable_value('b'))
    with col2: 
        S = st.number_input('Wing Area (m^2) `S`', value=get_variable_value('S'))
    lmbda = b**2 / S
    st.latex(f"\\lambda = \\frac{{b^2}}{{S}} = \\frac{{{b**2:.2f}}}{{{S}}} = {lmbda:.3f}")
    
    st.write("Calculate wing taper ratio `b`")
    col1, col2 = st.columns(2)
    with col1:
        l0 = st.number_input('Tip Chord Length (m) `l0`', value=get_variable_value('l0'))
    with col2:
        ls = st.number_input('Root Chord Length (m) `ls`', value=get_variable_value('ls'))
    n = l0 / ls
    st.latex(f"n = \\frac{{l_0}} {{l_s}} = \\frac{{{l0}}} {{{ls}}} = {n:.3f}")


    st.markdown('#### Mission parameters & wing geometry')
    wing_inputs = f"""
    | # | Parameter                           | Symbol                 | Value                       | Unit    |
    |---|-------------------------------------|------------------------|-----------------------------|---------|
    |1️⃣ | **_Mission Parameters_**            |                        |                             |         |
    | 1 | Cruise Lift Coefficient             | $C_{{z_{{krst}}}}$     | {c_z_krst:.3f}              | -       |
    | 6 | Cruising Speed                      | $v_{{krst}}$           | {v_krst:.2f}                | m/s     |
    | 7 | Air Density at Cruise Altitude      | $\\rho$                | {rho:.5f}                   | kg/m³   |
    |2️⃣ | **_Wing Geometry_**                 |                        |                             | -       |
    | 2 | Wing Aspect Ratio (λ)               | $\\lambda$             | {lmbda:.3f}                 | -       |
    | 3 | Tip Chord Length                    | $l_0$                  | {l0:.3f}                    | m       |
    | 4 | Root Chord Length                   | $l_s$                  | {ls:.3f}                    | m       |
    | 5 | Wing Taper Ratio (n)                | $n$                    | {n:.3f}                     | -       |
    """
    st.markdown(wing_inputs)

    spacer()
    
    st.markdown('#### Airfoil data inputs')
    airfoil_inputs = f"""
    | # | Parameter Name           | Symbol                | Tip         | Root       |
    |---|--------------------------|-----------------------|------------------|-----------------|
    | 1 | Airfoil name             |                       | NACA 65_2-415    | NACA 63_4-412   |
    | 2 | Max lift coefficient     | $C_{{z_{{max}}}}$     | {c_z_max_tip:.3f}| {c_z_max_root:.3f} |
    | 3 | Angle of zero lift       | $\\alpha_0$           | {alpha_0_tip:.2f}° | {alpha_0_root:.2f}° |
    | 4 | Lift gradient            | $a_0$                 | {a_0_tip:.3f}    | {a_0_root:.3f}   |
    """
    st.markdown(airfoil_inputs)

    st.markdown("***")

    fortran_inputs = f"""C     *************** UNOS ULAZNIH PODATAKA I OPCIJA *******************

C     IZBOR PRORACUNSKE OPCIJE: ZA VREDNOOST IZB=1 RACUNA SA UNAPRED
C     ZADATIM KOEFICIJENTOM UZGONA KRILA CZ; U SUPROTNOM, ZA SVAKI
C     DRUGI INTEGER (npr. IZB=0) CZ RACUNA NA OSNOVU SPECIFICNOG
C     OPTERECENJA KRILA, BRZINE I GUSTINE NA REZIMU KRSTARENJA

      IZB=1
      DATA CZ / {c_z_krst:.3f} /  !ZADATI KOEFICIJENT UZGONA KRILA
      DATA SPECOP /800. / !ZADATO SPECIFICNO OPTERECENJE KRILA [N/m^2]

C             PARAMETRI GEOMETRIJE KRILA I REZIMA KRSTARENJA:
C                                          konst.
C              broj    vitkost suzenje   vitop.   brzina   gustina
C            preseka                     [step.]  [km/h]   [kg/m^3]
      DATA      K,       LAM,   EN,       EPS_K,    V,        RO
    &     /    16,       {lmbda:.3f}, {n:.3f},      0.0,  {v_krst_kmh:.2f},    {rho:.3f} /

      DATA CZMAXAP_S / {c_z_max_root:.3f} / ! maks. koef. uzgona ap. u korenu krila
      DATA CZMAXAP_0 / {c_z_max_tip:.3f} / ! maks. koef. uzgona ap. na kraju krila
      DATA AAAP_S / {a_0_root:.3f} / !grad. uzgona ap. u korenu [1/o]
      DATA AAAP_0 / {a_0_tip:.3f} / !grad. uzgona ap. na kraju [1/o]
      !teorijska  vrednost gradijenta uzgona 2PI = 0.1096622 [1/o]
      DATA ANAP_S / {alpha_0_root:.1f} / !ugao nultog uzgona ap. u korenu krila [o]
      DATA ANAP_0 / {a_0_tip:.1f} / !ugao nultog uzgona ap. na kraju krila [o]
      DATA LS / {ls:.3f} /  ! duzina tetive u korenu krila u metrima

C     ******************** KRAJ UNOSA PODATAKA *************************"""
    st.code(fortran_inputs, language='fortran')

    st.markdown("***")
    
    # ==================== FORTRAN OUTPUT ====================

    with open('./modules/fortran/IZLAZ.TXT', 'r') as file:
        output = file.read()
        st.code(output, language='java')
        
    table_data, czmax_final = regex_fortran(output)

    #==================== dataframe ====================#
    st.subheader("Flow separation")
    df = pd.DataFrame(table_data)
    df['Highlight'] = df['Czmax ap.'].apply(lambda x: 'Yes' if x == czmax_final else 'No')
    st.dataframe(df, width=1100, use_container_width=False)

    # st.write(table_data)
    
    # y_b2 = Variable("y/(b/2)", df['y/(b/2)'].tolist(), "y_b2", r"y/(b/2)", "")
    # c_z_max = Variable("Max Lift Coefficient", df['Czmax ap.'].tolist(), "c_z_max", r"C_{z_{max}}", "")
    # c_z_max_cb_ca = Variable("Max Lift Coefficient - Cb/Ca", df['Czmax-Cb/Ca'].tolist(), "c_z_max_cb_ca", r"C_{z_{max}} - C_{b}/C_{a}")
    # c_z_lok = Variable("Max Lift Coefficient", df["Czlok"].tolist(), "c_z_lok", r"C_{z_{max}}", "")
    # p_max = Variable("Max pressure", df["Pmax [N/m]"].tolist(), "p_max", r"C_{z_{max}}", "N/m")
    
    spacer()       
    st.markdown("***")

    wing_trapezoid_image = st.image('./modules/draw/crop_white.png')


    # Update variables at the end of the session
    update_variables(page_values, locals())
    log_changed_variables()

if __name__ == "__main__":
    main()