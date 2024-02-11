# ./pages/4_Wing_drag.py
import streamlit as st
from PIL import Image, ImageOps
from modules.draw.draw import draw_shapes_with_lengths, crop_image
from variables_manager import initialize_session_state, get_variable_value, \
    get_variable_props, display_variable, update_variables, log_changed_variables
from utils import spacer, emoji_header 

def draw_wing_area(svg_file_path, show_labels=True):

    # radio buttons (2x)
    col1, col2 = st.columns(2)
    with col1:
        invert_choice = st.radio("Color", ["Black", "White"], index=0)
    with col2:
        labels_choice = st.radio("Show measures", ["All", "Area only"], index=0)

    if labels_choice == "Area only":
        show_labels = False
    
    # draw areas    
    img, shapes, lines = draw_shapes_with_lengths(svg_file_path, show_labels)
    
    # invert image colors (defailt to )
    if invert_choice == "Black":
        img = ImageOps.invert(img.convert('RGB'))

    cropped_img = crop_image(img, 1600, 3000)
    st.image(cropped_img, caption='Wing areas')

    return shapes

# actually x, inverted line['start']
def calculate_wingspan(shapes):

    conversion_hardcoded = 0.00584518884292006
    
    min_y = float('inf')
    max_y = float('-inf')

    for shape in shapes:
        for line in shape.lines:
            start_y, end_y = line['start'][0], line['end'][0]
            min_y = min(min_y, start_y, end_y)
            max_y = max(max_y, start_y, end_y)
        # st.code(f"min_y: {min_y}, max_y: {max_y}")
    # wingspan = max - min min y-coord (actually x here due to image redrawing in figma)
    wingspan = (max_y - min_y) * conversion_hardcoded
    return wingspan

