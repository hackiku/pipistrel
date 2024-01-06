# 3_wing_pg.py

import streamlit as st
from main import main as initialize_main
from data import Variable, save_variables_to_session, load_variables_from_session
from utils import spacer, variables_two_columns, display_generic_table
import pandas as pd
import matplotlib.pyplot as plt
import os
from main import (S as S_home, l0 as l0_home, l1 as l1_home, b as b_home, 
v_krst as v_krst_home, rho as rho_home, c_z_krst as c_z_krst_home)

# initialize_main()

# Hardcoded Airfoil Data
root_airfoil_data = ["NACA 65_2-415", 9.0, -2.8, 0.113, 1.62, "D", 16.5, 0.30, 11.5, 0.0040, -0.062, 0.266, -0.062]
tip_airfoil_data = ["NACA 63_4-412", 9.0, -3.0, 0.100, 1.78, "D", 15.0, 0.32, 9.6, 0.0045, -0.075, 0.270, -0.073]

# Extracting specific values from airfoil data
c_z_max_root = Variable("Max Lift Coefficient at Root", root_airfoil_data[4], "c_z_max_root", r"C_{z_{max}}", "")
alpha_0_root = Variable("Angle of Zero Lift at Root", root_airfoil_data[2], "alpha_0_root", r"\alpha_{0}", "degrees")
a_0_root = Variable("Lift Gradient at Root", root_airfoil_data[3], "a_0_root", r"a_{0}", "")

c_z_max_tip = Variable("Max Lift Coefficient at Tip", tip_airfoil_data[4], "c_z_max_tip", r"C_{z_{max}}", "")
alpha_0_tip = Variable("Angle of Zero Lift at Tip", tip_airfoil_data[2], "alpha_0_tip", r"\alpha_{0}", "degrees")
a_0_tip = Variable("Lift Gradient at Tip", tip_airfoil_data[3], "a_0_tip", r"a_{0}", "")

# geometry calcs
lambda_wing = Variable("Wing Aspect Ratio", 3.888, r"\lambda")
n = Variable("Wing Taper Ratio", 0.520, "n", "n")
phi = Variable("Sweep Angle", 27, "phi", r"\phi", "degrees")
alpha_n = Variable("Angle of Attack", -1.3, "alpha_n", r"\alpha_n", "degrees")

c_z_max = Variable("Max Lift Coefficient", 1.148, r"C_{z_{max}}", "")

data = [
    {"y/(b/2)": "0.000", "Cz_max": "1.254", "Cz_max_aero-Cb_ca": "1.298", "Cz_lok": "1.109", "P_max [N/m]": "62222.17"},
    {"y/(b/2)": "0.098", "Cz_max": "1.249", "Cz_max_aero-Cb_ca": "1.247", "Cz_lok": "1.150", "P_max [N/m]": "61482.50"},
    {"y/(b/2)": "0.195", "Cz_max": "1.244", "Cz_max_aero-Cb_ca": "1.210", "Cz_lok": "1.180", "P_max [N/m]": "59986.70"},
    {"y/(b/2)": "0.290", "Cz_max": "1.239", "Cz_max_aero-Cb_ca": "1.184", "Cz_lok": "1.202", "P_max [N/m]": "58030.61"},
    {"y/(b/2)": "0.383", "Cz_max": "1.234", "Cz_max_aero-Cb_ca": "1.164", "Cz_lok": "1.217", "P_max [N/m]": "55731.03"},
    {"y/(b/2)": "0.471", "Cz_max": "1.229", "Cz_max_aero-Cb_ca": "1.152", "Cz_lok": "1.225", "P_max [N/m]": "53174.51"},
    {"y/(b/2)": "0.556", "Cz_max": "1.225", "Cz_max_aero-Cb_ca": "1.148", "Cz_lok": "1.225", "P_max [N/m]": "50404.82"},
    {"y/(b/2)": "0.634", "Cz_max": "1.221", "Cz_max_aero-Cb_ca": "1.153", "Cz_lok": "1.216", "P_max [N/m]": "47446.35"},
    {"y/(b/2)": "0.707", "Cz_max": "1.217", "Cz_max_aero-Cb_ca": "1.169", "Cz_lok": "1.195", "P_max [N/m]": "44291.75"},
    {"y/(b/2)": "0.773", "Cz_max": "1.214", "Cz_max_aero-Cb_ca": "1.202", "Cz_lok": "1.159", "P_max [N/m]": "40903.96"},
    {"y/(b/2)": "0.831", "Cz_max": "1.211", "Cz_max_aero-Cb_ca": "1.260", "Cz_lok": "1.104", "P_max [N/m]": "37204.75"},
    {"y/(b/2)": "0.882", "Cz_max": "1.208", "Cz_max_aero-Cb_ca": "1.358", "Cz_lok": "1.022", "P_max [N/m]": "33073.96"},
    {"y/(b/2)": "0.924", "Cz_max": "1.206", "Cz_max_aero-Cb_ca": "1.527", "Cz_lok": "0.908", "P_max [N/m]": "28344.90"},
    {"y/(b/2)": "0.957", "Cz_max": "1.204", "Cz_max_aero-Cb_ca": "1.842", "Cz_lok": "0.752", "P_max [N/m]": "22813.59"},
    {"y/(b/2)": "0.981", "Cz_max": "1.203", "Cz_max_aero-Cb_ca": "2.527", "Cz_lok": "0.548", "P_max [N/m]": "16275.91"},
    {"y/(b/2)": "0.995", "Cz_max": "1.202", "Cz_max_aero-Cb_ca": "4.716", "Cz_lok": "0.294", "P_max [N/m]": "8611.25"}
]

