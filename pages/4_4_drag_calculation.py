# 4_drag_calculation.py

import streamlit as st
import matplotlib.pyplot as plt
from data import Variable
from utils import spacer, emoji_header, variables_two_columns, variables_three_columns

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
- DijagramskipokazatipolaruavionaifinesuavionaufunkcijiodCZ."
    st.header(4.1. Određivanje polare aviona""")

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






    #==================== spaceeee ====================#
    spacer('12em')
    st.subheader("4.1.2. Trup (Fuselage)")

    st.subheader("4.1.3. Horizontalni rep (Horizontal Tail)")

    st.subheader("4.1.4. Vertikalni rep (Vertical Tail)")

    st.subheader("4.1.5. Korigovani koeficijent minimalnog otpora (Corrected Minimum Drag Coefficient)")

    # =============== 4.2. ================== #
    st.markdown("***")
    st.header("4.2. Određivanje otpora zavisno od uzgona")

    st.subheader("4.2.1. Određivanje Osvaldovog faktora e i člana uz CZ2")

    st.subheader("4.2.2. Proračunska polara aviona (Aircraft Polar Calculation)")


if __name__ == "__main__":
    main()