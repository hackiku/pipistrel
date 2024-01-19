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

    invert_choice = st.radio("Color", ["Black", "White"], index=0)

    if invert_choice == "White":
        img = invert_image_color(img, invert=True)

    cropped_img = crop_image(img, 1600, 3000, invert=True)
    st.image(cropped_img, caption='Wing areas')

    return shapes


if __name__ == "__main__":
    shapes = draw_wing_area()  # Replace with actual SVG file path
