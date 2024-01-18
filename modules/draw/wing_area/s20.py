# ./modules/draw/s20.py

import streamlit as st
from PIL import Image, ImageOps
from modules.draw.draw import draw_shapes_with_lengths, crop_image, calculate_area

def invert_color(image):
    
    img = Image.open(image)
    
    inverted_img = ImageOps.invert(img) 
    return inverted_img

def draw_wing_area(svg_file_path):
    img, shapes, lines = draw_shapes_with_lengths(svg_file_path)

    # Radio button to choose color inversion
    invert_color = st.radio("Color", ["Black", "White"], index=0) == "Black"

    # Display cropped (and possibly inverted) image
    cropped_img = crop_image(img, 1500, invert=invert_color)
    st.image(cropped_img, caption='Cropped Image')


    # Use Streamlit widgets to modify shape properties
    with st.expander("Edit shape lengths (sliders)"):
        for i, shape in enumerate(shapes):
            st.subheader(f"Shape {i+1} {shape.area:.2f} m²")

            # Creating a markdown table for line lengths
            st.markdown("| Line | Length (m) |")
            st.markdown("| ---- | ----------- |")
            for j, line_dict in enumerate(shape.lines):
                length = line_dict['length_meters']
                st.markdown(f"| Line {j+1} | {length:.2f} |") 

            # Recompute area if lines are adjusted
            shape.area = calculate_area(shape.lines)
            st.write(f"Updated Area: {shape.area:.2f} square meters")

    return shapes

if __name__ == "__main__":
    shapes = draw_wing_area()  # Replace with actual SVG file path
