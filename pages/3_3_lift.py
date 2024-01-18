### 3_lift.py ###

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

def regex_extract_values(output):
    # Dictionary to hold the extracted values
    extracted_values = {}

    # Regular expressions for each line
    patterns = {
        'Cz': r"KOEFICIJENT UZGONA KRILA\s+Cz\s*=\s*([\d.]+)",
        'Cxi': r"KOEF\. INDUKOVANOG OTPORA KRILA\s+Cxi\s*=\s*([\d.]+)",
        'delta': r"Popravni faktor indukovanog otpora\s+delta\s*=\s*([\d.]+)",
        'a': r"GRADIJENT UZGONA KRILA\s+a\s*=\s*([\d.]+) \[1/o\]",
        'AlfaA': r"aerodinamicki napadni ugao krila\s+AlfaA\s*=\s*([\d.\-]+) \[o\]",
        'AlfaAs': r"aerodinamicki nap\. ugao u korenu\s+AlfaAs\s*=\s*([\d.\-]+) \[o\]",
        'Alfa': r"GEOMETRIJSKI NAPADNI UGAO KRILA\s+Alfa\s*=\s*([\d.\-]+) \[o\]",
        'AlfaN': r"UGAO NULTOG UZGONA KRILA\s+AlfaN\s*=\s*([\d.\-]+) \[o\]",
    }

    # Loop over the patterns and apply each regex
    for key, pattern in patterns.items():
        match = re.search(pattern, output)
        if match:
            # Convert to float if possible, otherwise keep as string
            try:
                extracted_values[key] = float(match.group(1))
            except ValueError:
                extracted_values[key] = match.group(1)

    return extracted_values



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
    
    st.markdown("***")    
    st.subheader("FORTRAN program")

    st.write("The following values are used in the FORTRAN program below. Values are default unless you calculated them on other pages, and you can change them here as well.")

    # ==================== INPUT PARAMETERS ====================
    with st.expander("Edit FORTRAN Input Parameters"):
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
        st.latex(f"\\lambda = \\frac{{b^2}}{{S}} = \\frac{{{b**2:.3f}}}{{{S}}} = {lmbda:.3f}")
        
        st.write("Calculate wing taper ratio `n`")
        col1, col2 = st.columns(2)
        with col1:
            l0 = st.number_input('Tip Chord Length (m) `l0`', value=get_variable_value('l0'))
        with col2:
            ls = st.number_input('Root Chord Length (m) `ls`', value=get_variable_value('ls'))
        n = l0 / ls
        st.latex(f"n = \\frac{{l_0}} {{l_s}} = \\frac{{{l0:.3f}}} {{{ls:.3f}}} = {n:.3f}")

    col1, col2 = st.columns(2)
    with col1:
        st.write("Calculated wing aspect ratio (λ) `lmbda`")
        st.latex(f"\\lambda = \\frac{{b^2}}{{S}} = \\frac{{{b**2:.3f}}}{{{S}}} = {lmbda:.3f}")
    with col2:
        st.write("Calculated wing taper ratio `n`")
        st.latex(f"n = \\frac{{l_0}} {{l_s}} = \\frac{{{l0:.3f}}} {{{ls:.3f}}} = {n:.3f}")

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
    
    spacer()
    st.success("🎉 Your values are loaded in FORTRAN input")
    
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

    st.markdown("#### FORTRAN Output")
    with open('./modules/fortran/IZLAZ.TXT', 'r') as file:
        output = file.read()
        if st.button("Show full FORTRAN Output"):
            st.code(output, language='java')
        
    table_data, czmax_final = regex_fortran(output)

    extracted_values = regex_extract_values(output)
    st.write(extracted_values)

    # ==================== GRAB VALUES ====================
    st.markdown("***")
    st.markdown(f"#### 1️⃣ Max lift coefficient – $C_{{z_{{max}}}}$ `c_z_max`")
    
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

    st.markdown("***")
    # ==================== 2. alpha_0 ============================================================
    st.markdown(r"### 2️⃣ Zero-lift angle of attack – $\\alpha_0$ `alpha_0`")
    
    st.latex(r"\\alpha_n = \\alpha_{ns} + \\varepsilon \cdot f_a")

    st.markdown(r"""
    - $$ \\alpha_{ns} $$ is the angle of zero lift of the airfoil in the plane of symmetry, $$ \\alpha_{ns} = -1^\\circ $$
    - $$ \\varepsilon $$ is the total twist of the wing, $$ \\varepsilon = \\varepsilon_a + \\varepsilon_k = 0.3^\\circ + 0^\\circ - 0.3^\\circ $$
    - $$ \\varepsilon_a $$ is the aerodynamic twist, $$ \\varepsilon_a = \\alpha_{ns} - \\alpha_{n0} = -1^\\circ - (-1.3^\\circ) \cdot 0.3^\\circ $$
    - $$ \\varepsilon_k $$ is the constructive twist, $$ \\varepsilon_k = 0^\\circ $$ (as there is no constructive twist)

    This is followed by an explanation that at the location where $$ cZ_{max} - cb = 1.148 $$, flow separation occurs, and that value becomes $$ ca $$.
    """)

    
    st.markdown("***")
    # ==================== 3. a_0 ============================================================
    
    st.markdown("#### 3️⃣ Lift Gradient – $a$ `a`")
    st.latex(r"a = \frac{a_0 \cdot \lambda}{2 + \sqrt{4 + \lambda^2 \cdot \beta^2 \cdot \left(1 + \frac{\tan^2(\phi)}{\beta^2}\right)}} = \frac{0.110 \cdot 3.888}{2 + \sqrt{4 + (3.888)^2 \cdot (0.71)^2 \cdot \left(1 + \frac{\tan^2(27^\circ)}{(0.71)^2}\right)}} = 0.07197 \approx 0.072")
    
    st.markdown("***")
    # ==================== 4. alpha_krst ============================================================
    st.markdown("#### 4️⃣ Critical angle of attack – $\\alpha_{{kr}}$ `alpha_kr`")





    # Update variables at the end of the session
    update_variables(page_values, locals())
    log_changed_variables()

if __name__ == "__main__":
    main()