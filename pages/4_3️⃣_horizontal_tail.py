# ./pages/4_3_horizontal_tail.py
import streamlit as st
from PIL import Image, ImageOps
from modules.draw.draw import draw_shapes_with_lengths, crop_image, calculate_area

def invert_image_color(img, invert=False):
    if invert:
        return ImageOps.invert(img.convert('RGB'))
    return img

def draw_horizontal_tail_area(svg_file_path):
    img, shapes, lines = draw_shapes_with_lengths(svg_file_path)

    invert_choice = st.radio("Color", ["Black", "White"], index=0)

    if invert_choice == "White":
        img = invert_image_color(img, invert=True)

    cropped_img = crop_image(img, 1600, 3000, invert=True)
    st.image(cropped_img, caption='Horizontal tail areas')

    return shapes

def invert_color(image):
    img = Image.open(image)
    inverted_img = ImageOps.invert(img) 
    return inverted_img

def main():
    st.title("Horizontal Tail Area Calculation")
    
    shapes = draw_horizontal_tail_area('./modules/draw/horizontal_draw/horizontal_tail.svg')

    # ===================== drawing =====================
    S_exp = shapes[0].area  # Exposed area of the horizontal tail
    
    # ===================== areas =====================
    st.markdown("##### Horizontal Tail Area from Drawing")

    st.latex(f"S_{{exp}} = {S_exp:.3f}  \\, \\text{{m}}^2")

    # Wetted area
    Swet = 2 * S_exp * 1.02
    st.latex(f"S_{{WET}} = 2 \\cdot S_{{exp}} \\cdot 1.02 = 2 \\cdot {S_exp:.3f} \\cdot 1.02 = {Swet:.3f}  \\, \\text{{m}}^2")

    st.markdown("##### Taper ratio")
    # Taper ratio
    l0 = shapes[0].lines[1]['length_meters']  # Tip chord
    lt = shapes[0].lines[3]['length_meters']  # Root chord
    n_t = lt / l0
    col1, col2 = st.columns(2)
    with col1:
        st.latex(f"l_0 = {l0:.3f}  \\, \\text{{m}}")
    with col2:
        st.latex(f"l_t = {lt:.3f}  \\, \\text{{m}}")
    st.latex(f"n_{{T}} = \\frac{{l_t}}{{l_0}} = \\frac{{{lt:.3f}}}{{{l0:.3f}}} = {n_t:.3f}")

    # Mean aerodynamic chord
    st.markdown("##### Mean aerodynamic chord")
    lsat = (2/3) * l0 * (1 + n_t + n_t**2) / (1 + n_t)
    st.latex(f"l_{{SAT}} = \\frac{{2}}{{3}} \\cdot l_0 \\cdot \\frac{{1 + n_t + n_t^2}}{{1 + n_t}} = \\frac{{2}}{{3}} \\cdot {l0:.3f} \\cdot \\frac{{1 + {n_t:.3f} + {n_t:.3f}^2}}{{1 + {n_t:.3f}}} = {lsat:.3f}  \\, \\text{{m}}")

    st.latex(f"l_{{SAT_{{hor}}}} = {lsat:.3f}  \\, \\text{{m}}")
    
    d_l_ratio = 0.06  # Relative thickness of horizontal tail airfoil
    st.latex(f"\\left(\\frac{{d}}{{l}}\\right) = {d_l_ratio}")

if __name__ == "__main__":
    main()