def main():
    
    st.title("Wing area drag")
    page_values = [
        'S', 'v_krst', 'nu'
    ]

    initialize_session_state()

    svg_file_path = './modules/draw/wing_area/wings_both.svg'
    shapes = draw_wing_area(svg_file_path)


    # ===================== areas =====================
    st.subheader("Wing areas from drawing")
    st.write("Note: These are formulas for a centerplane wing, i.e. consisting of a trapezoidal midsection with rectangular outer sections. The mean aerodyanmic chord is calculated to take this config into account. Later versions of the app will include formulas for different wing shapes.")
    
    st.write("Trapezoidal segments")
    col1, col2 = st.columns(2)
    with col1:
        St_drawing = shapes[1].area # both trapezoids
        St = st.number_input("Area of trapezoid `St`", value=St_drawing, key='St')
        st.latex(f"S_T = {St:.3f}  \\, \\text{{m}}^2")
    with col2:
        St_exp = St
        spacer('1em')
        st.write("Area of exposed trapezoid `St_exp` is the same as the other trapezoid area `St`")
        st.latex(f"S_{{T_{{exp}}}} = S_T = {St:.3f}  \\, \\text{{m}}^2")
    
    st.write("Rectangular segments")
    col1, col2 = st.columns(2)
    with col1:
        Sc_drawing = shapes[2].area # rectangle till root
        Sc = st.number_input("Area of rectangle till symmetry plane", value=Sc_drawing, key='Sc')
        st.latex(f"S_C = {Sc_drawing:.3f}  \\, \\text{{m}}^2")
    with col2:
        Sc_exp_drawing = shapes[3].area
        Sc_exp = st.number_input("Area of rectangle till fuselage (exposed to airflow)", value=Sc_exp_drawing, key='Sc_exp')
        st.latex(f"S_{{C_{{exp}}}} = {Sc_exp:.3f}  \\, \\text{{m}}^2")


    st.write("Normal wing areas")

    S_pr = Sc + St
    st.latex(f"S_{{pr}} = S_{{C}} + S_{{T}} = {Sc:.3f} + {St:.3f} = {S_pr:.3f}  \\, \\text{{m}}^2") 
    S = S_pr * 2
    st.latex(f"S = 2 \\cdot S_{{pr}} = 2 \\cdot {S_pr:.3f} = {S:.3f}  \\, \\text{{m}}^2")

    spacer('1em')
    
    col1, col2 = st.columns(2)
    with col1:
        spacer()
        st.write("Exposed wing areas")
    with col2:
        S_exp = Sc_exp + St_exp * 1.02
        S_exp_input = st.number_input("Change exposed wing area `S_exp`", value=S_exp, key='S_exp')
    
    spacer('1em')
    
    S_exp = S_exp_input
    st.latex(f"S_{{exp}} = S_{{C_{{exp}}}} + S_{{T_{{exp}}}} = {Sc_exp:.3f} + {St_exp:.3f} = {S_exp:.3f}  \\, \\text{{m}}^2")
    
    Swet = S_exp * 2
    st.latex(f"S_{{WET}} = S_{{exp}} \\cdot 2 \\cdot 1.2 = {S_exp:.3f} \\cdot 2 \\cdot 1.2 = {Swet:.3f}  \\, \\text{{m}}^2")
    
    st.markdown("***")
    
    # ===================== calc Lsat =====================

    st.markdown("##### Calculate mean aerodynamic chord (L_sat)")

    # extract chord lengths & span from drawing
    l0_drawing = shapes[0].lines[0]['length_meters']
    lt_drawing = shapes[0].lines[2]['length_meters']
    b_drawing = calculate_wingspan(shapes)

    col1, col2, col3 = st.columns(3)
    with col1:
        l0 = st.number_input("Change tip chord length `l0`", value=l0_drawing, key='l0')
        st.latex(f"l_0 = {l0:.3f}  \\, \\text{{m}}")
    with col2:
        lt = st.number_input("Change chord length at fuselage `lt`", value=lt_drawing, key='lt')
        st.latex(f"l_t = {lt:.3f}  \\, \\text{{m}}")
    with col3:
        b = st.number_input("Change wingspan", value=b_drawing, key='b')
        st.latex(f"b = {b:.3f}  \\, \\text{{m}}")

    lmbda = b**2 / S
    st.latex(f"\\lambda = \\frac{{b^2}}{{S}} = \\frac{{{b:.3f}^2}}{{{S:.3f}}} = {lmbda:.3f}")

    spacer()
    
    st.write("- **Trapezoidal section** taper ratio `nt` and mean aerodynamic chord `Lsat_t`")
    
    nt = l0 / lt
    st.latex(f"n_T = \\frac{{l_0}}{{l_t}} = \\frac{{{l0:.3f}}}{{{lt:.3f}}} = {nt:.3f}")    
    Lsat_t = (2/3) * lt * (1 + nt + nt**2) / (1 + nt)
    st.latex(f"L_{{SAT_{{T}}}} = \\frac{{2}}{{3}} \\cdot l_t \\cdot \\frac{{1 + n_T + n_T^2}}{{1 + n_T}} = \\frac{{2}}{{3}} \\cdot {lt:.3f} \\cdot \\frac{{1 + {nt:.3f} + {nt:.3f}^2}}{{1 + {nt:.3f}}} = {Lsat_t:.3f}  \\, \\text{{m}}")
    
    spacer()
    
    # rectangle mean aerodynamic chord
    st.write("- **Rectangular section** has no taper ratio, therefore the mean aerodynamic chord `Lsat_c` is simply the length of the root chord `lt`")

    Lsat_c = lt
    st.latex(f"L_{{SAT_{{C}}}} = {Lsat_c:.3f}  \\, \\text{{m}}")

    # centerplane mean aerodynamic chord
    lsat = ( Lsat_t * St_exp  +  Lsat_c * Sc_exp ) / S_exp
    st.latex(f"l_{{SAT}} = \\frac{{L_{{SAT_{{T}}}} \\cdot S_{{T_{{exp}}}} + L_{{SAT_{{C}}}} \\cdot S_{{C_{{exp}}}}}}{{S_{{exp}}}} = \\frac{{{Lsat_t:.3f} \\cdot {St_exp:.3f} + {Lsat_c:.3f} \\cdot {Sc_exp:.3f}}}{{{S_exp:.3f}}} = {lsat:.3f}  \\, \\text{{m}}")

    st.markdown("***")
    st.markdown("***")
    
    
    # ===================== form factor K readout =====================

    st.subheader("Form factor $K$ readout")
    st.write("First off, let's average the airfoil thicknesses at root and tip to get a relative thickness")
    
    # TODO interpolate NACA thickness
    col1, col2= st.columns(2)
    with col1:
        # lt_input2 = st.number_input("Change tip chord length `lt`", value=lt, key='lt2')
        # lt = lt_input2        
        dl_t = st.number_input('Relative thickness at the root', value=0.12, format="%.2f")
        st.latex(f"\\left(\\frac{{d}}{{l}}\\right)_t = {dl_t:.2f}")
        dt = lt * dl_t
        st.latex(f"d_t = l_t \\cdot (\\frac{{d}}{{l}})_t = {lt:.3F} \\cdot {dl_t:.3F} = {dt:.3f}")
        # st.latex(f"d_t = l_t \\cdot (\\frac{{d}}{{l}})_t = {l0:.3F} \\cdot {dl_t:.3F} = {dt:.3f}")
    with col2:
        # l0_input2 = st.number_input('Change root chord length `l0`', value=l0, key='l0_2')
        # l0 = l0_input2
        dl_0 = st.number_input('Relative thickness at the tip', value=0.09, format="%.2f")
        st.latex(f"\\left(\\frac{{d}}{{l}}\\right)_0 = {dl_0:.2f}")
        d0 = l0 * dl_0
        st.latex(f"d_t = l_t \\cdot (\\frac{{d}}{{l}})_t = {l0:.3F} \\cdot {dl_0:.3F} = {d0:.3f}") 

    dl_wing = (l0 * dl_0 + lt * dl_t) / (l0 + lt)

    st.write(f"The effective relative thickness of the wing `dl_wing` = {dl_wing}. You can change it below to recalculate manually:")
    st.latex(rf"(d/l)_{{eff_{{KR}}}} = \frac{{l_0 \cdot (d/l)_0 + l_T \cdot (d/l)_T}}{{l_0 + l_T}} = \frac{{{l0:.3f} \cdot {dl_0} + {lt:.3f} \cdot {dl_t}}}{{{l0:.3f} + {lt:.3f}}} = {dl_wing:.3f}")

    col1, col2 = st.columns(2)
    with col1:
        d_l_ratio = st.number_input("Effective relative thickness of wing", value=dl_wing, format="%.3f")
        st.latex(f"\\left(\\frac{{d}}{{l}}\\right) = {d_l_ratio:.3f}")
    with col2:
        phi = st.number_input("Sweep angle (degrees)", value=30.00, format="%.2f")
        st.latex(f"\\phi = {phi:.2f}°")
    
    st.image('./assets/tmp_assets/koef_min_otpora.png', )
    
    col1, col2 = st.columns(2)
    with col1:
        K = st.number_input("Form factor K", value=1.2, format="%.2f")
        st.latex(f"K = {K}")
    with col2:
        delta_K = st.number_input("Roughness correction factor", value=1.1, format="%.1f", step=0.1)
        st.latex(f"\\Delta K = {delta_K:.1f}")
    
    st.markdown("***")

    # =================== Reynolds number =================== #
    st.subheader("Reynolds number for wings")

    col1, col2 = st.columns(2)
    with col1:
        v_krst_input = st.number_input("Change cruising speed `v_krst` (m/s)", get_variable_value("v_krst"), format="%.3f")
        v_krst = v_krst_input
    with col2:
        nu_input = st.number_input("Change kinematic viscosity `nu` (m²/s)", get_variable_value("nu"), format="%.3e")
        nu = nu_input
    
    Re = v_krst * lsat / nu
    
    st.latex(rf"Re = \frac{{v_{{krst}} \cdot l_{{SAT_{{ver}}}}}}{{\nu}} = \frac{{{v_krst:.2f} \cdot {lsat:.3f}}}{{{nu:.2e}}} \approx {Re:.3e}")
    
    spacer()
    
    # placeholder graph
    st.markdown("""
    <div style="background-color: black; opacity: 0.3; padding: 100px"></div>""", unsafe_allow_html=True)

    spacer()
    
    Cf_readout = st.number_input("Read out skin friction drag coefficient $Cf$ from diagram 👆", value=0.00305, format="%.5f")
    Cf = Cf_readout * delta_K
    st.latex(f"C_{{f_{{kr}}}} = C_{{f}} \cdot \Delta K = {Cf_readout:.5f} \cdot {delta_K:.1f} = {Cf:.5f}")
    
    st.markdown("***")

    # =================================================================== #
    # ======================= MINIMUM DRAG COEFF ======================== #
    # =================================================================== #
    
    st.subheader("➡️ Minimum drag coefficient")    

    Cx_min_wing = K * Cf * Swet / S

    st.latex(rf"(C_{{X min}})_{{kr}} = \frac{{K_{{kr}} \cdot C_{{f_{{kr}}}} \cdot S_{{WET_{{kr}}}}}}{{S}} = \frac{{{K:.3f} \cdot {Cf:.5f} \cdot {Swet:.3f}}}{{{S:.3f}}} = {Cx_min_wing:.6f}")

    st.markdown("***")

    




    # =============================================================
    
    st.markdown("***")
    st.markdown("***")
    st.markdown("***")
    
    with st.expander("Line Lengths"):
        markdown_content = ""
        for i, shape in enumerate(shapes):
            markdown_content += f"### Shape {i+1}\n"
            markdown_content += "| Line | Length (m) |\n"
            markdown_content += "| ---- | ---------- |\n"
            for j, line_dict in enumerate(shape.lines):
                markdown_content += f"| Line {j+1} | {line_dict['length_meters']:.3f} |\n"    

        st.markdown(markdown_content)

    with st.expander("Area calculation code"):
        st.code("""from PIL import Image, ImageDraw, ImageFont, ImageOps
from svgpathtools import svg2paths

def extract_lines_from_svg(svg_file_path):
    paths, attributes = svg2paths(svg_file_path)
    lines_with_color = []

    for path, attr in zip(paths, attributes):
        for line in path:
            start = (line.start.real, line.start.imag)
            end = (line.end.real, line.end.imag)
            color = attr.get('stroke', '#FF0000')
            lines_with_color.append((start, end, color))

    return lines_with_color

    def calculate_area(lines):
    # Extracting lengths from line dictionaries
    a = lines[0]['length_meters']  # 1st line
    b = lines[2]['length_meters']  # 3rd line
    # height: 2nd and 4th line
    h = max(lines[1]['length_meters'], lines[3]['length_meters'])
    return 0.5 * (a + b) * h
""")

    update_variables(page_values, locals())
    log_changed_variables()

if __name__ == "__main__":
    main()
