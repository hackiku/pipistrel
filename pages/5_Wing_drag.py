# ./pages/5_Wing_drag.py
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
        'S', 'S_20', 'S_21', 'S_wet_kr', 'lT', 'l0', 'nT', 
        'l_sat_kr', 'Re', 'v_krst', 'Cf_kr', 'dl_eff_kr', 'K_kr', 'C_X_min_krilo'
    ]

    initialize_session_state()


    svg_file_path = './modules/draw/wing_area/wings_both.svg'
    shapes = draw_wing_area(svg_file_path)


    # ===================== drawing =====================
    
    l0 = shapes[0].lines[0]['length_meters']
    ls = shapes[0].lines[2]['length_meters']
    b = calculate_wingspan(shapes)


    # ===================== areas =====================
    st.markdown("##### Wing areas from drawing")
    st.write("Note: These are formulas for a centerplane wing, i.e. consisting of a trapezoidal midsection with rectangular outer sections. The mean aerodyanmic chord is calculated to take this config into accoutn. Later versions of the app will include formulas for different wing shapes.")
    
    st.write("Trapezoidal section")
    col1, col2 = st.columns(2)
    with col1:
        St_drawing = shapes[1].area # both trapezoids
        St = st.number_input("Area of trapezoid `St`", value=St_drawing, key='St')
        st.latex(f"S_T = {St_drawing:.3f}  \\, \\text{{m}}^2")
    with col2:
        St_exp = St
        spacer('1em')
        st.write("Area of exposed trapezoid `St_exp` is the same as the exposed area `St`")
        st.latex(f"S_{{T_{{exp}}}} = S_T = {St:.3f}  \\, \\text{{m}}^2")
    
    st.write("Rectangular section")
    col1, col2 = st.columns(2)
    with col1:
        Sc_drawing = shapes[2].area # rectangle till root
        Sc = st.number_input("Area of rectangle till symmetry plane", value=Sc_drawing, key='Sc')
        st.latex(f"S_C = {Sc_drawing:.3f}  \\, \\text{{m}}^2")
    with col2:
        Sc_exp_drawing = shapes[3].area
        Sc_exp = st.number_input("Area of rectangle till fuselage (exposed)", value=Sc_exp_drawing, key='Sc_exp')
        st.latex(f"S_{{C_{{exp}}}} = {Sc_exp:.3f}  \\, \\text{{m}}^2")


    st.write("Normal wing areas")

    S_pr = Sc + St
    st.latex(f"S_{{pr}} = S_{{C}} + S_{{T}} = {Sc:.3f} + {St:.3f} = {S_pr:.3f}  \\, \\text{{m}}^2") 
    S = S_pr * 2
    st.latex(f"S = 2 \\cdot S_{{pr}} = 2 \\cdot {S_pr:.3f} = {S:.3f}  \\, \\text{{m}}^2")

    col1, col2 = st.columns(2)
    with col1:
        st.write("Exposed wing areas")
    with col2:
        S_exp = Sc_exp + St_exp * 1.02
        S_exp_input = st.number_input("Change exposed wing area `S_exp`", value=S_exp, key='S_exp')
    
    S_exp = S_exp_input
    st.latex(f"S_{{exp}} = S_{{C_{{exp}}}} + S_{{T_{{exp}}}} = {Sc_exp:.3f} + {St_exp:.3f} = {S_exp:.3f}  \\, \\text{{m}}^2")
    
    Swet = S_exp * 2
    st.latex(f"S_{{WET}} = S_{{exp}} \\cdot 2 \\cdot 1.2 = {S_exp:.3f} \\cdot 2 \\cdot 1.2 = {Swet:.3f}  \\, \\text{{m}}^2")
    
    st.markdown("***")
    
    # ===================== calc Lsat =====================

    st.markdown("##### Calc mean aerodynamic chord (L_sat)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.latex(f"l_s = {ls:.3f}  \\, \\text{{m}}")
    with col2:
        st.latex(f"l_0 = {l0:.3f}  \\, \\text{{m}}")
    with col3:
        st.latex(f"b = {b:.3f}  \\, \\text{{m}}")

    lmbda = b**2 / S
    st.latex(f"\\lambda = \\frac{{b^2}}{{S}} = \\frac{{{b:.3f}^2}}{{{S:.3f}}} = {lmbda:.3f}")

    st.text("Trapezoidal section")
    nt = l0 / ls
    st.latex(f"n_T = \\frac{{l_0}}{{l_s}} = \\frac{{{l0:.3f}}}{{{ls:.3f}}} = {nt:.3f}")    
    Lsat_t = (2/3) * ls * (1 + nt + nt**2) / (1 + nt)
    
    st.text("Rectangular section")

    Lsat_c = S / b

    st.latex(f"L_{{SAT_{{T}}}} = \\frac{{2}}{{3}} \\cdot l_s \\cdot \\frac{{1 + n_T + n_T^2}}{{1 + n_T}} = \\frac{{2}}{{3}} \\cdot {ls:.3f} \\cdot \\frac{{1 + {nt:.3f} + {nt:.3f}^2}}{{1 + {nt:.3f}}} = {Lsat_t:.3f}  \\, \\text{{m}}")
    st.latex(f"L_{{SAT_{{C}}}} = \\frac{{S}}{{b}} = \\frac{{{S:.3f}}}{{{b:.3f}}} = {Lsat_c:.3f}  \\, \\text{{m}}")
    st.latex(f"l_{{SAT}} = \\frac{{2}}{{3}} \\cdot l_s \\cdot \\frac{{1 + n_T + n_T^2}}{{1 + n_T}} = \\frac{{2}}{{3}} \\cdot {ls:.3f} \\cdot \\frac{{1 + {nt:.3f} + {nt:.3f}^2}}{{1 + {nt:.3f}}} = {Lsat_t:.3f}  \\, \\text{{m}}")

    # TODO interpolate NACA thickness
    col1, col2= st.columns(2)
    with col1:
        st.latex(r"\left(\frac{d}{l}\right)_s = 0.15")
    with col2:
        st.latex(r"\left(\frac{d}{l}\right)_0 = 0.12")
    
    # Display the formula for ya
    st.latex(r'''
    y_a = \frac{y_{ac}S_c + y_{at}S_t}{S_c + S_t}
    ''')

    # =============================================================
    # ===================== final part ============================
    # =============================================================

    st.markdown("***")
    st.markdown("***")

    col1, col2, col3 = st.columns(3)
    with col1: 
        Swet_wing = st.number_input("Wetted area", value=9.046, key='Swet_wings')
        st.latex(rf"S_{{wet_{{KR}}}} = {Swet_wing:.3f} \, m^2")
    with col2:
        lmac_wing = st.number_input("Mean aerodynamic chord", value=1.545, key='l_sat_kr')
        st.latex(rf"l_{{SAT_{{kr}}}} =  {lmac_wing:.3f} \, m")
    with col3:
        v_krst_input = st.number_input("Cruise speed", value=get_variable_value('v_krst'), key='v_krst')
        v_krst = v_krst_input
        st.latex(rf"v_{{krst}} = {v_krst_input:.3f} \, m/s")
    spacer()
    
    st.write('Reynolds number')
    
    nu = get_variable_value('nu')  # Kinematic viscosity in m^2/s
    # 2.21e-5     # Kinematic viscosity in m^2/s
    Re = v_krst * lmac_wing / nu
    st.latex(rf"Re = \frac{{v_{{krst}} \cdot l_{{SAT_{{kr}}}}}}{{\nu}} = \frac{{{v_krst:.2f} \cdot {lmac_wing:.3f}}}{{{nu:.2e}}} \approx {Re:.2e}")
    
    # graph
    st.markdown("""<div style="background-color: black; opacity: 0.3; padding: 100px"></div>""", unsafe_allow_html=True)
    spacer()

    # ==================== cx wing ==================== #

    c_fkr = 0.0026 # TODO add to json
    Cf_fkr = st.number_input("Coefficient of friction drag", value=get_variable_value('Cf_kr'), key='Cf_kr', format="%.4f")
    st.latex(rf"C_{{f_{{KR}}}} = {c_fkr:.4f}")
    
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
