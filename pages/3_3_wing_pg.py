# 3_wing_pg.py

import streamlit as st
from data import Variable
from utils import spacer, variables_two_columns, display_generic_table
import pandas as pd
import matplotlib.pyplot as plt

# Instantiate variables using the Variable class
c_z_krst = Variable("Cruise Lift Coefficient", 0.247, r"C_{z_{krst}}", "")
c_z_max = Variable("Max Lift Coefficient", 1.46, r"C_{z_{max}}", "")  # Assuming max lift coefficient is from NACA 65-212
v_krst = Variable("Cruising Speed", 224.37, r"v_{krst}", "m/s")
alpha_n = Variable("Angle of Attack", -1.3, r"\alpha_n", "degrees")
lambda_wing = Variable("Wing Aspect Ratio", 3.888, r"\lambda")
n = Variable("Wing Taper Ratio", 0.520, "n")
rho = Variable("Air Density at Cruise Altitude", 0.736116, r"\rho", "kg/m^3")

l_s = Variable("Chord Length", 3.028, "l_s", "m")
l_0 = Variable("Root Chord Length", 1.576, "l_0", "m")
b = Variable("Wingspan", 8.942, "b", "m")
S = Variable("Wing Area", 20.602, "S", "m²")

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

    st.write("Za proračun uzgonskih karakteristika krila i dobijanje podataka za formiranje krive uzgona je korišćen program Trapezno krilo - Glauert, a ulazni parametri su:")

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
            n.value = l_0.value / l_s.value
            numbers = "=" + f"\\frac{{{l_0.value:.2f}}}{{{l_s.value:.2f}}}"
            n.formula = f"n = \\frac{{{l_0.latex}}}{{{l_s.latex}}} {numbers}"

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            l_0.value = st.number_input(f'{l_0.name} {l_0.unit}', value=l_0.value, step=0.01, format="%.3f")
        with col2:
            l_s.value = st.number_input(f'{l_s.name} {l_s.unit}', value=l_s.value, step=0.01, format="%.3f")
        with col3:
            st.latex(f"{l_0.latex} = {l_0.value:.3f} \ {l_0.unit}")
        with col4:
            st.latex(f"{l_s.latex} = {l_s.value:.3f} \ {l_s.unit}")

        calculate_taper_ratio()
        variables_two_columns(n, display_formula=True)  # n

    markdown_table = f"""
    | # | Parameter | Symbol | Value |
    |---|---|---|---|
    | 1 | Max Lift Coefficient | $C_{{z_{{max}}}}$ | {c_z_max.value} |
    | 2 | Wing Aspect Ratio | $\\lambda = \\frac{{b^2}}{{S}}$ | {lambda_wing.value:.3f} |
    | 3 | Root Chord Length | $l_0$ | {l_0.value:.3f} m |
    | 4 | Wing Taper Ratio | $n = \\frac{{l_0}}{{l_s}}$ | {n.value:.3f} |
    | 5 | Cruising Speed | $v_{{krst}}$ | {v_krst.value:.2f} m/s |
    | 6 | Air Density at Cruise Altitude | $\\rho$ | {rho.value:.5f} kg/m³ |
    """
    
    st.markdown(markdown_table)


    st.markdown("***")

    #  =============

    st.subheader("3.1.1. Max lift coefficient of wings")
    st.write("Proračun se u prvoj iteraciji u programu Trapezno krilo- Glauert obavlja pod pretpostavkom nultog konstruktivnog vitoperenja")

    fortran_inputs = f"""
    C     *************** UNOS ULAZNIH PODATAKA I OPCIJA *******************

    C     IZBOR PRORACUNSKE OPCIJE: ZA VREDNOOST IZB=1 RACUNA SA UNAPRED
    C     ZADATIM KOEFICIJENTOM UZGONA KRILA CZ; U SUPROTNOM, ZA SVAKI
    C     DRUGI INTEGER (npr. IZB=0) CZ RACUNA NA OSNOVU SPECIFICNOG
    C     OPTERECENJA KRILA, BRZINE I GUSTINE NA REZIMU KRSTARENJA

        IZB=1
        DATA CZ / {c_z_krst.value} /  !ZADATI KOEFICIJENT UZGONA KRILA
        DATA SPECOP /800. / !ZADATO SPECIFICNO OPTERECENJE KRILA [N/m^2]

    C             PARAMETRI GEOMETRIJE KRILA I REZIMA KRSTARENJA:
    C                                          konst.
    C              broj    vitkost suzenje   vitop.   brzina   gustina
    C            preseka                     [step.]  [km/h]   [kg/m^3]
        DATA      K,       LAM,   EN,       EPS_K,    V,        RO
        &     /    16,      {lambda_wing.value:.3f},   {n.value:.3f},      0.0,    {v_krst.value:.2f},    {rho.value:.6f} /

        DATA CZMAXAP_S / 1.5 / ! maks. koef. uzgona ap. u korenu krila
        DATA CZMAXAP_0 / 1.46 / ! maks. koef. uzgona ap. na kraju krila
        DATA AAAP_S / 0.100 / !grad. uzgona ap. u korenu [1/o]
        DATA AAAP_0 / 0.110 / !grad. uzgona ap. na kraju [1/o]
        !teorijska  vrednost gradijenta uzgona 2PI = 0.1096622 [1/o]
        DATA ANAP_S / -1.2 / !ugao nultog uzgona ap. u korenu krila [o]
        DATA ANAP_0 / -1.0 / !ugao nultog uzgona ap. na kraju krila [o]
        DATA LS / 2.583 /  ! duzina tetive u korenu krila u metrima

    C     ******************** KRAJ UNOSA PODATAKA *************************
    """ 
    st.code(fortran_inputs, language='fortran')

    st.image('./assets/glauert_inverted.png')
    
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
