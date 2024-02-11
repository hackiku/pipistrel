# ./pages/8_Landing_gear_drag.py

import streamlit as st
from PIL import Image, ImageOps
from utils import spacer, final_value_input_oneline
from modules.draw.draw import draw_shapes_with_lengths, crop_image, calculate_area
from variables_manager import initialize_session_state, get_variable_value,\
    get_variable_props, display_variable, update_variables, log_changed_variables

# Define a dictionary for the landing gear projection details
projection_details = {
    'front': {'name': 'Front Projection (landing gear)', 'svg_path': './modules/draw/landing_gear/landing_gear.svg', 'crop_y': (650, 1500)},
}

def draw_landing_gear_area(projection_details, key, show_labels=True):

    # choose color inversion and measurements
    col1, col2 = st.columns(2)
    with col1:
        invert_choice = st.radio("Color", ["Black", "White"], index=0, key=f"invert_choice_{key}")
    with col2:
        labels_choice = st.radio("Show measures", ["All", "Area only"], index=0, key=f"labels_choice_{key}")
        show_labels = labels_choice != "Area only"

    # draw the shapes    
    img, shapes, lines = draw_shapes_with_lengths(projection_details['svg_path'], show_labels)
    
    # invert image colors (defailt to )
    if invert_choice == "Black":
        img = ImageOps.invert(img.convert('RGB'))

    cropped_img = crop_image(img, *projection_details['crop_y'])
    st.image(cropped_img, caption=projection_details['name'])

    return shapes, lines

# =================================================================== #
# ======================= MAIN ====================================== #
# =================================================================== #

def main():
    st.title("Landing gear drag")

    initialize_session_state()
    
    # Initialize variables for individual areas
    individual_areas = {}

    key = 'front'
    details = projection_details[key]
        
    st.markdown(f"### {details['name']}")
    shapes, lines = draw_landing_gear_area(details, key)

    # Initialize markdown table rows for names and values
    markdown_area_names = "| Area "
    markdown_area_values = "| Value (m²) "

    # Display the title for the landing gear projection
    for i, shape in enumerate(shapes):
        area = shape.area
        individual_areas[f'S{i+1}'] = area

        # Append to markdown rows using dollar signs for LaTeX in markdown
        markdown_area_names += f"| $S_{{{i+1}}}$ "
        markdown_area_values += f"| {area:.3f} "

    markdown_area_names += "|"
    markdown_area_values += "|"

    # Display the markdown table with two rows
    markdown_table_divider = "| --- " * (len(shapes) + 1) + "|"
    markdown_table = markdown_area_names + "\n" + markdown_table_divider + "\n" + markdown_area_values
    st.markdown(markdown_table)

    # Calculate total area for the landing gear projection
    total_area = sum(individual_areas.values())
    st.latex(f"S_{{total}} = {total_area:.3f} \\, \\text{{m}}^2")

    st.markdown("***")

    # ===================== Landing Gear Drag Coefficient ===================== #

    S = get_variable_value('S')
    
    col1, col2 = st.columns(2)
    with col1:
        S_NN_input = st.number_input("Front wheel area (m²)", value=shapes[1].area, format="%.3f")
        S_NN = S_NN_input
    with col2:
        S_ST_input = st.number_input("Single wheel area (m²)", value=shapes[0].area, format="%.3f")
        S_ST = S_ST_input
    
    delta_Cx_min_NN = 0.25 * S_NN / S
    delta_Cx_min_ST = 0.25 * 2 * S_NN / S
    
    st.latex(rf"\Delta (C_{{Xmin}})_{{NN}} =  0.25 \cdot \frac{{{{S_{{NN}}}}}}{{{{S}}}} = 0.25 \cdot \frac{{{S_NN:.3f}}}{{{S:.3f}}} = {delta_Cx_min_NN:.5f}")
    st.latex(rf"\Delta (C_{{Xmin}})_{{ST}} = 0.25 \cdot \frac{{4 \cdot S_{{ST}}}}{{{{S}}}} = 0.25 \cdot \frac{{4 \cdot {S_ST:.3f}}}{{{S:.3f}}} = {delta_Cx_min_ST:.5f}")

    st.markdown("***")

if __name__ == "__main__":
    main()
