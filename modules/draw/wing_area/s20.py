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
    cropped_img = crop_image(img, 1600, 3000, invert=invert_color)
    st.image(cropped_img, caption='Wing areas')


    # recalculatre area with st.sliders
    # with st.expander("Edit shape lengths (sliders)"):
        # shape.area = calculate_area(shape.lines)
        # st.code(f"Updated Area: {shape.area:.2f} square meters")

    return shapes

if __name__ == "__main__":
    shapes = draw_wing_area()  # Replace with actual SVG file path
