# AREATEST.py
import streamlit as st
from modules.draw.wing_area.s20 import draw_wing_area


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
    
    shapes = draw_wing_area('./modules/draw/wing_area/s20.svg')

    # Display table of lines and lengths for each shape

    # Example calculations with placeholders for l0, ls, and b
    S0 = shapes[0].area
    S1 = shapes[1].area
    Spr = S0 + S1
    S = Spr * 2
    l0 = shapes[0].lines[1]['length_meters']
    ls = shapes[0].lines[3]['length_meters']
    wing_length = calculate_wingspan(shapes)
    b = wing_length * 2

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
        st.latex(f"S_{{pr}} = S_{{0}} + S_{{1}} = {Spr:.3f} \\, \\text{{m}}^2")
    
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
