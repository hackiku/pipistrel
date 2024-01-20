# ./pages/draw_wing_areas.py
import streamlit as st
from PIL import Image, ImageOps
from modules.draw.draw import draw_shapes_with_lengths, crop_image

def draw_wing_area(svg_file_path, show_labels=True):

    # choose color inversion and measurements
    col1, col2 = st.columns(2)
    with col1:
        invert_choice = st.radio("Color", ["Black", "White"], index=0)
    with col2:
        labels_choice = st.radio("Show measures", ["All", "Area only"], index=0)

    if labels_choice == "Area only":
        show_labels = False
    
    # draw the shapes    
    img, shapes, lines = draw_shapes_with_lengths(svg_file_path, show_labels)
    
    # invert image colors (defailt to )
    if invert_choice == "Black":
        img = ImageOps.invert(img.convert('RGB'))

    cropped_img = crop_image(img, 1600, 3000)
    st.image(cropped_img, caption='Wing areas')

    return shapes


def calculate_wingspan(shapes):

    conversion_hardcoded = 0.00584518884292006
    
    min_y = float('inf')
    max_y = float('-inf')

    # Iterate through each shape and update min and max y-coordinates
    for shape in shapes:
        for line in shape.lines:
            start_y, end_y = line['start'][1], line['end'][1]
            min_y = min(min_y, start_y, end_y)
            max_y = max(max_y, start_y, end_y)
        # st.code(f"min_y: {min_y}, max_y: {max_y}")
    # Calculate wingspan as the difference between max and min y-coordinates
    wingspan = (max_y - min_y) * conversion_hardcoded
    return wingspan

def main():
    st.title("Wing Area Test Page")
    
    svg_file_path = './modules/draw/wing_area/wings_both.svg'
    shapes = draw_wing_area(svg_file_path)

    # Display table of lines and lengths for each shape

    # ===================== drawing =====================
    Sc = shapes[1].area # rectangle
    St = shapes[0].area # trapezoid
    Sc_exp = shapes[2].area
    St_exp = St
    l0 = shapes[0].lines[0]['length_meters']
    ls = shapes[0].lines[2]['length_meters']
    b = 10.159
    S1 = Sc + St
    S = S1 * 2
    S_exp = Sc_exp + St_exp * 1.02 # TODO check in slides
    Swet = S_exp * 2


    # ===================== areas =====================
    st.markdown("##### Wing areas from drawing")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.latex(f"S_T = {St:.3f}  \\, \\text{{m}}^2")
    with col2:
        st.latex(f"S_C = {Sc:.3f}  \\, \\text{{m}}^2")
    with col3:
        st.latex(f"S_{{T_{{exp}}}} = S_T = {St:.3f}  \\, \\text{{m}}^2")
    
    st.latex(f"S_{{C_{{exp}}}} = {Sc_exp:.3f}  \\, \\text{{m}}^2")
        
    st.markdown("##### Calc wing areas")

    st.latex(f"S_{{1}} = S_{{C}} + S_{{T}} = {Sc:.3f} + {St:.3f} = {S1:.3f}  \\, \\text{{m}}^2")
    st.latex(f"S_{{exp}} = S_{{C_{{exp}}}} + S_{{T_{{exp}}}} = {Sc_exp:.3f} + {St_exp:.3f} = {S_exp:.3f}  \\, \\text{{m}}^2")
    st.latex(f"S = 2 \\cdot S_1 = 2 \\cdot {S1:.3f} = {S:.3f}  \\, \\text{{m}}^2")
    st.latex(f"S_{{WET}} = S_{{exp}} \\cdot 2 \\cdot 1.2 = {S_exp:.3f} \\cdot 2 \\cdot 1.2 = {Swet:.3f}  \\, \\text{{m}}^2")
    
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


if __name__ == "__main__":
    main()
