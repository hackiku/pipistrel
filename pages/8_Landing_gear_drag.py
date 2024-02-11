# ./pages/8_Landing_gear_drag.py

import streamlit as st
from PIL import Image, ImageOps
from utils import spacer, final_value_input_oneline
from modules.draw.draw import draw_shapes_with_lengths, crop_image, calculate_area
from variables_manager import initialize_session_state, get_variable_value,\
    get_variable_props, display_variable, update_variables, log_changed_variables

# Define a dictionary for the landing gear projection details
projection_details = {
    'front': {'name': 'Front Projection (1/3)', 'svg_path': './modules/draw/landing_gear/landing_gear.svg', 'crop_y': (650, 1500)},
}

def draw_landing_gear_area(projection_details, key):

    # Draw the shapes    
    img, shapes, lines = draw_shapes_with_lengths(projection_details['svg_path'], True)
    
    # Crop the image to the specified y coordinates
    cropped_img = crop_image(img, *projection_details['crop_y'])
    
    # Display the cropped image
    st.image(cropped_img, caption=projection_details['name'])

    return shapes, lines

# =================================================================== #
# ======================= MAIN ====================================== #
# =================================================================== #

def main():
    st.title("Landing Gear Drag Calculation")

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
    st.markdown("***")

    # ===================== Landing Gear Drag Coefficient ===================== #
    # Since the math is simplified and there's no need for user inputs, let's directly calculate the coefficients
    
    # Assuming 'v_krst' and 'nu' are available from the session state or user inputs
    v_krst = get_variable_value('v_krst')
    nu = get_variable_value('nu')
    
    # Coefficients as per the calculations in the image
    S22 = 0.06
    S23 = 0.094
    S = 25.55  # Replace with actual value if different

    delta_Cx_min_NN = (S22 / S) * 0.25 / S
    delta_Cx_min_ST = (4 * S23 / S) * 0.25 / S
    
    # Display the calculated drag coefficients
    st.latex(rf"\Delta (C_{{Xmin}})_{NN} = \frac{{S_{{22}}}}{{S}} \cdot 0.25 = \frac{{0.06}}{{25.55}} = {delta_Cx_min_NN:.5f}")
    st.latex(rf"\Delta (C_{{Xmin}})_{ST} = \frac{{4 \cdot S_{{23}}}}{{S}} \cdot 0.25 = \frac{{4 \cdot 0.094}}{{25.55}} = {delta_Cx_min_ST:.5f}")

    st.markdown("***")


if __name__ == "__main__":
    main()
