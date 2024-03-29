# ./pages/5_Horizontal_tail.py

import streamlit as st
from PIL import Image, ImageOps
from utils import spacer, final_value_input_oneline
from modules.draw.draw import draw_shapes_with_lengths, crop_image, calculate_area
from modules.graphs.graphs import readout_graph
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
        'S', 'v_krst', 'nu'
    ]

    initialize_session_state()
    
    st.title("Horizontal tail area drag")
    
    svg_file_path = './modules/draw/horizontal_draw/horizontal_tail.svg'
    shapes = draw_horizontal_tail(svg_file_path)

    # ===================== drawing =====================
    
    # ===================== areas =====================
    col1, col2 = st.columns([3,2])
    with col1:
        spacer()
        st.markdown("##### Horizontal tail area Draw&Drag™")
    with col2:
        S_exp_drawing = shapes[1].area
        S_exp = st.number_input("Exposed area `S_exp` (m²)", value=S_exp_drawing, format="%.3f")

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
    with col2:
        lt = st.number_input("Root chord at fuselage (m)", value=shapes[1].lines[2]['length_meters'], format="%.3f")
        st.latex(f"l_t = {lt:.3f}  \\, \\text{{m}}")
    
    n_t = l0 / lt
    st.latex(f"n_{{T}} = \\frac{{l_0}}{{l_t}} = \\frac{{{l0:.3f}}}{{{lt:.3f}}} = {n_t:.3f}")

    # ===============+++  Mean aerodynamic chord ============== #
    st.markdown("##### Mean aerodynamic chord")
    lsat = (2/3) * lt * (1 + n_t + n_t**2) / (1 + n_t)
    st.latex(f"l_{{SAT_{{hor}}}} = \\frac{{2}}{{3}} \\cdot l_t \\cdot \\frac{{1 + n_t + n_t^2}}{{1 + n_t}} = \\frac{{2}}{{3}} \\cdot {lt:.3f} \\cdot \\frac{{1 + {n_t:.3f} + {n_t:.3f}^2}}{{1 + {n_t:.3f}}} = {lsat:.3f}  \\, \\text{{m}}")

    st.latex(f"l_{{SAT_{{hor}}}} = {lsat:.3f}  \\, \\text{{m}}")
    
    
    spacer()

    # =============== form factor K ============== #

    col1, col2 = st.columns(2)
    with col1:
        d_l_ratio = st.number_input("Effective relative thickness of horizontal tail", value=0.12, format="%.2f")
        st.latex(f"\\left(\\frac{{d}}{{l}}\\right) = {d_l_ratio}")
    with col2:
        phi = st.number_input("Sweep angle (degrees)", value=7.01, format="%.2f")
        st.latex(f"\\phi = {phi:.2f}°")
    
    spacer()
    
    # ============ GRAPH K wing =================
    graph_key = 'K_wing'
    readout_graph(graph_key, 554, 358)
    default_readout = 1.30
    spacer()
    
    col1, col2 = st.columns(2)
    with col1:
        K = st.number_input("Form factor K", value=1.2, format="%.2f")
        st.latex(f"K = {K}")
    with col2:
        delta_K = st.number_input("Roughness correction factor", value=1.1, format="%.1f", step=0.1)
        st.latex(f"\\Delta K = {delta_K:.1f}")
        
    st.markdown("***")

    # =================== Reynolds number =================== #
    
    st.subheader("Reynolds number for the horizontal tail")
    
    col1, col2 = st.columns(2)
    with col1:
        v_krst_input = st.number_input("v_krst (m/s)", get_variable_value("v_krst"), format="%.3f")
        v_krst = v_krst_input
    with col2:
        nu_input = st.number_input("nu (m²/s)", get_variable_value("nu"), format="%.3e")
        nu = nu_input
    
    Re = v_krst * lsat / nu
    
    st.latex(rf"Re = \frac{{v_{{krst}} \cdot l_{{SAT_{{hor}}}}}}{{\nu}} = \frac{{{v_krst:.3f} \cdot {lsat:.3f}}}{{{nu:.2e}}} \approx {Re:.3e}")
    

    # ============ GRAPH Re horizontal =================
    graph_key = 'Re'
    readout_graph(graph_key, 484, 278)
    default_readout = 0.00464
    spacer()
    
    
    Cf_readout = st.number_input("Read out skin friction drag coefficient $Cf$ from diagram 👆", value=default_readout, format="%.5f")
    Cf = Cf_readout * delta_K
    st.latex(f"C_{{f_{{hor}}}} = C_{{f}} \cdot \Delta K = {Cf_readout:.5f} \cdot {delta_K:.1f} = {Cf:.5f}")


    st.markdown("***")


    # =================================================================== #
    # ======================= MINIMUM DRAG COEFF ======================== #
    # =================================================================== #

    S = get_variable_value("S")
    Cx_min_ht = K * Cf * Swet / S
    st.write(Cx_min_ht)
    # st.latex(r"C_{X min ht} = \frac{K_{HR_{ht}} \cdot C_{fHT} \cdot S_{WETHT}}{S} = \frac{1.135 \cdot 0.00305 \cdot 16.153}{20.602} = 0.002714")
    st.latex(rf"(C_{{X min}})_{{hor}} = \frac{{K_{{hor}} \cdot C_{{f_{{hor}}}} \cdot S_{{WET_{{hor}}}}}}{{S}} = \frac{{{K:.3f} \cdot {Cf:.5f} \cdot {Swet:.3f}}}{{{S:.3f}}} = {Cx_min_ht:.6f}")



if __name__ == "__main__":
    main()
