### 4_4_drag_incompressible.py ###
import streamlit as st
from variables_manager import initialize_session_state, get_variable_value, get_variable_props, display_variable, update_variables, log_changed_variables
from utils import spacer, emoji_header  # Assuming these are utility functions you've defined


def main():
    page_values = [
        'S', 'S_20', 'S_21', 'S_wet_kr', 'lT', 'l0', 'nT', 
        'l_sat_kr', 'Re', 'v_krst', 'Cf_kr', 'dl_eff_kr', 'K_kr', 'C_X_min_krilo'
    ]
    initialize_session_state()

    
    #==================== drag ====================#
    st.title("4. Drag polar")
    
    st.write("""Proračun otpora aviona (za nestišljivo strujanje. Za ovaj proračun proračun potrebno je:
- Definisati sve dimenzije elemenata konstrukcije aviona potrebne za proračun otpora;
- Odrediti jednačinu polare aviona;
- Izračunati maksimalnu finesu aviona i CZ pri kome se ona ostvaruje;
- Odrediti finesu aviona i potrebnu vučnu silu elise na režimu krstarenja;
- Dijagramski pokazati polaru aviona i finesu aviona u funkciji od CZ.""")

    st.markdown("***")    

    st.header("4.1. Characteristic dimensions ")

    # ==================== wing ==================== #
    st.subheader("Wing")
    
    spacer()
    
    st.text('– aerodynamic reference area')
    
    S_20 = get_variable_value('S_20')    
    S = 2 * S_20
    display_variable('S_20')
    st.latex(r"S = 2 \cdot S_{20} = 2 \cdot 10.301 = 20.602 \, m^2")
    
    st.text('– exposed area')
    S_21 = get_variable_value('S_21')
    S_exp_kr = 2 * S_21
    st.latex(rf"S_{{21}} = {S_21} \, m^2")
    st.latex(rf"S_{{expKR}} = 2 \cdot S_{{21}} = 2 \cdot {S_21} = {S_exp_kr} \, m^2")
    
    st.text('– wetted area')
    S_wet_kr = S_exp_kr * 2 * 1.02
    st.latex(rf"S_{{wetKR}} = S_{{expKR}} \cdot 2 \cdot 1.02 = {S_exp_kr} \cdot 2 \cdot 1.02 = {S_wet_kr:.3f} \, m^2")

    update_variables(page_values, locals())
    log_changed_variables()

    
    spacer()

    # dimensions =========
    
    st.text('– taper ratio')
    
    col1, col2 = st.columns(2)
    with col1:
        l0 = st.number_input("Trapezoid chord length", value=get_variable_value('l0'), key='l0')
        st.latex(rf"l_0 = {l0:.3f} \, m")
    with col2:
        lT = st.number_input("Tip chord length", value=get_variable_value('lT'), key='lT')
        st.latex(rf"l_T = {lT:.3f} \, m")
    nT = lT / l0
    st.latex(rf"n_T = \frac{{l_1}}{{l_0}} = \frac{{{lT:.3f}}}{{{l0:.3f}}} = {nT:.3f}")

    # Mean aerodynamic chord (l_sat_kr)
    st.text('– mean aerodynamic chord')
    l_sat_kr = (2/3) * lT * ((1 + nT + nT**2) / (1 + nT))
    st.latex(rf"l_{{satKR}} = \frac{{2}}{{3}} \cdot l_0 \cdot \frac{{1 + n_T + n_T^2}}{{1 + n_T}}")
    st.latex(rf"l_{{satKR}} = \frac{{2}}{{3}} \cdot {l0:.3f} \cdot \frac{{1 + {nT:.3f} + {nT:.3f}^2}}{{1 + {nT:.3f}}} = {l_sat_kr:.3f} \, m")

    # Reynolds number (Re)
    st.text('– Reynolds number')
    v_krst = 224.28  # Cruising speed in m/s (assuming constant or obtained elsewhere)
    nu = 2.21e-5     # Kinematic viscosity in m^2/s (assuming constant or obtained elsewhere)
    Re = v_krst * l_sat_kr / nu
    st.latex(rf"Re = \frac{{v_{{krst}} \cdot l_{{satKR}}}}{{\nu}} = \frac{{{v_krst:.2f} \cdot {l_sat_kr:.3f}}}{{{nu:.2e}}} \approx {Re:.2e}")

    update_variables(page_values, locals())
    log_changed_variables()
    
    nu = 2.21e-5     # Kinematic viscosity in m^2/s
    
    # graph
    st.markdown("""<div style="background-color: black; opacity: 0.3; padding: 100px"></div>""", unsafe_allow_html=True)
    spacer()

    # ==================== cx wing ==================== #

    
    st.write("Iz gore priloženog dijagrama očitava se koeficijent otpora trenja Cf")
    c_fkr = 0.0026 # TODO add to json
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
    
    spacer()
    col1, col2 = st.columns(2)
    with col1:
        st.write("Faktor otpora oblika krila K očitava se sa dijagrama na sledećoj strani, a koji pokazuje zavisnost relativne debljine i ugla strele od faktora otpora oblika.")
        dl = 0.109
        phi = 10
        st.latex(rf"(d/l)_{{effekKR}} = {dl:.3f}")
        st.latex(rf"\phi = {phi:.3f}")
        s = 20.602  # Reference area in square meters
        K_kr = st.number_input("Shape drag factor of the wing", value=get_variable_value('K_kr'), key='K_kr')
        c_x_min_krilo = (K_kr * c_fkr * S_wet_kr) / s
        st.write("Koeficijent minimalnog otpora krila")
        st.latex(rf"C_{{X min krilo}} = \frac{{K_{{KR}} \cdot C_{{fKR}} \cdot S_{{WET_{{KR}}}}}}{{S}} = \frac{{{K_kr:.2f} \cdot {c_fkr:.4f} \cdot {S_wet_kr:.3f}}}{{{s:.3f}}} = {c_x_min_krilo:.6f}")

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
    st.latex(rf"C_{{fT}} = {CfKR}")

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

    update_variables(page_values, locals())
    log_changed_variables()
    st.markdown("***")

if __name__ == "__main__":
    main()