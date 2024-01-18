# ./pages/SVG_EDIT.py
# Usage in Streamlit
import streamlit as st
from PIL import Image, ImageOps
from modules.draw.draw import draw_shapes_with_lengths, crop_image

# In your Streamlit page

def invert_color(image):
    img = Image.open(image)
    inverted_img = ImageOps.invert(img) 
    return inverted_img

def interactive_drawing_page(svg_file_path):
    img, shapes, lines = draw_shapes_with_lengths(svg_file_path)

    # Radio button to choose color inversion
    invert_color = st.radio("Color", ["Black", "White"], index=0) == "Black"

    # Display cropped (and possibly inverted) image
    cropped_img = crop_image(img, 1500, invert=invert_color)
    st.image(cropped_img, caption='Cropped Image')


    # Use Streamlit widgets to modify shape properties
    with st.expander("Shape Properties"):
        for i, shape in enumerate(shapes):
            st.subheader(f"Shape {i+1}")
            for j, line in enumerate(shape):
                start, end, length, color = line
                # Create a slider for each line's length
                new_length = st.slider(f"Shape {i+1} Line {j+1} Length", min_value=0.0, max_value=2*length, value=length, key=f"shape_{i}_line_{j}")
                shape[j] = (start, end, new_length, color)

    st.code(shapes)

if __name__ == "__main__":
    interactive_drawing_page('./modules/draw/s20.svg')