def main():
    
    # load variables from state
    variable_names_to_load = ['S', 'l0', 'l1', 'b', 'v_krst', 'rho', 'g', 'm_sr', 'c_z_krst']
    variables, code = load_variables_from_session(variable_names_to_load)
    st.code(code)
    
    S = variables.get('S', S_home)
    l0 = variables.get('l0', l0_home)
    l1 = variables.get('l1', l1_home)
    b = variables.get('b', b_home)
    v_krst = variables.get('v_krst', v_krst_home)
    rho = variables.get('rho', rho_home)
    c_z_krst = variables.get('c_z_krst', c_z_krst_home)
        
    st.code(f"S = {S.value}, l0 = {l0.value}, l1 = {l1.value}, b = {b.value}, v_krst = {v_krst.value}, rho = {rho.value}, c_z_krst = {c_z_krst.value}")
    st.title("3. Wing Design")
    st.write("""Da bismo formirali krivu uzgona krila, moramo odrediti četiri karakteristična parametra: - Maksimalni koeficijent uzgona krila cZmax
    - Ugaonultoguzgonakrilaαn
    - Gradijent uzgona krila α
    - Kritičninapadniugaokrilaαkr""")
    
    st.header("3.1 Lift characteristics of wing")
    st.markdown("Proračun se u prvoj iteraciji u programu Trapezno krilo- Glauert obavlja pod pretpostavkom nultog konstruktivnog vitoperenja")

    # key variables 
    # variables_two_columns(c_z_max)
    # variables_two_columns(alpha_n)
    
    st.markdown("***")

    st.subheader("mission parameters")

    #==================== EXPANDER ====================#
    with st.expander("Edit / calculate input parameters"):
        # # alpha crit 
        variables_two_columns(c_z_krst)
        variables_two_columns(v_krst) # = 224.37 m/s = 807.73 km/h
        variables_two_columns(rho) # ρ

        st.code("Calculate wing aspect ratio (λ)")
        
        def calculate_lambda_wing():
            lambda_wing.value = b.value**2 / S.value
            numbers = "=" + f"\\frac{{{b.value:.2f}^2}}{{{S.value:.2f}}}"
            lambda_wing.formula = f"\\lambda = \\frac{{{b.latex}^2}}{{{S.latex}}} {numbers}"
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            b.value = st.number_input(f'{b.name} {b.unit}', value=b.value, step=0.01, format="%.3f")
        with col2: 
            S.value = st.number_input(f'{S.name} {S.unit}', value=S.value, step=0.1, format="%.3f")
        with col3:
            st.latex(f"{b.latex} = {b.value:.3f} \ {b.unit}")
        with col4:
            st.latex(f"{S.latex} = {S.value:.3f} \ {S.unit}")
            # st.latex = (S.latex)
        # st.latex(lambda_wing.formula)               
        
        calculate_lambda_wing()
        variables_two_columns(lambda_wing, display_formula=True) # λ

        st.code("Calculate wing taper ratio (n)")
        def calculate_taper_ratio():
            n.value = l0.value / l1.value
            numbers = "=" + f"\\frac{{{l0.value:.2f}}}{{{l1.value:.2f}}}"
            n.formula = f"n = \\frac{{{l0.latex}}}{{{l1.latex}}} {numbers}"

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            l0.value = st.number_input(f'{l0.name} {l0.unit}', value=l0.value, step=0.01, format="%.3f")
        with col2:
            l1.value = st.number_input(f'{l1.name} {l1.unit}', value=l1.value, step=0.01, format="%.3f")
        with col3:
            st.latex(f"{l0.latex} = {l0.value:.3f} \ {l0.unit}")
        with col4:
            st.latex(f"{l1.latex} = {l1.value:.3f} \ {l1.unit}")

        calculate_taper_ratio()
        variables_two_columns(n, display_formula=True)  # n

    wing_inputs = f"""
    | # | Parameter Name                 | Symbol                                           | Value                                  | Unit     |
    |---|--------------------------------|--------------------------------------------------|----------------------------------------|----------|
    | 1 | Cruise Lift Coefficient        | ${c_z_krst.latex}$                               | {c_z_krst.value:.3f}                   |          |
    | 2 | Wing Aspect Ratio (λ)          | ${lambda_wing.formula}$                    | {lambda_wing.value:.3f} |          |
    | 3 | Tip Chord Length               | ${l0.latex}$                                     | {l0.value:.3f}                         | {l0.unit}|
    | 4 | Root Chord Length              | ${l1.latex}$                                     | {l1.value:.3f}                         | {l1.unit}|
    | 5 | Wing Taper Ratio (n)           | ${n.formula}$                          | {n.value:.3f}      |          |
    | 6 | Cruising Speed                 | ${v_krst.latex}$                                 | {v_krst.value:.2f}                     | {v_krst.unit} |
    | 7 | Air Density at Cruise Altitude | ${rho.latex}$                                    | {rho.value:.5f}                        | {rho.unit} |
    """

    
    st.markdown(wing_inputs)
    st.markdown("***")

    st.subheader("airfoil params")
    
    airfoil_inputs = f"""
    | # | Parameter Name              | Symbol             | Tip           | Root          |
    |---|-----------------------------|--------------------|---------------|---------------|
    | 1 | Airfoil                     |                    | NACA 65_2-41  | NACA 63_4-412 |
    | 2 | Max Lift Coefficient        | ${c_z_max_root.latex}$ | {c_z_max_root.value:.3f} | {c_z_max_tip.value:.3f} |
    | 3 | Angle of Zero Lift          | ${alpha_0_root.latex}$ | {alpha_0_root.value:.2f}° | {alpha_0_tip.value:.2f}° |
    | 4 | Lift Gradient               | ${a_0_root.latex}$  | {a_0_root.value:.3f} | {a_0_tip.value:.3f} |
    """

    st.markdown(airfoil_inputs)

    st.markdown("***")

    #  =============

    st.subheader("3.1.1. Max lift coefficient of wings")
    st.write("Proračun se u prvoj iteraciji u programu Trapezno krilo- Glauert obavlja pod pretpostavkom nultog konstruktivnog vitoperenja")

    fortran_inputs = f"""C     *************** UNOS ULAZNIH PODATAKA I OPCIJA *******************

C     IZBOR PRORACUNSKE OPCIJE: ZA VREDNOOST IZB=1 RACUNA SA UNAPRED
C     ZADATIM KOEFICIJENTOM UZGONA KRILA CZ; U SUPROTNOM, ZA SVAKI
C     DRUGI INTEGER (npr. IZB=0) CZ RACUNA NA OSNOVU SPECIFICNOG
C     OPTERECENJA KRILA, BRZINE I GUSTINE NA REZIMU KRSTARENJA

      IZB=1
      DATA CZ / {c_z_krst.value:.3f} /  !ZADATI KOEFICIJENT UZGONA KRILA
      DATA SPECOP /800. / !ZADATO SPECIFICNO OPTERECENJE KRILA [N/m^2]

C             PARAMETRI GEOMETRIJE KRILA I REZIMA KRSTARENJA:
C                                          konst.
C              broj    vitkost suzenje   vitop.   brzina   gustina
C            preseka                     [step.]  [km/h]   [kg/m^3]
      DATA      K,       LAM,   EN,       EPS_K,    V,        RO
    &     /    16,      {lambda_wing.value:.0f},   {n.value:.3f},      0.0,    {v_krst.value:.2f},    {rho.value:.6f} /

      DATA CZMAXAP_S / {c_z_max_root.value:.3f} / ! maks. koef. uzgona ap. u korenu krila
      DATA CZMAXAP_0 / {c_z_max_tip.value:.3f} / ! maks. koef. uzgona ap. na kraju krila
      DATA AAAP_S / {a_0_root.value:.3f} / !grad. uzgona ap. u korenu [1/o]
      DATA AAAP_0 / {a_0_tip.value:.3f} / !grad. uzgona ap. na kraju [1/o]
      !teorijska  vrednost gradijenta uzgona 2PI = 0.1096622 [1/o]
      DATA ANAP_S / {alpha_0_root.value:.1f} / !ugao nultog uzgona ap. u korenu krila [o]
      DATA ANAP_0 / {a_0_tip.value:.1f} / !ugao nultog uzgona ap. na kraju krila [o]
      DATA LS / {l1.value:.3f} /  ! duzina tetive u korenu krila u metrima

C     ******************** KRAJ UNOSA PODATAKA *************************"""


    st.code(fortran_inputs, language='fortran')

    with open('./fortran/IZLAZ.TXT', 'r') as file:
        output = file.read()
        
    st.code(output, language='python')    
    
    st.markdown(r'''
    $$
    \Delta k = \left(1 - 0.088 \cdot \cos^2 \phi\right)^{\frac{3}{4}} \cdot \cos^{\frac{4}{3}} \phi = \left(1 - 0.088 \cdot \cos^2 27^\circ\right)^{\frac{3}{4}} \cdot \cos^{\frac{4}{3}} 27^\circ = 0.85884 \approx 0.859
    $$
    ''')
    spacer()
    
    df = pd.DataFrame(data)

    col1, col2 = st.columns([2,3])

    with col1:
        st.markdown(display_generic_table(data), unsafe_allow_html=True)
    with col2:
        fig, ax = plt.subplots()
        ax.plot(df['y/(b/2)'], df['Cz_max'], marker='o', label='Cz_max')
        ax.plot(df['y/(b/2)'], df['Cz_max_aero-Cb_ca'], marker='x', label='Cz_max_aero-Cb_ca')
        ax.plot(df['y/(b/2)'], df['Cz_lok'], marker='s', label='Cz_lok')
        ax.set_xlabel('y/(b/2)')
        ax.set_ylabel('Coefficients')
        ax.set_title('Airfoil Performance')
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

    spacer()
    st.markdown("""Na mestu gde je cZmax −cb =1.148 dolazi do otcepljenja strujanja i ta vrednost postaje ca
    c = 1.225 . Pošto do otcepljenja dolazi na y = 0.556 polurazmaha, što je Zmax ()
    2 zahtevanih 0.7 nećemo konstruktivno vitoperiti krilo.""")
    
    
    st.markdown("***")

    st.subheader("3.1.2. Angle of Zero Lift of the Wing")
    st.markdown("Ugao nultog uzgona aeroprofila smo dobili u programu „Trapezno krilo – Glauert“ kao izlazni parametar, ali se može odrediti i analitički na osnovu jednačine:")
    
    st.latex("\\alpha_n = \\alpha_{ns} + \\varepsilon \cdot f_a")

    st.image('assets/geometrija_krila_inverted.png')
    st.markdown("""
    - $$ \\alpha_{ns} $$ is the angle of zero lift of the airfoil in the plane of symmetry, $$ \\alpha_{ns} = -1^\\circ $$
    - $$ \\varepsilon $$ is the total twist of the wing, $$ \\varepsilon = \\varepsilon_a + \\varepsilon_k = 0.3^\\circ + 0^\\circ - 0.3^\\circ $$
    - $$ \\varepsilon_a $$ is the aerodynamic twist, $$ \\varepsilon_a = \\alpha_{ns} - \\alpha_{n0} = -1^\\circ - (-1.3^\\circ) \cdot 0.3^\\circ $$
    - $$ \\varepsilon_k $$ is the constructive twist, $$ \\varepsilon_k = 0^\\circ $$ (as there is no constructive twist)

    This is followed by an explanation that at the location where $$ cZ_{max} - cb = 1.148 $$, flow separation occurs, and that value becomes $$ ca $$.
    """)

    st.markdown("***")

    st.subheader("3.1.3. Lift gradient")
    st.latex(r"a = \frac{a_0 \cdot \lambda}{2 + \sqrt{4 + \lambda^2 \cdot \beta^2 \cdot \left(1 + \frac{\tan^2(\phi)}{\beta^2}\right)}} = \frac{0.110 \cdot 3.888}{2 + \sqrt{4 + (3.888)^2 \cdot (0.71)^2 \cdot \left(1 + \frac{\tan^2(27^\circ)}{(0.71)^2}\right)}} = 0.07197 \approx 0.072")
    
    
    st.subheader("3.1.4. Critical angle of attack")



if __name__ == "__main__":
    main()


