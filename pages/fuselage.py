# ./pages/fuselage.py
import streamlit as st
from PIL import Image, ImageOps
from modules.draw.draw import draw_shapes_with_lengths, crop_image, calculate_area

# Define a dictionary for each projection with its details
projections_details = {
    'side': {'name': 'Side Projection', 'svg_path': './modules/draw/fuselage_draw/fuselage_side.svg', 'crop_y': (0, 650)},
    'front': {'name': 'Front Projection', 'svg_path': './modules/draw/fuselage_draw/fuselage_front.svg', 'crop_y': (650, 1500)},
    'planform': {'name': 'Planform Projection', 'svg_path': './modules/draw/fuselage_draw/fuselage_planform.svg', 'crop_y': (1500, 3000)},
}

def invert_image_color(img, invert=False):
    if invert:
        return ImageOps.invert(img.convert('RGB'))
    return img


def draw_fuselage_area(projection_details, key):
    img, shapes, lines = draw_shapes_with_lengths(projection_details['svg_path'])

    invert_choice = st.radio("Color", ["Black", "White"], index=0, key=f"{key}_color")

    if invert_choice == "White":
        img = invert_image_color(img, invert=True)

    cropped_img = crop_image(img, *projection_details['crop_y'])
    st.image(cropped_img, caption=projection_details['name'])

    return shapes, lines

def main():
    st.title("Fuselage Area Calculation")
    
    # Initialize dictionaries to store individual areas
    individual_areas = {
        'side': {},
        'front': {},
        'planform': {}
    }

    # Initialize variables for total areas
    S_tpl = 0  # total planform area (S_tpl)
    S_tb = 0   # total side projection area (S_tb)
    S_max = 0  # maximum cross-sectional area (S_max)

    # Initialize dictionary for LaTeX strings for sums
    latex_sum_strs = {
        'side': "",
        'front': "",
        'planform': ""
    }

    # side projection
    fuselage_areas = {}
    for key, details in projections_details.items():
        shapes, lines = draw_fuselage_area(details, key)
        fuselage_areas[key] = {'shapes': shapes, 'lines': lines}

        # Calculate and display each area for the projection
        st.markdown(f"#### {details['name']}")
        for i, shape in enumerate(shapes):
            area = shape.area
            individual_areas[key][f'S{i+1}'] = area
            st.markdown(f"**S{i+1} area:** {area:.3f} m²")
            latex_sum_strs[key] += f"S_{{{i+1}}} + "

        # Remove the last ' + ' from the string
        latex_sum_strs[key] = latex_sum_strs[key].rstrip(' + ')

        # Calculate total area for the current projection
        total_area = sum(individual_areas[key].values())
        
        # Assign the total area to the corresponding variable
        if key == 'planform':
            S_tpl = total_area
        elif key == 'side':
            S_tb = total_area
        elif key == 'front':
            S_max = total_area  # Assuming 'front' projection corresponds to the maximum cross-sectional area

        # Display the total area with the correct variable in LaTeX
        if key == 'planform':
            st.markdown(f"**Total Planform Area (S_tpl):** {S_tpl:.3f} m²")
            st.latex(f"S_{{tpl}} = {latex_sum_strs[key]} = {S_tpl:.3f}  \\, \\text{{m}}^2")
        elif key == 'side':
            st.markdown(f"**Total Side Projection Area (S_tb):** {S_tb:.3f} m²")
            st.latex(f"S_{{tb}} = {latex_sum_strs[key]} = {S_tb:.3f}  \\, \\text{{m}}^2")
        elif key == 'front':
            st.markdown(f"**Maximum Cross-Sectional Area (S_max):** {S_max:.3f} m²")
            st.latex(f"S_{{max}} = {latex_sum_strs[key]} = {S_max:.3f}  \\, \\text{{m}}^2")


    st.markdown("##### Fuselage Area from Drawing")
    st.markdown("#### Area Calculations")
    
    st.markdown(f"**Total Planform Area (S_tpl):** {S_tpl:.3f} m²")
    st.latex(f"S_{{tpl}} = {S_tpl:.3f}  \\, \\text{{m}}^2")
    
    st.markdown(f"**Total Side Projection Area (S_tb):** {S_tb:.3f} m²")
    st.latex(f"S_{{tb}} = {S_tb:.3f}  \\, \\text{{m}}^2")
    
    st.markdown(f"**Maximum Cross-Sectional Area (S_max):** {S_max:.3f} m²")
    st.latex(f"S_{{max}} = {S_max:.3f}  \\, \\text{{m}}^2")

    S_exp = shapes[0].area  # Assuming shapes[0] is the fuselage exposed area
    st.latex(f"S_{{exp}} = {S_exp:.3f}  \\, \\text{{m}}^2")

    l0 = shapes[0].lines[1]['length_meters']  # Base length of the fuselage
    lt = shapes[0].lines[3]['length_meters']  # Top length of the fuselage

    # Calculate wetted area (S_wet)
    S_wet = (S_tpl + S_tb) - (2 - 0.4 * (S_tpl / S_tb)) * (S_tpl / S_tb)
    st.markdown(f"**Wetted Area (S_wet):** {S_wet:.3f} m²")

    # Calculate equivalent diameter (D)
    D = ((4 * S_max) / 3.14159)**0.5
    st.markdown(f"**Equivalent Diameter (D):** {D:.3f} m")

    # Given fuselage length (L)
    L = 12.942  # This value appears to be given in the document
    st.markdown(f"**Fuselage Length (L):** {L:.3f} m")
    
    st.write(lines)

    with st.expander("Line Lengths"):
        markdown_content = ""
        for i, shape in enumerate(shapes):
            markdown_content += f"### Shape {i+1}\n"
            markdown_content += "| Line | Length (m) |\n"
            markdown_content += "| ---- | ---------- |\n"
            for j, line_dict in enumerate(shape.lines):
                markdown_content += f"| Line {j+1} | {line_dict['length_meters']:.3f} |\n"    

        st.markdown(markdown_content)


if __name__ == "__main__":
    main()
