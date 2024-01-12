### 4_4_drag_incompressible.py ###

import streamlit as st
import matplotlib.pyplot as plt
from data import Variable, save_variables_to_session, load_variables_from_session
from utils import spacer, emoji_header, variables_two_columns, variables_three_columns

S = Variable("Wing Area", 30.00, "S", "S", "m²")
S_20 = Variable("Aerodynamic reference area", 10.301, "S_20", "S_{20}", "m²")
S_21 = Variable("Area of the wing exposed to airflow", 7.568, "S_21", "S_{21}", "m²")
SWETKR = Variable("Wetted area of the wing", 30.877, "SWETKR", "S_{WETKR}", "m²")
l0 = Variable("Root chord length", 1.574, "l0", "l_{0}", "m")
lT = Variable("Tip chord length", 2.689, "lT", "l_{T}", "m")
nT = Variable("Taper ratio", 0.585, "nT", "n_{T}", "")
lSATKR = Variable("Mean aerodynamic chord of the exposed wing area", 2.179, "lSATKR", "l_{SATKR}", "m")
Re = Variable("Reynolds number", 2.211 * 10**7, "Re", "Re", "")
CfKR = Variable("Friction drag coefficient", 0.0026, "CfKR", "C_{fKR}", "")
dl_effekKR = Variable("Effective relative thickness", 0.109, "dl_effekKR", "(d/l)_{effekKR}", "")
KKR = Variable("Wing shape drag factor", 1.21, "KKR", "K_{KR}", "")
C_X_min_krilo = Variable("Minimum drag coefficient of the wing", 0.004715, "C_X_min_krilo", "C_{X min krilo}", "")


