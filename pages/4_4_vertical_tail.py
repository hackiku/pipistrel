# ./pages/4_4_vertical_tail.py
import streamlit as st
from PIL import Image, ImageOps
from modules.draw.draw import draw_shapes_with_lengths, crop_image, calculate_area

def invert_color(image):
    img = Image.open(image)
    inverted_img = ImageOps.invert(img) 
    return inverted_img

def draw_wing_area(svg_file_path):
    img, shapes, lines = draw_shapes_with_lengths(svg_file_path)

    invert_color = st.radio("Color", ["Black", "White"], index=0) == "Black"

    cropped_img = crop_image(img, 0, 650, invert=True)
    st.image(cropped_img, caption='Wing areas')

    return shapes


def main():
    st.title("Vertical Tail Area Test Page")
    
    # Replace the following with actual drawing code for the vertical tail
    shapes = draw_wing_area('./modules/draw/vertical_draw/vertical_tail.svg')

    # ===================== drawing =====================
    S_exp = shapes[0].area  # Exposed area of the vertical tail
    
    # ===================== areas =====================
    st.markdown("##### Vertical Tail Area from Drawing")
    col1, col2 = st.columns(2)
    with col1:
        st.latex(f"S_{{exp}} = {S_exp:.3f}  \\, \\text{{m}}^2")

    # Wetted area
    Swet = 2 * S_exp * 1.02
    st.latex(f"S_{{WET}} = 2 \\cdot S_{{exp}} \\cdot 1.02 = 2 \\cdot {S_exp:.3f} \\cdot 1.02 = {Swet:.3f}  \\, \\text{{m}}^2")

    # Taper ratio
    l0 = shapes[0].lines[0]['length_meters']  # Root chord
    lt = shapes[0].lines[1]['length_meters']  # Tip chord
    n_t = lt / l0
    st.latex(f"n_{{T}} = \\frac{{l_t}}{{l_0}} = \\frac{{{lt:.3f}}}{{{l0:.3f}}} = {n_t:.3f}")

    # Mean aerodynamic chord
    Lsat = (2/3) * l0 * (1 + n_t + n_t**2) / (1 + n_t)
    st.latex(f"L_{{SAT}} = \\frac{{2}}{{3}} \\cdot l_0 \\cdot \\frac{{1 + n_t + n_t^2}}{{1 + n_t}} = \\frac{{2}}{{3}} \\cdot {l0:.3f} \\cdot \\frac{{1 + {n_t:.3f} + {n_t:.3f}^2}}{{1 + {n_t:.3f}}} = {Lsat:.3f}  \\, \\text{{m}}")

    # Relative thickness
    d_l_ratio = 0.06  # Relative thickness of the vertical tail airfoil
    st.latex(r"\left(\frac{d}{l}\right) = 0.06")

    # Display the actual drawing and other relevant information
    # ...

if __name__ == "__main__":
    main()
