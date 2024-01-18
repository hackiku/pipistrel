# ./pages/AREATEST.py

import streamlit as st
from modules.draw.wing_area.s20 import draw_wing_area

def main():
    st.title("Wing Area Test Page")
    
    # Call the draw_wing_area function from s20
    shapes = draw_wing_area('./modules/draw/wing_area/s20.svg')

    # Additional code to display or process the shapes
    # For example, displaying shape areas:
    for i, shape in enumerate(shapes):
        st.write(f"Shape {i+1} Area: {shape.area:.2f} square meters")

    

if __name__ == "__main__":
    main()
