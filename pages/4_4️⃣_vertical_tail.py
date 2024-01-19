# ./pages/4_fuselage_dimensions.py

import streamlit as st
from modules.draw.fuselage_draw.fuselage_draw import draw_fuselage

def main():
    st.title("Wing Area Test Page")
    
    shapes = draw_fuselage('./modules/draw/fuselage_draw/fuselage.svg')

    with st.expander("Line Lengths"):
        markdown_content = ""
        for i, shape in enumerate(shapes):
            markdown_content += f"### Shape {i+1}\n"
            markdown_content += "| Line | Length (m) |\n"
            markdown_content += "| ---- | ---------- |\n"
            for j, line_dict in enumerate(shape.lines):
                markdown_content += f"| Line {j+1} | {line_dict['length_meters']:.2f} |\n"    

        st.markdown(markdown_content)

    h = 0.11
    b = 10.57
    A = h*b
    st.code(f"A = {A:.2f} m^2")
    
    hsmall = 0.11
    bsmall = 1.44
    Asmall = hsmall*bsmall
    st.code(f"A = {Asmall:.2f} m^2")

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
    
if __name__ == "__main__":
    main()
