# ./pages/draw_horizontal_tail_areas.py
import streamlit as st
from PIL import Image, ImageOps
from modules.draw.draw import draw_shapes_with_lengths, crop_image, calculate_area

def draw_horizontal_tail(svg_file_path, show_labels=True):

    # choose color inversion and measurements
    col1, col2 = st.columns(2)
    with col1:
        invert_choice = st.radio("Color", ["Black", "White"], index=0)
    with col2:
        labels_choice = st.radio("Show measures", ["All", "Area only"], index=0)
        show_labels = labels_choice != "Area only"

    # draw the shapes    
    img, shapes, lines = draw_shapes_with_lengths(svg_file_path, show_labels)
    
    # invert image colors (defailt to )
    if invert_choice == "Black":
        img = ImageOps.invert(img.convert('RGB'))

    cropped_img = crop_image(img, 1600, 3000)
    st.image(cropped_img, caption='Wing areas')

    return shapes

def main():
    st.title("Horizontal Tail Area Calculation")
    
    svg_file_path = './modules/draw/horizontal_draw/horizontal_tail.svg'
    shapes = draw_horizontal_tail(svg_file_path)

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