# ./pages/draw_horizontal_tail_areas.py
import streamlit as st
from PIL import Image, ImageOps
from utils import spacer, final_value_input_oneline
from modules.draw.draw import draw_shapes_with_lengths, crop_image, calculate_area
from variables_manager import initialize_session_state, get_variable_value,\
    get_variable_props, display_variable, update_variables, log_changed_variables
def draw_horizontal_tail(svg_file_path, show_labels=True):

    # choose color inversion and measurements
    col1, col2 = st.columns(2)
    with col1:
        invert_choice = st.radio("Color", ["Black", "White"], index=0)
    with col2:
        labels_choice = st.radio("Show measures", ["All", "Area only"], index=0)
        show_labels = labels_choice != "Area only"

    # draw the shapes    
    img, shapes, lines = draw_shapes_with_lengths(svg_file_path, show_labels)
    
    # invert image colors (defailt to )
    if invert_choice == "Black":
        img = ImageOps.invert(img.convert('RGB'))

    cropped_img = crop_image(img, 1600, 3000)
    st.image(cropped_img, caption='Wing areas')

    return shapes

def main():
    
    page_values = [
        'v_krst', 'nu'
    ]

    initialize_session_state()
    
    st.title("Horizontal Tail Area Calculation")
    
    svg_file_path = './modules/draw/horizontal_draw/horizontal_tail.svg'
    shapes = draw_horizontal_tail(svg_file_path)

    # ===================== drawing =====================
    
    # ===================== areas =====================
    st.markdown("##### Horizontal Tail Area from Drawing")

    S_exp = shapes[1].area  # Exposed area of the horizontal tail
    st.latex(f"S_{{exp}} = {S_exp:.3f}  \\, \\text{{m}}^2")

    Swet = 2 * S_exp * 1.02 # Wetted area horizontal tail
    st.latex(f"S_{{WET}} = 2 \\cdot S_{{exp}} \\cdot 1.02 = 2 \\cdot {S_exp:.3f} \\cdot 1.02 = {Swet:.3f}  \\, \\text{{m}}^2")
    st.latex(f"S_{{WET}} = {Swet:.3f}  \\, \\text{{m}}^2")
    
    # ===================== taper ratio =====================

    st.markdown("##### Taper ratio")
    
    col1, col2 = st.columns(2)
    with col1:
        l0 = st.number_input("Tip chord (m)", value=shapes[1].lines[0]['length_meters'], format="%.3f")
        st.latex(f"l_0 = {l0:.3f}  \\, \\text{{m}}")
        st.write(l0)
    with col2:
        lt = st.number_input("Root chord at fuselage (m)", value=shapes[1].lines[2]['length_meters'], format="%.3f")
        st.latex(f"l_t = {lt:.3f}  \\, \\text{{m}}")
        st.write(lt)
    
    n_t = l0 / lt
    st.latex(f"n_{{T}} = \\frac{{l_0}}{{l_t}} = \\frac{{{l0:.3f}}}{{{lt:.3f}}} = {n_t:.3f}")
    st.write(n_t)

    # ===============+++  Mean aerodynamic chord ============== #
    st.markdown("##### Mean aerodynamic chord")
    lsat = (2/3) * lt * (1 + n_t + n_t**2) / (1 + n_t)
    st.latex(f"l_{{SAT_{{hor}}}} = \\frac{{2}}{{3}} \\cdot l_t \\cdot \\frac{{1 + n_t + n_t^2}}{{1 + n_t}} = \\frac{{2}}{{3}} \\cdot {lt:.3f} \\cdot \\frac{{1 + {n_t:.3f} + {n_t:.3f}^2}}{{1 + {n_t:.3f}}} = {lsat:.3f}  \\, \\text{{m}}")

    st.latex(f"l_{{SAT_{{hor}}}} = {lsat:.3f}  \\, \\text{{m}}")
    
    # =================== Reynolds number =================== #
    st.markdown("***")
    
    col1, col2 = st.columns(2)
    with col1:
        v_krst_input = st.number_input("v_krst (m/s)", get_variable_value("v_krst"), format="%.3f")
        v_krst = v_krst_input
    with col2:
        nu_input = st.number_input("nu (m²/s)", get_variable_value("nu"), format="%.3e")
        nu = nu_input
    # nu = get_variable_value("nu")
    
    # nu = 2.44602e-5
    st.write("ν =", nu)
    Re = v_krst * lsat / nu
    
    st.latex(rf"Re = \frac{{v_{{krst}} \cdot l_{{SAT_{{kr}}}}}}{{\nu}} = \frac{{{v_krst:.2f} \cdot {lsat:.3f}}}{{{nu:.2e}}} \approx {Re:.3e}")
    
    spacer()
    
    col1, col2 = st.columns(2)
    with col1:
        Cf = st.number_input("Friction drag coefficient of horizontal tail from diagram", value=0.00305, format="%.5f")
    with col2:
        st.latex(f"C_{{f}} = {Cf:5f}")

    # placeholder graph
    st.markdown("""
    <div style="background-color: black; opacity: 0.3; padding: 100px"></div>""", unsafe_allow_html=True)


    # =============== form factor K ============== #

    d_l_ratio = 0.06  # Relative thickness of horizontal tail airfoil
    st.latex(f"\\left(\\frac{{d}}{{l}}\\right) = {d_l_ratio}")


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



if __name__ == "__main__":
    main()
