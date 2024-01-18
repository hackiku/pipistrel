# AREATEST.py
import streamlit as st
from modules.draw.wing_area.s20 import draw_wing_area

def main():
    st.title("Wing Area Test Page")
    
    shapes = draw_wing_area('./modules/draw/wing_area/s20.svg')

    # Display shape areas
    for i, shape in enumerate(shapes):
        st.write(f"Shape {i+1} Area: {shape.area:.2f} square meters")

    # Display table of lines and lengths for each shape
    for i, shape in enumerate(shapes):
        st.markdown(f"### Shape {i+1}")
        st.markdown("| Line | Length (m) |")
        st.markdown("| ---- | ---------- |")
        for j, line_dict in enumerate(shape.lines):
            st.markdown(f"| Line {j+1} | {line_dict['length_meters']:.2f} |")

    # Example calculations with placeholders for l0, ls, and b
    l0 = shapes[0].lines[0]['length_meters']
    ls = shapes[0].lines[1]['length_meters']
    b = 2 * 5.00  # Placeholder, replace with actual value
    S = l0 + ls  # Placeholder for the area calculation
    st.latex(f"S_{{20}} = \\frac{{{l0} + {ls}}}{2} \\cdot \\frac{{{b}}}{2} = \\frac{{{l0:.3f} + {ls:.3f}}}{2} \\cdot \\frac{{{b:.3f}}}{2} = {S:.3f} \\, \\text{{m}}^2")
    st.latex(f"S = S_{{20}} \\cdot 2 = {S*2:.3f} \\, \\text{{m}}^2")

if __name__ == "__main__":
    main()