def main():

    st.title("4. Drag calculation")
    st.write("""Proračun otpora aviona (za nestišljivo strujanje. Za ovaj proračun proračun potrebno je:
- Definisatisvedimenzijeelemenatakonstrukcijeavionapotrebnezaproračunotpora; - Odreditijednačinupolareaviona;
- IzračunatimaksimalnufinesuavionaiCZprikomeseonaostvaruje;
- Odreditifinesuavionaipotrebnuvučnusiluelisenarežimukrstarenja;
- DijagramskipokazatipolaruavionaifinesuavionaufunkcijiodCZ.""")

    st.markdown("***")    
    st.header("4.1. Određivanje polare aviona")

    # ==================== wing ==================== #
    st.subheader("4.1.1. Krilo (Wing)")
    
    # Aerodynamic reference area (S_20)
    st.write(f"Aerodynamic reference area: {S_20.value} {S_20.unit}")
    st.latex(rf"{S_20.latex} = {S_20.value} \, {S_20.unit}")

    def calculate_wing_areas():
        # Total wing area (S)
        S = 2 * S_20.value
        st.write(f"Total wing area: {S} {S_20.unit}")
        st.latex(rf"S = 2 \cdot {S_20.latex} = {S} \, {S_20.unit}")

        # Area of the wing exposed to airflow (S_exp_kr)
        S_exp_kr = 2 * S_21.value
        st.write(f"Area of the wing exposed to airflow: {S_exp_kr} {S_21.unit}")
        st.latex(rf"S_{{exp_{{KR}}}} = 2 \cdot {S_21.latex} = {S_exp_kr} \, {S_21.unit}")

        # Wetted area of the wing (S_WETKR)
        S_WETKR = S_exp_kr * 1.02
        st.write(f"Wetted area of the wing: {S_WETKR} {S_21.unit}")
        st.latex(rf"S_{{WET_{{KR}}}} = {S_exp_kr} \cdot 1.02 = {S_WETKR} \, {S_21.unit}")

        return S, S_exp_kr, S_WETKR

    calculate_wing_areas()

    st.markdown("***")

    def calculate_aerodynamics(l0_value, lT_value, v_krst, nu):
        # Taper ratio (nT)
        nT = l0_value / lT_value
        nT_latex = rf"n_T = \frac{{l_0}}{{l_T}} = \frac{{{l0_value:.3f}}}{{{lT_value:.3f}}} = {nT:.3f}"
        st.latex(nT_latex)

        # Mean aerodynamic chord (lSATKR)
        lSATKR = (2/3) * l0_value * ((1 + nT + nT**2) / (1 + nT))
        lSATKR_latex = rf"l_{{SATKR}} = \frac{{2}}{{3}} \cdot \frac{{1 + n_T + n_T^2}}{{1 + n_T}} \cdot l_T = \frac{{2}}{{3}} \cdot \frac{{1 + {nT:.3f} + {nT:.3f}^2}}{{1 + {nT:.3f}}} \cdot {lT_value:.3f} = {lSATKR:.3f} \, m"
        st.latex(lSATKR_latex)

        # Reynolds number (Re)
        Re = v_krst * lSATKR / nu
        Re_latex = rf"Re = \frac{{v_{{krst}} \cdot l_{{SATKR}}}}{{\nu}} = \frac{{{v_krst:.2f} \cdot {lSATKR:.3f}}}{{{nu:.2e}}} \approx {Re:.2e}"
        st.latex(Re_latex)

        return nT, lSATKR, Re
    
    l0_value = 1.574  # Root chord length in meters
    lT_value = 2.689  # Tip chord length in meters
    v_krst = 224.28  # Cruising speed in m/s
    nu = 2.21e-5     # Kinematic viscosity in m^2/s

    calculate_aerodynamics(l0_value, lT_value, v_krst, nu)
    
    # graph
    st.markdown("""<div style="background-color: black; opacity: 0.3; padding: 100px"></div>""", unsafe_allow_html=True)
    spacer()

    # ==================== cx wing ==================== #
    
    st.write("Iz gore priloženog dijagrama očitava se koeficijent otpora trenja Cf")
    c_fkr = 0.0026
    st.latex(rf"C_{{fKR}} = {c_fkr:.4f}")
    st.markdown("***")

    l0 = 1.574  # Root chord length in meters
    dl0 = 0.09  # Relative thickness at the root
    lT = 2.689  # Tip chord length in meters
    dlT = 0.12  # Relative thickness at the tip

    dl_effekKR = (l0 * dl0 + lT * dlT) / (l0 + lT)
    
    # Display the text and the equation
    st.write("Efektivna relativna debljina se dobija osrednjavanjem relativnih debljina u korenu i na kraju krila jer su različite:")
    st.latex(rf"(d/l)_{{effekKR}} = \frac{{l_0 \cdot (d/l)_0 + l_T \cdot (d/l)_T}}{{l_0 + l_T}} = \frac{{{l0:.3f} \cdot {dl0} + {lT:.3f} \cdot {dlT}}}{{{l0:.3f} + {lT:.3f}}} = {dl_effekKR:.3f}")
    
    S_WETKR = 30.877  # Wetted area of the wing in m^2
    
    spacer()
    col1, col2 = st.columns(2)
    with col1:
        st.write("Faktor otpora oblika krila K očitava se sa dijagrama na sledećoj strani, a koji pokazuje zavisnost relativne debljine i ugla strele od faktora otpora oblika.")
        dl = 0.109
        phi = 10
        st.latex(rf"(d/l)_{{effekKR}} = {dl:.3f}")
        st.latex(rf"\phi = {phi:.3f}")
        s = 20.602  # Reference area in square meters
        k_kr = Variable("Wing shape drag", 1.21, "KKR", "K_{KR}", "")
        variables_two_columns(k_kr)
        c_x_min_krilo = (k_kr.value * c_fkr * S_WETKR) / s
        st.write("Koeficijent minimalnog otpora krila")
        st.latex(rf"C_{{X min krilo}} = \frac{{K_{{KR}} \cdot C_{{fKR}} \cdot S_{{WET_{{KR}}}}}}{{S}} = \frac{{{k_kr.value:.2f} \cdot {c_fkr:.4f} \cdot {S_WETKR:.3f}}}{{{s:.3f}}} = {c_x_min_krilo:.6f}")

    with col2:
        st.image('./assets/tmp_assets/koef_min_otpora.png', )

    st.markdown("***")
    
    #======================================================#
    #==================== (2) fuselage ====================#
    #======================================================#

    st.subheader("4.1.2. Trup (Fuselage)")

    # Planform area of fuselage
    st.write("Za određivanje okvašene površine trupa potrebno je izračunati površine u plan i bočnoj projekciji.")
    S_tpl = sum([0.321, 1.432, 2.792, 2.588, 4.557, 1.326, 2.395, 1.784])
    st.latex(r"S_{tpl} = \sum_{i=1}^{16} S_i = 0.321 + 1.432 + 2.792 + 2.588 + 4.557 + 1.326 + 2.395 + 1.784 = 17.193 m^2")

    # Side area of fuselage
    S_tb = sum([0.306, 1.255, 2.329, 2.931, 2.633, 4.426, 2.676, 1.051])
    st.latex(r"S_{tb} = \sum_{i=9}^{16} S_i = 0.306 + 1.255 + 2.329 + 2.931 + 2.633 + 4.426 + 2.676 + 1.051 = 17.605 m^2")

    # Wetted area of fuselage
    st.write("Okvašena površina trupa")
    S_WETT = (S_tpl + S_tb) * (2 - 0.4 * S_tpl / S_tb)
    st.latex(r"S_{WETT} = (S_{tpl} + S_{tb}) \cdot \left(2 - 0.4 \cdot \frac{S_{tpl}}{S_{tb}}\right) = (17.193 + 17.605) \cdot \left(2 - 0.4 \cdot \frac{17.193}{17.605}\right) = 56 m^2")

    # Length of the fuselage as read from the drawing
    st.write("Proračunska dužina L očitana sa crteža je L_T=12.33m.")
    st.latex(r"L_{T} = 12.33 m")

    # Maximum cross-sectional area of fuselage in front projection
    st.write("Površina maksimalnog poprečnog preseka trupa u čeonoj projekciji je S_max")
    S_max_T = sum([0.917, 2.049, 0.268])
    st.latex(r"S_{max_T} = \sum_{i=17}^{19} S_i = 0.917 + 2.049 + 0.268 = 3.234 m^2")

    # Display a placeholder for the graph
    st.markdown("""<div style="background-color: black; opacity: 0.3; padding: 100px"></div>""", unsafe_allow_html=True)

    st.markdown("***")

    col1, col2 = st.columns(2)
    with col1:
        st.write("Ekvivalentni prečnik maksimalnog poprečnog preseka trupa transformisanog u krug")
        S_max_T = 3.234  # Maximum cross-sectional area in square meters
        D_T = (4 * S_max_T / 3.14159) ** 0.5
        st.latex(r"D_{T} = \sqrt{\frac{4 \cdot S_{max_{T}}}{\pi}} = \sqrt{\frac{4 \cdot 3.234}{\pi}} = 2.029m")

        # Fineness ratio of fuselage
        st.write("Vitkost trupa je tada")
        L_T = 12.33  # Length of the fuselage
        lambda_T = L_T / D_T
        st.latex(r"\lambda_{T} = \frac{L_{T}}{D_{T}} = \frac{12.33}{2.029} = 6.08")

        st.write("Faktor oblika trupa očitva se sa dijagrama")
        K_T = 1.23
        st.latex(r"K_{T} = 1.23")
    with col2:
        st.image('./assets/tmp_assets/koef_min_otpora.png', )

    # Reynolds number for the fuselage
    st.write("Rejnoldsov broj - potreban nam je za izračunavanje koeficijenta otpora trenja trupa")
    Re_T = (v_krst * L_T) / nu
    st.latex(r"Re = \frac{v_{krst} \cdot L_T}{\nu} = \frac{" + str(v_krst) + r" \cdot " + str(L_T) + r"}{" + str(nu) + r"} = " + str(round(Re_T, 2)))

    # Drag coefficient from diagram
    st.write("Iz prethodno datih dijagrama koeficijent otpora trenja trupa " + r"C_{fT} = " + str(CfKR.value))
    st.latex(r"C_{fT} = " + str(CfKR.latex))

    # Minimum drag coefficient of the fuselage
    st.write("Koeficijent minimalnog otpora trupa")
    # Given values
    K_T_value = 1.23  # Fuselage shape factor
    C_fT_value = 0.0026  # Coefficient of friction drag of the fuselage
    S_WETT_value = 56  # Wetted area of the fuselage in square meters
    S_value = 20.602  # Reference wing area in square meters

    # Calculation of minimum drag coefficient of the fuselage
    C_X_min_trup_value = (K_T_value * C_fT_value * S_WETT_value) / S_value

    # Display the calculation in the app
    st.write("Koeficijent minimalnog otpora trupa (Minimum drag coefficient of the fuselage):")
    st.latex(rf"C_{{X min trup}} = \frac{{K_T \cdot C_{{fT}} \cdot S_{{WETT}}}}{{S}} = \frac{{{K_T_value} \cdot {C_fT_value} \cdot {S_WETT_value}}}{{{S_value}}} = {C_X_min_trup_value:.6f}")

    st.markdown("***")
    #======================================================#
    #============== (3) horizontal stabilizer ==============#
    #======================================================#
    st.subheader("4.1.3. Horizontalni rep (Horizontal Tail)")

    # Exposed area of horizontal tail
    S_exp_ht = 7.918  # m²
    st.write(f"Exposed area of horizontal tail: {S_exp_ht} m²")
    st.latex(r"S_{exp_{ht}} = 2 \cdot S_{22} = 2 \cdot 3.959 = 7.918 \, m^2")

    # Wetted area of horizontal tail
    S_WETHT = S_exp_ht * 1.02
    st.write(f"Wetted area of horizontal tail: {S_WETHT:.2f} m²")
    st.latex(r"S_{WETHT} = S_{exp_{ht}} \cdot 1.02 = 7.918 \cdot 1.02 = 16.153 \, m^2")

    # Root chord length of horizontal tail
    l0_ht = 0.871  # m
    # Tip chord length of horizontal tail
    lT_ht = 2.059  # m
    # Taper ratio of horizontal tail
    nT_ht = l0_ht / lT_ht
    st.latex(r"n_{T_{ht}} = \frac{l_{0_{ht}}}{l_{T_{ht}}} = \frac{0.871}{2.059} = 0.423")

    # Mean aerodynamic chord of horizontal tail
    lSATHT = (2/3) * l0_ht * ((1 + nT_ht + nT_ht**2) / (1 + nT_ht))
    st.latex(r"l_{SATHT} = \frac{2}{3} \cdot l_{0_{ht}} \cdot \frac{1 + n_{T_{ht}} + n_{T_{ht}}^2}{1 + n_{T_{ht}}} = 1.545 \, m")

    # Reynolds number of horizontal tail
    Re_ht = 224.28 * lSATHT / 2.21e-5
    st.latex(r"Re_{ht} = \frac{v_{krst} \cdot l_{SATHT}}{\nu} = \frac{224.28 \cdot 1.545}{2.21 \cdot 10^{-5}} = 1.5679303 \times 10^7")

    spacer()
    # Friction drag coefficient of horizontal tail from diagram
    CfHT = 0.00305
    st.latex(r"C_{fHT} = 0.00305")

    # Effective relative thickness of horizontal tail
    dl_effekHT = 0.09
    st.latex(r"(d/l)_{effekHT} = 0.09")

    # Sweep angle of horizontal tail
    phi_ht = 41  # degrees
    st.latex(r"\phi_{ht} = 41^\circ")

    # Shape drag factor of horizontal tail from diagram
    KKR_ht = 1.135
    st.latex(r"K_{HR_{ht}} = 1.135")

    # Minimum drag coefficient of horizontal tail
    C_X_min_ht = KKR_ht * CfHT * S_WETHT / S.value
    st.latex(r"C_{X min ht} = \frac{K_{HR_{ht}} \cdot C_{fHT} \cdot S_{WETHT}}{S} = \frac{1.135 \cdot 0.00305 \cdot 16.153}{20.602} = 0.002714")
    #======================================================#
    #=============== (4) vertical stabilizer ==============#
    #======================================================#
    st.subheader("4.1.4. Vertikalni rep (Vertical Tail)")



    #==================== spaceeee ====================#
    spacer('12em')


    st.subheader("4.1.5. Korigovani koeficijent minimalnog otpora (Corrected Minimum Drag Coefficient)")

    # =============== 4.2. ================== #
    st.markdown("***")
    st.header("4.2. Određivanje otpora zavisno od uzgona")

    st.subheader("4.2.1. Određivanje Osvaldovog faktora e i člana uz CZ2")

    st.subheader("4.2.2. Proračunska polara aviona (Aircraft Polar Calculation)")



if __name__ == "__main__":
    main()