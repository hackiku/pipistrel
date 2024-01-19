# AREATEST.py
import streamlit as st
from modules.draw.wing_area.s20 import draw_wing_area

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
    
    shapes = draw_wing_area('./modules/draw/wing_area/wings_both.svg')

    # Display table of lines and lengths for each shape

    # ===================== drawing =====================
    Sc = shapes[0].area # rectangle
    St = shapes[1].area # trapezoid
    Sc_exp = shapes[2].area
    St_exp = St
    l0 = shapes[0].lines[0]['length_meters']
    ls = shapes[0].lines[2]['length_meters']
    b = 10.159
    # wing_length = calculate_wingspan(shapes)

    st.markdown("##### Trapezoids:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text("wingspan")
        st.latex(f"b = {b:.3f}  \\, \\text{{m}}")
    with col2:
        st.text("Rectangle to symmetry")
        st.latex(f"S_c = {Sc:.3f}  \\, \\text{{m}}^2")
    with col3:
        st.text("Trapezoids")
        st.latex(f"S_t = S_{{t_{{exp}}}} = {St:.3f}  \\, \\text{{m}}^2")

    # ===================== calculated =====================
    st.markdown("##### Calculated:")
    S1 = Sc + St
    S = S1 * 2
    col1, col2 = st.columns(2)
    with col1:
        st.latex(f"S_{{1}} = S_{{C}} + S_{{T}} = {Sc:.3f} + {St:.3f} = {S1:.3f}  \\, \\text{{m}}^2")
    with col2:
        st.code("single wing area to symmetry")
    
    st.latex(f"S_{{C_{{exp}}}} = {Sc_exp:.3f}  \\, \\text{{m}}^2")
    
    
    st.latex(f"S_1 = {S1:.3f}  \\, \\text{{m}}^2")

    lmbda = b**2 / S
    st.latex(f"\\lambda = \\frac{{b^2}}{{S}} = \\frac{{{b:.3f}^2}}{{{S:.3f}}} = {lmbda:.3f}")
    
    # st.latex(f"\\lambda = \\frac{{l_0 + l_s}}{{2b}} = \\frac{{{l0:.3f} + {ls:.3f}}}{{{S:.3f}}} = {lmbda:.3f}")
    st.latex(f" = {b:.3f}  \\, \\text{{m}}")


    st.markdown("***")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.latex(f"l_0 = {l0:.3f}  \\, \\text{{m}}")
    with col2:
        st.latex(f"l_s = {ls:.3f}  \\, \\text{{m}}")
    with col3:
        st.latex(f"b = {wing_length:.3f} \\cdot 2 = {b:.3f}  \\, \\text{{m}}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.latex(f"S_0 = {S0:.3f}  \\, \\text{{m}}^2")
    with col2:
        st.latex(f"S_1 = {S1:.3f}  \\, \\text{{m}}^2")
    with col3:
        st.latex( f"S_{{pr}} = S_{{0}} + S_{{1}} = {Spr:.3f} \\, \\text{{m}}^2")
    
    st.latex(f"S = S_{{pr}} \\cdot 2 = {Spr:.3f} \\cdot 2 = {S:.3f} \\, \\text{{m}}^2")

    with st.expander("Line Lengths"):
        markdown_content = ""
        for i, shape in enumerate(shapes):
            markdown_content += f"### Shape {i+1}\n"
            markdown_content += "| Line | Length (m) |\n"
            markdown_content += "| ---- | ---------- |\n"
            for j, line_dict in enumerate(shape.lines):
                markdown_content += f"| Line {j+1} | {line_dict['length_meters']:.2f} |\n"    

        st.markdown(markdown_content)

if __name__ == "__main__":
    main()
