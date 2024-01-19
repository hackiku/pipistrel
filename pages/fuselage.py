# ./pages/fuselage.py
import streamlit as st
from PIL import Image, ImageOps
from modules.draw.draw import draw_shapes_with_lengths, crop_image, calculate_area

st.image('./modules/draw/fuselage_draw/fuselage.svg')


def invert_image_color(img, invert=False):
    if invert:
        return ImageOps.invert(img.convert('RGB'))
    return img

def draw_fuselage_area(svg_file_path):
    img, shapes, lines = draw_shapes_with_lengths(svg_file_path)

    invert_choice = st.radio("Color", ["Black", "White"], index=0)

    if invert_choice == "White":
        img = invert_image_color(img, invert=True)

    cropped_img = crop_image(img, 0, 3000)
    st.image(cropped_img, caption='Fuselage areas')

    return shapes

def main():
    st.title("Fuselage Area Calculation")
    
    shapes = draw_fuselage_area('./modules/draw/fuselage_draw/fuselage.svg')

    # ===================== areas =====================
    st.markdown("##### Fuselage Area from Drawing")

    S_exp = shapes[0].area  # Assuming shapes[0] is the fuselage exposed area
    st.latex(f"S_{{exp}} = {S_exp:.3f}  \\, \\text{{m}}^2")

    # The rest of the calculations can be included here using the values from shapes
    # Ensure the line indices correspond to the fuselage diagram lines
    # For example, if l0 is the length of the fuselage at the base and lt is the length at the top
    l0 = shapes[0].lines[1]['length_meters']  # Base length of the fuselage
    lt = shapes[0].lines[3]['length_meters']  # Top length of the fuselage

    # Calculations for wetted area, taper ratio, etc., can follow the same pattern as the vertical tail

    # Example placeholder for additional calculations
    # st.latex(f"Other calculation results here...")

    # Display sliders for editing shape lengths and recalculating areas, if needed
    # ...

if __name__ == "__main__":
    main()
